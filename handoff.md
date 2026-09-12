# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪
1. **工具鏈與環境配置**：完成 .NET 10 SDK、微軟官方 PAC CLI (2.12.2)、Canvas Authoring MCP Server、powerplatform-mcp 安裝與全域 Chezmoi 同步。
2. **資料庫層擴充**：確認 SharePoint 清單（`報廢網頁`，GUID: `20d0cec4-6b56-45d7-83c0-a7d85c6d00af`），完成開放「會議紀錄平台」同仁讀取權限，並新增「審核狀態」欄位。
3. **Power Apps 前端權限隔離（選項 A）**：改寫 `MainScreen1.pa.yaml`，實作藥庫主管（`B305W2@chimei.org.tw`）全權限，會議同仁純唯讀安全瀏覽。
4. **藥品名稱與藥號雙向連動 + 英文首字母遞進篩選**：
   - 將「藥品名稱」升級為可搜尋式 ComboBox，支援輸入第 1 個英文字母即時依序展示匹配藥品，輸入第 2 個字母進一步精準過濾。
   - 點選藥品名稱自動即時填入對應「藥號（藥品代碼）」。
   - 輸入藥號時亦即時雙向反向自動選中對應之「藥品名稱」。
   - 保留手動輸入彈性（新藥或特殊耗材可手動鍵入並順利儲存）。
5. **Power Automate 雲端審核流程**：完成「當建立項目時」➔「啟動並等候核准」流程架構，並已打包產出標準流程匯入套件：`藥劑科報廢表單_Teams主管審核流程_匯入包.zip`。

## 🚦 目前狀態
- 前端 Power Apps 與後端 SharePoint、Power Automate 之鐵三角架構已全面連通。
- 藥品名稱與藥號之雙向連動與動態搜尋邏輯已寫入 `app_sources/MainScreen1.pa.yaml`。

## ➡️ 下一步
1. 藥劑科若需匯入全院數千筆 Excel 藥品主檔，可直接於 SharePoint 點擊「+ 新增清單」➔「從 Excel」上傳。
2. 在 Power Apps 提交一筆測試報廢單驗證品名搜尋與藥號自動帶出。
3. 將 Power Apps 正式發布至「藥庫溝通平台」與「會議紀錄平台」Teams 頻道。

## ⚠️ 注意事項
- 目前設定之藥庫管理主管帳號為 `B305W2@chimei.org.tw`。
- 本地未啟用遠端 git repo，本地 git 追蹤完整。

## 🕐 最後更新
- 時間：2026-09-12 21:16
- 更新者：Google Antigravity @ jiangruiyideMacBook-Air.local
