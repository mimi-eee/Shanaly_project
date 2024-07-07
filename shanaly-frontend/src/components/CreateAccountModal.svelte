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

    // Create Account Part

    import fastapi from "../lib/api";

    // Current datetime variable for preventing continuous clicking & too many requests toward API backend server
    let timeInterval = 5000; // [PARAMETER]
    let dateTimeNow = new Date();
    let dateTimeNowCount = 0;

    let success_msg = "";
    let err_msg = "";

    let email = "";
    let email_confirm = "";
    let agreeValue = false;
    let username = "";
    let password1 = "";
    let password2 = "";

    function createAccount(event) {

        event.preventDefault();

        // Simple Data Validation from Frontend
        if (
            email === "" ||
            username === "" ||
            password1 === "" ||
            password2 === ""
        ) {
            err_msg = "空白の入力はできません。"
            return;
        }

        if (email !== email_confirm) {
            err_msg = "入力いただいたメーレアドレスが一致しません。";
            return;
        }

        if (agreeValue === false) {
            err_msg = "利用契約の同義しないと会員登録ができません。"
            return;
        }

        // Check whether enough time has passed for updating this tab and its posts data
        let timeDiff = new Date() - new Date(dateTimeNow);

        if (timeDiff < timeInterval && dateTimeNowCount > 0) {
            err_msg = "セキュリティーの問題のため再実行を制限しております。10分後に試してください。";
            return;
        }
        
        let params = {
            email: email,
            username: username,
            password1: password1,
            password2: password2,
        }

        fastapi(
            "post",
            "/api/account/create",
            params,
            (result) => {
                // Set success messge
                // Remove error message
                err_msg = "";
                success_msg = result["detail"];

                // Reset the input values
                email = "";
                username = "";
                password1 = "";
                password2 = "";

                // Reset current Datetime
                dateTimeNow = new Date();
                dateTimeNowCount += 1;

                // Reset CAPTCHA
                captcha_matched = null; 

            },
            (result) => {
                // Error Case

                // Reset CAPTCHA
                captcha_matched = null; 

                // Display Error Message
                if (typeof result["detail"] === 'string') {
                    err_msg = result["detail"];
                    return;
                } 
                if (typeof result["detail"] === 'object') {
                    
                    for (let i of result["detail"]) {

                        if (i["msg"].toLowerCase().includes("email")) {
                            err_msg = "正しいEメールではありません。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("admin")) {
                            err_msg = "adminやshanalyやシャナリなどが入るユーザー名は使えません。";
                            return;
                        }
                        if (i["type"].toLowerCase().includes("string_too_long")) {
                            err_msg = "ユーザー名が長すぎです。最大15文字です。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("password1 and password2")) {
                            err_msg = "入力いただいたパスワードたちがお互いに一致しません。";
                            return;
                        }
                        if (i["type"].toLowerCase().includes("string_too_short")) {
                            err_msg = "パスワードの長さが正しくではありません。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("password1 and password2")) {
                            err_msg = "入力いただいたパスワードたちがお互いに一致しません。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("lower & upper")) {
                            err_msg = "パスワードには小文字と大文字の組み合わせが必要です。";
                            return;
                        }
                        if (i["msg"].toLowerCase().includes("special character")) {
                            err_msg = "パスワードには特殊文字が必要です。";
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
        username = "";
        password1 = "";
        password2 = "";

        success_msg = "";
        err_msg = "";

        agreeValue = false;
        document.getElementById("agreeCheckBox").checked = false;
        
    }

    function changeAgreeValue() {
        if (document.getElementById("agreeCheckBox").checked === true) {
            agreeValue = true;
        } else {
            agreeValue = false;
        }
    }

</script>



 <!-- Modal: Create Account -->
 <div class="modal fade" id="createAccount" tabindex="-1" aria-labelledby="createAccountLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <div class="modal-header">
        <h5 class="modal-title" id="createAccountModalLabel">会員登録</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="createAccountClose" on:click={clearValue}></button>
        </div>
        <div class="modal-body">

            <div class="mb-3">
                <!-- Accordion for Agreement -->
                <div class="accordion" id="accordionExample">
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                        <button id="agree-accord" class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            ユーザー名の設定などについて
                        </button>
                        </h2>
                    <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                        <div class="accordion-body">
                            <p class="my-0" style="font-size: 13px;">
                                <a href="https://shanaly.net/terms-of-use/" target="_blank" style="color: blue;">Shanalyの利用規約
                                </a>
                            </p>
                            <p class="mt-0 mb-3" style="font-size: 13px;">
                                <a href="https://shanaly.net/privacy-policy/" target="_blank" style="color: blue;">Shanalyのプライバシーポリシー
                                </a>
                            </p>
                            <p style="font-size: 13px;">
                                本サービスでは、なりすまし及び詐欺広告等を防止する目的で、人名（フルネーム）となり得るユーザー名の設定を一律ご遠慮いただいております。たとえご本人様であってもニックネームなどをご使用ください。なお、人名（フルネーム）の使用やプロフィール写真等を勘案して特定の個人を想起させるようなアカウントを発見した際には、アカウントを一時停止の上、ユーザー名やプロフィール写真の変更を運営よりご依頼致します。皆様が安心してご利用いただけますようご協力のほどよろしくお願い致します。
                            </p>
                            <p style="font-size: 13px;">
                                ＊今後、ご本人様確認が可能なプラン等も導入予定です。それまでは恐れ入りますが上記運用とさせていただきます。
                            </p>
                        </div>
                    </div>
                    </div>
                </div>

                <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="agreeCheckBox" on:click={changeAgreeValue} style="outline: 1px solid black;">
                    <label class="form-check-label" for="flexCheckDefault">
                        上記の内容に同意しました。
                    </label>
                </div>
            </div>
            
            {#if agreeValue === true}
            
            <form method="post">
                <!-- Input Email -->
                <div class="mb-3">
                    <label for="email_create">Eメール</label>
                    <input type="text" class="form-control" id="email_create" autocomplete="off" bind:value={email}>
                </div>
                <!-- Input Email Confirmation -->
                <div class="mb-3">
                    <label for="email_create_confirm">Eメール(再入力)</label>
                    <input type="text" class="form-control" id="email_create_confirm" autocomplete="off" bind:value={email_confirm}>
                </div>
                <!-- Input Username -->
                <div class="mb-3">
                    <label for="username_create">ユーザー名</label>
                    <input type="text" class="form-control" id="username_create" autocomplete="off" bind:value={username}>
                </div>
                <!-- Input Password 1-->
                <div class="mb-3">
                    <label for="password_create1">パスワード
                        <p class="my-0 fw-bolder" style="font-size:10px; color:gray;">※長さ8文字以上・小/大文字の組み合わせ・特殊文字必要</p>
                        <p class="my-0" style="font-size:10px; color:gray;">シャナリはユーザーの個人情報やセキュリティーを大事にしております。</p>
                    </label>
                    <input type="password" class="form-control" id="password_create1" autocomplete="off" bind:value={password1}>
                </div>
                <!-- Input Password 2-->
                <div class="mb-3">
                    <label for="password_create2">パスワード(再入力)</label>
                    <input type="password" class="form-control" id="password_create2" autocomplete="off" bind:value={password2}>
                </div>
            </form>


            {/if}


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


            {#if email !== "" && username !== "" && password1 !== "" && password2 !== "" && agreeValue !== false}
                <!-- CAPTCHA -->
                <div class="container mx-0 px-0">
                    <div class="mb-2">
                        <p class="fw-bold">※イメージを生成し見える文字を入力して「確認」ボタンをクリックしてください。</p>
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
            <button type="button" class="btn btn-primary" on:click={createAccount}>作成</button>
            
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