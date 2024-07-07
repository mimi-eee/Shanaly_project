<script>
    import { link, push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import TextEditorReport from "./TextEditorReport.svelte";
    import ImageUpload from "./ImageUpload.svelte";

    import PriceReturnReport from "./PriceReturnReport.svelte"; // User Input
    import ReturnGroupBadge from "./ReturnGroupBadge.svelte"; // Chart

    import PriceCandleReport from "./PriceCandleReport.svelte";  // User Input
    import CandleChartReport from "./CandleChartReport.svelte"; // Chart

    import PriceLineReport from "./PriceLineReport.svelte"; // User Input
    import LineChart from "./LineChart.svelte";

    import FinancialStatementReport from "./FinancialStatementReport.svelte"; // User Input
    import BarChartReport from "./BarChartReport.svelte"; // Chart

    import Tags from "svelte-tags-input";

    import moment from 'moment/min/moment-with-locales';
    moment.locale('ja');

    import { symbol_autocomplete_list } from "../lib/store";

    // [PARAMETER]
    let maxNumberComponents = 10;
    let maxLengthHeader = 50;
    let maxLengthText = 200;
    
    // Error message
    let err_msg = "";

    // Variables for Spinner
    let runningSubmit = false;
    let runningSaveDraft = false;
    let runningGetDraft = false;

    // Variables for Svlete Tags Input
    let tags = [];

    let title = "";
    let content = "";

    let editor_new;
    let editor_modify;
    
    let detail_arr = [];
    let text_value = "";

    let idx_to_be_changed = null;
    let idx_new_item = 0; // This should be zero at first because there is no data in the detail_arr
    let component_type = "選択してください";

    let imgUrl = null;
    let image_filename = "";

    // Variables for Price Return Group
    let symbols_select_arr = [];
    let symbols_return_data = {};

    // Variables for Price Candle Stick Chart
    let symbol;
    let symbolName;
    let period;
    let timeframe;
    let data;
    let indicator_arr = [];

    // Variables for Price Line Chart
    let lineColor = "#000000";

    // Variables for Financial Statement Bar Chart
    let data_financial_statement;
    let target_item_financial_statement= "item";
    let frequency_financial_statement = "q";
    let selected_bar_color = "#000000";

    // Variables for Draft Functions
    let draft_list = [];

    function addComponent() {

        // Reset the text value if exists
        if (text_value === "" || text_value === "<p></p>") {
            text_value = "";
        }

        let tmp_obj = {};

        if (component_type === "header") {
            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "value": text_value,
            }
        }

        if (component_type === "text") {
            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "value": editor_new.getSemanticHTML(),
            }
        }

        if (component_type === "embed") {
            let tmp_text_value;
            try {
                tmp_text_value = text_value.replace(/\bwidth=\d*/gi,'width=100%');
            } catch {
                tmp_text_value = text_value;
            }
            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "value": tmp_text_value
            }
        }

        if (component_type === "image") {
            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "value": imgUrl
            }
        }

        if (component_type === "price_return") {
            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "data": symbols_return_data,
            }
        }

        if (component_type === "price_candle") {

            // Sometimes, a user does not use symbolSearchHelper
            // Then I need fill out the symbol name
            if (symbolName === "" || symbolName === null || symbolName === undefined) {
                for (let item of $symbol_autocomplete_list) {
                    let symbol_item = item["symbol"].toLowerCase();
                    if (symbol_item.includes(symbol.toLowerCase())) {
                        symbolName = item["name"];
                    }
                }
            }

            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "symbol": symbol,
                "symbolName": symbolName,
                "timeframe": timeframe,
                "data": data,
                "indicator": indicator_arr,
            }
        }

        if (component_type === "price_line") {

            // Sometimes, a user does not use symbolSearchHelper
            // Then I need fill out the symbol name
            if (symbolName === "" || symbolName === null || symbolName === undefined) {
                for (let item of $symbol_autocomplete_list) {
                    let symbol_item = item["symbol"].toLowerCase();
                    if (symbol_item.includes(symbol.toLowerCase())) {
                        symbolName = item["name"];
                    }
                }
            }
            
            // Other process
            let tmp_arr = [];

            for (let i of data) {
                let tmp_obj = {}
                tmp_obj["time"] = i["time"];
                tmp_obj["close"] = i["close"];
                tmp_arr.push(tmp_obj);
            }

            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "symbol": symbol,
                "symbolName": symbolName,
                "data": tmp_arr,
                "lineColor": lineColor,
            }
        }

        if (component_type === "financial_statement") {

            // Sometimes, a user does not use symbolSearchHelper
            // Then I need fill out the symbol name
            if (symbolName === "" || symbolName === null || symbolName === undefined) {
                for (let item of $symbol_autocomplete_list) {
                    let symbol_item = item["symbol"].toLowerCase();
                    if (symbol_item.includes(symbol.toLowerCase())) {
                        symbolName = item["name"];
                    }
                }
            }

            let tmp_fs_arr = [];

            for (let i of data_financial_statement) {
                let tmp_obj = {}
                tmp_obj["asOfDate"] = i["asOfDate"];
                tmp_obj[target_item_financial_statement] = i[target_item_financial_statement];
                tmp_fs_arr.push(tmp_obj);
            }

            tmp_obj = {
                "idx": idx_new_item,
                "component_type": component_type,
                "symbol": symbol,
                "symbolName": symbolName,
                "frequency": frequency_financial_statement,
                "data": tmp_fs_arr,
                "category": target_item_financial_statement,
                "barColor": selected_bar_color,
            }
        }

        detail_arr.push(tmp_obj);
        detail_arr = detail_arr;

        idx_new_item += 1;

        // Reset the text value: make it empty
        text_value = "";

        // Reset the Quill Editor's value: make it empty
        try {
            editor_new.clipboard.dangerouslyPasteHTML("<p></p>");
        } catch {
            // Do nothing;
        }
        
        // Reset the imgUrl and image_filename; bind prop variables in ImageUpload.svelte (Chile Component)
        if (imgUrl !== null || image_filename !== "") {
            imgUrl = null;
            image_filename = "";
        }

        // Reset the variables for Price Candle Stick Chart
        symbol = "";
        symbolName = "";
        data = [];
        indicator_arr = [];

        // Reset the variables for Price Line CHart
        lineColor = "#000000"

        // Reset the variables for the Price Return Badges
        symbols_select_arr = [];
        symbols_return_data = {};

        // Reset the variables for the Financial Statement Bar Chart
        data_financial_statement = [];
        target_item_financial_statement= "item";
        frequency_financial_statement = "q";
        selected_bar_color = "#000000";
    }

    function moveComponent(idx, direction) {
        
        // Set temporary array and get the last number of the order
        let tmp_arr = [];
        let last_num = detail_arr[detail_arr.length - 1]["idx"];

        // Modify the order number
        if (direction === "up" && idx !== 0) {
            detail_arr[idx]["idx"] = idx - 1;
            detail_arr[idx - 1]["idx"] = detail_arr[idx]["idx"] + 1;
        } else if (direction === "down" && idx !== last_num) {
            detail_arr[idx]["idx"] = idx + 1;
            detail_arr[idx + 1]["idx"] = detail_arr[idx]["idx"] - 1;
        } else {
            return;
        }

        // Sorting the component by the newly defined order numbers
        for (let i = 0; i < detail_arr.length; i++) {
            for (const comp of detail_arr) {
                if (comp["idx"] === i) {
                    tmp_arr.push(comp);
                }
            }
        }
        // Assign the sorted and new array to the detail array
        detail_arr = tmp_arr;
    }

    // Because of Issue that Quill JS cannot parse the text value to the editor_modify
    // I made this function into an async function
    function getTargetIdxComponent(idx) {
        // Get the specific item by using idx, looping the detail_arr
        for (let i = 0; i < detail_arr.length; i++) {
            for (const comp of detail_arr) {
                if (comp["idx"] === idx) {
                    if (comp["component_type"] === "text") {
                        // [WARNING] Sometimes, the next line does not work because Chrome misses the range(?) of Quill JS Editor
                        // So, I added a sleep function for a bit of delay; give Chrome enought time delay
                        const sleep = (ms = 0) => new Promise(resolve => setTimeout(resolve, ms));
                        async function delayedGreeting() {
                            await sleep(750);
                            // Assign component value to editor's value; necessary for loading & modifying the value
                            editor_modify.clipboard.dangerouslyPasteHTML(comp["value"]);
                        };
                        delayedGreeting();
                        // Set the current selected component typew
                        component_type = comp["component_type"];
                    }
                    if (comp["component_type"] === "header") {
                        // Assign text_value to text_value; necessary for loading & modifying the value 
                        text_value = comp["value"];
                        // Set the current selected component typew
                        component_type = comp["component_type"];
                    }
                }
            }
        }
        idx_to_be_changed = idx;
    }

    function modifyComponent() {

        // Get the detail_arr
        let tmp_arr = [];
        tmp_arr = detail_arr;

        // Get the specific item by using idx, looping the detail_arr
        for (let i = 0; i < tmp_arr.length; i++) {
            for (const comp of tmp_arr) {
                if (comp["idx"] === idx_to_be_changed) {

                    if (comp["component_type"] === "embed") {
                        comp["value"] = text_value.replace(/\bwidth=\d*/gi,'width=100%');
                    } 
                    if (comp["component_type"] === "header") {
                        comp["value"] = text_value;
                    } 
                    if (comp["component_type"] === "text") {
                        comp["value"] = editor_modify.getSemanticHTML();
                    }
                }
            }
        }

        // Update the global detail arr
        detail_arr = tmp_arr;

        // Reset the text value: make it empty
        text_value = "";

        // Close the modal
        // You need to set the proper id in the modal button!
        document.querySelector("[id='modify-component-modal-close']").click();

    }

    function deleteComponent() {
        
        // Get the detail_arr
        let tmp_arr = [];
        tmp_arr = detail_arr;

        // Delete an item on the idx number in the detail_arr
        delete tmp_arr[idx_to_be_changed]

        // Remove empty object in the array
        tmp_arr = tmp_arr.filter(Object => Object);

        // Reassign correct idx numbers in the detail_arr
        for (let i = 0; i < tmp_arr.length; i++) {
            tmp_arr[i]["idx"] = i;
        }

        // Update the global detail_arr
        detail_arr = tmp_arr;

        // Update the idx of a new item in detail_arr
        idx_new_item = tmp_arr.length;

        // Reset the text value: make it empty
        text_value = "";

        // Close the modal
        // You need to set the proper id in the modal button!
        document.querySelector("[id='delete-component-modal-close']").click();

    }

    function submitPost() {

        let title_tmp;
        let content_tmp;
        let tmp_arr = null;
        let params = {};

        title_tmp = title;
        content_tmp = content;
        tmp_arr = detail_arr;

        let tags_str = tags.join("#"); // Add tags

        // Data Validation
        for (let i of tmp_arr) {
            // Regex for HTML tags
            let regex = /(<([^>]+)>)/ig;
            // e.g) {idx: 0, component_type: 'header', value: 'HEAD'}
            if (i["component_type"] === "header" && i["value"].length >= maxLengthHeader) {
                err_msg = `${i["idx"]+1}番目: ` + `ヘッダーの長さは${maxLengthHeader}文字が最大です。`; 
                return;
            }
            if (i["component_type"] === "text" && i["value"].replace(regex, "").length >= maxLengthText) {
                err_msg = `${i["idx"]+1}番目: ` + `テキストの長さは${maxLengthText}文字が最大です。`;
                return;
            }
        }
        if (title_tmp === "" || content_tmp === "") {
            err_msg = "タイトルとコンテンツに空白はできません。"; 
            return;
        }
        if (tmp_arr.length === 0) {
            err_msg = "カテゴリーを含めて投稿してください。"; 
            return;
        }
        if (tmp_arr.length >= maxNumberComponents) {
            err_msg = `カテゴリーの使用は${maxNumberComponents}個が最大です。`; 
            return;
        }

        // Check whether the detail exist or not
        params = {
            title: title_tmp,
            content: content_tmp,
            report: true,
            tags: tags_str,
            detail: {"data": tmp_arr}
        }

        // Spinner and Progress
        runningSubmit = true;
        // Disable some buttons while submitting post
        document.getElementById("submitButton").disabled = true;
        document.getElementById("saveButton").disabled = true;
        document.getElementById("continueButton").disabled = true;
        document.getElementById("backButton").disabled = true;

        // Send data to the backend api server
        fastapi(
            "post",
            "/api/post/create",
            params,
            (result) => {
                // Reset error message if successful
                err_msg = "";

                // Spinner and Progress
                runningSubmit = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                // Push the user to the home page
                push("/");
            },
            (result) => {

                // Display error message [1]
                if (typeof result["detail"] === 'string') {
                    err_msg = result["detail"];
                    return;
                }

                // Display error message [2]
                for (let i of result["detail"]) {
                    if (i["type"] === "string_too_long") {
                        let length_title = title.length;
                        let length_text = content.length;
                        err_msg = `タイトルは50文字、コンテンツは140文字が最大です。現在: タイトル=${length_title}, コンテンツ=${length_text}`;
                        break
                    }
                }

                // Spinner and Progress
                runningSubmit = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

            }
        )  
    }

    // Pause any video iframe
    function stopIframeVideoAll() {
	    var videos = document.querySelectorAll('iframe, video');
        Array.prototype.forEach.call(videos, function (video) {
            if (video.tagName.toLowerCase() === 'video') {
                video.pause();
            } else {
                var src = video.src;
                video.src = src;
            }
        })
    }

    //////// Draft Save and Load Functions /////////
    function submitDraft() {

        // Spinner and Progress
        runningSaveDraft = true;
        // Disable some buttons while submitting post
        document.getElementById("submitButton").disabled = true;
        document.getElementById("saveButton").disabled = true;
        document.getElementById("continueButton").disabled = true;
        document.getElementById("backButton").disabled = true;

        let params = {
            title: title,
            content: content,
            tags: {"tags": tags},
            data: {"data": detail_arr},
        }

        fastapi(
            "post",
            "/api/draft/save",
            params,
            (result) => {
                err_msg = "保存しました。";

                // Spinner and Progress
                runningSaveDraft = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                return;
            },
            (result) => {

                // Spinner and Progress
                runningSaveDraft = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                if (result["detail"] === "Over 3 drafts are not allowed") {
                    err_msg = "下書きは3つまで保存できます。"
                    return;
                }
            }
        )
    }
    function getDraftList() {

        // Spinner and Progress
        runningGetDraft = true;
        // Disable some buttons while submitting post
        document.getElementById("submitButton").disabled = true;
        document.getElementById("saveButton").disabled = true;
        document.getElementById("continueButton").disabled = true;
        document.getElementById("backButton").disabled = true;
        
        fastapi(
            "get",
            "/api/draft/list",
            {},
            (result) => {
                draft_list = result;

                // Spinner and Progress
                runningGetDraft = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                return;
            },
            (result) => {

                // Spinner and Progress
                runningGetDraft = false;
                document.getElementById("submitButton").disabled = false;
                document.getElementById("saveButton").disabled = false;
                document.getElementById("continueButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                return;
            }
        )
    }
    function deleteDraft(draft_id) {
        
        fastapi(
            "delete",
            `/api/draft/delete/${draft_id}`,
            {},
            (result) => {
                // Update the draft_list at Frontend
                let tmp_arr = [];
                for (let item of draft_list) {
                    if (item["id"] !== draft_id){
                        tmp_arr.push(item);
                    }
                }
                draft_list = tmp_arr;
                return;
            },
            (result) => {
                return;
            }

        )
    }
    function loadDraft(draft_id) {

        for (let item of draft_list) {
            if (item["id"] === draft_id) {
                // Assign the selected values to the input forms
                title = item["title"];
                content = item["content"];
                tags = item["tags"]["tags"];
                detail_arr = item["data"]["data"];
                // Close the modal
                document.getElementById("load-draft-modal-close").click();
                return;
            }
        }
    }

</script>

<div class="container-sm">

    <!-- Page Header -->
    <div class="container py-3 px-0">
        <h1><i class="bi bi-clipboard-fill"></i> レポート</h1>
    </div>

    <!-- Input Form for Title and Content -->
    <div class="mb-3">
        <label for="input-title" class="form-label">タイトル</label>
        <textarea class="form-control" id="input-title" rows="1" bind:value={title}></textarea>
    </div>
    <div class="mb-3">
        <label for="input-content" class="form-label">コンテンツ</label>
        <textarea class="form-control" id="input-content" rows="5" bind:value={content}></textarea>
    </div>
    
    <!-- Tags Area -->
    <div class="mb-3">
        <label for="input-tags" class="form-label">タグ</label>
        <Tags
        id={"input-tag-report"}
        bind:tags={tags}
        addKeys={[9,13]}
        placeholder={"..."}
        maxTags=10
        />
    </div>
    


    <!-- Newly Created Components -->
    <!-- will be display here -->

    <!-- The below key syntax refresh charts components as well -->
    {#key detail_arr}

    {#each detail_arr as item}

        {#if item.component_type === "header"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#modifyComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-pencil-fill"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">
                    <h3 style="word-wrap: break-word;">{item.value}</h3> 
                </div>
            </div>
        
        {:else if item.component_type === "text"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#modifyComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-pencil-fill"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">
                    <!-- <p style="word-wrap: break-word;">{item.value}</p> -->
                    <p style="word-wrap: break-word;">{@html item.value}</p>
                </div>
            </div>

        {:else if item.component_type === "embed"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <!-- <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#modifyComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-pencil-fill"></i></button> -->
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">
                    <!-- Adjust width and height of iframe into 100% -->
                    {@html item.value}
                </div>
            </div>
        
        {:else if item.component_type === "image"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <!-- <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#modifyComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-pencil-fill"></i></button> -->
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">

                    {#if imgUrl !== null || imgUrl !== undefined} 
                        <!-- Image Fluid is important! -->
                        <img src={item.value} class="img-fluid" alt="img_{item.idx}">
                    {/if}

                </div>
            </div>
        
        {:else if item.component_type === "price_return"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">

                    <ReturnGroupBadge data={item.data}/> 

                </div>
            </div>

        {:else if item.component_type === "price_candle"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3" style="height: 500px">

                    <CandleChartReport symbol={item.symbol} symbolName={item.symbolName} timeframe={item.timeframe} data={item.data} indicator_arr={item.indicator} chart_id={item.idx}/> 

                </div>
            </div>

        {:else if item.component_type === "price_line"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">

                    <LineChart symbol={item.symbol} symbolName={item.symbolName} data={item.data} lineColor={item.lineColor}/>

                </div>
            </div>

        {:else if item.component_type === "financial_statement"}
            <div class="container border my-2">
                <div class="container my-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "up")}><i class="bi bi-arrow-up"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" on:click={moveComponent(item.idx, "down")}><i class="bi bi-arrow-down"></i></button>
                    <button type="button" class="btn btn-outline-primary me-1" data-bs-toggle="modal" data-bs-target="#deleteConfirmComponentModal" on:click={getTargetIdxComponent(item.idx)}><i class="bi bi-trash-fill"></i></button>
                </div>
                <div class="container my-3">

                    <BarChartReport symbol={item.symbol} symbolName={item.symbolName} data={item.data} category={item.category} barColor={item.barColor}/> 

                </div>
            </div>

        {/if}
    
    {/each}

    {/key}


    <!-- Add Component Button -->
    <div class="d-flex justify-content-center my-3">
        <button class="btn btn-outline-primary add-comp-btn" data-bs-toggle="modal" data-bs-target="#addComponentModal">+</button>
    </div>

    <!-- Error Message -->
    {#if err_msg !== ""}
        <div class="alert alert-primary" role="alert">
            {err_msg}
        </div>
    {/if}
    
    <!-- Submit / Save / Go Back Buttons -->
    <div class="d-flex justify-content-end my-5">

        <button id="submitButton" class="btn btn-outline-primary btn-lg mx-1" on:click={submitPost} on:click={stopIframeVideoAll}>
            <!-- Spinner -->
            {#if runningSubmit === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            作成
        </button>
        <button id="saveButton" class="btn btn-outline-primary btn-lg mx-1" on:click={submitDraft}>
            <!-- Spinner -->
            {#if runningSaveDraft === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            保存
        </button>
        <button id="continueButton" class="btn btn-outline-primary btn-lg mx-1" data-bs-target="#loadDraftModal" data-bs-toggle="modal" on:click={getDraftList}>
            続き
        </button>
        <button id="backButton" class="btn btn-outline-primary btn-lg ms-1" on:click={stopIframeVideoAll} on:click={()=>{push("/")}}>戻る</button>
    </div>







    <!-- Modal for Adding Component -->
    <div class="modal fade" id="addComponentModal" tabindex="-1" aria-labelledby="addComponentModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="addComponentModalLabel">カテゴリー追加</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">

                <!-- Component Menus -->
                <select class="form-select form-select-lg mb-3" aria-label="Large select example" bind:value={component_type}>
                    <option selected>選択してください</option>
                    <option value="header">ヘッダー</option>
                    <option value="text">テキスト</option>
                    <option value="image">画像</option>
                    <option value="embed">埋め込み</option>
                    <option value="price_return">銘柄バッジ</option>
                    <option value="price_candle">ローソクチャート</option>
                    <option value="price_line">ラインチャート</option>
                    <option value="financial_statement">財務情報</option>
                    
                </select>

                <!-- Inputs for components will be here according to the value in the component select options -->
                {#if component_type === "header"}
                    <div class="mb-3">
                        <textarea class="form-control" id="textTextArea" rows="5" bind:value={text_value}></textarea>
                    </div>
                
                {:else if component_type === "text"}
                    <div class="mb-3">
                        <TextEditorReport bind:editor={editor_new} editorName={"Create"}/>
                    </div>

                {:else if component_type === "embed"}
                    <div class="mb-3">
                        <textarea class="form-control" id="textTextArea" rows="5" bind:value={text_value}></textarea>
                    </div>

                {:else if component_type === "image"}

                    <ImageUpload bind:imgUrl={imgUrl} bind:image_filename={image_filename} limitSizeByte={500000}/>

                {:else if component_type === "price_return"}
                    
                    <PriceReturnReport bind:data={symbols_return_data} bind:symbols_arr={symbols_select_arr}/>

                {:else if component_type === "price_candle"}
                    
                    <PriceCandleReport 
                    bind:symbol={symbol} 
                    bind:period={period} 
                    bind:timeframe={timeframe} 
                    bind:data={data} 
                    bind:indicator_arr={indicator_arr}/>
                
                {:else if component_type === "price_line"}
                    
                    <PriceLineReport 
                    bind:symbol={symbol} 
                    bind:symbolName={symbolName} 
                    bind:period={period} 
                    bind:data={data} 
                    bind:lineColor={lineColor}/>

                {:else if component_type === "financial_statement"}
                    
                    <FinancialStatementReport
                    bind:symbol={symbol}
                    bind:symbolName={symbolName}
                    bind:frequency={frequency_financial_statement}
                    bind:data={data_financial_statement}
                    bind:target_item={target_item_financial_statement}
                    bind:selected_color={selected_bar_color}/>

                {:else}
                    <!-- Do nothing -->
                {/if}

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-primary" on:click={addComponent}>追加</button>
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
            </div>
        </div>
        </div>
    </div>

    <!-- Modify Component Modal -->
    <div class="modal fade" id="modifyComponentModal" tabindex="-1" aria-labelledby="modifyComponentModalLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="modifyComponentModalLabel">カテゴリー修正</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="modify-component-modal-close"></button>
            </div>
            <div class="modal-body">
                <!-- Inputs for components will be here according to the value in the component select options -->
                {#if component_type === "header"}
                    <div class="mb-3">
                        <label for="headerTextArea" class="form-label">ヘッダー</label>
                        <textarea class="form-control" id="headerTextArea" rows="5" bind:value={text_value}></textarea>
                    </div>
                {/if}

                {#if component_type === "text"}
                    <div class="mb-3">
                        <label for="textTextArea" class="form-label">テキスト</label>
                        <TextEditorReport bind:editor={editor_modify} editorName={"Edit"}/>
                    </div>
                {/if}
                
                {#if component_type === "embed"}
                    <div class="mb-3">
                        <label for="embedTextArea" class="form-label">埋め込み</label>
                        <textarea class="form-control" id="embedTextArea" rows="5" bind:value={text_value}></textarea>
                    </div>
                {/if}

            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-primary" on:click={modifyComponent}>修正</button>
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
            </div>
        </div>
        </div>
    </div>

    <!-- Delete Confirmation Component Modal -->
    <div class="modal fade" id="deleteConfirmComponentModal" tabindex="-1" aria-labelledby="deleteConfirmComponentModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="deleteConfirmComponentModalLabel">カテゴリー削除</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="delete-component-modal-close"></button>
            </div>
            <div class="modal-body">
                このカテゴリーを削除しますか？削除すると戻せないのでご注意ください。
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-primary" on:click={deleteComponent} on:click={stopIframeVideoAll}>削除</button>
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
            </div>
        </div>
        </div>
    </div>

    <!-- Load Saved Draft Report Modal -->
    <div class="modal fade" id="loadDraftModal" tabindex="-1" aria-labelledby="loadDraftModalLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="loadDraftModalLabel">下書きリスト</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="load-draft-modal-close"></button>
            </div>
            <div class="modal-body">
                <div class="card">
                    <div class="card-body">

                        <!-- Spinner -->
                        {#if runningGetDraft === true}
                            <span class="spinner-border" role="status" aria-hidden="true"></span>
                        {/if}

                        {#if draft_list.length > 0 && runningGetDraft === false}
                            {#each draft_list as item}
                                <!-- Each Draft Cards -->
                                <div>
                                    <!-- Draft Title -->
                                    <button 
                                    type="button" 
                                    class="btn btn-link m-0 p-0" 
                                    style="text-decoration:none"
                                    on:click={loadDraft(item.id)}>
                                        <h5>{item.title}</h5>
                                    </button>
                                    <!-- Draft Content -->
                                    <p class="card-text">{item.content}</p>
                                </div>
                                <!-- Draft ID -->
                                <div class="d-flex flex-row justify-content-end" style="font-size: 13px">
                                    <p>下書き番号 = {item.id}</p>
                                </div>
                                <!-- Drafe Created At Timestamp -->
                                <div class="d-flex flex-row justify-content-end" style="font-size: 13px">
                                    {moment(item.created_at).format("YYYY年MM月DD日 A hh:mm")}
                                </div>
                                <div class="d-flex flex-row justify-content-end">
                                    <!-- Delete Draft Button -->
                                    <div>
                                        <button 
                                        type="button" 
                                        class="btn btn-link m-0 p-0" 
                                        style="text-decoration:none"
                                        on:click={deleteDraft(item.id)}>
                                            <i class="bi bi-trash-fill"></i>
                                        </button>
                                    </div>
                                </div>
                            {/each}
                        {/if}

                        {#if draft_list.length === 0 && runningGetDraft === false}
                            <!-- No Draft -->
                            <p class="card-text border-0">保存した下書きがありません。</p>
                        {/if}
                        
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-primary" data-bs-dismiss="modal">閉じる</button>
            </div>
        </div>
        </div>
    </div>


</div>


<style>

.container-sm {
    max-width: 576px;
}

.add-comp-btn {
    height: 80px;
    line-height: 80px;  
    width: 80px;  
    font-size: 2em;
    font-weight: bold;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

</style>