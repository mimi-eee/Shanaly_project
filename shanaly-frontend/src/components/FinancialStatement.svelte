<script>
    export let symbol = "";
    export let symbolName = "";
    export let data = [];

    let selected_color = "#000000";

    import { push } from "svelte-spa-router";
    import TextEditor from "./TextEditor.svelte";
    import Tags from "svelte-tags-input";

    // Variables for Svlete Tags Input
    let tags = [];

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

    /////////////////////////////////
    import BarChart from "./BarChart.svelte";

    let current_category1 = "カテゴリ";
    let current_category2 = "項目";
    let reflect_var = false;
    
    // Temp array for rendering values in the table
    let tmp_arr = [];

    function appendDataTmpArr() {
        
        if (current_category2 !== "項目") {
            
            tmp_arr = [];

            for (let i of data) { 
                if (i[current_category2] !== undefined) {
                    tmp_arr.push(i[current_category2]);
                } else {
                    tmp_arr.push(null);
                }
            }
            // Reflec the data to the bar chart
            reflect_var = !reflect_var;
        }
    }

    function reflectColor() {
        reflect_var = !reflect_var;
    }

    // Title & Content Part
    import fastapi from "../lib/api";

    let editor = null; // from Child Compoent: TextEditor.svelte 
    let title = "";

    function submitPost() {

        // Get data
        let title_tmp = title;
        // Get content from TextEditor.svelte Component
        let content_tmp = editor.getSemanticHTML(); // Quill JS

        let tags_str = tags.join("#");  // Add tags

        // Related item data only!
        let tmp_fs_arr = [];
        for (let i of data) {
            let tmp_obj = {}
            tmp_obj["asOfDate"] = i["asOfDate"];
            tmp_obj[current_category2] = i[current_category2];
            tmp_fs_arr.push(tmp_obj);
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
                        "component_type": "financial_statement",
                        "symbol": symbol,
                        "symbolName": symbolName,
                        "data": tmp_fs_arr,
                        "category": current_category2,
                        "barColor": selected_color,
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


<div class="container mx-0 p-0">

    <!-- Select Options Menu -->
    <div class="container mx-0 px-0">
        <div class="container my-1 mx-0 px-0">
            <!-- Options 1 -->
            <select class="form-select" aria-label="category1" bind:value={current_category1}>
              <option selected>カテゴリ</option>
              <option value="balance_sheet">貸借対照表 (Balance Sheet)</option>
              <option value="income_statement">損益計算書 (Income Statement)</option>
              <option value="cash_flow">キャッシュフロー計算書 (Cash Flow)</option>
            </select>
        </div>
        <div class="container my-1 mx-0 px-0">
          <!-- Options 2 -->
          <select class="form-select" aria-label="category2" bind:value={current_category2} on:change={appendDataTmpArr}>
            
            <option selected>項目</option>
            
            {#if current_category1 === "balance_sheet"}
                {#each balanceSheetOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}
            
            {:else if current_category1 === "cash_flow"}
                {#each cashFlowOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}
            
            {:else if current_category1 === "income_statement"}
                {#each incomeStatementOptions as item}
                    <option value="{item}">{translationDict[item]} ({item})</option>
                {/each}
            
            {:else}
                <!-- Diplsplay Nothing -->
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
                bind:value={selected_color} on:change={reflectColor}>
            </div>
        </div>

    </div>

    <!-- Financial Statement Table -->
    {#if current_category2 !== "項目"}

      <div class="container mx-0 p-0 my-3">
        <!-- Symbol Title -->
        <!-- <h3 class="mx-2">{symbol}</h3> -->
      </div>

      <!-- Bar Chart for Financial Statement -->
      <!-- Re-render the BarChart component if tmp_arr changes -->
      {#key reflect_var}
          <BarChart
          symbol={symbol}
          symbolName={symbolName}
          data={data} 
          category={current_category2}
          barColor={selected_color}/>
      {/key}

      <!-- Title and Content -->
      <div class="mt-3 pt-3">
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

    {/if}

</div>


<style>

</style>