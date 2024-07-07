<script>
    export let data = {};
    export let symbols_arr = [];

    import fastapi from "../lib/api";
    import SymbolSearchHelper from "./SymbolSearchHelper.svelte";

    // Varibales for Symbol Search Helper
    let helperOn = false;

    /////////

    let symbol;

    let err_msg = "";
    let running = false; // Running spinner

    function addSymbol() {
        // Limit the number of symbols not over 6
        if (symbols_arr.length < 6) {
            let tmp_arr = symbols_arr;
            tmp_arr.push(symbol.toString());
            symbols_arr = tmp_arr;
        }
    }

    function resetSymbolArr() {
        symbols_arr = [];
    }

    function resetSymbol() {
        symbol = "";
    }

    // Get data from Backend API server: Yahoo finance
    // Fetch data by using the backend API
    async function getYahooData(target_symbol_arr) {
        
        let params = {};
        let endpoint = "";
        
        params = {
            symbol: target_symbol_arr,
        };
        endpoint = "/api/data/price_yahoo_multiple";

        await fastapi(
            "post",
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
        await getYahooData(symbols_arr);
        running = false;
    }
    
</script>

<!-- Symbol Search Helper -->
<!-- This is hidden at first -->
{#if helperOn === true}
    <div class="mx-1 mb-3">
        <SymbolSearchHelper bind:userSelectSymbol={symbol}/>
    </div>
{/if}

<div class="mx-1 mb-3">
    <!-- Input for Symbol -->
    <label for="input-symbol" class="form-label">
        銘柄コード
    </label>
    <!-- Button for switching Symbol Search Helper -->
    <button class="btn btn-link text-align-center pt-0 px-0" on:click={()=>{helperOn = !helperOn;}}>
        <i class="bi bi-question-circle"></i>
    </button>
    <!-- Symbols will be typed here -->
    <textarea class="form-control" id="input-symbol" rows="1" bind:value={symbol}></textarea>
</div>

<div class="container mb-3">
    <p style="font-size: 11px;">「+」ボタンをクリック → 最大6個まで銘柄コードをリストに追加 → ダウンロード → チェックマークの確認 → 追加</p>
    <div class="row">
      <div class="col d-grid mx-0">
        <button type="button" class="btn btn-outline-primary" on:click={addSymbol} on:click={resetSymbol}>+</button>
      </div>
      <div class="col d-grid mx-0">
        <button type="button" class="btn btn-outline-primary" on:click={resetSymbolArr}>リセット</button>
      </div>
      <div class="col d-grid mx-0">
        <button type="button" class="btn btn-outline-primary" on:click={getData}>
            {#if running === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            {#if running === false && Object.keys(data).length > 0}
                <i class="bi bi-check-lg"></i>
            {/if}
            ダウンロード
        </button>
      </div>
    </div>
</div>

{#if err_msg !== ""}
    <!-- Error Message -->
    <div class="alert alert-primary" role="alert">
        {err_msg}
    </div>
{/if}

{#if symbols_arr.length > 0}
    <div class="container d-flex flex-row flex-wrap border rounded">
        {#each symbols_arr as sym}
            <button type="button" class="btn btn-link mx-1">{sym}</button>
        {/each}
    </div>
{/if}
    


