<script>
    export let unique_name;
    export let post_recommended = false;

    export let post;
    export let current_post_id
    export let current_post_title;
    export let current_post_content;
    export let current_post_timestamp;
    export let current_post_tags;
    export let current_post_username;

    export let current_post_num_likes;
    export let current_post_already_liked;

    export let current_post_num_reposted;
    export let current_post_already_reposted;
    
    export let detail_data_arr;

    import { link } from "svelte-spa-router";
    import moment from 'moment/min/moment-with-locales';
    moment.locale('ja');
    import fastapi from "../lib/api";
    import { post_list_stored, username, userid } from "../lib/store";

    let err_msg = "";

    // Count how many likes there
    let num_likes = post["like_users"].length;
    // Count how many replies there
    let num_replies = post["replies"].length;
    // Count how many times reposted
    let num_reposted = post["repost_users"].length;

    // Set user (potential criminal) ID for report if necessary
    let criminalId =  post["user"]["id"];
    
    // Check whether a currently logged-in user did like this post or not
    // This is variable is within Post.svelte; not bounded.
    let post_already_liked = false; // this is the default
    
    if (post["like_users"].length !== 0) {
        for (let j of post["like_users"]) {
            if (j["username"] === $username) {
                post_already_liked = true;
                break;
            }
        }
    }

    // Check whether a currently logged-in user did repost this post or not
    // This is variable is within Post.svelte; not bounded.
    let post_already_reposted = false;

    if (post["repost_users"].length !== 0) {
        for (let j of post["repost_users"]) {
            if (j["username"] === $username) {
                post_already_reposted = true;
                break;
            }
        }
    }

    // Open the Detail Modal
    function openDetailModal(post_id) {

        // Reset previous values in the next variables
        current_post_title = "";
        current_post_content = "";
        current_post_tags = "";
        current_post_timestamp;
        current_post_username;

        current_post_num_likes;
        current_post_already_liked;
        
        current_post_num_reposted;
        current_post_already_reposted;

        detail_data_arr = [];

        // Get detail data of a post from backend server
        fastapi(
            "get",
            `/api/post/detail/${post_id}`,
            {},
            (result) => {
                // CASE1: Post with Detail
                // Set the title of a detail modal
                // by searching the given postid by looping the post_list_stored variable which is an array
                for (const i of $post_list_stored) {
                    if (i["id"] === post_id) {

                        current_post_title = i["title"];
                        current_post_content = i["content"];
                        current_post_tags = i["tags"];
                        current_post_username = i["user"]["username"];

                        current_post_num_likes = i["like_users"].length;
                        current_post_num_reposted = i["repost_users"].length;
                        
                        // [Like] Assume this is false
                        current_post_already_liked = false;

                        if (i["like_users"].length !== 0) {
                            for (let j of i["like_users"]) {
                                if (j["username"] === $username) {
                                    current_post_already_liked = true;
                                }
                            }
                        }

                        // [Repost] Assume this is false
                        current_post_already_reposted = false;

                        if (i["repost_users"].length !== 0) {
                            for (let j of i["repost_users"]) {
                                if (j["username"] === $username) {
                                    current_post_already_reposted = true;
                                }
                            }
                        }

                        if (i["modified_at"] === null || i["modified_at"] === undefined) {
                            current_post_timestamp = moment(i["created_at"]).format("YYYY年MM月DD日 hh:mm A");  
                        } else {
                            current_post_timestamp = moment(i["modified_at"]).format("(変)YYYY年MM月DD日 hh:mm A"); 
                        }
                    }
                }

                // Assign the result to detail_data_arr variable
                detail_data_arr = result["data"]["data"];

                // Set the current post ID
                current_post_id = post_id;
            },
            (result) => {
                // CASE2: Post with No Detail
                // No data for the detail
                err_msg = result["detail"];
                
                // Set the title of a detail modal
                // by searching the given postid by looping the post_list_stored variable which is an array
                for (const i of $post_list_stored) {
                    if (i["id"] === post_id) {
                        current_post_title = i["title"];
                        current_post_content = i["content"];
                        current_post_tags = i["tags"];
                        current_post_username = i["user"]["username"];

                        current_post_num_likes = i["like_users"].length;
                        current_post_num_reposted = i["repost_users"].length;

                        // [Like] Assume this is false
                        current_post_already_liked = false;
                        
                        if (i["like_users"].length !== 0) {
                            for (let j of i["like_users"]) {
                                if (j["username"] === $username) {
                                    current_post_already_liked = true;
                                }
                            }
                        }

                        // [Repost] Assume this is false
                        current_post_already_reposted = false;

                        if (i["repost_users"].length !== 0) {
                            for (let j of i["repost_users"]) {
                                if (j["username"] === $username) {
                                    current_post_already_reposted = true;
                                }
                            }
                        }
                        
                        if (i["modified_at"] === null || i["modified_at"] === undefined) {
                            current_post_timestamp = moment(i["created_at"]).format("YYYY年MM月DD日 A hh:mm");  
                        } else {
                            current_post_timestamp = moment(i["modified_at"]).format("YYYY年MM月DD日 A hh:mm"); 
                        }
                    }
                }
                // Set post number which a user is currently looking at
                // This can be used for delete, like, reply and so on
                current_post_id = post_id;
            }
        )
    }

    // Like Post Button
    function likePost(post_id) {
        let target_element_id = `like-button-${post_id}`
        let params = {
            post_id: post_id,
        }
        fastapi(
            "post",
            "/api/post/like",
            params,
            (result) => {
                // Do nothing
            },
            (result) => {
                err_msg = result["detail"];
            }
        )
        
        // Change number and make it disabled
        let target_button_element = document.getElementById(target_element_id);
        let num_like = Number(target_button_element.innerText)
        num_like += 1
        target_button_element.innerHTML = '<i class="bi bi-hand-thumbs-up-fill"></i> ' + num_like.toString();
        target_button_element.className = "card-link btn btn-primary btn-sm border-0 mx-0";
        target_button_element.disabled = true;
        
        // Add a like_user to like_users for temporarily
        // Update $post_list_stored
        for (let post of $post_list_stored) {
            if (post["id"] === post_id) {
                let tmp_obj = {
                    id: "temp_id",
                    username: $username,
                }
                let tmp_arr = post["like_users"];
                tmp_arr.push(tmp_obj)
                post["like_users"] = tmp_arr;
                return;
            }
        }
    }

    function repostPost(post_id) {
        let target_element_id = `repost-button-${post_id}`
        let params = {
            post_id: post_id,
        }

        fastapi(
            "post",
            "/api/post/repost",
            params,
            (result) => {
                let server_response = result["detail"];

                if (server_response === "Repost") {
                    // Increase Reposted Number
                    let target_button_element = document.getElementById(target_element_id);
                    let num_repost = Number(target_button_element.innerText);
                    num_repost += 1;
                    target_button_element.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost.toString();
                    target_button_element.className = "card-link btn btn-primary btn-sm border-0 mx-0";
                    // target_button_element.disabled = true;

                    // Add a repost_user to repost_users for temporarily
                    // Update $post_list_stored
                    for (let post of $post_list_stored) {
                        if (post["id"] === post_id) {
                            let tmp_obj = {
                                id: "temp_id",
                                username: $username,
                            }
                            let tmp_arr = post["repost_users"];
                            tmp_arr.push(tmp_obj);
                            post["repost_users"] = tmp_arr;
                            return;
                        }
                    }
                }
                if (server_response === "Unrepost") {
                    // Decrease Reposted Number
                    let target_button_element = document.getElementById(target_element_id);
                    let num_repost = Number(target_button_element.innerText);
                    num_repost -= 1;
                    target_button_element.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost.toString();
                    target_button_element.className = "card-link btn btn-outline-primary btn-sm border-0 mx-0";
                    // target_button_element.disabled = true;

                    // Define a filter function
                    function myFilter(value) {
                        return value["username"] !== $username;
                    }
                    // Drop a user from repost_users array
                    for (let post of $post_list_stored) {
                        if (post["id"] === post_id) {
                            post["repost_users"] = post["repost_users"].filter(myFilter);
                            return;
                        }
                    }
                }
            },
            (result) => {
                err_msg = result["detail"];
            }
        )
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

<div class="my-2 rounded" id="post-corner">
    <div class="card rounded" >
        <div class="card-body rounded" id="post-body">

        <!-- Dot Dot Dot Menu -->
        <div class="d-flex flex-row justify-content-end" style="max-height: 5px">
            <div class="dropdown">
                <!-- Dot dot dot button -->
                <button class="btn btn-link" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="bi bi-three-dots"></i>
                </button>
                <ul class="dropdown-menu">
                    <!-- Prevent self report -->
                    {#if criminalId !== $userid}
                        <!-- Report criminal button -->
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
            
        
        <div class="d-flex flex-row align-items-center justify-content-start gap-2 mb-3">
            {#if post.user.picture !== null}
                <!-- User Profile Image -->
                <img src={post.user.picture} id="profile-pic" alt="profile_picture" style="width: 40px; height: 40px">
            {:else}
                <i class="bi bi-person" style="font-size: 30px;"></i>
            {/if}
            <!-- User Username -->
            <a
                use:link
                href="/profile/{post.user.username}"
                style="text-decoration:none; font-size: 15px;"
                class="fw-bold">
                {post.user.username}
            </a>
            <!-- Timestamp for Post -->
            {#if post.modified_at === null}
                <p class="card-subtitle mb-2 text-body-secondary mt-2" style="font-size: 10px;">{moment(post.created_at).format("YY年MM月DD日 A hh:mm ")}</p>
            {:else}
                <p class="card-subtitle mb-2 text-body-secondary mt-2" style="font-size: 10px;">{moment(post.modified_at).format("(変)YY年MM月DD日 A hh:mm")}</p>
            {/if}

        </div>
        
        <!-- Post Title -->
        <div class="container p-0 m-0">
            <div class="d-flex flex-row gap-2">
                {#if post_recommended === true}
                    <i class="bi bi-award" style="color: red"></i>
                {/if}
                <!-- Title Button -->
                <button
                    style="text-decoration:none; font-size: 18px;"
                    class="btn btn-link fw-bold p-0 m-0 text-start"
                    on:click={openDetailModal(post.id)}
                    data-bs-toggle="modal"
                    data-bs-target="#detailModal_{unique_name}">
                    <p class="fw-bold">{post.title}</p>
                </button>
                <!-- More contents mark: image or embed -->
                {#if post.detail_id !== null}
                    <i class="bi bi-card-image"></i>
                {/if}
                <!-- Report mark -->
                {#if post.report === true}
                    <i class="bi bi-clipboard-data"></i>
                {/if}
            </div>
        </div>

        <!-- Post Content -->
        <p class="card-text my-3">{@html post.content}</p>

        <div class="container p-0">
            <div class="row">
                <div class="col-4 py-0 d-flex justify-content-center">
                    <!-- Like Buttons -->
                    {#if post_already_liked === true}
                        <button 
                            id="like-button-{post.id}"
                            type="button" 
                            class="card-link btn btn-primary btn-sm border-0 mx-0">
                                <i class="bi bi-hand-thumbs-up-fill"></i> {num_likes}
                        </button>
                    {/if}
                    {#if post_already_liked === false}
                        <button 
                            id="like-button-{post.id}"
                            type="button" 
                            class="card-link btn btn-outline-primary btn-sm border-0 mx-0"
                            on:click={likePost(post.id)}>
                                <i class="bi bi-hand-thumbs-up-fill"></i> {num_likes}
                        </button>
                    {/if}
                </div>
                <div class="col-4 py-0 d-flex justify-content-center">
                    <!-- Repost Button -->
                    {#if post_already_reposted === true}
                        <button
                            id="repost-button-{post.id}"
                            type="button" 
                            class="card-link btn btn-primary btn-sm border-0 mx-0"
                            on:click={repostPost(post.id)}>
                                <i class="bi bi-repeat"></i> {num_reposted}
                        </button>
                    {/if}
                    {#if post_already_reposted === false}
                        <button
                            id="repost-button-{post.id}"
                            type="button" 
                            class="card-link btn btn-outline-primary btn-sm border-0 mx-0" 
                            on:click={repostPost(post.id)}>
                                <i class="bi bi-repeat"></i> {num_reposted}
                        </button>
                    {/if}
                </div>
                
                <div class="col-4 py-0 d-flex justify-content-center">
                    <!-- Reply Button -->
                    <button 
                        type="button" 
                        class="card-link btn btn-outline-primary btn-sm border-0 mx-0"
                        on:click={openDetailModal(post.id)}
                        data-bs-toggle="modal"
                        data-bs-target="#detailModal_{unique_name}">
                            <i class="bi bi-chat-fill"></i> {num_replies}
                    </button>
                </div>

                
            </div>
        </div>
        </div>
    </div>
</div>

<style>

#post-body {
    background-color: #F5F5F5;
}

#post-corner {
    background-color: #cac6c6;
}

#profile-pic {
  border-radius: 50%;
}

</style>