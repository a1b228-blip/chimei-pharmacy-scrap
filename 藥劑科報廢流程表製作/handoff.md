# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（`藥劑科報廢流程表製作/專案工作流程.md`）。

## ⏯️ 目前做到哪
- **2026-09-24 晚：「審核備註」功能完成並上線（App 版本 74，19:51 發布），Teams 實測通過；審核人已換回主管。**
  1. **SharePoint**「報廢網頁」欄位「審核備註」（多行文字；內部名 `OData__x5be9__x6838__x5099__x8a3b_`）。
  2. **Power Automate**「藥劑科報廢表單_Teams主管審核流程」→「更新項目」寫入
     `審核備註 = @{first(body('啟動並等候核准')?['responses'])?['comments']}`。
     審核人 `assignedTo` 已於 20:22 **換回 `980526@chimei.org.tw`（黃慧娟組長）**（測試期間暫改為使用者 `A00534@chimei.org.tw`）。
  3. **Power Apps 電腦版 `MainScreen1`** 第 10 列左右兩欄：左「備註說明」（W=460）、右「審核備註」`Input_ReviewRemarks`（X=836,Y=520,W=460,H=36，多行）。
     - `Default = If(varIsNewMode, "", varSelectedRecord.審核備註)`
     - `DisplayMode = DisplayMode.View`（**唯讀**，使用者要求主管回覆後不得更改）
     - `OnChange = false`（已移除回存公式，App 不寫入此欄，只有流程寫）
     - `HintText = "主管於 Teams 核准時填寫"`
- 版本 73（19:20）起手機版 `MobileScreen` 也已一併上線。

## 🚦 目前狀態
- 線上正式版：**版本 74**（即時）。App Checker 公式 0 錯誤。
- 測試單 `20260924001`（及 20:18 送的另一張）留在 SharePoint；20260924001 的審核備註為使用者手動刪除，未還原。
- ⚠️ 9/19 有 3 筆舊流程仍「正在執行」（舊測試單的審核），主管 Teams 可能還看得到卡片。
- ⚠️ 本機 `cloud_app_sources/` 仍是 09-19 版，未同步。

## ➡️ 下一步
1. 視需要刪除 SharePoint 測試單；到 Power Automate 執行紀錄取消 9/19 那 3 筆「正在執行」的舊審核。
2. 手機 Teams 實機送單驗收（手機版已上線，尚未實機測試）。
3. 重拍《員工操作教學》PDF（第 10 列已變兩欄、新增審核備註、可加手機版頁）；有 canvasauthoring MCP 時同步 `cloud_app_sources/`。

## ⚠️ 注意事項
- **Mac：`ctrl+a`／`cmd+a` 在 Studio 內都無法全選**。清空欄位用「點欄位 → Down×N → End → BackSpace×N」。
- **Studio 頁面比瀏覽器面板寬，會水平捲動**：捲頁面要把游標放在最底部捲軸列（y≈頁面底），放在畫布上只會捲畫布。改屬性前先確認屬性下拉與公式列位置，並先打一個字確認焦點真的在公式列，否則按鍵會跑到樹狀檢視。
- 發佈鈕要點兩次（第一次只顯示提示）；發佈對話框可能開在畫面外，用 viewport 放大截圖確認，再切回預設尺寸點「發行此版本」。
- viewport 模擬放大時點擊無效，只能截圖。截圖常慢一拍。
- `colHistoryRecords` 的 `id` 是 `Value(報廢單號)`，不是 SharePoint `ID`。
- 編輯鎖定：Studio 異常關閉後鎖定可能 >15 分鐘才釋放。
- 公式列輸入 `[...]` 會被自動補成 `]]`；關閉預覽用 Esc。
- Power Automate 審核流程開啟中（審核人黃慧娟組長），測試前先把審核人改成自己，測完務必換回。
- 教學 PDF 第 3 頁含同仁真實工號姓名，僅限科內傳閱。

## 🕐 最後更新
- 時間：2026-09-24 20:27
- 更新者：Claude Code (Opus 5.5) @ 江瑞益的MacBook Air
- Git push：待推
