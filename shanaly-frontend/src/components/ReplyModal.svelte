<script>
    export let unique_name;

    export let reply_data;
    export let current_post_id;

    import { link } from "svelte-spa-router";
    import { username } from "../lib/store";
    import fastapi from "../lib/api";
    import moment from 'moment/min/moment-with-locales';
    moment.locale('ja');
    
    let err_msg = "";
    let reply_text_value = "";

    // Paging for Replies
    let start_idx = 0;
    let howManyRepliesDisplay = 10; // PARAMETER

    function closeModal() {
        document.querySelector("[id='reply-modal-button']").click();
    }

    // Close the reply modal
    function submitReply() {
        // Check whether the value of textarea is blank or not
        if (document.getElementById("replyTextArea").value === "") {
            err_msg = "メッセージを入力してくだい";
            return;
        }

        let params = {
            post_id: current_post_id,
            content: reply_text_value,
        }

        fastapi(
            "post",
            "/api/reply/create",
            params,
            (result) => {
                // Append the created data obj to reply_data array as well
                reply_data = [result, ...reply_data];

                // Click the read reply tab
                document.querySelector("[id='read-reply-tab']").click();

                // Clear the replay textarea
                document.getElementById("replyTextArea").value = "";
                // Reset error message
                err_msg = "";
                
            },
            (result) => {
                err_msg = result["detail"];
            }
        ) 
    }

    function deleteReply(reply_id) {
        if (confirm("リプライを削除しますか？")) {
            
            // Delete the target reply in the DB
            fastapi(
                "delete",
                `/api/reply/delete/${reply_id}`,
                {},
                (result) => {
                    // Clear the replay textarea
                    document.getElementById("replyTextArea").value = "";
                    // Reset error message
                    err_msg = "";
                },
                (result) => {
                    err_msg = result["detail"];
                }
            )

            // Exclude the target reply in reply_data
            let tmp_arr = [];
            for (let i of reply_data) {
                if (i["id"] !== reply_id) {
                    tmp_arr.push(i);
                }
            }
            reply_data = tmp_arr;
        }
    }

    function getMoreReplies() {
        howManyRepliesDisplay += howManyRepliesDisplay;
    }
    

</script>

<!-- Reply Modal after the detail modal -->
<div class="modal fade" id="replyModalToggle_{unique_name}" aria-hidden="true" aria-labelledby="replyModalToggleLabel" tabindex="-1">
    <div class="modal-dialog modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="replyModalToggleLabel"><i class="bi bi-chat-fill"></i> 返信</h1>
          <!-- The next button has its own id! -->
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="reply-modal-button"></button>
        </div>

        <div class="modal-body">

            <!-- Two Tabs: Read Replies & Write a Reply -->
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button 
                        class="nav-link active" 
                        id="read-reply-tab" 
                        data-bs-toggle="tab" 
                        data-bs-target="#read-reply-tab-pane" 
                        type="button" 
                        role="tab" 
                        aria-controls="home-tab-pane" 
                        aria-selected="true">
                        リスト
                    </button>
                </li>
                <li class="nav-item" role="presentation">
                    <button 
                        class="nav-link" 
                        id="write-reply-tab" 
                        data-bs-toggle="tab" 
                        data-bs-target="#write-reply-pane" 
                        type="button" 
                        role="tab" 
                        aria-controls="popular-tab-pane" 
                        aria-selected="false">
                        作成
                    </button>
                </li>
            </ul>
            <!-- Inside of Tabs-->
            <div class="tab-content" id="myTabContent">

                <!-- Read Tab -->
                <div class="tab-pane fade" id="read-reply-tab-pane" role="tabpanel" aria-labelledby="read-reply-tab" tabindex="0">
                    <div class="container my-2 p-0">
                        
                        {#if reply_data.length !== 0}
                            {#each reply_data.slice(start_idx, howManyRepliesDisplay) as item}  
                                <div class="border mb-1 p-2 rounded">
                                    <!-- User Profile Picture Image -->
                                    {#if item.user.picture !== null}
                                        <img src={item.user.picture} id="profile-pic" alt="profile_picture" style="width: 40px; height: 40px">
                                    {:else}
                                        <i class="bi bi-person" style="font-size: 25px;"></i>
                                    {/if}
                                    <!-- Username -->
                                    <a use:link href="/profile/{item.user.username}" class="fw-bold" style="text-decoration:none" on:click={closeModal}>
                                        {item.user.username}
                                    </a>
                                    <!-- User Reply -->
                                    <p class="mt-2">{item.content}</p>
                                    <div class="d-flex flex-row justify-content-end m-0 p-0">
                                        <p class="m-0 p-0" style="font-size: 10px;">
                                            {moment(item.created_at).format("YY年MM月DD日 A hh:mm")}
                                        </p>
                                    </div>
                                    <!-- Delete button for the reply -->
                                    {#if $username === item.user.username}
                                        <div class="d-flex flex-row justify-content-end my-1">
                                            <button type="button" class="btn btn-sm btn-outline-primary" on:click={deleteReply(item.id)}>
                                                <i class="bi bi-trash-fill"></i>
                                            </button>
                                        </div>
                                    {/if}
                                </div>
                            {/each}
                        {:else}
                            <div class="my-2">リプライが現在ありません。</div>
                        {/if}

                        <!-- Get More Replies Button -->
                        <div class="d-flex justify-content-center my-3">
                            <button class="btn btn-outline-primary add-comp-btn" on:click={getMoreReplies}>+</button>
                        </div>

                    </div>
                </div>
                <!-- Write Tab -->
                <div class="tab-pane fade" id="write-reply-pane" role="tabpanel" aria-labelledby="write-reply-tab" tabindex="0">
                    <div class="mb-3">
                        <!-- Error Message -->
                        {#if err_msg !== ""}
                            <div class="alert alert-primary my-2" role="alert">
                                {err_msg}
                            </div>
                        {/if}
                        <textarea class="form-control my-2" id="replyTextArea" rows="5" bind:value={reply_text_value}></textarea>
                        <div class="container d-flex justify-content-end mx-0 px-0">
                            <button class="btn btn-outline-primary" on:click={submitReply}>OK</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="modal-footer">
          <!-- The below data-bs-ratget should be the id of the detail modal -->
          <button class="btn btn-outline-primary" data-bs-target="#detailModal_{unique_name}" data-bs-toggle="modal" id="reply-go-back-button">戻る</button>
        </div>
      </div>
    </div>
</div>

<style>

.add-comp-btn {
    height: 50px;
    line-height: 80px;  
    width: 50px;  
    font-size: 2em;
    font-weight: bold;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

#profile-pic {
  border-radius: 50%;
}

</style>