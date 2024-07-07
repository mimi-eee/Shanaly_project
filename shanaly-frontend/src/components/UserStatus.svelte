<script>
    export let username;
    import { link } from "svelte-spa-router";

    const currentDate = new Date();
    const formattedDate = `${currentDate.getFullYear()}年${currentDate.getMonth() + 1}月${currentDate.getDate()}日 ${currentDate.getHours()}時 ${currentDate.getMinutes()}分`;


</script>

<!-- Profile Component -->
<div class="container my-2 px-0">
    {#if username.length < 10}
        <h2><a use:link href="/profile/{username}" style="text-decoration:none" class="fw-bolder">{username}</a></h2>
    {:else}
        <h5><a use:link href="/profile/{username}" style="text-decoration:none" class="fw-bolder">{username}</a></h5>
    {/if}
    <p>{formattedDate}</p>
</div>

<!-- First Menu Component -->
<div class="container my-2 px-0">
    <div class="btn-group btn-group-md d-flex gap-1">
        <a use:link href="/create" class="btn btn-primary" aria-current="page" style="font-size: 17px;">
           <i class="bi bi-pencil-fill"></i> 投稿
        </a>
        <a use:link href="/search" class="btn btn-primary" style="font-size: 17px;">
            <i class="bi bi-search"></i> 検索
        </a>
    </div>
</div>