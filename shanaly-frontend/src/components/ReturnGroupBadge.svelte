<script>
    export let data = {};

    let tmp_arr = [];

    for (let key of Object.keys(data)) {
        let tmp_obj = {
            symbol: key,
            close: data[key]["close"],
            sim_ret_pct: data[key]["sim_ret_pct"],
        };
        tmp_arr.push(tmp_obj);
    }

</script>

<div class="d-flex flex-row flex-wrap">
    {#each tmp_arr as item}
    <div class="card" style="width: 9rem;">
        <div class="card-body">
            <h5 class="card-title">
                <a href="https://finance.yahoo.co.jp/quote/{item.symbol}" target="_blank" style="text-decoration: none;">
                    {item.symbol}
                </a>
            </h5>
            <p class="card-text">
                {item.close.toLocaleString()}
                {#if item.sim_ret_pct >= 0}
                    <span class="badge text-bg-success">
                        {item.sim_ret_pct} %
                    </span>
                    <p style="font-size: 10px">(前日比)</p>
                {:else}
                    <span class="badge text-bg-danger">
                        {item.sim_ret_pct} %
                    </span>
                    <p style="font-size: 10px">(前日比)</p>
                {/if}
            </p>
        </div>
    </div>
{/each}
</div>



