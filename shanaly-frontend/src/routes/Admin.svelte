<script>
    import fastapi from "../lib/api";
    import { link, push } from "svelte-spa-router";

    let err_msg = "";

    // Variables for criminals
    let criminal_stat = [];
    let criminal_info = [];

    // Variables for recommend posts
    let recommend_post_id = "";
    let admin_password = "";
    let recommended_msg = "";

    // Variables for Wiki words
    let search_wiki_word = "";
    let wiki_word_data = {};
    let err_msg_wiki = "";
    let success_msg_wiki = "";
    let current_word_id = "";
    let current_word_name = "";
    let current_yomikata = ""; 
    let current_category = "";
    let current_description = ""; 
    let current_link = "";
    let current_ready = "";

    fastapi(
        "get",
        "/api/admin/list/potential_criminals",
        {},
        (result) => {
            // Remove error message
            err_msg = "";

            criminal_stat = result["criminal_stat"];
            criminal_info = result["criminal_info"];

            for (let i of criminal_stat) {
                for (let j of criminal_info) {
                    if (i["criminal_id"] === j["id"]){
                        i["username"] = j["username"];
                        i["is_blocked"] = j["is_blocked"];
                    }
                }
            }
        },
        (result) => {
            err_msg = result["detail"];
        }
    )

    function blockCriminal(userid) {

        if (window.confirm("本当にBlockしますか?")) {

            fastapi(
                "post",
                `/api/admin/block/${userid}`,
                {},
                (result) => {
                    // Update Frontend side
                    let tmp_criminal_stat = criminal_stat;
                    for (let i of tmp_criminal_stat) {
                        if (i["criminal_id"] === userid) {
                            i["is_blocked"] = true;
                            break;
                        }
                    }
                    criminal_stat = tmp_criminal_stat;

                    let tmp_criminal_info = criminal_info;
                    for (let i of tmp_criminal_info) {
                        if (i["id"] === userid) {
                            i["is_blocked"] = true;
                            break;
                        }
                    }
                    criminal_info = tmp_criminal_info;
                },
                (result) => {
                    // Do nothing
                }
            )
        } 
    }

    function unblockCriminal(userid) {

        fastapi(
            "post",
            `/api/admin/unblock/${userid}`,
            {},
            (result) => {
                // Update Frontend side
                let tmp_criminal_stat = criminal_stat;
                for (let i of tmp_criminal_stat) {
                    if (i["criminal_id"] === userid) {
                        i["is_blocked"] = false;
                        break;
                    }
                }
                criminal_stat = tmp_criminal_stat;

                let tmp_criminal_info = criminal_info;
                for (let i of tmp_criminal_info) {
                    if (i["id"] === userid) {
                        i["is_blocked"] = false;
                        break;
                    }
                }
                criminal_info = tmp_criminal_info;
            },
            (result) => {
                // Do nothing
            }
        )
    }

    function deleteAllPosts(criminal_id) {
        if (window.confirm(`このユーザー (ID=${criminal_id}) の投稿を全て削除しますか?`)) {
            fastapi(
                "delete",
                `/api/admin/posts/${criminal_id}`,
                {},
                (result) => {
                    alert(result["detail"]);
                },
                (result) => {
                    alert(result["detail"]);
                }
            )
        }
    }

    function deleteAllReplies(criminal_id) {
        if (window.confirm(`このユーザー (ID=${criminal_id}) の返信を全て削除しますか?`)) {
            fastapi(
                "delete",
                `/api/admin/replies/${criminal_id}`,
                {},
                (result) => {
                    alert(result["detail"]);
                },
                (result) => {
                    alert(result["detail"]);
                }
            )
        }
    }

    function resetNumReported(criminal_id) {
        if (window.confirm(`このユーザー (ID=${criminal_id}) の申告数をリセットしますか?`)) {
            fastapi(
                "patch",
                `/api/admin/reset/${criminal_id}`,
                {},
                (result) => {
                    // Update Frontend side
                    let tmp_criminal_stat = criminal_stat;
                    for (let i of tmp_criminal_stat) {
                        if (i["criminal_id"] === criminal_id) {
                            i["num_reported"] = 0;
                            break;
                        }
                    }
                    criminal_stat = tmp_criminal_stat;
                    // Alert message
                    alert(result["detail"]);
                },
                (result) => {
                    alert(result["detail"]);
                }
            )
        }
    }

    function recommendPost() {
        let params = {
            post_id: parseInt(recommend_post_id),
            password: admin_password,
        }
        fastapi(
            "post",
            "/api/admin/recommend",
            params,
            (result) => {
                recommended_msg = result["detail"];

                // Reset values
                admin_password = "";
            },
            (result) => {
                document.getElementById("admin-recommend-modal-close").click();
                // If fail, then logout
                admin_password = "";
                logout();
            }
        )
    }

    function getWordData() {
        let params = {
            word: search_wiki_word,
        }
        fastapi(
            "get",
            "/api/admin/wiki_get",
            params,
            (result) => {
                err_msg_wiki = "";
                wiki_word_data = result;

                // Set the values
                current_word_id = wiki_word_data["id"];
                current_word_name = wiki_word_data["word"];
                current_yomikata = wiki_word_data["yomikata"];
                current_category = wiki_word_data["category"];
                current_description = wiki_word_data["description"];
                current_link = wiki_word_data["link"];
                current_ready = String(wiki_word_data["ready"]);
            },
            (result) => {
                err_msg_wiki = result["detail"];
            }
        )
    }

    function modifyWord() {

        let tmp_current_ready;

        if (current_ready === "false") {
            tmp_current_ready = false;
        } 
        if (current_ready === "true") {
            tmp_current_ready = true;
        }

        let params = {
            id: current_word_id,
            description: current_description,
            link: current_link,
            ready: tmp_current_ready,
        }

        fastapi(
            "patch",
            "/api/admin/wiki_modify",
            params,
            (result) => {
                clearWikiValues();
                success_msg_wiki = result["detail"];
            },
            (result) => {
                err_msg_wiki = result["detail"];
                success_msg_wiki = "";
            }
        )
    }

    function clearWikiValues() {
        // Variables for Wiki words
        search_wiki_word = "";
        wiki_word_data = {};
        err_msg_wiki = "";
        success_msg_wiki = "";
        current_word_id = "";
        current_word_name = "";
        current_yomikata = ""; 
        current_category = "";
        current_description = ""; 
        current_link = "";
        current_ready;
    }

</script>

<div class="container-sm">
    <!-- Header -->
    <h1>Admin管理</h1>

    <div class="d-flex flex-row my-2 gap-1">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#adminRecommendModal">
            おすすめ投稿
        </button>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#adminWikiModal">
            用語検索変更
        </button>
    </div>



    <p>※30日の間の集計</p>

    <!-- Error Message -->

    {#if err_msg !== ""}
        <div class="my-3">
            {err_msg}
        </div>    
    {/if}


    

    <table class="table table-hover">
        <thead>
            <tr>
                <th scope="col">ID</th>
                <th scope="col">ユーザー名</th>
                <th scope="col">申告された数</th>
                <th scope="col">アクション</th>
            </tr>
        </thead>
        <tbody>
            {#if criminal_stat.length !== 0}
                {#each criminal_stat as item}
                    <tr>
                        <!-- Potential Criminal Users -->
                        <td>{item.criminal_id}</td>
                        <td>{item.username}</td>
                        <td>{item.num_reported}</td>
                        <td>
                            <div class="d-flex flex-row gap-1">
                                <!-- Check Activity of A User -->
                                <a use:link href="/profile/{item.username}" class="btn btn-sm btn-outline-primary" style="font-size: 11px; text-align: center;">確認</a>
                                
                                <!-- Block or Unblock Button -->
                                {#if item.is_blocked === false}
                                    <button type="button" class="btn btn-sm btn-outline-danger" style="font-size: 11px;" on:click={blockCriminal(item.criminal_id)}>ブロック</button>
                                {:else}
                                    <button type="button" class="btn btn-sm btn-outline-success" style="font-size: 11px;" on:click={unblockCriminal(item.criminal_id)}>ブロック解除</button>
                                {/if}
                                
                                <!-- Delete All Posts or Replies Buttons -->
                                <div class="d-flex flex-column">
                                    <button type="button" class="btn btn-sm btn-outline-primary" style="font-size: 9px;" on:click={deleteAllPosts(item.criminal_id)}>全ての投稿削除</button>
                                    <button type="button" class="btn btn-sm btn-outline-primary" style="font-size: 9px;" on:click={deleteAllReplies(item.criminal_id)}>全ての返信削除</button>
                                </div>

                                <!-- Reset the Number of Reported Button -->
                                <button type="button" class="btn btn-sm btn-outline-primary" style="font-size: 11px;" on:click={resetNumReported(item.criminal_id)}>リセット</button>
                            </div>  
                        </td>
                    </tr>
                {/each}
            {/if}
        </tbody>
    </table>

    <!-- Admin Recommend Modal -->
    <div class="modal fade" id="adminRecommendModal" tabindex="-1" aria-labelledby="adminRecommendModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="adminRecommendModalLabel">おすすめ投稿</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="admin-recommend-modal-close"></button>
            </div>
            <div class="modal-body">

                <form method="post">
                    <!-- Post ID -->
                    <div class="mb-3">
                        <label for="post_recommend">投稿ID</label>
                        <input type="text" class="form-control" id="post_recommend" autocomplete="off" bind:value={recommend_post_id}>
                    </div>
                    <!-- Admin Password -->
                    <div class="mb-3">
                        <label for="password_create1">ADMINパスワード</label>
                        <input type="password" class="form-control" id="password_create1" autocomplete="off" bind:value={admin_password}>
                    </div>
                    <!-- Submit Button -->
                    <div class="mb-3">
                        <button type="button" class="btn btn-primary" on:click={recommendPost}>OK</button>
                    </div>    
                </form>
                
                <!-- Message -->
                {#if recommended_msg !== ""}
                    <div class="alert alert-primary" role="alert">
                        {recommended_msg}
                    </div>
                {/if}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
            </div>
        </div>
        </div>
    </div>


    <!-- Admin Wiki Modal -->
    <div class="modal fade" id="adminWikiModal" tabindex="-1" aria-labelledby="adminWikiModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="adminWikiModalLabel">用語検索変更</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="admin-wiki-modal-close"></button>
            </div>
            <div class="modal-body">

                {#if err_msg_wiki !== ""}
                    <div class="alert alert-primary my-1" role="alert">
                        {err_msg_wiki}
                    </div>
                {/if}
                
                <!-- Wiki Word Search -->
                <form method="get">
                    <label for="wiki_word_search">用語名</label>
                    <div class="d-flex flex-row mb-3 gap-1">
                        <input type="text" class="form-control" id="wiki_word_search" autocomplete="off" bind:value={search_wiki_word}>
                        <!-- Search Button -->
                        <button class="btn btn-outline-primary" on:click={getWordData}>
                            <i class="bi bi-search"></i>
                        </button>
                    </div>
                </form>
                
                <!-- Clear Values Button -->
                <div class="d-grid gap-2 my-3">
                    <button class="btn btn-primary" type="button" on:click={clearWikiValues}>クリア</button>
                </div>

                {#if success_msg_wiki !== ""}
                    <div class="alert alert-success my-1" role="alert">
                        {success_msg_wiki}
                    </div>
                {/if}

                <!-- Form -->
                {#if wiki_word_data.word !== undefined}
                    <div class=mb-3>
                        <label for="wiki_word_id">用語ID</label>
                        <input type="text" class="form-control" id="wiki_word_id" autocomplete="off" bind:value={current_word_id} disabled>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_name">用語名</label>
                        <input type="text" class="form-control" id="wiki_word_name" autocomplete="off" bind:value={current_word_name} disabled>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_yomikata">読み方</label>
                        <input type="text" class="form-control" id="wiki_word_yomikata" autocomplete="off" bind:value={current_yomikata} disabled>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_category">カテゴリ</label>
                        <input type="text" class="form-control" id="wiki_word_category" autocomplete="off" bind:value={current_category} disabled>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_description">用語意味 (Markdown可能)</label>
                        <textarea class="form-control" id="wiki_word_description" rows="5" bind:value={current_description}></textarea>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_link">リンク</label>
                        <input type="text" class="form-control" id="wiki_word_link" autocomplete="off" bind:value={current_link}>
                    </div>
                    <div class=mb-3>
                        <label for="wiki_word_ready">準備中(公開)?</label>
                        <select class="form-select" aria-label="Default select example" bind:value={current_ready}>
                            <option value="false" selected>false</option>
                            <option value="true">true</option>
                            
                        </select>
                    </div>
                {/if}
                
            </div>
            <div class="modal-footer">
                {#if wiki_word_data.word !== undefined}
                    <button type="button" class="btn btn-primary" on:click={modifyWord}>変更</button>
                {/if}
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal" on:click={clearWikiValues}>閉じる</button>
            </div>
        </div>
        </div>
    </div>

    

</div>

    
<style>

.container-sm {
    max-width: 576px;
}

</style>