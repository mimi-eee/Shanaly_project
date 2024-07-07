<script>
    export let unique_name;

    export let current_post_id;
    export let current_post_title;
    export let current_post_content;
    export let current_post_timestamp;
    export let current_post_username;
    export let current_post_tags;
    export let current_post_tags_arr;
    export let current_post_reply;
    export let current_post_num_likes;
    export let current_post_already_liked;

    export let current_post_num_reposted;
    export let current_post_already_reposted;

    export let detail_data_arr;
    export let editor;
    export let chart;

    import { link } from "svelte-spa-router"; 
    import LineChart from "./LineChart.svelte";
    import CandleChart from "./CandleChart.svelte";
    import BarChart from "./BarChart.svelte";
    import ReturnGroupBadge from "./ReturnGroupBadge.svelte";
    import { post_list_stored, username } from "../lib/store";
    import fastapi from "../lib/api";

    // This prevents the backsrop effect in Bootstrap5 Modal
    // when a user clicks or uses browser's BACK BUTTON!
    window.addEventListener('popstate', (event) => {
        try {
            document.querySelector("[id='detail-modal-button']").click();
        } catch {
            // Do nothing
        }
        
    });

    function getReplyData() {
        fastapi(
            "get",
            `/api/reply/all/${current_post_id}`,
            {},
            (result) => {
                current_post_reply = result;

                // This makes read-reply-tab displays the replies!
                document.querySelector("[id='write-reply-tab']").click();
                document.querySelector("[id='read-reply-tab']").click();
            },
            (result) => {
                // Do nothing
            }
        )
    }

    // Re-fit the content of lightweight chart
    function resizePriceChart() {
        try {
            chart.timeScale().fitContent();
        } catch {
            return;
        }
    }

    // Pause any video iframe
    function stopIframeVideoAll() {
	    var videos = document.querySelectorAll('iframe, video');
        Array.prototype.forEach.call(videos, function (video) {
            if (video.tagName.toLowerCase() === 'video') {
                video.pause();
            } else {
                var src = video.src;
                video.src = src;
            }
        })
    }

    // Get the original values of a target post for modify
    function getTargetPostValue(post_id) {
        for (const i of $post_list_stored) {
            if (i["id"] === post_id) {
                // Insert title
                document.getElementById("modifyTextAreaTitle").value = i["title"];
                // Insert content
                // Quill JS
                editor.clipboard.dangerouslyPasteHTML(i["content"]);
                
                // Insert tags as a String 
                current_post_tags = i["tags"];
                // Insert tags as an Array
                current_post_tags_arr = i["tags"].split("#");
            }
        }
    }

    // Close modal if clicking any tag link
    function closeModal() {
        document.querySelector("[id='detail-modal-button']").click();
    }

    // Like Post Button
    function likePost(post_id) {
        let params = {
            post_id: post_id,
        }
        fastapi(
            "post",
            "/api/post/like",
            params,
            (result) => {
                // Change the LikeIt number in the like button in the detail modal and make it disabled
                let target_button_element = document.getElementById("like-button-detail-modal");
                let num_like = Number(target_button_element.innerText)
                num_like += 1
                target_button_element.innerHTML = '<i class="bi bi-hand-thumbs-up-fill"></i> ' + num_like.toString();
                target_button_element.className = "btn btn-primary btn-sm me-1";
                target_button_element.disabled = true;

                // Change the LikeIt number in the like button in the <Post/> in Home.svetle
                let target_button_element_home = document.getElementById(`like-button-${post_id}`);
                let num_like_home = Number(target_button_element_home.innerText)
                num_like_home += 1
                target_button_element_home.innerHTML = '<i class="bi bi-hand-thumbs-up-fill"></i> ' + num_like_home.toString();
                target_button_element_home.className = "btn btn-primary btn-sm me-1";
                target_button_element_home.disabled = true;

                // Update the $post_list_stored
                // Add a like_user to like_users for temporarily
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

            },
            (result) => {
                err_msg = result["detail"];
            }
        )
    }

    // RePost Button
    function repostPost(post_id) {
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
                    // Increase the RePost number in the RePost button in the detail modal and make it disabled
                    let target_button_element = document.getElementById(`repost-button-detail-modal`);
                    let num_repost = Number(target_button_element.innerText);
                    num_repost += 1;
                    target_button_element.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost.toString();
                    target_button_element.className = "btn btn-primary btn-sm me-1";
                    // target_button_element.disabled = true;

                    // Increase the RePost number in the RePost button in the <Post/> in Home.svetle
                    let target_button_element_home = document.getElementById(`repost-button-${post_id}`);
                    let num_repost_home = Number(target_button_element_home.innerText);
                    num_repost_home += 1;
                    target_button_element_home.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost_home.toString();
                    target_button_element_home.className = "btn btn-primary btn-sm me-1";
                    // target_button_element_home.disabled = true;

                    // Update the $post_list_stored
                    // Add a like_user to like_users for temporarily
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
                    // Decrease the RePost number in the RePost button in the detail modal and make it disabled
                    let target_button_element = document.getElementById("repost-button-detail-modal");
                    let num_repost = Number(target_button_element.innerText);
                    num_repost -= 1;
                    target_button_element.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost.toString();
                    target_button_element.className = "btn btn-outline-primary btn-sm me-1";
                    // target_button_element.disabled = true;

                    // Decrease the RePost number in the RePost button in the <Post/> in Home.svetle
                    let target_button_element_home = document.getElementById(`repost-button-${post_id}`);
                    let num_repost_home = Number(target_button_element_home.innerText);
                    num_repost_home -= 1;
                    target_button_element_home.innerHTML = '<i class="bi bi-repeat"></i> ' + num_repost_home.toString();
                    target_button_element_home.className = "btn btn-outline-primary btn-sm me-1 border-0";
                    // target_button_element_home.disabled = true;
                    
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

</script>

<!-- Detail Modal; this is basically hidden unless a user clicks the title of a post -->
<div class="modal fade modal-lg" id="detailModal_{unique_name}" tabindex="-1" aria-labelledby="detailModalLabel" aria-hidden="true" on:focus={resizePriceChart}>
    <div class="modal-dialog modal-dialog-scrollable">
    <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5 word-wrap text-break" id="detailModalLabel">{current_post_title}</h1>
            <!-- The next button has its own id! -->
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="detail-modal-button" on:click={stopIframeVideoAll}></button>
        </div>
        <div class="modal-body">
            <div class="d-flex justify-content-end p-0 m-0">
                <p class="p-0 m-0" style="font-size: 9px">
                    投稿ID: {current_post_id} 
                </p>
            </div>
            <div class="d-flex justify-content-end p-0 mb-3">
                <p class="p-0 m-0" style="font-size: 10px">
                    {current_post_timestamp}
                </p>
            </div>

            <!-- Content -->
            <div class="p-0 mb-5">
                <p style="word-wrap: break-word;">{@html current_post_content}</p>
            </div>

            <!-- Create and list all components by order -->
            {#if detail_data_arr.length !== 0}
                {#each detail_data_arr as comp}

                    <!-- Component: Text -->
                    {#if comp.component_type === "text"}
                        <div class="mx-0 mb-3 p-0">
                            <!-- {comp.value} -->
                            <p style="word-wrap: break-word;">{@html comp.value}</p>
                        </div>
                    
                    <!-- Component Header -->
                    {:else if comp.component_type === "header"}
                        <div class="mx-0 mb-3 p-0">
                            <h3>{comp.value}</h3>
                        </div>
                    
                    <!-- Component Embeded -->
                    {:else if comp.component_type === "embed"}
                        <div class="mx-0 mb-3 p-0">
                            {@html comp.value}
                        </div>
                    
                    <!-- Component Image -->
                    {:else if comp.component_type === "image"}
                        <div class="mx-0 mb-3 p-0">
                            <!-- Image Fluid is important! -->
                            <img src="{comp.value}" alt="" class="img-fluid">
                        </div>

                    <!-- Component: Price Return -->
                    {:else if comp.component_type === "price_return"}
                        <!-- DEV -->
                        <div class="mt-5 mb-3 p-0">
                            <ReturnGroupBadge data={comp.data}/>
                        </div>
                    
                    <!-- Component: Price Line Chart -->
                    {:else if comp.component_type === "price_line"}

                        <div class="mt-2 mb-3 p-0">
                            <LineChart symbol={comp.symbol} symbolName={comp.symbolName} data={comp.data} lineColor={comp.lineColor}/>
                        </div>

                    <!-- Component: Price Candlestick -->
                    {:else if comp.component_type === "price_candle"}

                        <div class=" container mt-5 mb-3 p-0" style="height: 450px;">
                            <CandleChart symbol={comp.symbol} symbolName={comp.symbolName} timeframe={comp.timeframe} data={comp.data} indicator_arr={comp.indicator} chart_id={comp.idx} bind:chart={chart}/>
                        </div>
                    
                    <!-- Component: Financial Statement -->    
                    {:else if comp.component_type === "financial_statement"}
                        <div class="mt-5 mb-3  p-0">
                            <BarChart symbol={comp.symbol} symbolName={comp.symbolName} category={comp.category} data={comp.data} barColor={comp.barColor}/>
                        </div>
                    
                    {:else}
                        Component Type should be text or price or financial_statement!
                    {/if}
                {/each}
            {:else}
                <!-- Do not append detail component because there is no detail component for this post -->
            {/if}
        </div>

        <div class="modal-footer">
            <!-- Tags -->
            <div class="container d-flex mt-0 mb-2 mx-1 p-0">
                
                {#each String(current_post_tags).split("#") as tag}
                        #<a use:link href="/search/{tag}" style="text-decoration:none" on:click={closeModal}>{tag}&nbsp;</a>
                {/each}

            </div>

            <!-- Buttons -->
            <div class="container d-flex justify-content-end mx-0">
                <!-- Like Button -->
                {#if current_post_already_liked === false}
                    <button id="like-button-detail-modal" type="button" class="btn btn-outline-primary btn-sm me-1" on:click={likePost(current_post_id)}><i class="bi bi-hand-thumbs-up-fill"></i> {current_post_num_likes}</button>
                {:else}
                    <button type="button" class="btn btn-primary btn-sm me-1"><i class="bi bi-hand-thumbs-up-fill"></i> {current_post_num_likes}</button>
                {/if}

                <!-- Repost Button -->
                <!-- This can be reposted and UNreposted like a switch -->
                {#if current_post_already_reposted === false}
                    <button id="repost-button-detail-modal" type="button" class="btn btn-outline-primary btn-sm me-1" on:click={repostPost(current_post_id)}><i class="bi bi-repeat"></i> {current_post_num_reposted}</button>
                {:else}
                    <button id="repost-button-detail-modal" type="button" class="btn btn-primary btn-sm me-1" on:click={repostPost(current_post_id)}><i class="bi bi-repeat"></i> {current_post_num_reposted}</button>
                {/if}

                <!-- Reply Button -->
                <button 
                    type="button"
                    class="btn btn-outline-primary btn-sm me-1" 
                    data-bs-target="#replyModalToggle_{unique_name}" 
                    data-bs-toggle="modal"
                    id="detail-modal-reply-button"
                    on:click={getReplyData}>
                    <i class="bi bi-chat-fill"></i>返信
                </button>
                
                <!-- Modify and Delete Buttons -->
                {#if $username === current_post_username}
                    <button type="button" class="btn btn-outline-primary btn-sm me-1" data-bs-target="#modifyModalToggle_{unique_name}" data-bs-toggle="modal" on:click={getTargetPostValue(current_post_id)}><i class="bi bi-pencil-fill"></i> 修正</button>
                    <button type="button" class="btn btn-outline-primary btn-sm me-1" data-bs-target="#deleteModalToggle_{unique_name}" data-bs-toggle="modal"><i class="bi bi-trash-fill"></i> 削除</button>
                {/if}
                
                <button type="button" class="btn btn-outline-primary btn-sm me-1" data-bs-dismiss="modal" on:click={stopIframeVideoAll}>閉じる</button>
            </div>
        </div>
    </div>
    </div>
</div>
