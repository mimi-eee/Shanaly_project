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
    import { email } from "../lib/store";

    let err_msg = "";
    let success_msg = "";

    let new_email = "";
    let password1 = "";
    let password2 = "";

    function changeEmail() {

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
            new_email: new_email,
            password1: password1,
            password2: password2,
        }

        fastapi(
            "patch",
            "/api/account/change_email",
            params,
            (result) => {
                err_msg = "";
                captcha = null;
                captcha_matched = null;
                success_msg = result["detail"];

                // Set the new email
                $email = new_email;

                // Reset
                new_email = "";
                password1 = "";
                password2 = "";

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

<!-- Email Change Modal -->
<div class="modal fade" id="emailChangeModal" tabindex="-1" aria-labelledby="emailChangeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="emailChangeModalLabel">メールの変更</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="email-change-modal-close"></button>
        </div>
            <div class="modal-body">
                

                <form method="post">
                    <!-- Input New Email -->
                    <div class="mb-3">
                        <label for="new_email">新しいメールアドレス</label>
                        <input type="text" class="form-control" id="new_email" autocomplete="off" bind:value={new_email}>
                    </div>
                    <!-- Input Password 1-->
                    <div class="mb-3">
                        <label for="password1_emailchange">パスワード</label>
                        <input type="password" class="form-control" id="password1_emailchange" autocomplete="off" bind:value={password1}>
                    </div>
                    <!-- Input Password 2-->
                    <div class="mb-3">
                        <label for="password2_emailchange">パスワード（再入力）</label>
                        <input type="password2" class="form-control" id="password2_emailchange" autocomplete="off" bind:value={password2}>
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

                
                {#if new_email !== "" && password1 !== "" && password2 !== ""}
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
                <button type="button" class="btn btn-primary" on:click={changeEmail}>提出</button>
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