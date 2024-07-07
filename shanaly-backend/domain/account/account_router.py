from typing import Annotated
import os
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form,
    BackgroundTasks,
    Request,
)
from fastapi.responses import (
    Response,
    JSONResponse,
    RedirectResponse,
)
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
import secrets
from jose import jwt, JWTError, ExpiredSignatureError
from sqlmodel import (
    Session,
    select,
)
from models import (
    Users,
)
from domain.account.account_schema import (
    UserCreate,
    UserVerifyRequest,
    UserResponse,
    UserError,
    UserCredException,
    UserLoginForm,
    Token,
    UserPasswordChange,
    UserEmailChange,
    UserUsernameChange,
    UserDelete,
    UserResetPassword,
    UserProfilePictureUpload,
    UserProfileMsgChange,
)
from database import get_session
from datetime import datetime, timedelta, timezone
from core.util import send_verification_mail, send_reset_password_mail

router = APIRouter(prefix="/api/account", tags=["Account API"])

# PARAMETERS: Get Environment Variables
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")
CRYPTO_SECRET_KEY = os.getenv("CRYPTO_SECRET_KEY")
CRYPTO_ALGORITHM = os.getenv("CRYPTO_ALGORITHM")
EMAIL_VERIFY_DURATION_MINUTES = int(os.getenv("EMAIL_VERIFY_DURATION_MINUTES"))
ACCESS_TOKEN_DURATION_MINUTES = int(os.getenv("ACCESS_TOKEN_DURATION_MINUTES"))
SALT = os.getenv("SALT")

# Some security objects and Jinja2 template object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer() # HTTP Bearer

@router.post("/create")
def create_account(*,
                session: Session=Depends(get_session),
                background_tasks: BackgroundTasks,
                user_create: UserCreate):
    # This method is weak at automated repetition attacks,
    # So you have to implement CAPTCHA at the frontend user interface!

    # Check whether the email exists already in DB or not
    user_db = (
        session
        .exec(
            select(Users)
            .where(
                (Users.email == user_create.email)
            )
        )
        .first()
    )
    if user_db is not None:
        raise HTTPException(
            status_code=400,
            detail="もう使われてるEメールです。他のメールアドレスを選んでください。"
        )
    
    # Check whether the username exists already in DB or not
    user_db = (
        session
        .exec(
            select(Users)
            .where(
                (Users.username == user_create.username)
            )
        )
        .first()
    )

    if user_db is not None:
        raise HTTPException(
            status_code=400,
            detail="もう使われてるユーザー名です。他のユーザー名を選んでください。"
        )

    # If not exist, then create a user

    # Create a hashed password with SALT for strong password security
    hashed_password = pwd_context.hash(user_create.password1 + SALT)

    user_new = Users(
        email=user_create.email,
        username=user_create.username,
        password=hashed_password,
        created_at=datetime.now(),
        is_verified=False,
        is_admin=False,
        plan_id=1, # Free plan
    )

    # Add it to Database
    session.add(user_new)
    session.commit()
    session.refresh(user_new)

    # Create a token for email verification
    # [2024/05/12]
    # You have to use "timezone.utc"
    # if you use datetime.now() not datetime.utcnow() which is deprecated
    # because pyhton-jose considers UTC time only!
    data = {
        "user_id": user_new.id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EMAIL_VERIFY_DURATION_MINUTES)
    }

    token = jwt.encode(
        claims=data,
        key=CRYPTO_SECRET_KEY,
        algorithm=CRYPTO_ALGORITHM,
    )

    # Send a verification email to the new user's email
    # by using FastAPI's background task
    background_tasks.add_task(
        send_verification_mail,
        receiver=user_new.email,
        subject="【シャナリ】メール認証【Shanaly】",
        token=token,
    )

    return JSONResponse(
        status_code=200,
        content={"detail": f"アカウントの作成に成功しました。 ご登録いただいたメールアドレス( {user_create.email} )に認証メールが届きますのでご確認ください。メール認証後、ログインすることが可能になります。"}
    )


@router.get("/verify",
            response_class=RedirectResponse,
            responses={
                200: {"description": "Redirect users to base url page"},
                401: {"model": UserCredException, "description": "Invalid token or Token expiration"},
            })
def verify_email(*,
                 session: Session=Depends(get_session),
                 request: Request,
                 token: UserVerifyRequest=Depends()): # Make this into a query parameter by using Depends()
    # Define some exceptions
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    token_expire_exception = HTTPException(
        status_code=401,
        detail="The Token has expired",
        headers={"WWW-Authenticate":"Bearer"},
    )
    
    # Decode the token
    try:
        payload = jwt.decode(
            token=token.token,
            key=CRYPTO_SECRET_KEY,
            algorithms=[CRYPTO_ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise token_expire_exception
    except JWTError:
        raise credentials_exception
    else:
        # Get the user information
        user_db = session.get(Users, user_id)
        if user_db is None:
            credentials_exception
        # Make it verified
        user_db.is_verified = True
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        # Redirect users to the home page
        return RedirectResponse(BACKEND_BASE_URL)

@router.post("/login",
             responses={
                 200: {"model": Token, "description": "You can use this HTTP Bearer token; headers: new Headers( {'Authorization': 'Bearer <YOUR TOKEN>'} )"},
                 400: {"model": UserError, "description": "Your inputs will cause this error"},
                 401: {"model": UserError},
             })
def login_for_getting_access_token(
        *,
        session: Session = Depends(get_session),
        email: Annotated[str, Form()], # Form -> "media type" : application/x-www-form-urlencoded
        password: Annotated[str, Form()], # Form -> "media type" : application/x-www-form-urlencoded
    ):

    # Validate the inputs of email and password
    # This might be solved in the future:
    # https://github.com/tiangolo/fastapi/issues/10370
    try:
        login_form = UserLoginForm(email=email, password=password)
    except:
        raise HTTPException(
            status_code=400,
            detail="ご入力いただいたEメールもしくはパスワードが適切ではありません。",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get user information
    user_db = (
        session
        .exec(
            select(Users)
            .where(Users.email == login_form.email)
        )
        .first()
    )
    # Check whether the user exists in DB or not
    if user_db is None:
        raise HTTPException(
            status_code=400,
            detail="そのユーザーは存在しません。",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check whether the user's email is verified or not
    if user_db.is_verified is False:
        raise HTTPException(
            status_code=400,
            detail="ご登録いただいたEメールがまだ認証されてないです。メールボックスをご確認ください。",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check whether the input password is matched with the password stored in DB
    # SALT is used here
    if not user_db or not pwd_context.verify(login_form.password + SALT, user_db.password):
        raise HTTPException(
            status_code=400,
            detail="Eメールもしくはパスワードが違います。",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Update the latest login_at time
    user_db.sqlmodel_update(
        {"login_at": datetime.now()}
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    # [Checking Blocked user]
    # If this user is blocked by admin, then do not return a token
    # Instead, send a message
    if user_db.is_blocked == True:
        raise HTTPException(
            status_code=400,
            detail="当該アカウントはShanalyの定める運営ルールに違反している可能性があるため、一時的にブロックされました。詳細はHPのお問い合わせからご照会ください。",
            headers={"WWW-Authenticate": "Bearer"}
        ) 

    # Create an access token and return it
    # [2024/05/12]
    # You have to use "timezone.utc"
    # if you use datetime.now() not datetime.utcnow() which is deprecated
    # because pyhton-jose considers UTC time only!
    data = {
        "email": user_db.email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
    }
    access_token = jwt.encode(
        claims=data,
        key=CRYPTO_SECRET_KEY,
        algorithm=CRYPTO_ALGORITHM
    )
    token = (
        Token(
            access_token=access_token,
            token_type="bearer",
            email=user_db.email,
            userid=user_db.id,
            username=user_db.username,
            status_msg=user_db.status_msg,
        )
        .model_dump()
    )
    return token

def get_current_user(token: str=Depends(bearer_scheme), # HTTP Bearer
                     session: Session=Depends(get_session)) -> Users:
    # Define some exceptions
    credentials_exception = HTTPException(
        status_code=400,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    token_expire_exception = HTTPException(
        status_code=401,
        detail="The Token has expired",
        headers={"WWW-Authenticate":"Bearer"},
    )
    
    # Validate the token
    try:
        payload = jwt.decode(
            token=token.credentials,
            key=CRYPTO_SECRET_KEY,
            algorithms=[CRYPTO_ALGORITHM]
        )
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise token_expire_exception
    except JWTError:
        raise credentials_exception
    else:
        # Return the user information
        user_db = (
            session
            .exec(
                select(Users)
                .where(Users.email == email)
            )
            .first()
        )
        if user_db is None:
            credentials_exception
        return user_db
    
@router.patch("/change_password",
              responses={
                  200: {"model": UserResponse},
                  400: {"model": UserError},
                  401: {"model": UserCredException, "description":"Token expired"},
                  403: {"model": UserCredException, "description":"Not authenticated"},
              })
def change_password(*,
                    session: Session=Depends(get_session),
                    current_user: Users=Depends(get_current_user),
                    password_change: UserPasswordChange):

    # Check the password is correct or not
    if not pwd_context.verify(password_change.current_password + SALT, current_user.password):
        raise HTTPException(status_code=400, detail="パスワードが違います。")

    # Change the old password with the new password
    hashed_password = pwd_context.hash(password_change.new_password1 + SALT)
    current_user.password = hashed_password
    
    # Save it to DB
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return JSONResponse(
        status_code=200,
        content={"detail": "パスワードを変更しました"}
    )

@router.patch("/change_email",
               responses={
                  200: {"model": UserResponse},
                  400: {"model": UserError},
                  401: {"model": UserCredException, "description":"Token expired"},
                  403: {"model": UserCredException, "description":"Not authenticated"},
              })
def change_email(*,
                 session: Session=Depends(get_session),
                 current_user: Users=Depends(get_current_user),
                 email_change: UserEmailChange):
    # Check whether the new email is already being used in DB
    user_db = (
        session
        .exec(
            select(Users)
            .where(Users.email == email_change.new_email)
        )
        .first()
    )

    if user_db is not None:
        return JSONResponse(
            status_code=400,
            content={"detail": "そのメールはもう使っているメールです。他のメールを選んでくださうい。"}
        )

    # Check the password is correct or not
    if not pwd_context.verify(email_change.password1 + SALT, current_user.password):
        raise HTTPException(status_code=400, detail="パスワードが違います。")

    # Change the old email with the new email
    current_user.email = email_change.new_email
    
    # Save it to DB
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return JSONResponse(
        status_code=200,
        content={"detail": f"メールアドレスを変更しました: {current_user.email}"}
    )

@router.patch("/change_username",
               responses={
                  200: {"model": UserResponse},
                  400: {"model": UserError},
                  401: {"model": UserCredException, "description":"Token expired"},
                  403: {"model": UserCredException, "description":"Not authenticated"},
              })
def change_username(*,
                    session: Session=Depends(get_session),
                    current_user: Users=Depends(get_current_user),
                    username_change: UserUsernameChange):
    # Check whether the new username is already being used in DB
    user_db = (
        session
        .exec(
            select(Users)
            .where(Users.username == username_change.new_username)
        )
        .first()
    )

    if user_db is not None:
        return JSONResponse(
            status_code=400,
            content={"detail": "そのユーザー名はもう使われてます。他のユーザー名を選んでください。"}
        )

    # Check the password is correct or not
    if not pwd_context.verify(username_change.password1 + SALT, current_user.password):
        raise HTTPException(status_code=400, detail="パスワードが違います。")

    # Change the old username with the new username
    current_user.username = username_change.new_username
    
    # Save it to DB
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return JSONResponse(
        status_code=200,
        content={"detail": f"ユーザー名を変更しました: {current_user.username}"}
    )

@router.delete("/delete",
               responses={
                  200: {"model": UserResponse},
                  400: {"model": UserError},
                  401: {"model": UserCredException, "description":"Token expired"},
                  403: {"model": UserCredException, "description":"Not authenticated"},
              })
def delete_user(*,
                session: Session=Depends(get_session),
                current_user: Users=Depends(get_current_user),
                user_delete: UserDelete):
    # Check the password is correct or not
    if not pwd_context.verify(user_delete.password1 + SALT, current_user.password):
        raise HTTPException(status_code=400, detail="パスワードが違います。")

    # Delete the user
    session.delete(current_user)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": f"ユーザーを削除しました。"}
    )

@router.post("/reset_password",
             responses={
                 200: {"model": UserResponse},
                 400: {"model": UserError},
             })
def reset_password(*,
                   session: Session=Depends(get_session),
                   background_tasks: BackgroundTasks,
                   user_reset: UserResetPassword):
    # This method is weak at automated repetition attacks,
    # So you have to implement CAPTCHA at the frontend user interface!

    # Check whether the user exists or not, with the email
    user_db = (
        session
        .exec(
            select(Users)
            .where(
                (Users.email == user_reset.email)
            )
        )
        .first()
    )

    if user_db is None:
        raise HTTPException(status_code=400, detail="そのメールを使うユーザーは存在しません。")

    # Generate temporary password (10 letters)
    temp_password = secrets.token_urlsafe(10)
    
    # Convert it into a hashed password
    hashed_temp_password = pwd_context.hash(temp_password + SALT)

    # Change the old password into the temporary password
    user_db.password = hashed_temp_password

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    # Send an email with the temporary password
    # by using FastAPI's background task
    background_tasks.add_task(
        send_reset_password_mail,
        receiver=user_db.email,
        subject="【シャナリ】臨時パスワード【Shanaly】",
        temp_password=temp_password,
    )

    return JSONResponse(
        status_code=200,
        content={"detail": f"パスワードがリセットされました。登録した時のEメール( {user_db.email} )をご確認お願いいたします。臨時パスワードを使ってログインしてください。そして自分が欲しいパスワードに変更してください。"}
    )

@router.post("/upload_profile_pic")
def upload_profile_picture(*,
                           session: Session=Depends(get_session),
                           current_user: Users=Depends(get_current_user),
                           upload_profile_picture: UserProfilePictureUpload):
    current_user.picture = upload_profile_picture.picture

    # Save it to DB
    session.add(current_user)
    session.commit()
    
    return JSONResponse(
        status_code=200,
        content={"detail": "プロフィール写真は正常にアップロードされました。"}
    )

@router.get("/remove_profile_pic")
def remove_profile_picture(*,
                           session: Session=Depends(get_session),
                           current_user: Users=Depends(get_current_user)):
    current_user.picture = None

    # Save it to DB
    session.add(current_user)
    session.commit()

    return JSONResponse(
        status_code=200,
        content={"detail": "プロフィール写真を削除しました。"}
    )

@router.post("/change_profile_status_msg")
def change_profile_status_message(*,
                                  session: Session=Depends(get_session),
                                  current_user: Users=Depends(get_current_user),
                                  change_profile_status: UserProfileMsgChange):
    current_user.status_msg = change_profile_status.status_msg

    # Save it to DB
    session.add(current_user)
    session.commit()
    
    return JSONResponse(
        status_code=200,
        content={"detail": "プロフィールメッセージを変更しました。"}
    )