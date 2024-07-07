<script>

import { onMount } from 'svelte';
import 'quill/dist/quill.snow.css'; // For using Quill JS
import MagicUrl from 'quill-magic-url'; // For using Quill JS

// This editor variable will be used in the parent component
// That is the reason why it has export let syntax!
export let editor;  // For using Quill JS
export let editorName;

// Quill JS for Text Editor
onMount(async () => {
    // Tool bar option for Quill JS
    const toolbarOptions = ['link'];

        // For using Quill JS
    const { default: Quill } = await import('quill');
    // the true in the below code will suppuress warning messages
    Quill.register('modules/magicUrl', MagicUrl, true);
    const quill = new Quill(`#editor${editorName}`, {
        theme: 'snow',
        placeholder: '...',
        modules: {
            toolbar: toolbarOptions,
            magicUrl: {
                // Regex used to check URLs during typing
                urlRegularExpression: /(https?:\/\/[\S]+)|(www.[\S]+)|(tel:[\S]+)/g,
                // Regex used to check URLs on paste
                globalRegularExpression: /(https?:\/\/|www\.|tel:)[\S]+/g,
            }
        },
        formats: ["link"]
    });
    editor = quill;
});

</script>

<div class="container editor" id="editor{editorName}"></div>

<style>
/* Quill JS; change the font size into Bootstrap's basic font size */
.editor {
    font-size: 16px;
}
</style>