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


    // Reset Password Part
    import fastapi from "../lib/api";

    // Current datetime variable for preventing continuous clicking & too many requests toward API backend server
    let timeInterval = 300000; // [PARAMETER]
    let dateTimeNow = new Date();
    let dateTimeNowCount = 0;

    let success_msg = "";
    let err_msg = "";

    // Reset password variables
    let email = "";

    function resetPassword() {

        // Input Validation
        if (email === "") {
            err_msg = "空白は入力できません。"
            return;
        }

        // Check whether enough time has passed for updating this tab and its posts data
        let timeDiff = new Date() - new Date(dateTimeNow);

        if (timeDiff < timeInterval && dateTimeNowCount > 0) {
            err_msg = "5分後に試してください。";
            return;
        }

        let params = {
            email: email,
        }

        dateTimeNow = new Date();
        dateTimeNowCount += 1;
        
        fastapi(
            "post",
            "/api/account/reset_password",
            params,
            (result) => {
                err_msg = "";
                success_msg = result["detail"];

                // Reset current Datetime
                dateTimeNow = new Date();
                dateTimeNowCount += 1;

                // Reset CAPTCHA and Others
                captcha = null;
                captcha_matched = null;
                email = "";

            },
            (result) => {
                success_msg = "";
                err_msg = result["detail"];

                captcha_matched = null;

                if (typeof result["detail"] === 'object') {
                    
                    for (let i of result["detail"]) {

                        if (i["msg"].toLowerCase().includes("email")) {
                            err_msg = "正しいEメールではありません。";
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

    function clearValue() {
        captcha = null;
        captcha_matched = null;
        email = "";
    }

</script>


<!-- Modal: Reset Password -->
<div class="modal fade" id="resetPassword" tabindex="-1" aria-labelledby="resetPasswordLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="resetPasswordModalLabel">パスワードのリセット</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="resetPasswordClose" on:click={clearValue}></button>
        </div>
        <div class="modal-body">
            <div>
                <p>会員登録した時のEメールに臨時パスワードをお送りいたします。
                    臨時パスワードを使ってログインしパスワードを変更してください。</p>
            </div>
            <!-- Inputs -->
            <form method="post">
                <div class="mb-3">
                    <label for="your-email-forgot" class="mb-1">会員登録した時のEメール</label>
                    <input type="email" class="form-control" id="your-email-forgot" autocomplete="on" bind:value="{email}">
                </div>
            </form>

            {#if err_msg !== ""}
                <!-- Error message -->
                <div>
                    <div class="alert alert-primary" role="alert">
                        {err_msg}
                    </div>
                </div>
            {/if}
            {#if success_msg !== ""}
                <!-- Success message -->
                <div>
                    <div class="alert alert-success" role="alert">
                        <p class="fw-bolder">
                            <i class="bi bi-stars"></i>
                            {success_msg}
                        </p>
                    </div>
                </div>
            {/if}

            
            {#if email !== ""}
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
                <button type="button" class="btn btn-primary" on:click={resetPassword}>送信</button>
            {/if}
                
            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={clearValue}>閉じる</button>
        </div>
    </div>
    </div>
</div>

<style>

#image{
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