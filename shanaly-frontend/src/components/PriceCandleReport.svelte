<script>
    export let symbol = "";
    export let symbolName = "";
    export let period;
    export let timeframe;
    export let data = [];
    export let indicator_arr = [];

    import fastapi from "../lib/api";
    import SymbolSearchHelper from "./SymbolSearchHelper.svelte";

    // Varibales for Symbol Search Helper
    let helperOn = false;

    let err_msg = "";
    let running = false; // Running spinner

    // SMA Values
    let currnet_indicator = "SMA";
    let ma_num_options = [5,10,14,20,50,120,200];
    let sma_n;
    let sma_color = "#000000";

    // Get data from Backend API server: Yahoo finance
    // Fetch data by using the backend API
    async function getYahooData(target_symbol, target_period, target_timeframe) {
        
        let params = {};
        let endpoint = "";
        
        params = {
            symbol: target_symbol,
            period: target_period,
            timeframe: target_timeframe,
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
        await getYahooData(symbol, period, timeframe);
        running = false;
    }

    function addIndicator() {
        let tmp_indicator_arr = indicator_arr;
        
        // Cannot add indicators more than 3!
        if (tmp_indicator_arr.length >= 3) {
            return;
        }
        // Depends on Indicator
        if (currnet_indicator === "SMA") {
            tmp_indicator_arr.push({
                "indicator_name_display": "単純移動平均",
                "indicator_name": "SMA",
                "params": {
                    "N": Number(sma_n),
                    "color": sma_color,
                }
            })
        }
        indicator_arr = tmp_indicator_arr;
    }

    function clearIndicatorArray() {
        let tmp_indicator_arr = [];
        indicator_arr = tmp_indicator_arr;
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
    <div class="mx-1">
        <label for="input-timeframe" class="form-label">足</label>
        <select class="form-select" aria-label="default-select" id="input-timeframe"  bind:value={timeframe}>
            <option selected value="1d">日足</option>
            <option value="1wk">週足</option>
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
            <div class="mb-1">
                <label for="input-technical" class="form-label">テクニカル指標</label>
                <select class="form-select" aria-label="default-select" id="input-technical" bind:value={currnet_indicator}>
                    <option value="SMA">単純移動平均</option>
                    <option value="coming-soon">「準備中」</option>
                </select>
            </div>
            
            <!-- SMA -->
            {#if currnet_indicator === "SMA"}
                <div class="mb-1">
                    <label for="input-sma-n" class="form-label mt-1">N日</label>
                    <select class="form-select" aria-label="default-select" id="input-sma-n" bind:value={sma_n}>
                        {#each ma_num_options as num}
                            <option value={num}>{num}</option>
                        {/each}
                    </select>
                    <!-- Color Picker -->
                    <div class="my-1">
                        <label for="color-picker" class="form-label">色</label>
                        <input class="container-fluid rounded p-0" type="color" id="color-picker" bind:value={sma_color}>
                    </div>
                </div>
            {/if}

        </div>
    </div>

    <!-- Add or Reset Indicator Buttons -->
    <div class="d-flex flex-row justify-content-end gap-1">
        <button type="button" class="btn btn-outline-primary" on:click={addIndicator}>指標追加</button>
        <button type="button" class="btn btn-outline-primary" on:click={clearIndicatorArray}>リセット</button>
    </div>

    <!-- Display the Current Indicators List -->
    {#if indicator_arr.length > 0}
    <div class="container my-2 border rounded">
        <p class="fw-bold mt-3 mb-0 p-0" style="font-size: 15px">指標リスト(３つまで)</p>
        <ol class="list-group list-group-flush">
            {#each indicator_arr as item}
                <li class="list-group-item my-0">
                    {item.indicator_name_display} {item.params.N} <i class="bi bi-square-fill" style="color: {item.params.color};"></i>
                </li>
            {/each}
        </ol>
    </div>
    {/if}

{/if}

    
    


