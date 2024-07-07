<script>
    // https://www.youtube.com/watch?v=Uo9Jme8IwlM
    export let imgUrl = null;
    export let image_filename = "";
    export let limitSizeByte = 500000;

    import { onMount } from "svelte";

    let previous_imgUrl;
    let err_trigger = false;

    // [PARAMETER] [DEV]
    // const maxWidth = 100;

    // [DEV]
    // function resizeImg(imgElement, oriWidth, oriHeight) {

    //     if (oriWidth > maxWidth) {
    //         let ratio = oriWidth / oriHeight;
    //         let newWidth = maxWidth * ratio; // maxWidth is a Parameter!
    //         let newHeight = newWidth / ratio;

    //         const canvas = document.createElement('canvas');
    //         canvas.width = newWidth;
    //         canvas.height = newHeight;

    //         const ctx = canvas.getContext('2d');
    //         ctx.drawImage(imgElement, 0, 0, newWidth, newHeight);
    //     } else {
    //         const ctx = canvas.getContext('2d');
    //         ctx.drawImage(imgElement, 0, 0, oriWidth, oriHeight);
    //     }
        
    //     return canvas.toDataURL('image/jpeg')
    // }

    onMount(()=>{
        const selectImage = document.querySelector('.select-image');
        const inputFile = document.querySelector('#file');
        const imgArea = document.querySelector('.img-area');

        selectImage.addEventListener('click', function () {
            inputFile.click();
            err_trigger = false;
        })

        inputFile.addEventListener('change', function () {
            let image = this.files[0]
            previous_imgUrl = image.name;
            if (image.size < limitSizeByte) {
                const reader = new FileReader();
                reader.onload = (event)=> {
                    const allImg = imgArea.querySelectorAll('img');
                    allImg.forEach(item => item.remove());
                    // const imgUrl = reader.result; // Original Code
                    imgUrl = reader.result;
                    const img = document.createElement('img');

                    // [DEV] Resize the image
                    // img.onload = function () {
                    //     let oriWidth = this.width;
                    //     let oriHeight = this.height;
                    //     imgUrl = resizeImg(img, oriWidth, oriHeight);
                    // }

                    img.src = imgUrl;
                    inputFile.value = ""; // Reset the value in the input form
                    // imgArea.appendChild(img);
                    // imgArea.classList.add('active');
                    // imgArea.dataset.img = image.name;
                }
                reader.readAsDataURL(image);
            } else {
                document.getElementById("file").value = "";
                err_trigger = true;
            }
        })
    })

    function getFileName() {
        let fileform=document.getElementById("file");
        fileform.addEventListener("change", (e) => {
            if (window.File) {
                var inputfile = fileform.files[0];
                try {
                    image_filename = inputfile.name;
                } catch {
                    image_filename = "";
                }
                
            }
        });
    }

    function clearInput() {
        document.getElementById("file").value = "";
        image_filename = "";
        imgUrl = null;
    }



</script>

<div class="container">
    <input type="file" id="file" accept="image/*" hidden>
    <button class="select-image btn btn-outline-primary" on:click={getFileName}>ファイル選択</button>
    <div class="img-area" data-img="">
        <i class='bx bxs-cloud-upload icon'></i>
        <p style="font-size: 12px;">ファイルサイズは<span>{limitSizeByte/1000}KB</span>以下</p>
    </div>
    {#if image_filename !== "" && imgUrl !== null}
        <div class="d-flex">
            <p class="fw-bold mx-2">{image_filename}</p>
            <button class="btn btn-outline-primary" on:click={clearInput}><i class="bi bi-trash-fill"></i></button>
        </div>
    {/if}
    {#if err_trigger === true}
        <div class="alert alert-primary" role="alert">
            Over {limitSizeByte/1000}KB
        </div>
    {/if}
</div>