<script>
    import SearchSymbol from "../components/SearchSymbol.svelte";
    import SearchGeneral from "../components/SearchGeneral.svelte";

    let symbol_mode = true

    function switchMode() {
        symbol_mode = !symbol_mode;
    }

</script>

<div class="container-sm">

    <!-- Mode Switcher -->
    <div class="container my-0 d-flex justify-content-end">
        <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" on:click={switchMode}>
            <label class="form-check-label" for="flexSwitchCheckDefault">一般検索</label>
        </div>
    </div>

    {#if symbol_mode === true}
        <SearchSymbol/>
    {:else}
        <SearchGeneral/>
    {/if}


</div>


<style>

.container-sm {
    max-width: 576px;
}
    
</style>