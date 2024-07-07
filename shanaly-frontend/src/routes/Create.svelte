<script>
    import SimplePost from "../components/SimplePost.svelte";
    import Report from "../components/Report.svelte";

    let report_mode = false;

    function switchMode() {
        report_mode = !report_mode;
    }

    
</script>

<div class="container-sm">

    <!-- Mode Switcher -->
    <div class="container my-0 d-flex justify-content-end">
        <div class="form-check form-switch" id="switch">
            <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" on:click={switchMode}>
            <label class="form-check-label" for="flexSwitchCheckDefault">レポート</label>
        </div>
    </div>

    {#if report_mode === false}
        <SimplePost/>
    {:else}
        <Report/>
    {/if}

</div>


<style>

.container-sm {
    max-width: 576px;
}

</style>