<script>
    export let symbol = "";
    export let symbolName = "";
    export let timeframe = "";
    export let data = [];
    export let indicator_arr = [];
    export let chart_id = "";

    import { onMount } from "svelte";
    import { createChart, CrosshairMode, LineStyle, PriceScaleMode } from "lightweight-charts";

    export let chart;

    let candlestickSeries;
    let volumeSeries;

    onMount(() => {
        // Seprate ohlv and volume
        let ohlc_arr = [];
        let volume_arr = [];

        for (let i of data) {
            ohlc_arr.push({
                "time": i["time"],
                "open": i["open"],
                "high": i["high"],
                "low": i["low"],
                "close": i["close"]
            });
        }

        for (let i of data) {
            volume_arr.push({
                "time": i["time"],
                "value": i["volume"]
            });
        }

        // OHLC
        let chartOptions = {
            layout: {
                textColor: 'black',
                background: { type: 'solid', color: '#ffffff' },
            },
            autoSize: true,
            localization: {
                dateFormat: 'yyyy-MM-dd',
            },
        };
        chart = createChart(document.getElementById(`chart_${chart_id}`), chartOptions);

        chart.applyOptions({
            crosshair: {
                // Change mode from default 'magnet' to 'normal'.
                // Allows the crosshair to move freely without snapping to datapoints
                mode: CrosshairMode.Normal,

                // Vertical crosshair line (showing Date in Label)
                vertLine: {
                    width: 8,
                    color: '#C3BCDB44',
                    style: LineStyle.Solid,
                },
                // Horizontal crosshair line (showing Price in Label)
                // horzLine: {
                //     color: '#9B7DFF',
                //     labelBackgroundColor: '#9B7DFF'
                // }
            },
            // rightPriceScale: {
            //     mode: PriceScaleMode.Logarithmic
            // }
        });

        candlestickSeries = chart.addCandlestickSeries({
            upColor: '#ffffff',
            downColor: '#000000',
            borderUpColor: "#000000",
            borderDownColor: '#000000',
            borderVisible: true,
            wickUpColor:
            '#000000',
            wickDownColor: '#000000',
            priceLineVisible: true,
            priceLineColor: "#000000",
            lastValueVisible: true,
            // title: "Close",


        });

        candlestickSeries.setData(ohlc_arr);

        // Volume
        volumeSeries = chart.addHistogramSeries({
            color: '#000000',
            priceFormat: {
                type: 'volume',
            },
            priceScaleId: '', // set as an overlay by setting a blank priceScaleId
            // set the positioning of the volume series
            scaleMargins: {
                top: 0.9, // highest point of the series will be 70% away from the top
                bottom: 0,
            },
            priceLineVisible: false,
            priceLineColor: "#000000",
            lastValueVisible: false,
            // title: "Close",

        });
        volumeSeries.priceScale().applyOptions({
            scaleMargins: {
                top: 0.8, // highest point of the series will be 70% away from the top
                bottom: 0,
            },
        });
        volumeSeries.setData(volume_arr);

        // Add Technical Indicators
        if (indicator_arr.length > 0) {
            
            for (let item of indicator_arr) {

                if (item["indicator_name"] === "SMA") {
                    let maData = calculateMovingAverageSeriesData(ohlc_arr, item["params"]["N"]);
                    let maSeries = chart.addLineSeries({
                        color: item["params"]["color"],
                        lineWidth: 1,
                        priceLineVisible: false
                    });
                    maSeries.setData(maData);
                }
            }
        }
        // Last finishing by fitting the content
        chart.timeScale().fitContent();
    });

    // Indicator Calculation Functions

    // Moving Average
    function calculateMovingAverageSeriesData(candleData, maLength) {
        const maData = [];
        for (let i = 0; i < candleData.length; i++) {
            if (i < maLength) {
                // Provide whitespace data points until the MA can be calculated
                maData.push({ time: candleData[i].time });
            } else {
                // Calculate the moving average, slow but simple way
                let sum = 0;
                for (let j = 0; j < maLength; j++) {
                    sum += candleData[i - j].close;
                }
                const maValue = sum / maLength;
                maData.push({ time: candleData[i].time, value: maValue });
            }
        }
        return maData;
    }

    </script>


<!-- Tradingview Light-weight Chart -->
<div id="chart_{chart_id}" style="width: auto; height: 350px;">
    <!-- Lightweight Charts Attribution Message and Link -->
    <div class="lw-attribution">
        <p class="my-0">
            <strong>
                <a href="/" onclick="return false;" style="text-decoration: none;">
                    {#if timeframe.toLowerCase() === "1wk"}
                        <h4>{symbol} (週足)</h4>
                    {:else if timeframe.toLowerCase() === "1d"}
                        <h4>{symbol} (日足)</h4>
                    {:else}
                        <h4>{symbol} ({timeframe})</h4>
                    {/if}
                    <p class="p-0 m-0" style="font-size: 10px; color: gray;">{symbolName}</p>
                </a>
            </strong>
        </p>
        <p class="my-0">
            <a style="font-size: 11px" href="https://tradingview.github.io/lightweight-charts/" target="_blank">
                Powered by Lightweight Charts™
            </a>
            <!-- Indicator Names and Colors -->
            {#each indicator_arr as item}
                <div class="d-flex flex-column"></div>
                <a href="/" onclick="return false;" style="text-decoration: none; font-size: 10px;" class="d-flex flex-row gap-1 p-0 m-0">
                    {item.indicator_name_display} {item.params.N}
                    <i class="bi bi-square-fill" style="color: {item.params.color}; font-size: 10px;"></i>
                </a>
            {/each}
        </p>
    </div>
</div>