# 藥劑科報廢流程表（專案藍圖）

> 本檔為跨 Agent 通用的專案藍圖（AGENTS.md 開放標準）。任何 Agent 的每個 session 都應先讀本檔＋`handoff.md`。

## 專案簡介
佳里奇美醫院藥劑科藥品與耗材報廢作業流程表。採用 **Power Apps（前端表單）+ Power Automate（後端審核/Teams 推播）+ SharePoint 清單（雲端結構化資料庫）** 醫療自動化鐵三角技術架構，未來直接於院內 Microsoft Teams 團隊頻道發布使用。

## 關鍵時程
- 2026-09-11：專案三層級自動初始化完成。
- 2026-09-11：完成 .NET 10 SDK、微軟官方 PAC CLI (2.12.2)、Canvas Authoring MCP Server 與 powerplatform-mcp 工具鏈配置。
- 2026-09-11：成功連線奇美醫院環境，解包雲端 Power Apps 原始碼，解析 SharePoint 33 欄位結構。
- 2026-09-12：完成雙 Teams 平台權限隔離（選項 A），並完成 Power Automate 主管審核流程與 Teams 自適應推播卡片之建置。
- 2026-09-13：實證 Agent 本地 Code-First 打包流程（抗生素報廢管理 App），整合全院 3,427 筆藥品主檔秒搜連動，正名 PRN (Pro Re Nata) 智慧導航版面，並產出全套大字版流程圖與出版級 PDF 指南。

## 目標與路線圖
- [x] 階段一：專案基礎建設與三層級初始化（L1 本地藍圖＋L3 Obsidian 知識庫）
- [x] 階段二：建立本地 Power Platform (Power Apps / Power Automate / SharePoint) 工具鏈與 MCP 伺服器
- [x] 階段三：匯入現有 `.msapp` 檔案並進行解包（`pac canvas unpack`）
- [x] 階段四：梳理報廢流程各節點（申請、主管審核、狀態變更、Teams 自動化推播）
- [x] 階段五：由 Agent 補全 Power Apps 前端畫面邏輯與 Power Automate 流程設定（完成雙平台權限隔離與審核卡片）
- [x] 階段六：端到端測試驗證、PRN 智慧導航整合、全套 PDF 指南編譯與本地版本封裝
- [ ] 階段七：院內 Teams 頻道與 PRN 智慧門戶正式發布上線

## 資料夾結構
```
藥劑科報廢流程表/
├── .gitignore
├── AGENTS.md                                                # 專案藍圖（開放標準）
├── handoff.md                                               # 跨 Agent / 跨電腦交接檔
├── 報廢流程表.msapp                                          # 微軟官方雲端下載實體 App 檔
├── 抗生素報廢管理App.msapp                                   # 本地 Code-First 打包實體 App (62 KB)
├── 藥劑科報廢表單_Teams主管審核流程_匯入包.zip                 # Power Automate 流程匯入包
├── AI_Agent本地開發PowerApps與整合發布全流程指南.pdf           # 3 頁完整版本地開發指南
├── 醫院IT新手專案指南_微軟五大工具完整串接SOP.pdf             # 3 頁新手白話五星串接手冊
├── PRN醫療自動化智慧導航版面整合指南.pdf                      # 3 頁 PRN (Pro Re Nata) 智慧中樞指南
├── PowerApps_Agent開發流程圖.png                             # 高解析度架構流程圖 (3800x2100)
├── 微軟五大工具串接架構圖.png                                 # 五大工具五星閉環架構圖 (3800x2200)
├── PRN系統與微軟五大工具串接架構圖.png                        # PRN 智慧導航六大中樞架構圖 (3800x2300)
├── 抗生素報廢管理App_方法二本地驗收模擬器.html                 # 內載 3,427 筆藥品本機驗收模擬器
├── 藥品藥號.xlsx                                             # 全院 3,427 筆藥品學名對照清冊主檔
├── app_sources/                                             # 官方 Coauthoring 原始碼
└── unpacked_app/                                            # 解包原始碼檔案庫
```

## 同步層級（本專案初始化至 L1 + L3）

| 層級 | 平台 | 位置 | 讀取時機 |
|------|------|------|---------|
| L1 | 本地 | `AGENTS.md`＋`handoff.md` | 每個 session |
| L2 | GitHub | 未啟用（此電腦未安裝 `gh` CLI，本地 git 追蹤完整） | 指定時 |
| L3 | Obsidian | `藥劑科報廢流程表/專案工作流程.md` | 有需要時 |

## 工作約定
- 任何 Agent、任何電腦：**開工先讀 `handoff.md`，收工必更新 `handoff.md`**
- 修改共用檔案前先讀最新內容，避免覆蓋其他 Agent 的變更
- 所有回應與文件一律使用**台灣繁體中文**
- 中文與英文、半形數字之間保留半形空格
- 修改前先確認計畫，優先保留原有資料結構
