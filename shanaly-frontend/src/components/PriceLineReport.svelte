<script>
    export let symbol = "";
    export let symbolName = "";
    export let period;
    export let data = [];
    export let lineColor = "";

    import fastapi from "../lib/api";
    import SymbolSearchHelper from "./SymbolSearchHelper.svelte";

    // Varibales for Symbol Search Helper
    let helperOn = false;

    let err_msg = "";
    let running = false; // Running spinner
    // Get data from Backend API server: Yahoo finance
    // Fetch data by using the backend API
    async function getYahooData(target_symbol, target_period) {
        
        let params = {};
        let endpoint = "";
        
        params = {
            symbol: target_symbol,
            period: target_period,
            timeframe: "1d",
        };
        endpoint = "/api/data/price_yahoo";

        await fastapi(
            "get",
            endpoint,
            params,
            (result) => {
                // Assign the received result to data
                data = result;
                // Reset Error message if successful
                err_msg = "";
            },
            (result) => {
                err_msg = result["detail"];
            }
        )
    }

    async function getData() {
        running = true;
        await getYahooData(symbol, period);
        running = false;
    }

</script>

<!-- Symbol Search Helper -->
<!-- This is hidden at first -->
{#if helperOn === true}
    <div class="mx-1 mb-3">
        <SymbolSearchHelper bind:userSelectSymbol={symbol} bind:userSelectSymbolName={symbolName}/>
    </div>
{/if}

<!-- Input Form for Title and Content -->
<div class="mb-3 d-flex flex-row">
    <div class="mx-1">
        <!-- Symbol Input Label -->
        <label for="input-symbol" class="form-label">銘柄コード</label>
        <!-- Button for switching Symbol Search Helper -->
        <button class="btn btn-link text-align-center pt-0 px-0" on:click={()=>{helperOn = !helperOn;}}>
            <i class="bi bi-question-circle"></i>
        </button>
        <!-- Symbol Input -->
        <textarea class="form-control" id="input-symbol" rows="1" bind:value={symbol}></textarea>
    </div>
    <div class="mx-1">
        <label for="input-period" class="form-label">期間</label>
        <select class="form-select" aria-label="default-select" id="input-period" bind:value={period}>
            <option value="1mo">1ヶ月</option>
            <option selected value="3mo">3ヶ月</option>
            <option value="6mo">6ヶ月</option>
            <option value="1y">1年</option>
            <option value="2y">2年</option>
            <option value="5y">5年</option>
        </select> 
    </div>
</div>

{#if symbol !== "" && symbol !== null && symbol !== undefined}
    <div class="mb-3 d-flex flex-row mx-1">
        <button type="button" class="btn btn-outline-primary" on:click={getData}>
            {#if running === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            <!-- Whether Data is donwloaded or not-->
            {#if data.length > 0 && err_msg === "" && running == false}
                <!-- Check mark -->
                <i class="bi bi-check-lg"></i>
            {/if}
            ダウンロード
        </button>    
    </div>
    {#if err_msg !== ""}
        <!-- Error Message -->
        <div class="alert alert-primary" role="alert">
            {err_msg}
        </div>
    {/if}
{/if}

{#if data.length > 0 && running === false && err_msg === ""}
    <div class="mb-3 d-flex flex-row">    
        
        <div class="container-fluid mx-1">
            <!-- Select Technical Indicators -->
            <div class="mb-2">
                <!-- Color Picker -->
                <div class="my-3">
                    <label for="color-picker" class="form-label">色</label>
                    <input class="container-fluid rounded p-0" type="color" id="color-picker" bind:value={lineColor}>
                </div>
            </div>

        </div>
    </div>
    
{/if}

    
    


