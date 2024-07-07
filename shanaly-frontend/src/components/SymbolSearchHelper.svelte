<script>

    export let userSelectSymbol;
    export let userSelectSymbolName;

    import { symbol_autocomplete_list } from "../lib/store";

    // Variables for autocomplete
    let userInput = ""; // User input value in the input form
    let candidate_arr = []; // Array for containing candidate search keywords (display purpose)

    // When a user is typing something, show the autocomplete result
    function showResult() {
        let tmp_display_arr = [];
        if (userInput !== null & userInput !== "") {

            for (let item of $symbol_autocomplete_list) {
                let symbol = item["symbol"].toLowerCase();
                let name = item["name"].toLowerCase();
                if (symbol.includes(userInput.toLowerCase()) || name.includes(userInput.toLowerCase())) {
                    tmp_display_arr.push(`${item["symbol"]} > ${item["name"]}`);
                }
            }
            candidate_arr = tmp_display_arr; // This is for Human
        }
    }

    function selectOneCandidate(item, index) {
        // Set the keyword in the search bar
        userInput = candidate_arr[index];
        // Set the final search keyword on the input form
        document.querySelector("[id='user-input-form-symbol-search']").value = candidate_arr[index];
        // Clear candidate search keywords array
        candidate_arr = [];
        // Set the user selected symbol
        userSelectSymbol = userInput.split(" > ")[0];
        // Set the user selected symbolName
        userSelectSymbolName = userInput.split(" > ")[1];
    }

</script>

<div class="d-flex flex-row gap-2">
    <!-- User Input -->
    <input
    type="text"
    class="form-control rounded-pill search"
    placeholder="銘柄コード or 銘柄名"
    id="user-input-form-symbol-search"
    autocomplete="off"
    bind:value={userInput}
    />
    <!-- Search Button -->
    <button class="btn btn-outline-primary" on:click={showResult}>
        <i class="bi bi-search"></i>
    </button>
</div>


<!-- Candidate Items -->
{#if candidate_arr.length !== 0}
    <div class="container mt-1 result-box border rounded py-0">
        <ul>
            {#each candidate_arr as item, index}
                <li>
                    <button class="text-start" on:click={selectOneCandidate(item, index)}>{item}</button>
                </li>
            {/each}
        </ul>
    </div>
{/if}


<style>

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