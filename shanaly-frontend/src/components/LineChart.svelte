<script>
    export let symbol = "";
    export let symbolName = "";
    export let data = [];
    export let lineColor;

    import { onMount } from "svelte";
    import Chart from 'chart.js/auto';

    let x_data = [];
    let y_data = [];
    let ctx;
    let canvas;

    function Unix_timestamp(t){
        var date = new Date(t*1000);
        var year = date.getFullYear();
        var month = "0" + (date.getMonth()+1);
        var day = "0" + date.getDate();
        // var hour = "0" + date.getHours();
        // var minute = "0" + date.getMinutes();
        // var second = "0" + date.getSeconds();
        return year + "-" + month.slice(-2) + "-" + day.slice(-2);
    }

    onMount(() => {

        for (let i of data) {
            let datetime = Unix_timestamp(i["time"]);
            x_data.push(datetime);
            y_data.push(i["close"]);     
        }

        ctx = canvas.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: x_data,
                datasets: [
                    {
                        label: symbol,
                        data: y_data,
                        borderWidth: 2,
                        backgroundColor: lineColor,
                        borderColor: lineColor,
                        pointStyle: false,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: symbol + " " + "(日足)",
                        font: {size: 20},
                        color: "#000000",
                        padding: 1,
                    },
                    subtitle: {
                        display: true,
                        text: symbolName,
                        font: {size: 10},
                        padding: 5,
                    },
                    legend: {
                        display: false,
                        position: "right"
                    },
                },
                scales: {
                    x: {ticks: {maxTicksLimit: 16}},
                    y: {position: "right"},
                }
            }
        });
    });

</script>

<!-- Line Chart: Close Price-->
<div class="container my-3 justify-content-center" style="position: relative; width: auto; height: 50vh; over-flow">
    <!-- Chart.js -->
    <canvas bind:this={canvas}/>
</div>
