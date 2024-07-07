<script>
    export let symbol = "";
    export let symbolName = "";

    export let data = [];
    export let category = "";
    export let barColor;

    // Translation dict
    let translationDict = {
        'AccountsPayable': '買掛金/営業債務及びその他の債務',
        'AccountsReceivable': '売掛金(+受取手形)/営業債権、その他の債権及び契約資産',
        'AccruedInterestReceivable': '未収利息',
        'AccumulatedDepreciation': '減価償却累計額合計',
        'AllowanceForDoubtfulAccountsReceivable': '貸倒引当金',
        'AvailableForSaleSecurities': '投資有価証券/金融分野における投資及び貸付+その他の金融資産',
        'BuildingsAndImprovements': '建物および構築物',
        'CapitalStock': '資本金',
        'CashAndCashEquivalents': '現金及び預金/現金及び現金同等物',
        'CommercialPaper': 'コマーシャルペーパー',
        'ConstructionInProgress': '建設仮勘定',
        'CurrentAccruedExpenses': '未払費用',
        'CurrentAssets': '流動資産合計',
        'CurrentDebt': '短期借入金/社債及び借入金',
        'FinancialAssets': '金融資産',
        'ForeignCurrencyTranslationAdjustments': '為替換算調整勘定',
        'Goodwill': 'のれん',
        'GoodwillAndOtherIntangibleAssets': '無形固定資産',
        'HeldToMaturitySecurities': '満期保有目的有価証券',
        'IncomeTaxPayable': '未払法人税',
        'InterestPayable': '未払利息',
        'Inventory': '棚卸資産',
        'LandAndImprovements': '土地',
        'Leases': 'リース資産',
        'LoansReceivable': '貸付金',
        'LongTermDebt': '長期借入金/社債及び借入金',
        'LongTermProvisions': '長期引当金/引当金',
        'MachineryFurnitureEquipment': '機械、運搬具及び工具器具備品',
        'MinorityInterest': '非支配株主持分',
        'NetDebt': '借入金',
        'NetPPE': '有形固定資産合計/有形固定資産+使用権資産',
        'NetTangibleAssets': '有形固定資産',
        'NotesReceivable': '受取手形',
        'RawMaterials': '原材料及び貯蔵品',
        'RetainedEarnings': '利益剰余金',
        'TotalAssets': '資産合計',
        'TotalCapitalization': '純資産合計',
        'TotalDebt': '負債合計',
        'TradingSecurities': '売買目的有価証券',
        'TreasuryStock': '自己株式',
        'WorkInProcess': '仕掛品',
        'CapitalExpenditure': '有形+無形固定資産等の取得による支出',
        'CashFlowFromContinuingFinancingActivities': '財務活動によるキャッシュフロー',
        'NetIncome': '親会社に帰属する当期純利益/当期純利益の帰属(当社の所有者・株主)',
        'EndCashPosition': '期末現金残高',
        'OperatingCashFlow': '営業活動によるキャッシュフロー',
        'ChangeInAccountPayable': '仕入債務の増減額',
        'ChangeInInventory': '棚卸資産の増減額',
        'DepreciationAndAmortization': '減価償却費',
        'InvestingCashFlow': '投資活動によるキャッシュフロー',
        'ChangesInAccountReceivables': '売掛金の増減額',
        'BeginningCashPosition': '期首現金残高',
        'Amortization': '減価償却費',
        'CostOfRevenue': '売上原価/原価',
        'DepreciationAmortizationDepletionIncomeStatement': '減価償却費',
        'DepreciationAndAmortizationInIncomeStatement': '減価償却費',
        'DepreciationIncomeStatement': '減価償却費',
        'EBIT': 'EBIT',
        'EBITDA': 'EBITDA',
        'GainOnSaleOfBusiness': '事業売却益',
        'GainOnSaleOfPPE': '固定資産売却益',
        'GainOnSaleOfSecurity': '有価証券証券売却益',
        'GeneralAndAdministrativeExpense': '一般管理費',
        'GrossProfit': '売上総利益',
        'InterestExpense': '支払利息',
        'InterestIncome': '受取利息',
        'OperatingExpense': '販売費及び一般管理費',
        'OperatingIncome': '営業利益',
        'ProvisionForDoubtfulAccounts': '貸倒引当金',
        'ResearchAndDevelopment': '研究開発費',
        'SalariesAndWages': '人件費',
        'SellingAndMarketingExpense': '販売費',
        'SellingGeneralAndAdministration': '販売費および一般管理費',
        'TotalRevenue': '売上高/収益',
        'PretaxIncome': '税金等調整前当期純利益',
        'ReconciledDepreciation': '減価償却費',
    }


    // Chart.js
    import { onMount } from 'svelte';
    import Chart from 'chart.js/auto';

    let x_data = [];
    let y_data = [];
    let ctx;
    let canvas;

    for (let i of data) {
        // Create label (x-axis)
        x_data.push(i["asOfDate"])
        // Create data (y-axis)
        y_data.push(i[category] / 1000000) // in Million
    }

    onMount(() => {
        ctx = canvas.getContext('2d');
        var chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: x_data,
                datasets: [
                    {
                        label: translationDict[category] + "(百万)",
                        data: y_data,
                        backgroundColor: barColor,
                        borderColor: "rgb(0,0,0)",
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: symbol,
                        font: {size: 20},
                        color: "#000000",
                        padding: 0,
                    },
                    subtitle: {
                        display: true,
                        text: symbolName,
                        font: {size: 10},
                        padding: 0,
                    },
                }
            }
        });
    });

</script>


<!-- Bar Chart for Financial Statement-->
<div class="container my-3 justify-content-center" style="position: relative; width: auto; height: 50vh; over-flow">
    <!-- Chart.js -->
    <canvas bind:this={canvas}/>
</div>