<script>
    export let symbol;
    export let symbolName;
    export let frequency;
    export let data = [];
    export let target_item;

    // Bar Chart
    export let selected_color;

    import fastapi from "../lib/api"
    import SymbolSearchHelper from "./SymbolSearchHelper.svelte";

    // Varibales for Symbol Search Helper
    let helperOn = false;

    let err_msg = "";
    let running = false; // Running spinner

    // Classify item by financial statement
    let balanceSheetOptions = [
        'CashAndCashEquivalents',
        'AccountsReceivable',
        'Inventory',
        'WorkInProcess',
        'RawMaterials',
        'CurrentAssets',
        'BuildingsAndImprovements',
        'MachineryFurnitureEquipment',
        'LandAndImprovements',
        'AccumulatedDepreciation',
        'Goodwill',
        'GoodwillAndOtherIntangibleAssets',
        'AvailableForSaleSecurities',
        'NetPPE',
        'TotalAssets',
        'AccountsPayable',
        'CurrentDebt',
        'LongTermProvisions',
        'CapitalStock',
        'RetainedEarnings',
        'TreasuryStock',
        'MinorityInterest',
        'TotalCapitalization',

        // 'AccruedInterestReceivable',
        // 'AllowanceForDoubtfulAccountsReceivable',
        // 'CommercialPaper',
        // 'ConstructionInProgress',
        // 'CurrentAccruedExpenses',
        // 'FinancialAssets',
        // 'ForeignCurrencyTranslationAdjustments',
        // 'HeldToMaturitySecurities',
        // 'IncomeTaxPayable',
        // 'InterestPayable',
        // 'Leases',
        // 'LoansReceivable',
        // 'NetDebt',
        // 'NotesReceivable',
        // 'TotalDebt',
        // 'TradingSecurities',
    ]

    let cashFlowOptions = [
        "PretaxIncome",
        "ReconciledDepreciation",
        'ChangesInAccountReceivables',
        'ChangeInInventory',
        'ChangeInAccountPayable',
        'OperatingCashFlow',
        'CapitalExpenditure',
        'InvestingCashFlow',
        'CashFlowFromContinuingFinancingActivities',
        'EndCashPosition',
        // 'BeginningCashPosition',
        // 'NetIncome',
        // 'DepreciationAndAmortization',
    ]

    let incomeStatementOptions = [

        'TotalRevenue',
        'CostOfRevenue',
        'GrossProfit',
        'OperatingExpense',
        'OperatingIncome',
        'NetIncome',

        // 'Amortization',
        // 'DepreciationAmortizationDepletionIncomeStatement',
        // 'DepreciationAndAmortizationInIncomeStatement',
        // 'DepreciationIncomeStatement',
        // 'EBIT',
        // 'EBITDA',
        // 'GainOnSaleOfBusiness',
        // 'GainOnSaleOfPPE',
        // 'GainOnSaleOfSecurity',
        // 'GeneralAndAdministrativeExpense',
        // 'InterestExpense',
        // 'InterestIncome',
        // 'ProvisionForDoubtfulAccounts',
        // 'ResearchAndDevelopment',
        // 'SalariesAndWages',
        // 'SellingAndMarketingExpense',
        // 'SellingGeneralAndAdministration',
    ]

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

    // Variables for Financial Statement
    let category1 = "balance_sheet";

    // Get data from Backend API server: Yahoo finance
    // Fetch data by using the backend API
    async function getYahooData(target_symbol, target_frequency) {
        
        let params = {};
        let endpoint = "";

        params = {
            symbol: target_symbol,
            frequency: target_frequency,
        };

        endpoint = "/api/data/financial_statement_yahoo";
        
        await fastapi(
            "get",
            endpoint,
            params,
            (result) => {
                // Assign the received result to data
                data = result;
                // Reset error message
                err_msg = "";
            },
            (result) => {
                err_msg = result["detail"];
            }
        )
    }

    async function getData() {
        running = true;
        await getYahooData(symbol, frequency);
        running = false;
    }

</script>

<!-- Symbol Search Helper -->
<!-- This is hidden at first -->
{#if helperOn === true}
    <div class="mx-1 mb-3">
        <SymbolSearchHelper bind:userSelectSymbol={symbol} bind:userSelectSymbolName={symbolName}/>
    </div>
{/if}

<!-- Input Form for Title and Content -->
<div class="mb-3 d-flex flex-row">
    <div class="mx-1">
        <!-- Symbol Input Label -->
        <label for="input-title" class="form-label">銘柄コード</label>
        <!-- Button for switching Symbol Search Helper -->
        <button class="btn btn-link text-align-center pt-0 px-0" on:click={()=>{helperOn = !helperOn;}}>
            <i class="bi bi-question-circle"></i>
        </button>
        <!-- Symbol Input -->
        <textarea class="form-control" id="input-title" rows="1" bind:value={symbol}></textarea>
    </div>
    <div class="mx-1">
        <label for="input-symbol" class="form-label">頻度</label>
        <select class="form-select" aria-label="default-select" id="input-symbol" bind:value={frequency}>
            <option selected value="q">四半期</option>
            <option value="a">年度</option>
        </select>     
    </div>
</div>

{#if symbol !== "" && symbol !== null && symbol !== undefined}
    <div class="mb-3 d-flex flex-row mx-1">
        <button type="button" class="btn btn-outline-primary" on:click={getData}>
            {#if running === true}
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {/if}
            ダウンロード
        </button>
        <!-- Whether Data exist or not by displaying O or X Symbol-->
        {#if data.length > 0 && err_msg === ""}
            <!-- O mark -->
            <div class="mx-2">
                <h3><i class="bi bi-check-lg"></i></h3>
            </div>
        {/if}
    </div>
    {#if err_msg !== ""}
        <!-- Error Message -->
        <div class="alert alert-primary" role="alert">
            {err_msg}
        </div>
    {/if}
{/if}

{#if data.length > 0 && running === false && err_msg === ""}
    
    <div class="mx-1 mb-3">
        <label for="input-symbol" class="form-label">カテゴリ1</label>
        <select class="form-select" aria-label="default-select" id="input-symbol" bind:value={category1}>
            <option selected value="balance_sheet">貸借対照表 (Balance Sheet)</option>
            <option select value="income_statement">損益計算書 (Income Statement)</option>
            <option value="cash_flow">キャッシュフロー計算書 (Cash Flow)</option>
        </select>     
    </div>
    <div class="mx-1 mb-3">
        <label for="input-symbol" class="form-label">カテゴリ2</label>
        <select class="form-select" aria-label="default-select" id="input-symbol" bind:value={target_item}>

            <option value="item" selected>項目</option>

            {#if category1 === "balance_sheet"}
                {#each balanceSheetOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}
        
            {:else if category1 === "cash_flow"}
                {#each cashFlowOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}
            
            {:else if category1 === "income_statement"}
                {#each incomeStatementOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}

            {/if}

        </select>     
    </div>
    <!-- Color Picker -->
    <div>    
        <div class="my-3">
            <input
            class="container-fluid rounded p-0"
            type="color"
            id="color-picker"
            bind:value={selected_color}>
        </div>
    </div>

{/if}
