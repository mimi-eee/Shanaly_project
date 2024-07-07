<script>
    export let unique_name;

    export let current_post_id;

    import { post_list_stored } from "../lib/store";
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    
    // Delete the target post
    function deletePost() {
        
        // Set the target_post_id by getting value from current_post_id
        let target_post_id = null;
        target_post_id = current_post_id;
        
        fastapi(
            "delete",
            `/api/post/delete/${target_post_id}`,
            {},
            (json) => {

                // Reset the current_post_id
                current_post_id = null;

                // Close the detail modal itself as well as the delete modal
                // because there is no more detail modal for this anymore!
                // You need to set the proper id in the modal button!
                document.querySelector("[id='delete-modal-button']").click();

                // Update the post_list and $post_list_stored
                for (let i = 0; i < $post_list_stored.length; i++) {
                    if ($post_list_stored[i]["id"] === target_post_id) {
                         // Update $post_list_stored
                         delete $post_list_stored[i]
                    }
                }

                // Remove empty object in the array
                $post_list_stored = $post_list_stored.filter(Object => Object);

                // push back to the home
                push("/");
                location.reload();
            },
            (json) => {
                // Do nothing
            }
        )
    }
</script>

<!-- Delete Modal after the detail modal -->
<div class="modal fade" id="deleteModalToggle_{unique_name}" aria-hidden="true" aria-labelledby="deleteModalToggleLabel" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="deleteModalToggleLabel"><i class="bi bi-trash-fill"></i> 投稿の削除</h1>
          <!-- The next button has its own id! -->
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="delete-modal-button"></button>
        </div>
        <div class="modal-body">
           この投稿を削除しますか？削除すると戻せないのでご注意ください。
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-primary" on:click={deletePost}>削除</button>
          <!-- The below data-bs-ratget should be the id of the detail modal -->
          <button class="btn btn-outline-primary" data-bs-target="#detailModal_{unique_name}" data-bs-toggle="modal" id="modify-go-back-button">戻る</button>
        </div>
      </div>
    </div>
</div>