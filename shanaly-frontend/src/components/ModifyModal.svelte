<script>
    export let unique_name;

    export let current_post_id;
    export let current_post_title;
    export let current_post_content;
    export let current_post_tags;
    export let current_post_tags_arr;
    export let editor;

    import { post_list_stored } from "../lib/store";
    import fastapi from "../lib/api";
    import TextEditor from "./TextEditor.svelte";
    import Tags from "svelte-tags-input";

    import { onMount } from "svelte";
    
    // Modify the Target Post
    function modifyPost(post_id) {
        // Check whether the value of textarea is blank or not
        if (document.getElementById("modifyTextAreaTitle").value === "") {
            alert("タイトルを入力してくだい");
            return;
        }
        // Quill JS
        if (editor.getLength() === 1) {
            alert("コンテンツを入力してくだい");
            return;
        }

        let target_post_id = 0;
        let tmp_title = "";
        let tmp_content = "";
        let tmp_tags = "";

        target_post_id = post_id;
        tmp_title = document.getElementById("modifyTextAreaTitle").value;
        // Quill JS
        tmp_content = editor.getSemanticHTML();

        // Convert the tags in Array into a string joined with "#"
        tmp_tags = current_post_tags_arr.join("#");

        // Creat a param object
        let params = {};

        params = {
            post_id: target_post_id,
            title: tmp_title,
            content: tmp_content,
            tags: tmp_tags,
        }

        fastapi(
            "patch",
            "/api/post/modify",
            params,
            (result) => {
                // Update the current_post_title and current_post_content
                // With the refreshed info from the backend server
                current_post_title = result["title"];
                current_post_content = result["content"];

                // This is a tags displayed in the detail modal!
                current_post_tags = result["tags"];

                // Update the post_list and $post_list_stored
                for (let i = 0; i < $post_list_stored.length; i++) {
                    if ($post_list_stored[i]["id"] === target_post_id) {
                        // Update $post_list_stored
                        $post_list_stored[i] = result;
                    }
                }
            },
            (result) => {
                // Do nothing
            }
        )

        // Reset the values in the modify textarea
        document.getElementById("modifyTextAreaTitle").value = "";
        // Quill JS
        editor.setText("");

        // Close the modify modal
        // You need to set the proper id in the modal button!
        document.querySelector("[id='modify-go-back-button']").click();
    }

</script>

<!-- Modify Modal after the detail modal -->
<div class="modal fade" id="modifyModalToggle_{unique_name}" aria-hidden="true" aria-labelledby="modifyModalToggleLabel" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="modifyModalToggleLabel"><i class="bi bi-pencil-fill"></i> 修正</h1>
          <!-- The next button has its own id! -->
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="modify-modal-button"></button>
        </div>
        <div class="modal-body">
            <!-- Original Textarea -->
            <div class="mb-3">
                <label for="modifyTextAreaTitle" class="form-label">タイトル</label>
                <textarea class="form-control" id="modifyTextAreaTitle" rows="1"></textarea>
            </div>
            <div class="mb-3">
                <label for="modifyTextAreaContent" class="form-label">コンテンツ</label>
                <!-- Quill JS -->
                <TextEditor bind:editor={editor}/>
            </div>
            <div class="mb-3">
                <!-- Tags -->
                <label for="input-tags" class="form-label">タグ</label>
                <Tags
                    id={"input-tag-modify"}
                    bind:tags={current_post_tags_arr}
                    addKeys={[9,13]}
                    maxTags=10
                />
            </div>
            
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline-primary" on:click={modifyPost(current_post_id)}>作成</button>
          <!-- The below data-bs-ratget should be the id of the detail modal -->
          <button class="btn btn-outline-primary" data-bs-target="#detailModal_{unique_name}" data-bs-toggle="modal" id="modify-go-back-button">戻る</button>
        </div>
      </div>
    </div>
</div>