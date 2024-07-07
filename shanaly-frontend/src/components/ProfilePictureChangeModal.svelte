<script>
    export let imgUrl = null;

    import ImageUpload from "./ImageUpload.svelte";
    import fastapi from "../lib/api";

    let err_msg = "";
    let success_msg = "";

    // Image Base64 String
    let imgUrlInside = null;

    function uploadProfilePicture() {

        if (imgUrlInside === null) {
            err_msg = "写真イメージをアップロードしてください。";
            return;
        }

        let params = {
            picture: imgUrlInside,
        }

        fastapi(
            "post",
            "/api/account/upload_profile_pic",
            params,
            (result) => {
                err_msg = "";
                success_msg = result["detail"];
                // Set the profile picture outside this modal
                imgUrl = imgUrlInside;
                imgUrlInside = null;
            },
            (result) => {
                success_msg = "";
                err_msg = result["detail"];
            }
        )
    }

    function removeProfilePicture() {
        if (imgUrl === null) {
            err_msg = "削除するプロフィール写真がないです。";
            return;
        }
        fastapi(
            "get",
            "/api/account/remove_profile_pic",
            {},
            (result) => {
                err_msg = "";
                success_msg = result["detail"];
                
                // Remove the profile picture on fronend side and modal side both
                imgUrl = null;
                imgUrlInside = null;
            },
            (result) => {
                success_msg = "";
                err_msg = result["detail"];
            }
        )
    }

    function clearAlerts() {
        success_msg = "";
        err_msg = "";
    }

</script>


<!-- Username Change Modal -->
<div class="modal fade" id="profilePictureChangeModal" tabindex="-1" aria-labelledby="profilePictureChangeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="profilePictureChangeModalLabel">プロフィール写真の変更</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="profile-picture-change-modal-close"></button>
        </div>
            <div class="modal-body">

                <div class="d-flex flex-column align-items-center justify-content-center">
                    <!-- Profile Image -->
                    {#if imgUrl !== null}
                        <img src={imgUrl} id="profile-pic" alt="profile_picture" style="width: 200px; height: 200px">
                    {:else if (imgUrlInside !== null)}
                        <img src={imgUrlInside} id="profile-pic" alt="profile_picture" style="width: 200px; height: 200px">
                    {:else}
                        <p class="fs-1 pt-2 pb-0"><i class="bi bi-person"></i></p>
                    {/if}
                </div>
                <!-- Image Upload Button -->
                <div class="d-flex flex-column align-items-center justify-content-center my-2">
                    <div>
                        <ImageUpload bind:imgUrl={imgUrlInside} limitSizeByte={300000}/>
                    </div>
                </div>
                {#if imgUrl !== null}
                    <!-- Remove Picture Button -->
                    <div class="d-flex flex-column align-items-end justify-content-end my-2">
                        <button type="button" class="btn btn-outline-primary" on:click={removeProfilePicture}>
                            <i class="bi bi-trash"></i> 削除
                        </button>
                    </div>
                {/if}
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

            {#if imgUrlInside !== null}
                <button type="button" class="btn btn-primary" on:click={uploadProfilePicture}>OK</button>
            {/if}

            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={clearAlerts}>閉じる</button>

        </div>
    </div>
    </div>
</div>

<style>

#profile-pic {
  border-radius: 50%;
}

</style>