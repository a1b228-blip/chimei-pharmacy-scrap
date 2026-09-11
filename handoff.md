# 交接檔（handoff.md）

> 任何 Agent、任何電腦接手前**必讀**；收工時**必更新**。本檔只放交接必需的精簡資訊，詳細脈絡放 Obsidian（若有 L3）。

## ⏯️ 目前做到哪
完成微軟醫療自動化三神器（Power Apps + Power Automate + SharePoint）之本地工具鏈與 MCP 伺服器建置：
1. 配置 .NET 10 SDK（macOS arm64）。
2. 安裝微軟官方 Power Platform CLI (`pac` v2.12.2)，支援 `pac canvas`（解包/打包 .msapp）與 `pac power-automate`（雲端流程檢視與執行）。
3. 安裝微軟官方 `CanvasAuthoringMcpServer` (v1.1.5) 與 `powerplatform-mcp` 全域套件。
4. 全域 MCP 設定檔（`~/.gemini/config/mcp_config.json`）已完成登錄並同步至 Chezmoi。

## 🚦 目前狀態
工具鏈與 MCP 伺服器已就緒。可隨時進行：
- 本地 `.msapp` 畫布應用程式解包、原始碼分析、Power Fx 編輯與重打包。
- Power Automate 雲端流程診斷與設計。
- SharePoint 清單結構對齊與連線。

## ➡️ 下一步
1. 請使用者將現有已製作部分的 Power App 匯出為 `.msapp` 檔案，放置於本專案資料夾中。
2. 透過 `pac canvas unpack` 解包為 YAML / Power Fx 原始碼。
3. 梳理報廢流程各節點（申請、藥庫/主管審核、管制藥會驗、狀態變更、Teams 自動化推播）。
4. 由 Agent 補全 Power Apps 前端畫面邏輯與 Power Automate 流程設定。

## ⚠️ 注意事項
- 執行 `pac` 指令前需確認環境變數 `DOTNET_ROOT="$HOME/.dotnet"`（已寫入 `~/.zprofile` 與 `~/.zshrc`）。
- 本專案路徑為 `/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表`，保持獨立專案運作。
- 後端資料採用 SharePoint List，於 Teams 頻道發布無需購買 Power Apps Premium 進階授權。

## 🕐 最後更新
- 時間：2026-09-11 21:50
- 更新者：Google Antigravity @ jiangruiyideMacBook-Air.local
- Git push：—（本專案未啟用遠端 git repo）
