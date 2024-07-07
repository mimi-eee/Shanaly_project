<script>
    // CAPTCHA
    let captcha;
    let captcha_matched;

    function generate() {

        // Clear old input
        document.getElementById("submit").value = "";

        // Access the element to store
        // the generated captcha
        captcha = document.getElementById("image");
        let uniquechar = "";

        const randomchar = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        // Generate captcha for length of
        // 6 with random character
        for (let i = 1; i < 7; i++) {
            uniquechar += randomchar.charAt(
                Math.random() * randomchar.length)
        }

        // Store generated input
        captcha.innerHTML = uniquechar;
    }

    function printmsg() {
        const usr_input = document
            .getElementById("submit").value;

        // Check whether the input is equal
        // to generated captcha or not
        if (usr_input == captcha.innerHTML) {
            generate();
            captcha_matched = true;
        }
        else {
            generate();
            captcha_matched = false;
        }
    }

    // Change Password Part
    import fastapi from "../lib/api";
    import { username } from "../lib/store";

    let err_msg = "";
    let success_msg = "";

    let new_username = "";
    let password1 = "";
    let password2 = "";

    function changeUsername() {

        // Simple Data Validation from Frontend
        if (
            new_email === "" ||
            password1 === "" ||
            password2 === ""
        ) {
            err_msg = "空白の入力はできません。"
            return;
        }

        let params = {
            new_username: new_username,
            password1: password1,
            password2: password2,
        }

        fastapi(
            "patch",
            "/api/account/change_username",
            params,
            (result) => {
                err_msg = "";
                captcha = null;
                captcha_matched = null;
                success_msg = result["detail"];

                // Change the username store variable
                $username = new_username;

                // Reset
                new_username = "";
                password1 = "";
                password2 = "";

            },
            (result) => {
                success_msg = "";
                captcha_matched = null;

                if (result["detail"].includes("ユーザー名")) {
                    err_msg = "そのユーザー名はもう使われてます。他のユーザー名を選んでください。";
                    return;
                }

                if (result["detail"] === 'パスワードが正しくではありません。') {
                    err_msg = 'パスワードが正しくではありません。';
                    return;
                }

                if (typeof result["detail"] === 'object') {

                    for (let i of result["detail"]) {
                        if (i["type"] === "string_too_short") {
                            err_msg = "新しいパスワードが短いです。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("email")) {
                            err_msg = "正しいEメールではありません。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("password1 and password2")) {
                            err_msg = "パスワードたちが一致しません。";
                            return;
                        }
                    }
                } 
            }
        )
    }

    function resetMatchNotMatch() {
        captcha_matched = null; 
    }

</script>

<!-- Username Change Modal -->
<div class="modal fade" id="usernameChangeModal" tabindex="-1" aria-labelledby="usernameChangeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="usernameChangeModalLabel">ユーザー名の変更</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="username-change-modal-close"></button>
        </div>
            <div class="modal-body">

                
                <form method="post">
                    <!-- Input New Email -->
                    <div class="mb-3">
                        <label for="new_username">新しいユーザー名</label>
                        <input type="text" class="form-control" id="new_username" autocomplete="off" bind:value={new_username}>
                    </div>
                    <!-- Input Password 1-->
                    <div class="mb-3">
                        <label for="password1_usernamechange">パスワード</label>
                        <input type="password" class="form-control" id="password1_usernamechange" autocomplete="off" bind:value={password1}>
                    </div>
                    <!-- Input Password 2-->
                    <div class="mb-3">
                        <label for="password2_usernamechange">パスワード（再入力）</label>
                        <input type="password" class="form-control" id="password2_usernamechange" autocomplete="off" bind:value={password2}>
                    </div>
                </form>


                {#if err_msg !== ""}
                    <!-- Error message -->
                    <div class="mt-2">
                        <div class="alert alert-primary" role="alert">
                            {err_msg}
                        </div>
                    </div>
                {/if}
                {#if success_msg !== ""}
                    <!-- Success message -->
                    <div class="mt-2">
                        <div class="alert alert-success" role="alert">
                            <p class="fw-bolder">
                                <i class="bi bi-stars"></i>
                                {success_msg}
                            </p>
                        </div>
                    </div>
                {/if}

                
                {#if new_username !== "" && password1 !== "" && password2 !== ""}
                    <!-- CAPTCHA -->
                    <div class="container mx-0 px-0">
                        <div class="mb-2">
                            <p>イメージを生成し見える文字を入力して「確認」ボタンをクリックしてください。</p>
                        </div>
                        <div class="d-flex flex-row gap-1 mb-2">
                            <!-- Generated Image will be here -->
                            <div id="image" class="inline" selectable="False"></div>
                            <!-- Random Generator Button-->
                            <button class="btn btn-lg btn-outlie-primary" type="button" on:click={generate} on:click={resetMatchNotMatch}>
                                <i class="bi bi-arrow-clockwise">生成</i>
                            </button>
                        </div>
                        <!-- User Input -->
                        <div class="p-0 m-0 mb-2">
                            <div id="user-input" class="inline">
                                <input type="text" class="form-control" id="submit" placeholder="">
                            </div>
                        </div>
                        <!-- Check Button -->
                        <div class="b-2 d-flex flex-row gap-2">
                            <button type=button class="btn btn-outline-primary" on:click={printmsg}>確認</button>
                            {#if captcha_matched === true}
                                <p class="fw-bolder" style="font-size: 30px;"><i class="bi bi-check-lg"></i></p>
                            {:else if captcha_matched === false}
                                <p class="fw-bolder" style="font-size: 30px;"><i class="bi bi-x-lg"></i></p>
                            {:else}
                                <p></p>
                            {/if}
                        </div>
                    </div>
                {/if}


            </div>
        
        
        
            <div class="modal-footer">
            
            {#if captcha_matched === true}
                <button type="button" class="btn btn-primary" on:click={changeUsername}>送信</button>
            {/if}

            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>

        </div>
    </div>
    </div>
</div>

<style>

#image {
    margin-top: 5px;
    width: 120px;;
    font-weight: 400;
    height: 40px;
    user-select: none;
    text-decoration:line-through;
    font-style: italic;
    font-size: x-large;
    border: red 2px solid;
}

</style>