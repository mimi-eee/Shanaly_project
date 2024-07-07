<script>
    export let profileStatusMsg;

    import fastapi from "../lib/api";

    let err_msg = "";
    let success_msg = "";

    function changeProfileMsg() {

        // Get modified profile status messag text value
        let new_profile_msg = document.getElementById("new_profile_msg").value;

        if (new_profile_msg === profileStatusMsg) {
            if (success_msg !== "") {
                success_msg = "";
            }
            err_msg = "既存のプロフィールメッセージと同じです。";
            return;
        }
        
        // Simple data validation
        if (new_profile_msg === "" || new_profile_msg === undefined || new_profile_msg === null) {
            if (success_msg !== "") {
                success_msg = "";
            }
            err_msg = "空白は入力できません。";
            return;
        }

        let params = {
            status_msg: new_profile_msg,
        }
        
        fastapi(
            "post",
            "/api/account/change_profile_status_msg",
            params,
            (result) => {
                err_msg = "";
                success_msg = result["detail"];

                // Reset Values
                profileStatusMsg = new_profile_msg;
            },
            (result) => {
                
                // Display Error Message
                if (typeof result["detail"] === 'string') {
                    success_msg = "";
                    err_msg = result["detail"];
                    return;
                } 
                if (typeof result["detail"] === 'object') {
                    
                    for (let i of result["detail"]) {
                        if (i["type"].toLowerCase().includes("string_too_long")) {
                            err_msg = "プロフィールメッセージが長すぎます。";
                            return;
                        }
                    }
                }
            }
        )
    }

    function clearValue() {
        success_msg = "";
        err_msg = "";
        document.getElementById("new_profile_msg").value = profileStatusMsg;
    }

</script>



<!-- Username Change Modal -->
<div class="modal fade" id="profileStatusMsgChangeModal" tabindex="-1" aria-labelledby="profileStatusMsgChangeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="profileStatusMsgChangeModalLabel">プロフィールメッセージの変更</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="profile-status-msg-change-modal-close" on:click={clearValue}></button>
        </div>
            <div class="modal-body">

                <form method="post">
                    <!-- Input Profile Status -->
                    <div class="mb-3">
                        <label for="new_profile_msg">新しいプロフィールメッセージ</label>
                        <textarea class="form-control mt-1" id="new_profile_msg" rows="5" value={profileStatusMsg}></textarea>
                    </div>
                </form>
                
                <!-- Alert Messages -->
                {#if err_msg !== ""}
                    <div class="alert alert-primary" role="alert">
                        {err_msg}
                    </div>
                {/if}
                {#if success_msg !== ""}
                    <div class="alert alert-success" role="alert">
                       {success_msg}
                    </div>
                {/if}
            </div>
        
        
            <div class="modal-footer">

            <button type="button" class="btn btn-outline-primary" on:click={changeProfileMsg}>OK</button>
            
            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={clearValue}>閉じる</button>

        </div>
    </div>
    </div>
</div>