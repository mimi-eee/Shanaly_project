<script>
    // Just oridary props
    export let symbol = "";
    export let symbolName = "";
    export let timeframe = "";
    export let data = [];
    
    import { push } from "svelte-spa-router";
    import LineChart from "./LineChart.svelte";
    import TextEditor from "./TextEditor.svelte";
    import Tags from "svelte-tags-input";

    // Variables for Svlete Tags Input
    let tags = [];

    // Variables for Chart.js
    let selected_color = "#000000"; // Black
    let reflect_var = false;

    function reflectColor() {
        reflect_var = !reflect_var;
    }

    // Title & Content Part
    let editor = null; // from Child Compoent: TextEditor.svelte 
    let title = "";

    import fastapi from "../lib/api";

    function submitPost() {

        // Get data
        let title_tmp = title;
        // Get content from TextEditor.svelte Component
        let content_tmp = editor.getSemanticHTML(); // Quill JS

        let tags_str = tags.join("#");  // Add tags

        // Related Data Only
        let tmp_data = [];

        for (let i of data) {
            let tmp_obj = {}
            tmp_obj["time"] = i["time"];
            tmp_obj["close"] = i["close"];
            tmp_data.push(tmp_obj);
        }

        let params = {
            title: title_tmp,
            content: content_tmp,
            report: false,
            tags: tags_str,
            detail: {
                "data": [
                    {
                        "idx": 0,
                        "component_type": "price_line",
                        "symbol": symbol,
                        "symbolName": symbolName,
                        "timeframe": timeframe,
                        "data": tmp_data,
                        "lineColor": selected_color
                    }
                ]
            }   
        }

        // Sending data to the DB in the backend server
        fastapi(
            "post",
            "/api/post/create",
            params,
            (result) => {
                push("/");
            },
            (result) => {
                // Do nothing
            }
        )

    }

</script>

<div class="container mx-0 mb-3 pb-0 px-0">

    <!-- Menus -->
    <div class="container mx-0 my-3 p-0">
        <div>
            <!-- Color Picker -->
            <div class="my-3">
                <input
                class="container-fluid rounded p-0"
                type="color"
                id="color-picker"
                bind:value={selected_color} on:change={reflectColor}>
            </div>
        </div>
    </div>
    
    {#key reflect_var}
        <!-- Line Chart -->
        <LineChart bind:symbol={symbol} bind:symbolName={symbolName} bind:lineColor={selected_color} bind:data={data}/>
    {/key}

    <!-- Title and Content -->
    <div class="mt-2 pt-2">
        <label for="WriteTextAreaTitle" class="form-label">タイトル</label>
        <textarea class="form-control" id="WriteTextAreaTitle" rows="1" bind:value={title}></textarea>
    </div>

    <!-- Quill Editor -->
    <div class="container mt-1 pt-1 pb-2 mb-0 mx-0 px-0">
        <label for="WriteTextAreaContent" class="form-label">コンテンツ</label>
        <TextEditor bind:editor={editor}/>
    </div>

    <!-- Tags Area -->
    <div class="mb-1">
        <label for="input-tags" class="form-label">タグ</label>
        <Tags
        id={"input-tag"}
        bind:tags={tags}
        addKeys={[9,13]}
        placeholder={"..."}
        maxTags=10
        />
    </div>

    <!-- Button for Post -->
    <div class="container mt-1 mb-5 p-0">
        <div class="d-flex justify-content-end">
            <button class="btn btn-outline-primary btn-lg" on:click={submitPost}>投稿</button>
        </div>
    </div>


</div>

