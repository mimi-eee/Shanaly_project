<script>
    // This is for clicking tags in the detail modal
    // and redirect the user to the SearchGeneral.svelte
    // with a parameter value which is a tag in this case
    export let params = {};
    let at_first = true;

    //////////////////////////////////////////////

    import { link } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import moment from 'moment/min/moment-with-locales';
    moment.locale('ja');
    import { post_list_stored } from "../lib/store";

    import Post from "../components/Post.svelte";
    import DetailModal from "../components/DetailModal.svelte";
    import ReplyModal from "../components/ReplyModal.svelte";
    import ModifyModal from "../components/ModifyModal.svelte";
    import DeleteModal from "../components/DeleteModal.svelte";

    import Search from "../routes/Search.svelte";
    import TopicRecommend from "./TopicRecommend.svelte"

    let err_msg = "";

    // Variables for Seach Category and Word
    let searchCategory = "tag_latest";
    let searchWord = "";
    let running = false;
    let running_more = false;

    // Variables for Paging
    let howManyItemsPerClick = 10; // [PARAMETER]
    let last_page_idx = 0;

    // Arrays for containing data
    // Users array
    let users_arr = [];

    // Post array with store variable
    $post_list_stored = [];

    // This is for clicking tags in the detail modal
    // and redirect the user to the SearchGeneral.svelte
    // with a parameter value which is a tag in this case
    $: if (params.tag !== undefined && at_first === true) {
        // Invoke your method to reload data
        searchCategory = "tag_popular";
        searchWord = params.tag;

        // Prevent executing this reactive statement
        // This reactive statement only works at first!
        at_first = false;
    }

    function usernameSearch(word) {

        err_msg = "";

        // Reset
        last_page_idx = 0;

        let params = {
            skip: 0,
            limit: howManyItemsPerClick,
        }

        fastapi(
            "get",
            `/api/search/user/${word}`,
            params,
            (result) => {
                users_arr = result; // Different here
                err_msg = "";
                running = false;
            },
            (result) => {
                running = false;
                if (result["detail"] === "No data") {
                    err_msg = "データがありません。"
                    return;
                }
            }
        )
        
        // While downloading data asynchronously, make running true!
        running = true;
    }

    function usernameSearchMore(word) {
        
        err_msg = "";
        
        // Different here
        last_page_idx += howManyItemsPerClick;

        let params = {
            skip: last_page_idx,
            limit: howManyItemsPerClick,
        }

        fastapi(
            "get",
            `/api/search/user/${word}`,
            params,
            (result) => {
                users_arr = users_arr.concat(result); // Different here
                err_msg = "";
                running_more = false;
            },
            (result) => {
                running_more = false;
                if (result["detail"] === "No data") {
                    err_msg = "データがありません。"
                    return;
                }
            }
        )

        // While downloading data asynchronously, make running true!
        running_more = true;
    }

    function tagLatestSearch(word) {

        err_msg = "";

        // Reset
        last_page_idx = 0;

        let params = {
            skip: 0,
            limit: howManyItemsPerClick,
        }
        
        fastapi(
            "get",
            `/api/search/tag/latest/${word}`,
            params,
            (result) => {
                $post_list_stored = result;
                err_msg = "";
                running = false;
            },
            (result) => {
                running = false;
                if (result["detail"] === "No data") {
                    err_msg = "データがありません。"
                    return;
                }
            }
        )

        // While downloading data asynchronously, make running true!
        running = true;
    }

    function tagLatestSearchMore(word) {
        
        err_msg = "";
        
        // Reset
        last_page_idx += howManyItemsPerClick;

        let params = {
            skip: last_page_idx,
            limit: howManyItemsPerClick,
        }
        
        fastapi(
            "get",
            `/api/search/tag/latest/${word}`,
            params,
            (result) => {
                let tmp_arr = [];
                tmp_arr = $post_list_stored;
                tmp_arr = tmp_arr.concat(result);;
                $post_list_stored = tmp_arr
                err_msg = "";
                running_more = false;
            },
            (result) => {
                running_more = false;
                if (result["detail"] === "No data") {
                    err_msg = "データがありません。"
                    return;
                }
            }
        )

        // While downloading data asynchronously, make running true!
        running_more = true;
    }

    function tagPopularSearch(word) {    
        
        err_msg = "";

        fastapi(
            "get",
            `/api/search/tag/popular/${word}`,
            {},
            (result) => {
                $post_list_stored = result;
                err_msg = "";
                running = false;
            },
            (result) => {
                running = false;
                if (result["detail"] === "No data") {
                    err_msg = "データがありません。"
                    return;
                }
            }
        )

        // While downloading data asynchronously, make running true!
        running = true;
    }

    function executeSearch() {
        // This function aggregates user input values
        // and execute an appropriate seach function based on them.

        // Input data validation
        if (searchWord === "") {
            err_msg = "空白の検索はできません。"
            return;
        }

        // Reset
        users_arr = [];
        $post_list_stored = [];

        if (searchCategory === "username") {
            usernameSearch(searchWord);
        }
        if (searchCategory === "tag_latest") {
            tagLatestSearch(searchWord);
        }
        if (searchCategory === "tag_popular"){
            tagPopularSearch(searchWord);
        }
    }

    function resetArray() {
        // Reset
        users_arr = [];
        $post_list_stored = [];
        err_msg = "";
    }

    ////////// Posts and Detail Modals Part ////////////////

    // For using Quill JS
    let editor = null;

    // CandleStick Chart Control;
    // when modal is opened, necessary to resize the lightweight chart!
    let chart = null;

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

</script>


<div class="container-sm my-1 px-0">
    <!-- Title -->
    <h1><i class="bi bi-search"></i> 一般検索</h1>

    <!-- Search Bar and Button -->
    <div class="container my-3 p-0">
        <!-- Select Options for Search Categories -->
        <div class="mb-2">
            <select class="form-select rounded-pill" aria-label="Default select example" bind:value={searchCategory} on:change={resetArray}>
                <option value="tag_popular" selected>タグ (人気)</option>
                <option value="tag_latest" selected>タグ (最新)</option>
                <option value="username">ユーザー名</option>
            </select>
        </div>
        <!-- Input for Search Keyword -->
        <div class="mb-2">
            <input
            type="text"
            class="form-control rounded-pill search"
            placeholder="入力"
            id="user-input-form-general-search"
            autocomplete="off"
            bind:value={searchWord}
            />
        </div>
        <!-- Alert -->
        {#if err_msg !== ""}
            <div class="alert alert-primary" role="alert">
                {err_msg}
            </div>
        {/if}
        <!-- Execution Button for Search -->
        <div class="d-grid gap-2">
            <button 
            id="execute-search-button"
            class="btn btn-outline-primary" 
            type="button" 
            on:click={executeSearch}>検索</button>
        </div>
        
    </div>

    <!-- Search Result -->

        
    <!-- [1] Username Seach Result -->
    {#if users_arr.length !== 0}

        {#each users_arr as item}

            <div class="card rounded mb-1">
                <div class="d-flex flex-row m-1 p-1 gap-3">
                    <h4 class="card-title">
                        {#if item.username < 15}
                            <a use:link
                            href="/profile/{item.username}"
                            style="text-decoration:none">
                            {item.username}</a>
                        {:else}
                            <a use:link
                            href="/profile/{item.username}"
                            style="text-decoration:none; font-size: 15px;">
                            {item.username}</a>
                        {/if}
                    </h4>
                    <p class="pt-1" style="font-size: 14px">{item.posts.length} 投稿</p>
                    <p class="pt-1" style="font-size: 14px">{item.followees.length} フォロー中</p>
                    <p class="pt-1" style="font-size: 14px">{item.followers.length} フォロワー</p>
                </div>
                <div class="m-1 p-1">
                    <p>{item.status_msg}</p>
                </div>
                <div class="d-flex flex-row justify-content-end" style="font-size: 13px;">
                    会員登録日 {moment(item.created_at).format("YY年MM月DD日")}
                </div>
            </div>

        {/each}

        {#if running_more === true && err_msg === ""}
            <!-- Spinner for More Button -->
            <div class="d-flex justify-content-center my-3">
                <div class="spinner-border" role="status" style="width: 5rem; height: 5rem;">
                    <span class="visually-hidden"></span>
                </div>
            </div>
        {:else}
            <!-- Get More Posts Button -->
            <div class="d-flex justify-content-center my-3">
                <button class="btn btn-outline-primary add-comp-btn" on:click={usernameSearchMore(searchWord)}>+</button>
            </div>
        {/if}    

    {/if}


    <!-- [2] Post Search Results -->

    {#if $post_list_stored.length !== 0}

        {#each $post_list_stored as post}

            <Post
            unique_name={"search_general"}
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

            bind:detail_data_arr={detail_data_arr}/>
        
        
        {/each}

        <!-- Get more posts button is only for search posts by tag in time order  -->
        <!-- This button is not for popular posts with a specific tag -->
        {#if searchCategory === "tag_latest"}

            {#if running_more === true && err_msg === ""}
                <div class="d-flex justify-content-center my-3">
                    <div class="spinner-border" role="status" style="width: 5rem; height: 5rem;">
                        <span class="visually-hidden"></span>
                    </div>
                </div>
            {:else}
                <!-- Get More Posts Button -->
                <div class="d-flex justify-content-center my-3">
                    <button class="btn btn-outline-primary add-comp-btn" on:click={tagLatestSearchMore(searchWord)}>+</button>
                </div>
            {/if}
        
        {/if}
    
    {/if}

    <!-- Spinner for the tab -->
    {#if running === true && err_msg === ""}
        <div class="d-flex justify-content-center my-5">
            <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
                <span class="visually-hidden"></span>
            </div>
        </div>
    {/if}

    
    <DetailModal
    unique_name={"search_general"}
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
    unique_name={"search_general"}
        bind:reply_data={current_post_reply}
        bind:current_post_id={current_post_id}/>
    
    <ModifyModal
    unique_name={"search_general"}
        bind:current_post_id={current_post_id}
        bind:current_post_title={current_post_title}
        bind:current_post_content={current_post_content}
        bind:current_post_tags={current_post_tags}
        bind:current_post_tags_arr={current_post_tags_arr}
        bind:editor={editor}/>

    <DeleteModal
    unique_name={"search_general"}
        bind:current_post_id={current_post_id}/>
    

    <!-- Symbol Recoomendation -->
    <!-- <div class="my-5"><TopicRecommend/></div> -->
    
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

</style>