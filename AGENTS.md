# 藥劑科報廢流程表（專案藍圖）

> 本檔為跨 Agent 通用的專案藍圖（AGENTS.md 開放標準）。任何 Agent 的每個 session 都應先讀本檔＋`handoff.md`。

## 專案簡介
佳里奇美醫院藥劑科藥品與耗材報廢作業流程表。採用 **Power Apps（前端表單）+ Power Automate（後端審核/Teams 推播）+ SharePoint 清單（雲端結構化資料庫）** 技術架構，未來直接於院內 Microsoft Teams 團隊頻道發布使用。

## 關鍵時程
- 2026-09-11：專案三層級自動初始化完成。
- 2026-09-11：完成 .NET 10 SDK、微軟官方 PAC CLI (2.12.2)、Canvas Authoring MCP Server 與 powerplatform-mcp 工具鏈配置。

## 目標與路線圖
- [x] 階段一：專案基礎建設與三層級初始化（L1 本地藍圖＋L3 Obsidian 知識庫）
- [x] 階段二：建立本地 Power Platform (Power Apps / Power Automate / SharePoint) 工具鏈與 MCP 伺服器
- [ ] 階段三：匯入現有 `.msapp` 檔案並進行解包（`pac canvas unpack`）
- [ ] 階段四：梳理報廢流程各節點（申請、藥庫/主管審核、管制藥會驗、狀態變更、Teams 自動化推播）
- [ ] 階段五：由 Agent 補全 Power Apps 前端畫面邏輯與 Power Automate 流程設定
- [ ] 階段六：測試驗證與院內 Teams 頻道部署

## 資料夾結構
```
藥劑科報廢流程表/
├── .gitignore
├── AGENTS.md          # 專案藍圖（開放標準）
├── handoff.md         # 跨 Agent / 跨電腦交接檔
└── app_sources/       # （預備存放解包後的 Power Apps 原始碼）
```

## 同步層級（本專案初始化至 L1 + L3）

| 層級 | 平台 | 位置 | 讀取時機 |
|------|------|------|---------|
| L1 | 本地 | `AGENTS.md`＋`handoff.md` | 每個 session |
| L2 | GitHub | 未啟用（此電腦未安裝 `gh` CLI） | 指定時 |
| L3 | Obsidian | `藥劑科報廢流程表/專案工作流程.md` | 有需要時 |

## 工作約定
- 任何 Agent、任何電腦：**開工先讀 `handoff.md`，收工必更新 `handoff.md`**
- 修改共用檔案前先讀最新內容，避免覆蓋其他 Agent 的變更
- 所有回應與文件一律使用**台灣繁體中文**
- 中文與英文、半形數字之間保留半形空格
- 修改前先確認計畫，優先保留原有資料結構
