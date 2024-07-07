<script>
    import fastapi from "../lib/api";
    import { push } from "svelte-spa-router";
    import { access_token, userid, username, email, is_login } from "../lib/store"

    import CreateAccountModal from "../components/CreateAccountModal.svelte";
    import ResetPasswordModal from "../components/ResetPasswordModal.svelte";

    // Error message
    let err_msg = "";

    // Login variables
    let login_email = "";
    let login_password = "";


    function login(event) {

        event.preventDefault();

        if (login_email === "" || login_password === "" ||
        login_email === null || login_password === null ||
        login_email === undefined || login_password === undefined) {
            err_msg = "空白の入力はできません。"
        } else {
            let params = {
                email: login_email,
                password: login_password,
            };
            fastapi(
                "login",
                "/api/account/login",
                params,
                (json) => {
                    // Set store variables, based on the token
                    $access_token = json.access_token;
                    $userid = json.userid;
                    $username = json.username;
                    $email = json.email;
                    $is_login = true;
                    err_msg = "";
                    push("/");
                },
                (json) => {
                    err_msg = json["detail"];
                }
            )
        }
    }

</script>



<div class="container-sm">
    <h2 class="my-3 mx-0 pb-3 border-bottom">ログイン</h2>
    
    {#if err_msg !== ""}
        <div class="alert alert-primary" role="alert">
            {err_msg}
        </div>
    {/if}

    <form method="post">
        <!-- Input Email -->
        <div class="mb-3">
            <label for="email">Eメール</label>
            <input type="text" class="form-control" id="email" autocomplete="on" bind:value="{login_email}">
        </div>
        <!-- Input Password -->
        <div class="mb-3">
            <label for="password">パスワード</label>
            <input type="password" class="form-control" id="password" autocomplete="on" bind:value="{login_password}">
        </div>

        <div class="d-flex flex-column gap-1">
            <!-- Login Button -->
            <button 
            type="submit" 
            class="btn btn-outline-primary" 
            style="font-size: 20px;"
            on:click={login}>ログイン</button>

            <!-- Forgot Password Button-->
            <button
            type="button"
            class="btn btn-outline-primary"
            style="font-size: 20px;"
            data-bs-toggle="modal"
            data-bs-target="#resetPassword">
                パスワードを忘れた方はこちら
            </button>
            <!-- Create Account Button-->
            <button 
                type="button" 
                class="btn btn-outline-primary"
                style="font-size: 20px;"
                data-bs-toggle="modal" 
                data-bs-target="#createAccount">
                <i class="bi bi-stars"></i>会員登録
            </button>
        </div>

    </form>

    <!-- Modal: Reset Password -->
    <ResetPasswordModal/>

    <!-- Modal: Create Account -->
    <CreateAccountModal/>


</div>


<style>

.container-sm {
    max-width: 576px;
}

</style>


