# 佳里奇美醫院 藥劑科報廢流程表
## Power Apps 原生表單匯入與從零建置全流程 SOP 指南

> 本手冊為佳里奇美醫院藥劑科報廢表單之專屬部署指引。提供「極速匯入實體 App」與「Studio 手工從零建置」雙軌教學，確保在醫院受限帳號與防護機制下 100% 成功上線。

---

## 🚀 路徑 A：極速直達——直接匯入已產出的實體 .msapp 檔案（建議首選）

本專案目錄已為您以微軟官方 PAC CLI (2.12.2) Code-First 原生技術編譯產出實體應用程式：
**📁 實體檔案**：`佳里奇美_藥劑科報廢表單_原生正式版.msapp` (130 KB)

### 匯入四步驟（免開發、免寫公式、60 秒發布）：
1. **登入微軟 Power Apps**：
   - 於院內電腦或個人筆電瀏覽器開啟微軟官方入口：https://make.powerapps.com
   - 確認右上角環境切換至「**奇美醫療財團法人 (預設)**」或所屬工作環境。
2. **開啟實體應用程式**：
   - 點擊左側導航欄的【**應用程式 (Apps)**】。
   - 點擊頂部選單的【**開啟 (Open)**】➔【**瀏覽檔案 (Browse)**】。
   - 選取本目錄下的 `佳里奇美_藥劑科報廢表單_原生正式版.msapp`。
3. **檢查資料來源連線**：
   - 開啟後，左側圓柱體圖示（資料）會自動連結 SharePoint 清單：
     - `報廢網頁`（主要報廢單據儲存庫）
     - `藥品主檔`（全院 3,427 筆藥品清冊快取）
   - 若顯示驚嘆號，點擊「...」選擇【重新整理】或重新登入醫院 M365 帳號即可。
4. **儲存並發布**：
   - 點擊右上角【儲存 (Save)】➔【發布 (Publish)】➔【發布此版本】。
   - 完成！應用程式已正式於院內雲端就緒。

---

## 🛠️ 路徑 B：逐步教學指引——在 Power Apps Studio 手工從零建置

若您希望親自體驗在 Power Apps Studio 畫面中從空白畫布一步步拉出與 HTML 100% 相同視覺與功能的表單，請遵循以下步驟：

### 第一步：建立畫布應用程式並配置版型
1. 在 make.powerapps.com 點擊【**+ 建立**】➔【**空白應用程式**】➔【**空白畫布應用程式**】。
2. 應用程式名稱填寫：`佳里奇美醫院 - 藥劑科報廢流程管理系統`，格式選擇【**平板電腦 (Tablet)**】（寬度 1366 × 高度 768，最適合醫院電腦螢幕與 Teams 嵌入）。

### 第二步：解開 3,427 筆藥品限制（全域快取設定）
1. 點擊左側樹狀檢視頂部的【**App**】。
2. 在屬性下拉選單選取【**OnStart**】，貼入以下公式：
```powerappsfl
// 平行載入全院 3,427 筆藥品，突破 2,000 筆委派限制
Concurrent(
    ClearCollect(DrugCachePart1, Filter('藥品主檔', ID <= 2000)),
    ClearCollect(DrugCachePart2, Filter('藥品主檔', ID > 2000))
);
ClearCollect(AllDrugs, DrugCachePart1, DrugCachePart2);
```
3. 點擊 `App` 右側的三個點【...】，點選【**執行 OnStart**】載入資料。

### 第三步：打造 1:1 奇美醫療深藍 Header
1. 插入一個【水平容器 (Horizontal Container)】，命名為 `HeaderContainer`：
   - `Width`: `Parent.Width`
   - `Height`: `65`
   - `Fill`: `RGBA(2, 75, 125, 1)`（奇美醫療標準深藍）
2. 在容器內插入【影像 (Image)】控制項：
   - 載入奇美醫院 Logo 圖檔，`Width: 150, Height: 40`。
3. 在容器內插入【文字標籤 (Label)】：
   - `Text`: "佳里奇美醫院 - 藥劑科報廢流程管理系統"
   - `Color`: `RGBA(255, 255, 255, 1)`
   - `FontWeight`: `FontWeight.Bold`
   - `Size`: `18`
4. 插入右上角操作按鈕群：
   - **重設按鈕**：`Fill: RGBA(138, 136, 134, 1)`，`OnSelect: ResetForm(SharePointForm1)`
   - **儲存發送按鈕**：`Fill: RGBA(16, 124, 65, 1)`（醫療綠），`OnSelect: SubmitForm(SharePointForm1)`

### 第四步：配置左側歷史清單 Gallery (320px)
1. 插入【垂直資源庫 (Blank vertical gallery)】，命名為 `HistoryGallery`：
   - `X: 0, Y: 65, Width: 320, Height: Parent.Height - 65`
   - `Items`: `Sort('報廢網頁', Created, SortOrder.Descending)`
2. 在資源庫範本內加入卡片元素：
   - **藥名標籤**：`ThisItem.藥品名稱`（粗體，14px）
   - **藥號與日期**：`ThisItem.藥品代碼 & " | " & Text(ThisItem.報廢日期, "yyyy/mm/dd")`
   - **審核狀態徽章**：`ThisItem.審核狀態`（待審核顯示黃色底，已核准顯示綠色底）

### 第五步：建置右側 11 個標準表單欄位 (EditForm)
1. 插入【編輯表單 (Edit form)】，命名為 `SharePointForm1`：
   - `X: 340, Y: 85, Width: Parent.Width - 360, Height: Parent.Height - 105`
   - `DataSource`: `'報廢網頁'`
   - `Item`: `HistoryGallery.Selected`
2. 點擊右側【編輯欄位】，依序加入 11 個卡片：
   1. **藥品代碼 (藥號)**：卡片值 `DataCardValue1`
   2. **藥品名稱**：解除卡片鎖定，刪除原生文字框，插入 `ComboBox1`
   3. **報廢日期**：`DatePicker`，`DefaultDate: Today()`
   4. **申請人**：文字框，預設 `User().FullName`
   5. **複核人**：文字框
   6. **藥庫複核人員**：文字框
   7. **批號**：文字框
   8. **報廢數量**：文字框，格式設為數字
   9. **報廢原因**：下拉選單，`Items: ["藥品過期", "包裝破損 / 變質", "病患退藥無法再利用", "調配失誤報廢", "冷藏失效 / 溫控異常", "其他原因"]`
   10. **備註說明**：文字框，模式設為多行文字
   11. **照片或附件**：原生 Attachments 卡片

### 第六步：設定 ComboBox 與藥號雙向連動公式
1. **`ComboBox1`（藥品名稱）關鍵屬性**：
   - `Items`: `Sort(Filter(AllDrugs, IsBlank(Self.SearchText) Or StartsWith(藥品學名, Self.SearchText) Or StartsWith(藥號, Self.SearchText) Or Self.SearchText in 藥品學名), 藥品學名, SortOrder.Ascending)`
   - `IsSearchable`: `true`
   - `SearchFields`: `["藥品學名", "藥號"]`
   - `OnChange`:
     ```powerappsfl
     If(!IsBlank(Self.Selected.藥號),
         UpdateContext({ locDrugName: Self.Selected.藥品學名, locDrugCode: Self.Selected.藥號 });
         Reset(DataCardValue1)
     )
     ```
2. **`DataCardValue1`（藥品代碼文字框）關鍵屬性**：
   - `Default`: `If(!IsBlank(locDrugCode), locDrugCode, Parent.Default)`
   - `OnChange`（反向連動：輸入藥號反查藥名）：
     ```powerappsfl
     If(!IsBlank(Self.Text),
         With({ matched: LookUp(AllDrugs, 藥號 = Self.Text) },
             If(!IsBlank(matched.藥品學名),
                 UpdateContext({ locDrugName: matched.藥品學名, locDrugCode: Self.Text });
                 Reset(ComboBox1)
             )
         )
     )
     ```

---

## 🏥 路徑 C：將 App 發布至醫院 Microsoft Teams 頻道

1. 開啟院內 Microsoft Teams 電腦版或網頁版。
2. 進入【**藥劑科**】或【**藥庫溝通平台**】團隊頻道。
3. 點擊頂部索引標籤列右側的【**＋ (新增索引標籤)**】。
4. 在應用程式清單中選取【**Power Apps**】。
5. 在搜尋框輸入：`佳里奇美醫院 - 藥劑科報廢流程管理系統`，點擊選取並按【**儲存**】。
6. 👉 **成果**：全科藥師與主管免切換視窗，直接在 Teams 頂部即可填寫報廢單與查詢歷程！
