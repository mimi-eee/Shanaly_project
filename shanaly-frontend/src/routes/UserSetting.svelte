<script>
    import PasswordChangeModal from "../components/PasswordChangeModal.svelte";
    import EmailChangeModal from "../components/EmailChangeModal.svelte";
    import UsernameChangeModal from "../components/UsernameChangeModal.svelte";
    import DeleteUserModal from "../components/DeleteUserModal.svelte";
    import ProfilePictureChangeModal from "../components/ProfilePictureChangeModal.svelte";
    import ProfileStatusMsgChangeModal from "../components/ProfileStatusMsgChangeModal.svelte";

    import { username, email } from "../lib/store";
    import fastapi from "../lib/api";

    let err_msg = "";

    let user_data = {};
    let current_plan_name_eng = "";
    let profile_picture = null;
    let profile_status_msg = "";

    fastapi(
        "get",
        `/api/user/info/${$username}`,
        {},
        (result) => {
            user_data = result;
            current_plan_name_eng = user_data["user_info"]["plan"]["plan_name_eng"];
            profile_picture = user_data["user_info"]["picture"];
            profile_status_msg = user_data["user_info"]["status_msg"];
        },
        (result) => {
            // Do nothing
        }
    )

    

</script>

<div class="container-sm">

    <div class="container my-3 p-0">
        <h1><i class="bi bi-gear"></i> アカウント設定</h1>
    </div>

    <div class="container my-3 p-0">
        <div class="d-flex flex-row gap-2 align-items-center">
            <!-- Profile Image -->
            {#if profile_picture !== null}
                <img src={profile_picture} id="profile-pic" alt="profile_picture" style="width: 70px; height: 70px">
            {:else}
                <p class="fs-3 pt-2 pb-0"><i class="bi bi-person"></i></p>
            {/if}
            <h2 class="fw-bold">{$username}</h2>
        </div>
        <p>( {$email} )</p>
        <p class="text-break word-wrap">{profile_status_msg}</p>
        <p>ご利用のプラン： {current_plan_name_eng}</p>
    </div>
    

    <div class="btn-group-vertical d-flex gap-2" role="group" aria-label="Vertical button group">
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#planChangeModal" disabled><i class="bi bi-stars"></i> プランの変更</button>
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#passwordChangeModal">パスワードの変更</button>
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#profilePictureChangeModal"><i class="bi bi-person"></i>プロフィール写真の変更</button>
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#profileStatusMsgChangeModal"><i class="bi bi-chat-left-dots"></i> プロフィールメッセージの変更</button>
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#emailChangeModal">メールアドレスの変更</button>
        <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#usernameChangeModal">ユーザー名の変更</button>
        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#userDeleteModal">アカウントの削除</button>
    </div>
    
    <PasswordChangeModal/>

    <EmailChangeModal/>

    <UsernameChangeModal/>

    <DeleteUserModal/>

    <ProfilePictureChangeModal bind:imgUrl={profile_picture}/>

    <ProfileStatusMsgChangeModal bind:profileStatusMsg={profile_status_msg}/>

</div>


<style>

.container-sm {
    max-width: 576px;
}

#profile-pic {
  border-radius: 50%;
}

</style>