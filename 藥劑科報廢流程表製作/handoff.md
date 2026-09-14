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

## 🚦 目前狀態
線上 Power Apps 應用程式（App ID: `d8ae7885-7892-4805-816a-a9593e587077`）所有核心連動、即時秒搜、存檔與歷史清單點閱機能均已實測運作正常。最新雲端原始碼已完整同步快取至 `cloud_app_sources/`。

## ➡️ 下一步
1. 於線上 Power Apps Studio 進行最後儲存並正式發布（Publish）。
2. 與 Power Automate 後端審核推播流程連動測試（Teams 自適應卡片主管核准）。
3. 視科內需求補齊檔案照片上傳（`AttachmentBox`）實際儲存 SharePoint 附件之邏輯。

## ⚠️ 注意事項
- 微軟 `canvasauthoring` MCP 僅支援雲端同步下載（`sync_canvas`）與本地驗證，無法反向直接覆寫線上編輯畫面。
- 下拉選單（ComboBox）若需動態選取，必須設定在 `DefaultSelectedItems`，不可使用 `Default`。
- Collection 集合（如 `colHistoryRecords`）嚴格鎖定欄位型態，`id` 務必維持一致的數值型態（`Value(...)`）。

## 🕐 最後更新
- 時間：2026-09-14 16:50
- 更新者：Google Antigravity @ jiangruiyideMacBook-Air.local
- Git push：✅ 已推 (60311ac)
