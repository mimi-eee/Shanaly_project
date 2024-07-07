<script>

    let topic_arr = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
    ];

    let result_arr = [];

    function shuffle(array) {
        var m = array.length, t, i;

        // While there remain elements to shuffle…
        while (m) {

            // Pick a remaining element…
            i = Math.floor(Math.random() * m--);

            // And swap it with the current element.
            t = array[m];
            array[m] = array[i];
            array[i] = t;
        }

        return array;
    }

    function generateArrray() {
        result_arr = shuffle(topic_arr);
    }

</script>


<div class="container mb-3">
    <h1>Topic Recommend</h1>
    <button type="button" class="btn btn-outline-primary btn-lg" on:click={generateArrray}>Shuffle</button>
</div>
<div class="container mb-3">
    {#each result_arr as item}
        <p>{item}</p>
    {/each}
</div>
