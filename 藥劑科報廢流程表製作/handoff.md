# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（`藥劑科報廢流程表製作/專案工作流程.md`）。

## ⏯️ 目前做到哪
- **2026-09-22 晚：手機版填單畫面 `MobileScreen` 建置完成，已存檔（22:48），尚未發布。**
  - 原因：App 本來就是「回應式」版面（縮放以符合已關閉），電腦版固定 1366 寬座標在手機直向被裁切。
  - 做法：同一 App 加手機專用畫面、電腦版不動、Teams 分頁不用改。
    `App.StartScreen = If(Host.OSType = "iOS" || Host.OSType = "Android" || App.Width < 700, MobileScreen, MainScreen1)`
  - 結構：`mRoot`（垂直自動版面）→ `mHeader`（深藍標題＋單號）／`mBody`（可捲動，1～11 單欄）／`mFooter`（固定底部「送出審核」`mBtnSubmit`）；附件 `mForm_Attachment`（1 欄、最小寬度 0）。依使用者決定**只做填單**，不含歷史清單。
  - `mBtnSubmit.OnSelect`：與電腦版同一套 Patch 寫入 SharePoint '報廢網頁'＋`mForm_Attachment.Updates`，送出後刷新 `colHistoryRecords` 並清空欄位；另加「報廢原因」必填與防連點 `locSubmitting`。
  - 4 個連資料的下拉選單（`mCombo_DrugName`／`_Applicant`／`_Reviewer`／`_WarehouseReviewer`）為 Studio 原生插入；其餘控制項由 `mobile/MobileScreen_controls.pa.yaml` 貼上。
  - Studio 預覽 iPhone 12（390×844）驗證：版面正常、藥號↔藥名雙向連動、藥師／藥庫名單正常；App Checker 0 錯誤。**未實際送單、未用實機測試。**
- 更早里程碑（09-19 UI 美化 7 項已發布、SharePoint 真實寫入、附件、狀態徽章、Teams 審核、教學 PDF）詳見 Obsidian 與 git log。

## 🚦 目前狀態
- 線上正式版（App ID `d8ae7885-7892-4805-816a-a9593e587077`，「報廢流程表1」）仍為 09-19 發布版；手機畫面只在 Studio 草稿中。
- 電腦版 `MainScreen1` 未改動；正式版清單已確認能讀到 SharePoint（Studio 顯示「共 1 筆」）。
- ⚠️ 本機 `cloud_app_sources/` 仍是 09-19 09:51 版，未同步美化與手機畫面。

## ➡️ 下一步
1. 使用者發布 → 電腦版 Teams 分頁確認照舊 → 手機 Teams 確認自動進入手機畫面。
2. 用手機送一張測試單：確認附件拍照、SharePoint 寫入、組長 Teams 收到審核卡片。
3. 重拍《員工操作教學》PDF（欄位順序已變、可加手機版操作頁）；有 canvasauthoring MCP 時 `sync_canvas` 更新 `cloud_app_sources/`。

## ⚠️ 注意事項
- **YAML 貼上的連資料下拉選單會選項全空白**（Items 為紀錄表時）：改用「插入」原生新增 → 改名 → 公式列設屬性 → 右鍵「重新排序」移位（新插入會放在容器最後）。
- 公式列輸入 `[...]` 會被自動補成 `]]`，需刪掉多的括號；連續改屬性每步等約 1 秒，否則設定會漏寫。
- 關閉預覽用 Esc，不要點右上角 X（視窗尺寸變動時會誤點「發佈」）。
- YAML 貼上流程：瀏覽器 `navigator.clipboard.writeText()` 寫剪貼簿 → 畫布／樹狀檢視右鍵「貼上」；純量值不可含半形「: 」。
- Studio 內不要用快速鍵複製貼上控制項（會卡在「請稍候…」）。
- 電腦版座標規則與 HTML 文字防捲軸做法見 Obsidian 09-19 紀錄。
- Power Automate 審核流程開啟中（審核人黃慧娟組長），送單前確認是否為正式單據。
- 教學 PDF 第 3 頁含同仁真實工號姓名，僅限科內傳閱。

## 🕐 最後更新
- 時間：2026-09-22 22:55
- 更新者：Claude Code @ jiangruiyideMacBook-Air
- Git push：待推
