<script>
    export let params = {};
    let username_input = params.username;

    // Watch the params.username for changes
    $: if (params.username !== username_input) {
        // This works for same page (/profile/{username})reloading with different username within the page
        // From User's follow modal, if you click another user, then the Profile page should be reloaded, right?
        // This enables the above!
        // From another svelte components, this does not matter

        // Invoke your method to reload data
        username_input = params.username;

        // Be careful here because if you make a mistake, the program repeats downloading dat again and again!
        updateData();
    }

    ///////////// User Part /////////////

    import { onMount } from "svelte";
    import fastapi from "../lib/api";
    import { post_list_stored, username, userid } from "../lib/store";

    // Selected Tab
    // Very Important Code!!!!!!!
    let selected_tab = "";

    // Variables for Spinner
    let running = false;

    // Set the current page's user
    let current_page_username = "";

    // This variable holds all necessary data about a specific user!
    let user_data = {}; 
    let num_follower;
    let num_followee;
    let num_total_likes;
    let user_plan_id = 1;
    let following_signal = false;
    let profile_picture;
    let criminalId;

    // Current datetime variable for preventing continuous clicking & too many requests toward API backend server
    let timeInterval = 3000; // [PARAMETER]
    let dateTimeNowCount = 0;
    let dateTimeNow = new Date();
    let waitingSignal = false;

    // Variable for get more data and display function
    let howManyPostDisplayed = 20 // [PARAMETER]
    let last_index = 0;

    onMount(()=>{

        // Spinner
        running = true;

        fastapi(
            "get",
            `/api/user/info/${username_input}`,
            {},
            (result) => {
                // Core data about the user
                user_data = result["user_info"];
                num_total_likes = result["total_num_likes"]
                
                $post_list_stored = user_data["posts"];

                // Set the current page username
                current_page_username = user_data["username"];

                // Set the user's plan
                user_plan_id = user_data["plan"]["id"];

                // Compute the number of followers and followee
                num_follower = user_data["followers"].length;
                num_followee = user_data["followees"].length;

                // Profile Image
                profile_picture = user_data["picture"];

                // Potential Criminal User
                criminalId = user_data["id"];

                // Check whether the logged-in user is following this page's user
                for (let i of user_data["followers"]) {
                    if (i["username"] === $username) {
                        following_signal = true;
                        break;
                    }
                }

                // Always start with users_posts tab
                document.getElementById("user-reposted-posts-tab").click();
                document.getElementById("user-posts-tab").click();
                selected_tab = "usersPostsTab";

                // Spinner
                running = false;
            },
            (result) => {
                // Spinner
                running = false;
                // Do nothing
            }
        );
    })

    function updateData() {
        // Check whether enough time has passed for updating this tab and its posts data
        let timeDiff = new Date() - new Date(dateTimeNow);

        if (timeDiff < timeInterval && dateTimeNowCount > 0) {
            waitingSignal = true; // Turn on waiting alert
            return;
        }

        // Spinner
        running = true;

        fastapi(
            "get",
            `/api/user/info/${username_input}`,
            {},
            (result) => {
                // Core data about the user
                user_data = result["user_info"];
                num_total_likes = result["total_num_likes"]
                
                // Do not show all data always!
                $post_list_stored = user_data["posts"].slice(last_index, howManyPostDisplayed);

                // Set the current page username
                current_page_username = user_data["username"];

                // Set the user's plan
                user_plan_id = user_data["plan"]["id"];

                // Compute the number of followers and followee
                num_follower = user_data["followers"].length;
                num_followee = user_data["followees"].length;

                // Profile Image
                profile_picture = user_data["picture"];

                // Check whether the logged-in user is following this page's user
                for (let i of user_data["followers"]) {
                    if (i["username"] === $username) {
                        following_signal = true;
                        break;
                    }
                }
                // Spinner
                running = false;
            },
            (result) => {
                // Spinner
                running = false;
                // Do nothing
            }
        )
        // Always start with users_posts tab
        document.getElementById("user-reposted-posts-tab").click();
        document.getElementById("user-posts-tab").click();
        selected_tab = "usersPostsTab";

        // Reset current Datetime
        if (dateTimeNowCount == 0) {
            dateTimeNowCount += 1;
        }
        dateTimeNow = new Date();
        waitingSignal = false; // Turn off waiting alert
    }

    // User Follow & Unfollow Functions
    function followUser() {
        fastapi(
            "post",
            `/api/user/follow/${current_page_username}`,
            {},
            (result) => {
                let server_response = result["detail"];

                // Change the button
                following_signal = !following_signal;

                if (server_response === "Follow") {

                    num_follower += 1;

                }
                if (server_response === "Unfollow") {

                    if (num_follower !== 0) {
                        num_follower -= 1
                    }
                }
            },
            (result) => {
                // Do nothing
            }
        )
    }

    ///////////////// Post Part ///////////////////
    import Post from "../components/Post.svelte";
    import DetailModal from "../components/DetailModal.svelte";
    import ReplyModal from "../components/ReplyModal.svelte";
    import ModifyModal from "../components/ModifyModal.svelte";
    import DeleteModal from "../components/DeleteModal.svelte";
    import FollowList from "../components/FollowList.svelte";

    // Initialize or Reset
    // Very Important Code!!!!!!!
    $post_list_stored = []; 

    // Error Message Variable
    let err_msg = "";

    // For using Quill JS
    let editor = null;

    // CandleStick Chart Control;
    // when modal is opened, necessary to resize the lightweight chart!
    let chart = null;

    let current_post_id;
    let current_post_title;
    let current_post_content;
    let current_post_tags = ""; // This a tags in string for displayed in the detail modal
    let current_post_tags_arr = []; // This is an array with tags for being modified in the modify modal
    let current_post_timestamp;
    let current_post_username;
    let current_post_reply = [];

    let current_post_num_likes;
    let current_post_already_liked;

    let current_post_num_reposted;
    let current_post_already_reposted;

    let detail_data_arr = [];

    function getUserPosts() {
        // Initialize or Reset
        // Very Important Code!!!!!!!
        $post_list_stored = [];

        // Set the last index
        last_index = 0;
        // Change & Fill the data
        $post_list_stored = user_data["posts"].slice(last_index, howManyPostDisplayed);
        // Change the seletected tab
        selected_tab = "usersPostsTab";
    }
    function getUserPostsMore() {
        // Add 1 (or number of how many posts will be displayed) to the last index
        last_index += howManyPostDisplayed;
        // Change & Fill the data
        $post_list_stored = $post_list_stored.concat(user_data["posts"].slice(last_index, last_index + howManyPostDisplayed));
        // Change the seletected tab
        selected_tab = "usersPostsTab";
    }

    function getUserRepostedPosts() {
        // Initialize or Reset
        // Very Important Code!!!!!!!
        $post_list_stored = [];

        // Set the last index
        last_index = 0;
        // Change & Fill the data
        $post_list_stored = user_data["repost_posts"].slice(last_index, howManyPostDisplayed);
        // Change the seletected tab
        selected_tab = "userRepostedPostsTab";
    }
    function getUserRepostedPostsMore() {
        // Add 1 (or number of how many posts will be displayed) to the last index
        last_index += howManyPostDisplayed;
        // Change & Fill the data
        $post_list_stored = $post_list_stored.concat(user_data["repost_posts"].slice(last_index, last_index + howManyPostDisplayed));
        // Change the seletected tab
        selected_tab = "userRepostedPostsTab";
    }

    function getUserLikePosts() {
        // Initialize or Reset
        // Very Important Code!!!!!!!
        $post_list_stored = [];

        // Set the last index
        last_index = 0;
        // Change & Fill the data
        $post_list_stored = user_data["like_posts"].slice(last_index, howManyPostDisplayed);
        // Change the seletected tab
        selected_tab = "userLikePostsTab";
    }
    function getUserLikePostsMore() {
        // Add 1 (or number of how many posts will be displayed) to the last index
        last_index += howManyPostDisplayed;
        // Change & Fill the data
        $post_list_stored = $post_list_stored.concat(user_data["like_posts"].slice(last_index, last_index + howManyPostDisplayed));
        // Change the seletected tab
        selected_tab = "userLikePostsTab";
    }

    function reportUser() {
        fastapi(
            "post",
            `/api/user/report/${criminalId}`,
            {},
            (result) => {
                alert(result["detail"]);
            },
            (result) => {
                alert(result["detail"]);
            }
        )
    }

</script>

<div class="container-sm">

    <!-- Spinner -->
    {#if running === true}
        <div class="d-flex justify-content-center my-5">
            <div class="spinner-border" role="status" style="width: 6rem; height: 6rem;">
                <span class="visually-hidden"></span>
            </div>
        </div>
    {:else}
        <!-- User's Profile -->
        <div class="container my-2 px-0">

            <!-- Dot Dot Dot Menu -->
            <div class="d-flex flex-row justify-content-end" style="max-height: 5px">
                <div class="dropdown">
                    <!-- Report this user button -->
                    <button class="btn btn-link" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="bi bi-three-dots"></i>
                    </button>
                    <ul class="dropdown-menu">
                        <!-- Prevent self report -->
                        {#if criminalId !== $userid}
                        <li>
                            <button class="dropdown-item btn btn-link" style="text-decoration: none;" on:click={reportUser}>
                                このユーザーを報告する
                            </button>
                        </li>
                        {:else}
                            <!-- Report criminal button (Disabled) -->
                            <li>
                                <button class="dropdown-item btn btn-link" style="text-decoration: none;" disabled>
                                    このユーザーを報告する
                                </button>
                            </li>
                        {/if}
                    </ul>
                </div>
            </div>

            <!-- UserName -->
            <div class="d-flex flex-row align-items-center m-0 p-0">
                <!-- Profile Image -->
                {#if profile_picture !== null}
                    <img src={profile_picture} id="profile-pic" alt="profile_picture" style="width: 70px; height: 70px">
                {:else}
                    <p class="fs-3 pt-2 pb-0 mx-0"><i class="bi bi-person"></i></p>
                {/if}
                {#if profile_picture !== null}
                    <!-- Username (Clickable) -->
                    <button 
                    type="button" 
                    class="btn btn-link my-2 ms-2 me-0 p-0 text-start" 
                    style="text-decoration:none;" 
                    on:click={updateData}>
                        {#if username_input.length < 10}
                            <h2 class="fw-bolder">{username_input}</h2>
                        {:else}
                            <h5 class="fw-bolder">{username_input}</h5>
                        {/if}
                    </button>
                {:else}
                    <!-- Username (Clickable) -->
                    <button 
                    type="button" 
                    class="btn btn-link m-0 p-0 text-start" 
                    style="text-decoration:none;" 
                    on:click={updateData}>
                    {#if username_input.length < 10}
                        <h2 class="fw-bolder">{username_input}</h2>
                    {:else}
                        <h5 class="fw-bolder">{username_input}</h5>
                    {/if}
                    </button>
                {/if}
                <!-- Plan Name and Badge -->
                {#if user_plan_id === 2}
                    <p class="mx-2 pt-2" style="font-size: 14px;">
                        <i class="bi bi-star-fill"></i>
                    </p>
                {/if}
            </div>

            <!-- Current Logged-in User cannot follow him/her self -->
            {#if $username !== user_data.username}
                <!-- Follow or Unfollow Button -->
                {#if following_signal === false}
                    <div class="my-1">
                        <button 
                        type="button" 
                        class="btn btn-outline-primary" 
                        style="font-size: 15px;"
                        on:click={followUser}>
                            フォロー
                        </button>
                    </div>
                {/if}
                {#if following_signal === true}
                <div class="my-1">
                    <button 
                    type="button" 
                    class="btn btn-primary" 
                    style="font-size: 15px;"
                    on:click={followUser}>
                        フォロー中
                    </button>
                </div>
                {/if}
            {/if}

            <!-- Number of Following and Followers -->
            <div class="d-flex flex-row my-1">
                <button 
                type="button"
                data-bs-target="#followModal"
                data-bs-toggle="modal"
                class="btn btn-link border-0 me-3 px-0"
                style="text-decoration:none">
                    <span class="fw-bold">{num_followee}</span> フォロー中
                </button>
                <button 
                type="button"
                data-bs-target="#followModal"
                data-bs-toggle="modal"
                class="btn btn-link border-0 me-3 px-0" 
                style="text-decoration:none">
                    <span class="fw-bold">{num_follower}</span> フォロワー
                </button>
                <button 
                type="button"
                class="btn btn-link border-0 me-3 px-0" 
                style="text-decoration:none">
                    <span class="fw-bold">{num_total_likes}</span> 合計いいね
                </button>
            </div>

            <!-- Status Message -->
            <div class="my-1">
                <p class="word-wrap text-break">{user_data.status_msg}</p>
            </div>
        </div>
    {/if}
    
    <!-- Tabs and Posts -->
    <div class="container my-2 px-0">
        <ul class="nav nav-underline nav-justified" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button
                    class="nav-link active"
                    id="user-posts-tab" 
                    data-bs-toggle="tab" 
                    data-bs-target="#user-posts-tab-pane" 
                    type="button"
                    role="tab" 
                    aria-controls="user-posts-tab-pane" 
                    aria-selected="true"
                    on:click={getUserPosts}>
                    <i class="bi bi-chat-square-text"></i> 投稿
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button 
                    class="nav-link" 
                    id="user-reposted-posts-tab" 
                    data-bs-toggle="tab" 
                    data-bs-target="#user-reposted-tab-pane" 
                    type="button" 
                    role="tab" 
                    aria-controls="user-reposted-tab-pane" 
                    aria-selected="false"
                    on:click={getUserRepostedPosts}>
                    <i class="bi bi-arrow-repeat"></i> 共有
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button 
                    class="nav-link" 
                    id="user-like-posts-tab" 
                    data-bs-toggle="tab" 
                    data-bs-target="#user-like-tab-pane" 
                    type="button" 
                    role="tab" 
                    aria-controls="user-like-tab-pane" 
                    aria-selected="false"
                    on:click={getUserLikePosts}>
                    <i class="bi bi-hand-thumbs-up"></i> いいね
                </button>
            </li>
        </ul>


        <div class="tab-content" id="myTabContent">
            
            <!-- User's Posts Tab -->
            <div class="tab-pane fade" id="user-posts-tab-pane" role="tabpanel" aria-labelledby="user-posts-tab" tabindex="0">

                <!-- Warning for too many clicking & switching tabs -->
                {#if waitingSignal === true}
                    <div class="alert alert-primary my-1" role="alert">
                        タブをクリックして更新できます。3秒後にもう一度お試しください。
                    </div>
                {/if}
               
                {#if selected_tab === "usersPostsTab" && running == false}

                {#each $post_list_stored as post}
                    <Post
                        unique_name={"profile"}
                        post={post}
                        bind:current_post_id={current_post_id}
                        bind:current_post_title={current_post_title}
                        bind:current_post_content={current_post_content}
                        bind:current_post_tags={current_post_tags}
                        bind:current_post_timestamp={current_post_timestamp}
                        bind:current_post_username={current_post_username}

                        bind:current_post_num_likes={current_post_num_likes}
                        bind:current_post_already_liked={current_post_already_liked}

                        bind:current_post_num_reposted={current_post_num_reposted}
                        bind:current_post_already_reposted={current_post_already_reposted}

                        bind:detail_data_arr={detail_data_arr}
                    />
                {/each}

                <!-- Get More Posts Button -->
                <div class="d-flex justify-content-center my-3">
                    <button class="btn btn-outline-primary add-comp-btn" on:click={getUserPostsMore}>+</button>
                </div>

                {/if}

            </div>
            
            <!-- User's Reposted Posts Tab -->
            <div class="tab-pane fade" id="user-reposted-tab-pane" role="tabpanel" aria-labelledby="user-reposted-tab" tabindex="0">

                <!-- Warning for too many clicking & switching tabs -->
                {#if waitingSignal === true}
                    <div class="alert alert-primary my-1" role="alert">
                        タブをクリックして更新できます。3秒後にもう一度お試しください。
                    </div>
                {/if}

                {#if selected_tab === "userRepostedPostsTab"}
                
                {#each $post_list_stored as post}
                    <Post
                        unique_name={"profile"}
                        post={post}
                        bind:current_post_id={current_post_id}
                        bind:current_post_title={current_post_title}
                        bind:current_post_content={current_post_content}
                        bind:current_post_tags={current_post_tags}
                        bind:current_post_timestamp={current_post_timestamp}
                        bind:current_post_username={current_post_username}

                        bind:current_post_num_likes={current_post_num_likes}
                        bind:current_post_already_liked={current_post_already_liked}

                        bind:current_post_num_reposted={current_post_num_reposted}
                        bind:current_post_already_reposted={current_post_already_reposted}

                        bind:detail_data_arr={detail_data_arr}
                    />
                {/each}

                <!-- Get More Posts Button -->
                <div class="d-flex justify-content-center my-3">
                    <button class="btn btn-outline-primary add-comp-btn" on:click={getUserRepostedPostsMore}>+</button>
                </div>

                {/if}

            </div>

            <!-- User's Like Posts Tab -->
            <div class="tab-pane fade" id="user-like-tab-pane" role="tabpanel" aria-labelledby="user-like-tab" tabindex="0">

                <!-- Warning for too many clicking & switching tabs -->
                {#if waitingSignal === true}
                    <div class="alert alert-primary my-1" role="alert">
                        タブをクリックして更新できます。3秒後にもう一度お試しください。
                    </div>
                {/if}

                {#if selected_tab === "userLikePostsTab"}
                
                {#each $post_list_stored as post}
                    <Post
                        unique_name={"profile"}
                        post={post}
                        bind:current_post_id={current_post_id}
                        bind:current_post_title={current_post_title}
                        bind:current_post_content={current_post_content}
                        bind:current_post_tags={current_post_tags}
                        bind:current_post_timestamp={current_post_timestamp}
                        bind:current_post_username={current_post_username}

                        bind:current_post_num_likes={current_post_num_likes}
                        bind:current_post_already_liked={current_post_already_liked}

                        bind:current_post_num_reposted={current_post_num_reposted}
                        bind:current_post_already_reposted={current_post_already_reposted}

                        bind:detail_data_arr={detail_data_arr}
                    />
                {/each}

                <!-- Get More Posts Button -->
                <div class="d-flex justify-content-center my-3">
                    <button class="btn btn-outline-primary add-comp-btn" on:click={getUserLikePostsMore}>+</button>
                </div>

                {/if}

            </div>
        
        </div>

        <DetailModal
        unique_name={"profile"}

        bind:current_post_id={current_post_id}
        bind:current_post_title={current_post_title}
        bind:current_post_content={current_post_content}
        bind:current_post_tags={current_post_tags}
        bind:current_post_tags_arr={current_post_tags_arr}
        bind:current_post_timestamp={current_post_timestamp}
        bind:current_post_username={current_post_username}
        bind:current_post_reply={current_post_reply}

        bind:current_post_num_likes={current_post_num_likes}
        bind:current_post_already_liked={current_post_already_liked}

        bind:current_post_num_reposted={current_post_num_reposted}
        bind:current_post_already_reposted={current_post_already_reposted}

        detail_data_arr={detail_data_arr}
        chart={chart} 
        bind:editor={editor}/>

        <ReplyModal
        unique_name={"profile"}
        bind:reply_data={current_post_reply}
        bind:current_post_id={current_post_id}/>
    
        <ModifyModal
        unique_name={"profile"}
        bind:current_post_id={current_post_id}
        bind:current_post_title={current_post_title}
        bind:current_post_content={current_post_content}
        bind:current_post_tags={current_post_tags}
        bind:current_post_tags_arr={current_post_tags_arr}
        bind:editor={editor}/>

        <DeleteModal
        unique_name={"profile"}
        bind:current_post_id={current_post_id}/>

        <!-- /////////////////////////// -->

        <FollowList
        followees_array={user_data.followees}
        followers_array={user_data.followers}/>


    </div>

</div>


<style>

.container-sm {
    max-width: 576px;
}

.add-comp-btn {
    height: 80px;
    line-height: 80px;  
    width: 80px;  
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