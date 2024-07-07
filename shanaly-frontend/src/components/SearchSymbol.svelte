<script>
    import fastapi from "../lib/api";
    import Price from "./Price.svelte";
    import FinancialStatement from "./FinancialStatement.svelte";
    import SymbolRecommend from "./SymbolRecommend.svelte";
    import { onMount } from "svelte";
    import { symbol_autocomplete_list } from "../lib/store";

    // Variables for err and sucess message
    let err_msg = "";

    // Variables for autocomplete
    let userInput = ""; // User input value in the input form
    let candidate_arr = []; // Array for containing candidate search keywords (display purpose)

    // Variables for Search Parameters
    let detailSelect = false;
    let target_symbol = "";
    let target_symbol_name = "";
    let target_asset_type = "";
    let target_kind = "price";
    let target_period = "1mo";
    let target_frequency = "q";

    // Variable for downloaded data
    let currentSymbol = "";
    let currentSymbolName = "";
    let currentTimeFrame = "";
    let currentReceivedData = []; // Array for containing price data downloaded from the backend API
    let currentReceivedDataKind = ""; // Array for classifying the kind of data: price or financial statement currently
    let running = false;

    // When a user is typing something, show the autocomplete result
    function showResult() {

        // if a user already downloaded data,
        // Reset the variables for the previous downloaded data
        currentSymbol = "";
        currentSymbolName = "";
        currentTimeFrame = "";
        currentReceivedData = []; // Array for containing price data downloaded from the backend API
        currentReceivedDataKind = ""; // Array for classifying the kind of data: price or financial statement currently
        running = false;

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

    // Fetch data by using the backend API
    function getYahooData() {
        let params = {};
        let endpoint = "";

        if (target_kind === "price") {
            params = {
                symbol: target_symbol,
                period: target_period,
                timeframe: "1d",
            };
            endpoint = "/api/data/price_yahoo";
        }
        if (target_kind === "financial_statement") {
            params = {
                symbol: target_symbol,
                frequency: target_frequency, // This should be "q" or "a" either
            };
            endpoint = "/api/data/financial_statement_yahoo";
        }

        fastapi(
            "get",
            endpoint,
            params,
            (result) => {
                // Assign the received result data to currentReceivedData
                currentReceivedData = result;
                
                if (target_kind === "price") {
                    // Classify the kind of data
                    currentReceivedDataKind = "price";
                }
                if (target_kind === "financial_statement") {
                    // Classify the kind of data
                    currentReceivedDataKind = "financial_statement";
                }
                
                // Reset userInput If Successful
                userInput = "";
                target_symbol = "";
                target_asset_type = "";
                target_kind = "price";
                target_period = "1mo";
                target_frequency = "q";

            },
            (result) => {
                err_msg = result["detail"];
                running = false;
            }
        )
        // Reset detail_select for hiding detail select dropdowns while loading data
        detailSelect = false;

        // While downloading data asynchronously, make running true!
        running = true;
    }

    function selectOneCandidate(item, index) {
        
        // Set the keyword in the search bar
        userInput = candidate_arr[index];
        // Set the final search keyword on the input form
        document.querySelector("[id='user-input-form-symbol-search']").value = candidate_arr[index];
        // Clear candidate search keywords array
        candidate_arr = [];
        // Clear the currentReceivedData array
        currentReceivedData = [];
        // Set the target symbol
        target_symbol = userInput.split(" > ")[0];
        // Set the target symbol name
        target_symbol_name = userInput.split(" > ")[1];

        for (let i of $symbol_autocomplete_list) {
            if (i["symbol"] === target_symbol) {
                target_asset_type = i["asset_type"];
                break
            }
        }
        // Open some dropdown menus for setting details
        detailSelect = true;

        // Set current symbol & timeframe
        currentSymbol = target_symbol;
        currentSymbolName = target_symbol_name;
        currentTimeFrame = "1d";
    }

</script>

    
<!-- Title -->
<div class="container my-1 px-0">
    <h1><i class="bi bi-bar-chart-fill"></i> 銘柄検索</h1>
</div>

<!--　Autocomplete Search Bar -->
<div class="container my-3 p-0">

        <!-- User Input -->
        <input
        type="text"
        class="form-control rounded-pill search"
        placeholder="銘柄コード or 銘柄名"
        id="user-input-form-symbol-search"
        autocomplete="off"
        bind:value={userInput}
        />

        <!-- Execution Button for Search -->
        <div class="d-grid gap-2 my-2">
            <button 
            id="execute-search-button"
            class="btn btn-outline-primary" 
            type="button" 
            on:click={showResult}>検索</button>
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

        {#if detailSelect === true && userInput !== ""}

            <div class="d-flex flex-column gap-2">

                <select class="form-select" id="kind" bind:value={target_kind}>
                    <option value="price" selected>価格</option>
                    
                    {#if target_asset_type === "equity"}
                        <option value="financial_statement">財務情報</option>
                    {/if}
                    
                </select>
                
                    {#if target_kind === "price"}
                        <select class="form-select" id="period" bind:value={target_period}>
                            <option value="1mo" selected>1ヶ月</option>
                            <option value="3mo" selected>3ヶ月</option>
                            <option value="6mo" selected>6ヶ月</option>
                        </select>
                    {/if}

                    {#if target_kind === "financial_statement"}
                        <select class="form-select" id="period" bind:value={target_frequency}>
                            <option value="q" selected>四半期</option>
                            <option value="a" selected>年度</option>
                        </select>
                    {/if}

                <!-- Get Data and Create Charts and Post -->
                <div class="d-grid gap-2 mb-2">
                    <button 
                    id="create-chart-post-button"
                    class="btn btn-outline-primary" 
                    type="button" 
                    on:click={getYahooData}>ダウンロード</button>
                </div>
                
            </div>
            
        {/if}
</div>

<!-- Search Result will be display here with the confirmed search keyword -->
{#if running === true && currentReceivedData.length === 0 && err_msg === ""}
    <div class="d-flex justify-content-center my-5">
        <div class="spinner-border" role="status" style="width: 10rem; height: 10rem;">
            <span class="visually-hidden"></span>
        </div>
    </div>
{:else if running === false && err_msg !== ""}
    <div class="alert alert-primary" role="alert">
        {err_msg}
    </div>
{:else}
    {#if currentReceivedDataKind === "price" && currentReceivedData.length > 0}
        <!--Price: TradingView Light-weight Chart -->
        <Price symbol={currentSymbol} symbolName={currentSymbolName} data={currentReceivedData} timeframe={currentTimeFrame}/>
    {/if}
    {#if currentReceivedDataKind === "financial_statement"}
        <!-- Financial Statement -->
        <FinancialStatement symbol={currentSymbol} symbolName={currentSymbolName} data={currentReceivedData}/>
    {/if}
    {#if userInput === "" || userInput === null || userInput === undefined}
        <!-- Symbol Recoomendation -->
        <!-- <SymbolRecommend/> -->
    {/if}
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
