# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪
1. **報廢日期鎖定**：解決 `DisplayMode: ==DisplayMode.View` 語法錯誤，成功鎖定當天日期（`Today()`）防呆禁止手動修改。
2. **流水號單號自動編碼**：完成 `FormHeaderTitle` 自動依日期與當日筆數編碼（格式如：`20260914001`）。
3. **全表單深度重設清空**：修正 `BtnReset` 與 `BtnNew`，一鍵徹底淨空連動變數（`locDrugRecord`、`locDrugCode`）與藥號、批號、數量、備註及原因，解決登入或新增時殘留範例值的問題。
4. **報廢原因選項調整**：將「其他原因」精準更名為「其他原因（請於備註說明）」。
5. **儲存並發送審核連動報廢紀錄清單**：
   - 解決微軟集合型態衝突（字串 vs 數值 `id: Value(varCurrentSerial)`），修復 `Collect` 寫入失敗問題。
   - 將左側靜態卡片升級為 `Gallery_History`（垂直資源庫），依 `id` 降冪排列，最新單號永遠排第一筆。
   - 實現三層式卡片呈現：第一層純單號（數值）、第二層藥號與藥名、第三層批號與數量。
6. **歷史紀錄 100% 完整原封還原**：點擊清單任一筆紀錄時，右側表單之藥號、藥名、日期、申請人、複核人、藥庫人員、批號、數量、報廢原因（`DefaultSelectedItems`）與備註全數原汁原味重現。
7. **申請人欄位解鎖**：將 `Input_Applicant` 的 `DisplayMode` 改為 `DisplayMode.Edit`，背景改為純白，開放藥師手動輸入或自訂。
8. **真正寫入 SharePoint**：已在 `BtnSubmit.OnSelect` 加上 `Patch('報廢網頁', Defaults(...), {...})`，寫入藥號、藥名、日期、批號、數量、原因、備註及審核狀態（固定 `"待審核"`）。
9. **（2026-09-17 完工）UI 緊湊美化與第 11 項附件格子可視化調整**：
   - 徹底解決播放模式下第 11 項附加檔案被視窗下緣截斷之問題。
   - 刪除殘留撐大捲軸的幽靈控制項 `ComboBox4`（原 Y=728）。
   - 23 個控制項 Y 座標緊湊重排，附件區底部上移至 650px，距螢幕底部狀態列維持 86px 巨大安全餘裕，全畫面文字與元件 100% 不超出螢幕。
10. **（2026-09-17 完工）打通 SharePoint 附件上傳通道與按鈕編譯錯誤清零**：
    - 定位出原按鈕點擊毫無反應之根本原因：微軟禁止直接對 SharePoint 原生 `{Attachments}` 執行常規 Patch，造成 4 個編譯錯誤鎖死按鈕。
    - 成功建立微軟原生表單 `Form_Attachment`（DataSource: `'報廢網頁'`，僅保留原生 `{Attachments}` 卡片，X=346, Y=540, W=950, H=110），取代舊有獨立控制項 `AttachmentsControl1`。
    - 按鈕公式升級為原子整合版：`Patch('報廢網頁', Defaults('報廢網頁'), { ... }, Form_Attachment.Updates); ResetForm(Form_Attachment);`。
    - 按鈕致命編譯錯誤徹底清零（0 Critical Errors），本機已備妥測試檔 `TEST20260917.pdf`（2,430 bytes）。

## 🚦 目前狀態
線上 Power Apps 應用程式（App ID: `d8ae7885-7892-4805-816a-a9593e587077`，名稱「報廢流程表1」）最新狀態已存檔並已發布。表單排版優雅緊湊、無越界問題，按鈕語法完全合法，具備隨單上傳附件之底層結構。

## ➡️ 下一步（下次開工第一優先）
1. **【使用者指定核心任務】SharePoint 申請人／複核人／藥庫複核人員三欄呈現**：
   - **問題現況**：目前 SharePoint 清單「報廢網頁」中看不到這三人的名字，主因是當初在 SharePoint 建為「人員或群組 (Person/Group)」型別，微軟禁止原地改為文字且無法直接存入表單選單的純文字，導致目前 Patch 略過這三欄。
   - **下次開工執行 SOP**：
     1. 前往 SharePoint「報廢網頁」清單主畫面（或清單設定），將舊的「申請人」、「複核人」、「藥庫複核人員」三欄刪除。
     2. 點擊「+ 新增資料欄」，重新建立同名的 3 個 **「單行文字 (Single line of text)」** 欄位。
     3. 在 Power Apps Studio 將「報廢網頁」資料來源「重新整理 (Refresh)」。
     4. 在 `BtnSubmit.OnSelect` 的 `Patch` 公式中補入這三欄：
        - `申請人: Coalesce(ComboBox1.Selected.DisplayText, "未填寫")`
        - `複核人: Coalesce(ComboBox2.Selected.DisplayText, "未填寫")`
        - `藥庫複核人員: Coalesce(Combo_WarehouseReviewer.Selected.DisplayText, "未填寫")`
2. **端到端實測送單**：在 Preview 模式填表並拖入 `TEST20260917.pdf`，按「儲存並發送審核」，確認 SharePoint 清單同時出現「文字資料」、「三位人員姓名」以及「`TEST20260917.pdf` 附件」。
3. **Power Automate 流程開啟與 Teams 推播驗證**：確認後端主管審核 Adaptive Card 流程處於開啟狀態。

## ⚠️ 注意事項
- 微軟 `canvasauthoring` MCP 僅支援雲端同步下載（`sync_canvas`）與本地驗證，無法反向直接覆寫線上編輯畫面。
- SharePoint 清單的 `{Attachments}` 欄位為二進位串流，嚴禁使用常規 `{ 附件: ... }` 進行 Patch，必須使用 `Form_Attachment.Updates` 方式隨 Patch 一併寫入。
- 下拉選單（ComboBox）若需動態選取，必須設定在 `DefaultSelectedItems`，不可使用 `Default`。
- Collection 集合（如 `colHistoryRecords`）嚴格鎖定欄位型態，`id` 務必維持一致的數值型態（`Value(...)`）。

## 🕐 最後更新
- 時間：2026-09-17 16:15
- 更新者：Google Antigravity (指揮官) @ 江瑞益的MacBook Air
- 狀態：UI 緊湊排版與 Form_Attachment 結構完工，等待下次開工執行 SharePoint 三欄位單行文字重建與連動補齊。
