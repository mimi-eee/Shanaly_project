<script>
    export let followees_array = []; 
    export let followers_array = []; 

    import { onDestroy, onMount } from "svelte";
    import { link } from "svelte-spa-router";

    // Variables for controlling how many items will be displayed at first
    // And how many items will be added whenever clicking the add more button

    let followee_last_index = 0;
    // [PARAMETER] How many items will be displayed at first
    let followee_end_index = 1;
    // [PARAMETER] How many items will be added per clicking the more button
    let followee_howManyItemsPerClick = 1;

    let follower_last_index = 0;
    // [PARAMETER] How many items will be displayed at first
    let follower_end_index = 1;
    // [PARAMETER] How many items will be added per clicking the more button
    let follower_howManyItemsPerClick = 1;

    onMount(() => {
        document.getElementById("follow-list-followers-tab").click();
        document.getElementById("follow-list-followees-tab").click();

    })

    function closeFollowListModal() {
        document.getElementById("follow-modal-close-button").click();
    }

    function getMoreItemsFollowee() {
        followee_end_index += followee_howManyItemsPerClick;
    }

    function getMoreItemsFollower() {
        follower_end_index += follower_howManyItemsPerClick;
    }

</script>


<!-- Followees & Followers Modal -->
<div class="modal fade" id="followModal" tabindex="-1" aria-labelledby="followModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="followModalLabel">フォロー情報</h1>
            <!-- The next button has its own id! -->
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="follow-modal-close-button"></button>
        </div>
        <!-- Modal Body -->
        <div class="modal-body">
            
            <!-- Followees Tab -->
            <ul class="nav nav-underline nav-justified">
                <li class="nav-item">
                    <button
                        class="nav-link active"
                        id="follow-list-followees-tab" 
                        data-bs-toggle="tab" 
                        data-bs-target="#follow-list-followees-tab-pane" 
                        type="button"
                        role="tab" 
                        aria-controls="follow-list-followees-tab-pane" 
                        aria-selected="true">
                        フォロー中
                    </button>
                </li>
                <!-- Followers Tab -->
                <li class="nav-item">
                    <button
                        class="nav-link"
                        id="follow-list-followers-tab" 
                        data-bs-toggle="tab" 
                        data-bs-target="#follow-list-followers-tab-pane" 
                        type="button"
                        role="tab" 
                        aria-controls="follow-list-followers-tab-pane" 
                        aria-selected="true">
                        フォロワー
                    </button>
                </li>
            </ul>

            <div class="tab-content" id="myTabContent">
            
                <!-- Followees Tab Result -->
                <div class="tab-pane fade" id="follow-list-followees-tab-pane" role="tabpanel" aria-labelledby="follow-list-followees-tab" tabindex="0">
                    <div class="my-1 mx-0">
                        <!-- Cards -->
                        {#each followees_array.slice(followee_last_index, followee_end_index) as item}
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a use:link
                                        href="/profile/{item.username}"
                                        style="text-decoration:none"
                                        on:click={closeFollowListModal}>
                                        {item.username}</a>
                                    </h5>
                                    <p class="card-text">{item.status_msg}</p>
                                </div>
                            </div>
                        {/each}
                        <!-- Get More Item Button -->
                        <div class="d-flex justify-content-center my-3">
                            <button class="btn btn-outline-primary add-comp-btn" on:click={getMoreItemsFollowee}>+</button>
                        </div>
                    </div>
                </div>
                
                <!-- Followers Tab Resul -->
                <div class="tab-pane fade" id="follow-list-followers-tab-pane" role="tabpanel" aria-labelledby="follow-list-followers-tab" tabindex="0">
                    <div class="my-1 mx-0">
                        <!-- Cards -->
                        {#each followers_array.slice(follower_last_index, follower_end_index) as item}
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        <a use:link
                                        href="/profile/{item.username}"
                                        style="text-decoration:none"
                                        on:click={closeFollowListModal}>
                                        {item.username}</a>
                                    </h5>
                                    <p class="card-text">{item.status_msg}</p>
                                </div>
                            </div>
                        {/each}
                        <!-- Get More Item Button -->
                        <div class="d-flex justify-content-center my-3">
                            <button class="btn btn-outline-primary add-comp-btn" on:click={getMoreItemsFollower}>+</button>
                        </div>
                    </div>
                </div>
            
            </div>

        </div>
        <!-- Modal Footer -->
        <div class="modal-footer">
            <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
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

</style>