from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    ValidationInfo,
    Field,
)

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(max_length=30)
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)

    @field_validator("username","password1","password2","email")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise ValueError("Blank value is not allowed")
        return v
    
    @field_validator("password2")
    @classmethod
    def password_match(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if "password1" in data and v != data["password1"]:
            raise ValueError("Password1 and Password2 are not equal")
        return v
    
    @field_validator("password1")
    @classmethod
    def password_upper_lower_mix(clas, v: str) -> str:
        if ( sum(1 for c in v if c.islower()) == 0) or (sum(1 for c in v if c.isupper()) == 0 ):
            raise ValueError("Password should have lower & upper mixed characters")
        return v

    @field_validator("password1")
    @classmethod
    def password_special_chracter(clas, v: str) -> str:
        special_characters = "[@_!#$%^&*()<>?/\|}{~:]"
        if sum(1 for c in v if (c in special_characters)) == 0:
            raise ValueError("Password should have special characters")
        return v

    @field_validator("username")
    @classmethod
    def not_include_admin_username(cls, v: str):
        if (
            "admin" in v.lower() or
            "shanaly" in v.lower() or
            "シャナリ" in v.lower() or
            "しゃなり" in v.lower()):
            raise ValueError("Username cannot have a substring 'admin'")
        return v

class UserVerifyRequest(BaseModel):
    token: str
    
class UserLoginForm(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email","password")
    @classmethod
    def not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError("Blank value is not allowed")
        return v

class UserResponse(BaseModel):
    detail: str

class UserSuccess(BaseModel):
    detail: str

class UserError(BaseModel):
    detail: str

class UserCredException(BaseModel):
    detail: str

class Token(BaseModel):
    access_token: str
    token_type: str
    email: str
    userid: int
    username: str
    email: str

class UserPasswordChange(BaseModel):
    current_password: str
    new_password1: str = Field(min_length=3)
    new_password2: str = Field(min_length=3)

    @field_validator("current_password","new_password1","new_password2")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise ValueError("Blank value is not allowed")
        return v

    @field_validator("new_password2")
    @classmethod
    def password_match(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if "new_password1" in data and v != data["new_password1"]:
            raise ValueError("Password1 and Password2 are not equal")
        return v
    
    @field_validator("new_password1")
    def no_difference_new_old_password(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if v == data["current_password"]:
            raise ValueError("New password is same with the current password")
        return v
    
class UserEmailChange(BaseModel):
    new_email: EmailStr
    password1: str
    password2: str

    @field_validator("new_email","password1","password2")
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise ValueError("Blank value is not allowed.")
        return v

    @field_validator("password2")
    def password_match(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if "password1" in data and v != data["password1"]:
            raise ValueError("Password1 and Password2 are not equal")
        return v
    
class UserUsernameChange(BaseModel):
    new_username: str
    password1: str
    password2: str

    @field_validator("new_username","password1","password2")
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise ValueError("Blank value is not allowed.")
        return v

    @field_validator("password2")
    def password_match(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if "password1" in data and v != data["password1"]:
            raise ValueError("Password1 and Password2 are not equal")
        return v
    
class UserDelete(BaseModel):
    password1: str
    password2: str

    @field_validator("password1","password2")
    def not_blank(cls, v: str) -> str:
        if v == "" or v.strip() == "":
            raise ValueError("Blank value is not allowed.")
        return v

    @field_validator("password2")
    def password_match(cls, v: str, values: ValidationInfo) -> str:
        data = values.data
        if "password1" in data and v != data["password1"]:
            raise ValueError("Password1 and Password2 are not equal")
        return v
    
class UserResetPassword(BaseModel):
    email: EmailStr

class UserProfilePictureUpload(BaseModel):
    picture: str

class UserProfileMsgChange(BaseModel):
    status_msg: str = Field(max_length=200)