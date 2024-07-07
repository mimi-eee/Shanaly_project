<script>
    import fastapi from "../lib/api";
    import { onMount } from "svelte";
    import { marked } from 'marked';
    import { update_date_wiki, wiki_autocomplete_list } from "../lib/store";

    // Words array for autocomplete
    let words_arr = [];

    onMount(() => {
        if ($update_date_wiki === 0 || $update_date_wiki === null || $update_date_wiki === undefined || $wiki_autocomplete_list === []) {

            // Set the update date
            $update_date_wiki = new Date();

            // Update Wiki
            fastapi(
                "get",
                "/api/others/wiki/dict",
                {},
                (result) => {
                    // Set the wiki word list
                    $wiki_autocomplete_list = result;
                    words_arr = $wiki_autocomplete_list; // Important!!!
                },
                (result) => {
                    // Display error message
                    err_msg = result["detail"];
                }
            )
        } else {
            // Check whether enough time has passed for updating wiki words array
            let diff = new Date() - new Date($update_date_wiki);

            words_arr = $wiki_autocomplete_list; // Important!!!
            
            if (diff > 3600000) {
                
                // Update Wiki
                fastapi(
                    "get",
                    "/api/others/wiki/dict",
                    {},
                    (result) => {
                        // Set the wiki word list
                        $wiki_autocomplete_list = result;
                        words_arr = $wiki_autocomplete_list; // Important!!!
                        // Set the update date
                        $update_date_wiki = new Date();
                    },
                    (result) => {
                        // Display error message
                        err_msg = result["detail"];
                    }
                )
            }
        }
    })


    // Variables for autocomplete
    let userInput = "";
    let candidate_arr = [];
    let search_word = "";
    let output = {"word": "", "description": "", "link": ""};

    function showResult() {

        let tmp_arr = [];

        if (userInput !== null & userInput !== "") {

            for (var i = 0; i < words_arr.length; i++) {
                let w = words_arr[i].toLowerCase();
                if (w.includes(userInput.toLowerCase())) {
                    tmp_arr.push(words_arr[i]);
                }
            }
            candidate_arr = tmp_arr;
        }
    }
    function getWordData(search_word) {
        // Some words have slash("/"), so Path parameter does not work!
        // This is the reason why I use Query parameter here
        let params = {
            keyword: search_word,
        }

        fastapi(
            "get",
            `/api/others/wiki/word`,
            params,
            (json) => {
                output["word"] = json["word"];
                output["description"] = json["description"];
                output["link"] = json["link"];
                output["ready"] = json["ready"];
            },
            (json) => {
                // Display error message
                err_msg = json["detail"];
            }
        )
    }

    function enterMovement(e) {
        if (e.key === "Enter" && candidate_arr.length == 1) {
            search_word = candidate_arr[0];
            document.querySelector("[id='user-input-form-wiki-search']").value = candidate_arr[0];
            candidate_arr = [];
        }
    }

    function selectOneCandidate(item) {
        userInput = item;
        candidate_arr = [];
        search_word = item;

        // Get the target keyword's data
        getWordData(search_word);
    }

</script>

<div class="container-sm">

    <!-- Autocomplete Search Bar -->
    <div class="container px-0">

            <div class="d-flex flex-row gap-2">
                <input
                type="text"
                class="form-control rounded-pill search"
                placeholder="検索..."
                id="user-input-form-wiki-search"
                autocomplete="off"
                on:keyup={enterMovement}
                bind:value={userInput}
                />
                <!-- Search Button -->
                <button class="btn btn-outline-primary" on:click={showResult}>
                    <i class="bi bi-search"></i>
                </button>
            </div>
            
            <!-- Candidate Items -->
            {#if candidate_arr.length !== 0}
            <div class="container result-box border rounded py-0">
                <ul>
                    {#each candidate_arr as item}
                        <li>
                            <button class="text-start" on:click={selectOneCandidate(item)}>{item}</button>
                        </li>
                    {/each}
                </ul>
            </div>
            {/if}
    </div>

    <!-- Search Result (Output) -->
    {#if search_word !== ""}
        <div class="container my-3 p-0">
            {#if output !== {}}
                <div class="container my-2 p-0">
                    <!-- Word Title -->
                    <div class="container my-2 mx-0 p-0 word-wrap">
                        <h5 class="fw-bold">{output.word}</h5>
                    </div>
                    <!-- Word Description -->
                    <div class="container my-2 p-0 word-wrap">
                        <!-- You cannot show Nomura's description directly -->
                        <!-- It is necessary to paraphrase the desc into my own description -->
                        <!-- When you are ready with your own description, -->
                        <!-- You can change the column 'ready' to True in Wiki Table in DB -->
                        <!-- Then the description will be displayed -->
                        {#if output.ready === false}
                            <div class="my-3 p-0 word-wrap">
                                <p class="fs-3">「準備中」</p>
                            </div>
                        {:else}
                            <!--  -->
                            {@html marked.parse(output.description)}
                        {/if}
                    </div>
                    <!-- If you are ready with your own description, then reference will be not displayed as well -->
                    {#if output.ready === false}
                        <div class="container my-2 mx-0 p-0 word-wrap">
                            <a href="{output.link}" target="_blank" style="color: blue;">参考資料</a>
                        </div>
                    {/if}
                </div>
                
            {/if}
            
        </div>
    {/if}

</div>

<style>
.container-sm {
    max-width: 576px;
}

.result-box {
    max-height: 150px;
    overflow-y: scroll;
}

.result-box ul {
    padding: 10px 1px;
}
.result-box ul li {
    list-style: none;
    border-radius: 3px;
    padding: 1px 1px;
    cursor: pointer;
}
.result-box ul li:hover {
    background: #e9f3ff;
}

.result-box button {
    border: unset;
    background: unset;
}



</style>
