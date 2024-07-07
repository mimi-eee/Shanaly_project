<script>
    import fastapi from "../lib/api";
    import { onMount } from "svelte";
    import { is_login, userid, username, last_selected_tab, post_list_stored} from "../lib/store";
    import { update_date_symbol, symbol_autocomplete_list } from "../lib/store";
    import UserStatus from "../components/UserStatus.svelte";
    import Post from "../components/Post.svelte";
    import DetailModal from "../components/DetailModal.svelte";
    import ReplyModal from "../components/ReplyModal.svelte";
    import ModifyModal from "../components/ModifyModal.svelte";
    import DeleteModal from "../components/DeleteModal.svelte";
    import { push } from "svelte-spa-router";

    // Initialize
    // Very Important Code!!!
    $post_list_stored = [];

    // Variables for Spinner
    let running = false;
    let runningMore = false;

    // Very Important Code!!!
    // This is different from last_selected tab in store variables: different purpose!
    let selected_tab = "";

    // For using Quill JS
    let editor = null;

    // CandleStick Chart Control;
    // when modal is opened, necessary to resize the lightweight chart!
    let chart = null;

    // User Profile variable
    let username_display = $username;

    // Current datetime variable for preventing continuous clicking & too many requests toward API backend server
    let timeInterval = 3000; // [PARAMETER]
    let dateTimeNowCount = 0;
    let dateTimeNow = new Date();
    let waitingSignal = false;

    // How many Posts get when you click more button
    let howManyPostsMore = 10; // [PARAMETER]

    // Error Message Variable
    let err_msg = "";

    // Detail modal variables
    let current_post_title = "";
    let current_post_content = "";
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

    // Current post variables: used for modify, delete and so on
    let current_post_id = null;

    onMount(()=>{
        // This code is for memorizing the tab selected by user
        // And click the lastly selected tab and show the posts
        try {
            if ($last_selected_tab === ""){

                $last_selected_tab = "latestTab";
                // getLatestPosts();
                document.getElementById("latest-tab").click();

                selected_tab = "latestTab";
            
            } else if ($last_selected_tab === "popularTab") {
                
                // Popular Tab
                document.getElementById("popular-tab").click();
                selected_tab = "popularTab";

            } else if ($last_selected_tab === "latestTab"){
                
                // Latest Tab
                document.getElementById("latest-tab").click();
                selected_tab = "latestTab";
                
            } else if ($last_selected_tab === "followingTab"){
                
                // Following Tab
                document.getElementById("following-tab").click();
                selected_tab = "followingTab";

            } else if ($last_selected_tab === "recommendedTab") {

                // Recommended Tab
                document.getElementById("recommended-tab").click();
                selected_tab = "recommendedTab";
                
            } else {

                // document.getElementById("latest-tab").click();
                // selected_tab = "latest-tab";
                
            }
        } catch {
            push("/user-login");
        }


        // Update AutoComplete Data List
        if ($update_date_symbol === 0 || $update_date_symbol === null || $update_date_symbol === undefined || $symbol_autocomplete_list === []) {

            // Record updated datetime
            $update_date_symbol = new Date();   

            fastapi(
                "get",
                "/api/others/symbol/dictionary",
                {},
                (result) => {
                    // Store variable
                    $symbol_autocomplete_list = result;
                    
                }
            )
        } else {
            // Check whether enough time has passed for updating wiki words array
            let diff = new Date() - new Date($update_date_symbol);

            if (diff > 3600000) {
                
                // Update Wiki
                fastapi(
                    "get",
                    "/api/others/symbol/dictionary",
                    {},
                    (result) => {
                        // Store variable
                        $symbol_autocomplete_list = result;
                        // Set the update date
                        $update_date_symbol = new Date();
                    },
                    (result) => {
                        // Display error message
                        err_msg = result["detail"];
                    }
                )
            }
        }

    })

    ////////////////////////////////////////////////

    // Category 1-1 = Popular Posts
    function getPopularPosts() {

        // Initialize or Reset
        $post_list_stored = [];

        // Set the currently selected tab
        selected_tab = "popularTab"; // Important Code!

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
            "/api/post/popular_posts",
            {},
            (result) => {
                $post_list_stored = result; // Store the result (data) into a store variable named post_list_stored in store.js
                // Spinner
                running = false;

            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                running = false; 
            }
        )

        // Set info about the last clicked tab
        $last_selected_tab = "popularTab";
        
        // Reset current Datetime
        if (dateTimeNowCount == 0) {
            dateTimeNowCount += 1;
        }
        dateTimeNow = new Date();
        waitingSignal = false; // Turn off waiting alert
        
    }

    // Category 2-1 = Latest Posts
    function getLatestPosts() {

        // Initialize or Reset
        $post_list_stored = [];

        // Set the currently selected tab
        selected_tab = "latestTab"; // Important Code!

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
            "/api/post/latest_posts",
            {},
            (result) => {
                $post_list_stored = result; // Store the result (data) into a store variable named post_list_stored in store.js
                // Spinner
                running = false;

            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                running = false;         
            }
        )

        // Set info about the last clicked tab
        $last_selected_tab = "latestTab";

        // Reset current Datetime
        if (dateTimeNowCount == 0) {
            dateTimeNowCount += 1;
        }
        dateTimeNow = new Date();
        waitingSignal = false; // Turn off waiting alert
        
    }
    // Category 2-2 = Latest Posts (Get More)
    function getLatestPostsMore() {
        let last_post_id = $post_list_stored.at(-1)["id"];
        let params = {
            last_post_id: last_post_id,
            // If you need to read N posts more per clicking "+" Button"; default is 10;
            limit: howManyPostsMore,
        }

        // Spinner
        runningMore = true;

        fastapi(
            "get",
            "/api/post/latest_posts",
            params,
            (result) => {
                // Store the result (data) into a store variable named post_list_stored in store.js
                $post_list_stored =  $post_list_stored.concat(result);
                // Spinner
                runningMore = false;

            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                runningMore = false;    
            }
        )
    }
    
    // Category 3-1 = Following (Followees) Posts
    function getFollowingPosts() {

        // Initialize or Reset
        $post_list_stored = [];

        // Set the currently selected tab
        selected_tab = "followingTab"; // Important Code!

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
            "/api/post/following_posts",
            {},
            (result) => {
                $post_list_stored = result; // Store the result (data) into a store variable named post_list_stored in store.js
                // Spinner
                running = false;
            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                running = false;      
            }
        )
        // Set info about the last clicked tab
        $last_selected_tab = "followingTab";

        // Reset current Datetime
        if (dateTimeNowCount == 0) {
            dateTimeNowCount += 1;
        }
        dateTimeNow = new Date();
        waitingSignal = false; // Turn off waiting alert

        // Set info about the last clicked tab
        $last_selected_tab = "followingTab";
    }

    // Category 3-2 = Following (Followees) Posts (More)
    function getFollowingPostsMore() {
        let last_post_id = $post_list_stored.at(-1)["id"];
        let params = {
            last_post_id: last_post_id,
            // If you need to read N posts more per clicking "+" Button"; default is 10;
            limit: howManyPostsMore,
        }
        // Spinner
        runningMore = true;

        fastapi(
            "get",
            "/api/post/following_posts",
            params,
            (result) => {
                // Store the result (data) into a store variable named post_list_stored in store.js
                $post_list_stored =  $post_list_stored.concat(result);
                // Spinner
                runningMore = false;
            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                runningMore = false;            
            }
        )
    }

    // Category 4-1 = Recommended Posts
    function getRecommendedPosts() {

        // Initialize or Reset
        $post_list_stored = [];

        // Set the currently selected tab
        selected_tab = "recommendedTab"; // Important Code!

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
            "/api/post/recommended_posts",
            {},
            (result) => {
                $post_list_stored = result; // Store the result (data) into a store variable named post_list_stored in store.js
                // Spinner
                running = false;
            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                running = false;        
            }
        )

        // Set info about the last clicked tab
        $last_selected_tab = "recommendedTab";

        // Reset current Datetime
        if (dateTimeNowCount == 0) {
            dateTimeNowCount += 1;
        }
        dateTimeNow = new Date();
        waitingSignal = false; // Turn off waiting alert
    }

    // Category 4-2 = Recommended Posts (More)
    function getRecommendedPostsMore() {
        let last_post_id = $post_list_stored.at(-1)["id"];
        let params = {
            last_post_id: last_post_id,
            // If you need to read N posts more per clicking "+" Button"; default is 10;
            limit: howManyPostsMore,
        }
        // Spinner
        runningMore = true;

        fastapi(
            "get",
            "/api/post/recommended_posts",
            params,
            (result) => {
                // Store the result (data) into a store variable named post_list_stored in store.js
                $post_list_stored =  $post_list_stored.concat(result);
                // Spinner
                runningMore = false;
            },
            (result) => {
                err_msg = result["detail"];
                // Spinner
                runningMore = false;        
            }
        )
    }

</script>
  
<!-- The next code prevents flashing main menus and htmls from application -->
{#if $is_login === true}

<div class="container-sm">
    
    <UserStatus username={username_display}/>

    <!-- Second Menu Component -->
    <ul class="nav nav-underline nav-justified" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
            <button 
                class="nav-link" 
                id="popular-tab" 
                data-bs-toggle="tab" 
                data-bs-target="#popular-tab-pane" 
                type="button" 
                role="tab" 
                aria-controls="popular-tab-pane" 
                aria-selected="false"
                on:click={getPopularPosts}>
                <i class="bi bi-fire"></i> 人気
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button 
                class="nav-link" 
                id="latest-tab" 
                data-bs-toggle="tab" 
                data-bs-target="#latest-tab-pane" 
                type="button" 
                role="tab" 
                aria-controls="latest-tab-pane" 
                aria-selected="false"
                on:click={getLatestPosts}>
                <i class="bi bi-clock"></i> 最新
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link"
                id="following-tab"
                data-bs-toggle="tab" 
                data-bs-target="#following-tab-pane" 
                type="button" 
                role="tab" 
                aria-controls="following-tab-pane" 
                aria-selected="false"
                on:click={getFollowingPosts}>
                <i class="bi bi-eye"></i> フォロー中
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button
                class="nav-link"
                id="recommended-tab" 
                data-bs-toggle="tab" 
                data-bs-target="#recommended-tab-pane" 
                type="button" role="tab" 
                aria-controls="recommended-tab-pane" 
                aria-selected="false"
                on:click={getRecommendedPosts}>
                <i class="bi bi-award"></i> おすすめ
            </button>
        </li>
    </ul>

    <!-- Post Component -->
    <div class="tab-content" id="myTabContent">

        <!-- Popular Tab: Posts -->
        <div class="tab-pane fade" id="popular-tab-pane" role="tabpanel" aria-labelledby="popular-tab" tabindex="0">

            <!-- Warning for too many clicking & switching tabs -->
            {#if waitingSignal === true}
                <div class="alert alert-primary my-1" role="alert">
                    タブをクリックして更新できます。3秒後にもう一度お試しください。
                </div>
            {/if}
            
            <!-- Posts in Card -->
            {#if selected_tab === "popularTab"}
                <!-- Spinner -->
                {#if running === true}
                    <div class="d-flex justify-content-center my-5">
                        <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {:else}
                    <!-- Posts -->
                    <!-- If you click the tab, pgm will get new data and assign it to $post_list_stored -->
                    <!-- However, <Post/> should be re-rendered, so I put {#key} here! -->
                    <!-- Currently, this is only for popularTab! -->
                    {#key $post_list_stored}
                        {#each $post_list_stored as post}
                            <Post
                            unique_name={"home"}
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
                    {/key}
                {/if}
            {/if}
            
        </div>
        
        
        <!-- Latest Tab: Posts  -->
        <div class="tab-pane fade" id="latest-tab-pane" role="tabpanel" aria-labelledby="latest-tab" tabindex="0">
            
            <!-- Warning for too many clicking & switching tabs -->
            {#if waitingSignal === true}
                <div class="alert alert-primary my-1" role="alert">
                    タブをクリックして更新できます。3秒後にもう一度お試しください。
                </div>
            {/if}
            
            <!-- Posts in Card -->
            {#if selected_tab === "latestTab"}
                <!-- Spinner -->
                {#if running === true}
                    <div class="d-flex justify-content-center my-5">
                        <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {:else}
                    <!-- Posts -->
                    {#each $post_list_stored as post}
                        <Post
                        unique_name={"home"}
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
                {/if}
                {#if runningMore === true}
                    <div class="d-flex justify-content-center my-3">
                        <div class="spinner-border" role="status" style="width: 5rem; height: 5rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {/if}
                {#if running === false && runningMore === false}
                    <!-- Get More Posts Button -->
                    <div class="d-flex justify-content-center my-3">
                        <button class="btn btn-outline-primary add-comp-btn" on:click={getLatestPostsMore}>+</button>
                    </div>
                {/if}
            {/if}

        </div>
        
        
        <!-- Following Tab: Posts  -->
        <div class="tab-pane fade" id="following-tab-pane" role="tabpanel" aria-labelledby="following-tab" tabindex="0">

            <!-- Warning for too many clicking & switching tabs -->
            {#if waitingSignal === true}
                <div class="alert alert-primary my-1" role="alert">
                    タブをクリックして更新できます。3秒後にもう一度お試しください。
                </div>
            {/if}

            <!-- Posts in Card -->
            {#if selected_tab === "followingTab"}
                <!-- Spinner -->
                {#if running === true}
                    <div class="d-flex justify-content-center my-5">
                        <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {:else}
                    <!-- Posts -->
                    {#each $post_list_stored as post}
                        <Post
                        unique_name={"home"}
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
                {/if}

                {#if runningMore === true}
                    <div class="d-flex justify-content-center my-3">
                        <div class="spinner-border" role="status" style="width: 5rem; height: 5rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {/if}
                {#if running === false && runningMore === false}
                    <!-- Get More Posts Button -->
                    <div class="d-flex justify-content-center my-3">
                        <button class="btn btn-outline-primary add-comp-btn" on:click={getFollowingPostsMore}>+</button>
                    </div>
                {/if}
            {/if}

        </div>


        <!-- Recommend Tab: Posts -->
        <div class="tab-pane fade" id="recommended-tab-pane" role="tabpanel" aria-labelledby="recommended-tab" tabindex="0">
            
            <!-- Warning for too many clicking & switching tabs -->
            {#if waitingSignal === true}
                <div class="alert alert-primary my-1" role="alert">
                    タブをクリックして更新できます。3秒後にもう一度お試しください。
                </div>
            {/if}

            <!-- Posts in Card -->
            {#if selected_tab === "recommendedTab"}
                <!-- Spinner -->
                {#if running === true}
                    <div class="d-flex justify-content-center my-5">
                        <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {:else}
                    <!-- Posts -->
                    {#each $post_list_stored as post}
                        <Post
                        unique_name={"home"}
                        post={post}
                        post_recommended={true}
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
                {/if}
                {#if runningMore === true}
                    <div class="d-flex justify-content-center my-3">
                        <div class="spinner-border" role="status" style="width: 5rem; height: 5rem;">
                            <span class="visually-hidden"></span>
                        </div>
                    </div>
                {/if}
                {#if running === false && runningMore === false}
                    <!-- Get More Posts Button -->
                    <div class="d-flex justify-content-center my-3">
                        <button class="btn btn-outline-primary add-comp-btn" on:click={getRecommendedPostsMore}>+</button>
                    </div>
                {/if}
            {/if}

        </div>

        
    </div>


    <DetailModal
    unique_name={"home"}
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
    unique_name={"home"}
        bind:reply_data={current_post_reply}
        bind:current_post_id={current_post_id}/>
    
    <ModifyModal
    unique_name={"home"}
        bind:current_post_id={current_post_id}
        bind:current_post_title={current_post_title}
        bind:current_post_content={current_post_content}
        bind:current_post_tags={current_post_tags}
        bind:current_post_tags_arr={current_post_tags_arr}
        bind:editor={editor}/>

    <DeleteModal
    unique_name={"home"}
        bind:current_post_id={current_post_id}/>
    
</div>

{/if}

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

</style>