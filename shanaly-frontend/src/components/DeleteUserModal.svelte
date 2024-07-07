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

    // Delete User Part
    import { push } from "svelte-spa-router";
    import { is_login, access_token, userid, username, email, post_list_stored } from "../lib/store";
    import fastapi from "../lib/api";

    let err_msg = "";
    let success_msg = "";

    let password1 = "";
    let password2 = "";

    function logout() {
        $is_login = false;
        $access_token = "";
        $userid = 0;
        $username = "";
        $email = "";

        $post_list_stored = [];

        push("/user-login");

        // Close the modal
        document.getElementById("user-delete-modal-close").click();
    }

    function deleteUser() {

        if (window.confirm("本当にアカウントを削除しますか？")) {
            
            // Simple Data Validation from Frontend
            if (
                password1 === "" ||
                password2 === ""
            ) {
                err_msg = "空白の入力はできません。"
                return;
            }

            let params = {
                password1: password1,
                password2: password2,
            }

            fastapi(
                "delete",
                "/api/account/delete",
                params,
                (result) => {
                    err_msg = "";
                    captcha = null;
                    captcha_matched = null;
                    success_msg = result["detail"];

                    // Reset
                    password1 = "";
                    password2 = "";

                    // Logout
                    logout();
                },
                (result) => {
                    success_msg = "";
                    captcha_matched = null;

                    if (result["detail"] === 'パスワードが正しくではありません。') {
                        err_msg = 'パスワードが正しくではありません。';
                        return;
                    }

                    if (typeof result["detail"] === 'object') {

                        for (let i of result["detail"]) {
                            if (i["msg"].toLowerCase().includes("password1 and password2")) {
                                err_msg = "パスワードたちが一致しません。";
                                return;
                            }
                        }
                    } 
                }
            )
            
        } else {
            return;
        }
    }

    function resetMatchNotMatch() {
        captcha_matched = null; 
    }

</script>

<!-- User Delete Modal -->
<div class="modal fade" id="userDeleteModal" tabindex="-1" aria-labelledby="userDeleteModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="userDeleteModalLabel">アカウントの削除</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="user-delete-modal-close"></button>
        </div>
            
        
            <div class="modal-body">

                <div class="alert alert-danger fw-bolder" role="alert">
                    本当にアカウントを削除しますか？今までの投稿やレポートやリプライや良いねなどが全部削除されます。回復できませんので、ご注意ください。削除後にはログイン画面に戻ります。
                </div>
                
                <form method="delete">
                    <!-- Input Password 1-->
                    <div class="mb-3">
                        <label for="password1_deleteuser">パスワード</label>
                        <input type="password" class="form-control" id="password1_deleteuser" autocomplete="off" bind:value={password1}>
                    </div>
                    <!-- Input Password 2-->
                    <div class="mb-3">
                        <label for="password2_deleteuser">パスワード（再入力）</label>
                        <input type="password" class="form-control" id="password2_deleteuser" autocomplete="off" bind:value={password2}>
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


                {#if password1 !== "" && password2 !== ""}
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
                <button type="button" class="btn btn-danger" on:click={deleteUser}>削除</button>
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