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

    let err_msg = "";
    let success_msg = "";

    let old_password = "";
    let new_password1 = "";
    let new_password2 = "";

    function changePassword() {

        // Simple Data Validation from Frontend
        if (
            old_password === "" ||
            new_password1 === "" ||
            new_password2 === ""
        ) {
            err_msg = "空白の入力はできません。"
            return;
        }

        let params = {
            current_password: old_password,
            new_password1: new_password1,
            new_password2: new_password2,
        }

        fastapi(
            "patch",
            "/api/account/change_password",
            params,
            (result) => {
                err_msg = "";
                captcha = null;
                captcha_matched = null;
                success_msg = result["detail"];

                // Reset
                old_password = "";
                new_password1 = "";
                new_password2 = "";

            },
            (result) => {
                success_msg = "";
                captcha_matched = null;

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
                            err_msg = "新しいパスワードたちが一致しません。";
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

<!-- Password Change Modal -->
<div class="modal fade" id="passwordChangeModal" tabindex="-1" aria-labelledby="passwordChangeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="passwordChangeModalLabel">パスワードの変更</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="password-change-modal-close"></button>
        </div>
            <div class="modal-body">
                
                
                <form method="post">
                    <!-- Input Old Password -->
                    <div class="mb-3">
                        <label for="old_password">現在のパスワード</label>
                        <input type="password" class="form-control" id="old_password" autocomplete="off" bind:value={old_password}>
                    </div>
                    <!-- Input New Password 1-->
                    <div class="mb-3">
                        <label for="new_password1">新しいパスワード</label>
                        <input type="password" class="form-control" id="new_password1" autocomplete="off" bind:value={new_password1}>
                    </div>
                    <!-- Input New Password 2-->
                    <div class="mb-3">
                        <label for="new_password2">新しいパスワード（再入力）</label>
                        <input type="password" class="form-control" id="new_password2" autocomplete="off" bind:value={new_password2}>
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

                
                {#if old_password !== "" && new_password1 !== "" && new_password2 !== ""}
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
                <button type="button" class="btn btn-primary" on:click={changePassword}>送信</button>
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