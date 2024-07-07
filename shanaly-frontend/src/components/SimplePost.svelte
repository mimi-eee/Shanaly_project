<script>
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import TextEditor from "../components/TextEditor.svelte";
    import ImageUpload from "./ImageUpload.svelte";
    import Tags from "svelte-tags-input";
    
    // Error message
    let err_msg = "";

    // Variables for Spinner
    let running = false;

    // Quill JS
    let editor = null;
    let title = "";
    let image_clicked = false;
    let embed_clicked = false;

    // Variables for Svlete Tags Input
    let tags = [];

    // Variables for Image
    let image_filename = "";
    let imgUrl = null;

    // Variables and others for Embeded
    let embed_value = "";
    $: processEmbedValue(embed_value);

    function disableEmbeded() {
        image_clicked = true;
        embed_clicked = false;
        embed_value == "";
    }

    function disableImage() {
        image_clicked = false;
        embed_clicked = true;
        imgUrl = null;
    }

    function submitPost() {

        let title_tmp = null;
        let content_tmp = null;
        let params = {};

        title_tmp = title;
        content_tmp = editor.getSemanticHTML(); // Quill JS

        let tags_str = tags.join("#"); // Add tags

        // Data Validation for content_tmp: Quill JS 
        if (title_tmp === "" || content_tmp === "<p></p>") {
            err_msg = "タイトルとコンテンツに空白はできません";
            return;
        }

        let title_tmp_length = title_tmp.length;
        let content_tmp_length = content_tmp.replace(/(<([^>]+)>)/gi, '').length;

        if (title_tmp_length >= 51 || content_tmp_length >= 151) {
            err_msg = `タイトルは50文字、コンテンツは150文字が最大です。現在: タイトル=${title_tmp_length}, コンテンツ=${content_tmp_length}`;
            return;
        }

        if (embed_value == "" && imgUrl === null) {
            params = {
                title: title_tmp,
                content: content_tmp,
                report: false,
                tags: tags_str,
                detail: null
            }
        } else {
            if (embed_value != "") {
                params = {
                    title: title_tmp,
                    content: content_tmp,
                    report: false,
                    tags: tags_str,
                    detail: {
                        "data": [
                            {
                                "idx": 0,
                                "component_type": "embed",
                                "value": embed_value,
                            }
                        ]
                    }
                }
            }
            if (imgUrl !== null) {
                params = {
                    title: title_tmp,
                    content: content_tmp,
                    report: false,
                    tags: tags_str,
                    detail: {
                        "data": [
                            {
                                "idx": 0,
                                "component_type": "image",
                                "value": imgUrl,
                            }
                        ]
                    }
                }
            }     
        }

        // Spinner and Progress
        running = true;
        // Disable some buttons while submitting post
        document.getElementById("submitButton").disabled = true;
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
                running = false;
                // Disable some buttons while submitting post
                document.getElementById("submitButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                push("/");
            },
            (result) => {

                // Spinner and Progress
                running = false;
                // Disable some buttons while submitting post
                document.getElementById("submitButton").disabled = false;
                document.getElementById("backButton").disabled = false;

                // Display error message [1]
                if (typeof result["detail"] === 'string') {
                    err_msg = result["detail"];
                    return;
                }

                // Display error message [2]
                for (let i of result["detail"]) {
                    if (i["type"] === "string_too_long") {
                        let length_title = title.length;
                        let length_text = editor.getSemanticHTML().replace(/(<([^>]+)>)/gi, '').length;
                        err_msg = `タイトルは50文字、コンテンツは150文字が最大です。現在: タイトル=${length_title}, コンテンツ=${length_text}`;
                        break
                    }
                }
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

    // Process embeded iframe value
    function processEmbedValue() {
        let tmp_text_value;
        try {
            tmp_text_value = (
                embed_value
                .replace(/\bwidth=\d*/gi,'width=100% ')
            );
        } catch {
            tmp_text_value = embed_value;
        }
        embed_value = tmp_text_value
    }

</script>

<div class="container-sm">
    <!-- Page Header -->
    <div class="container py-3 px-0">
        <h1><i class="bi bi-pencil-fill"></i> 投稿</h1>
    </div>

    <!-- Error Message -->
    {#if err_msg !== ""}
        <div class="alert alert-primary" role="alert">
            {err_msg}
        </div>
    {/if}
    
    <!-- Input Form for Title and Content -->
    <div class="mb-3">
        <label for="WriteTextAreaTitle" class="form-label">タイトル</label>
        <textarea class="form-control" id="WriteTextAreaTitle" rows="1" bind:value={title}></textarea>
    </div>
    <div class="mb-3">
        <label for="WriteTextAreaContent" class="form-label" id="WriteTextAreaContent">コンテンツ</label>
        <!-- Quill JS Editor -->
        <TextEditor bind:editor={editor}/>
    </div>

    <!-- Tags Area -->
    <div class="mb-3">
        <label for="input-tags" class="form-label">タグ</label>
        <Tags
        id={"input-tag-simple-post"}
        bind:tags={tags}
        addKeys={[9,13]}
        placeholder={"..."}
        maxTags=10
        />
    </div>
    
    
    <!-- Image -->
    {#if imgUrl !== null} 
        <div class="mb-3">
            <img src={imgUrl} class="img-fluid" alt="">
        </div>
    {/if}
    
    <!-- Embeded -->
    {#if embed_value !== ""} 
    <div class="mb-3">
        {@html embed_value}
    </div>
    {/if}

    <!-- Attachments -->
    <ul class="nav nav-tabs" id="myTab" role="tablist">
        <li class="nav-item" role="presentation">
          <button
            class="nav-link" id="image-tab"
            data-bs-toggle="tab" data-bs-target="#image-tab-pane"
            type="button" role="tab" aria-controls="home-tab-pane"
            aria-selected="false" on:click={disableEmbeded}>画像</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link" id="embed-tab"
                data-bs-toggle="tab" data-bs-target="#embed-tab-pane"
                type="button" role="tab" aria-controls="popular-tab-pane"
                aria-selected="true" on:click={disableImage}>埋め込み</button>
        </li>      
    </ul>
    <div class="tab-content" id="myTabContent">
        <!-- Image Tab -->
        <div class="tab-pane fade" id="image-tab-pane" role="tabpanel" aria-labelledby="image-tab" tabindex="0">
            <!-- Uploaded Image -->
            <div class="mb-3">
                <div class="d-flex my-2">
                    <ImageUpload bind:imgUrl={imgUrl} bind:image_filename={image_filename} limitSizeByte={500000}/>
                </div>
                
            </div>
        </div>
        <!-- Embede Tab -->
        <div class="tab-pane fade" id="embed-tab-pane" role="tabpanel" aria-labelledby="embed-tab" tabindex="0">
            <!-- Embed -->
            <div class="mb-3">
                <div class="my-2"></div>
                <textarea class="form-control" id="textTextArea" rows="3" bind:value={embed_value}></textarea>
            </div>
        </div>
    </div>

    <!-- Submit / Save / Go Back Buttons -->
    <div class="d-flex justify-content-end my-1">
        <!-- Submit Button -->
        <button id="submitButton" class="btn btn-outline-primary btn-lg mx-1" on:click={submitPost} on:click={stopIframeVideoAll}>
            <!-- Spinner -->
            {#if running === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            投稿
        </button>
        <!-- Go Back Button -->
        <button id="backButton" class="btn btn-outline-primary btn-lg ms-1" on:click={stopIframeVideoAll} on:click={()=>{push("/")}}>戻る</button>
    </div>

</div>

<style>

</style>