import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# 註冊中文字型
font_path = '/Library/Fonts/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('ArialUnicode', font_path))

pdf_filename = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/AI_Agent本地開發PowerApps與整合發布全流程指南.pdf'

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('ArialUnicode', 8)
        self.setFillColor(colors.HexColor('#64748B'))
        
        # 頁首 (第 2 頁開始)
        if self._pageNumber > 1:
            self.drawString(54, 800, '佳里奇美醫院 藥劑科 醫療自動化標準作業手冊 (SOP)')
            self.drawRightString(541, 800, '本地端即時模擬驗證與 Power Apps / Power BI 完整串接指南')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        # 頁尾
        self.drawString(54, 38, '機密等級：內部作業指南 · 未經授權請勿外流')
        page_text = f'第 {self._pageNumber} 頁 / 共 {page_count} 頁'
        self.drawRightString(541, 38, page_text)
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.5)
        self.line(54, 50, 541, 50)
        
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=A4,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    fontName='ArialUnicode',
    fontSize=18,
    leading=24,
    textColor=colors.HexColor('#0F172A'),
    alignment=1,
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    fontName='ArialUnicode',
    fontSize=11,
    leading=16,
    textColor=colors.HexColor('#0284C7'),
    alignment=1,
    spaceAfter=14
)

h1_style = ParagraphStyle(
    'SectionH1',
    fontName='ArialUnicode',
    fontSize=12,
    leading=16.5,
    textColor=colors.HexColor('#005A9E'),
    spaceBefore=11,
    spaceAfter=5,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    fontName='ArialUnicode',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=7,
    spaceAfter=3,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyDark',
    fontName='ArialUnicode',
    fontSize=8.8,
    leading=13.2,
    textColor=colors.HexColor('#334155'),
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'BulletText',
    fontName='ArialUnicode',
    fontSize=8.6,
    leading=12.8,
    textColor=colors.HexColor('#334155'),
    leftIndent=14,
    spaceAfter=2.5
)

story = []

# ==================== 第 1 頁：封面資訊與全流程架構圖 ====================
story.append(Spacer(1, 5))
story.append(Paragraph('佳里奇美醫院 藥劑科 醫療自動化專題手冊', subtitle_style))
story.append(Paragraph('AI Agent 本地端即時模擬驗證模式<br/>3,427 筆藥品連動、Teams 審核與 Power BI 串接全流程指南', title_style))
story.append(Spacer(1, 4))

# 資訊摘要盒
info_data = [
    [Paragraph('<b>文件編號</b>：CMH-PHARM-202609-SOP', body_style), Paragraph('<b>編製人員</b>：藥劑科智慧藥事小組 / Google Antigravity', body_style)],
    [Paragraph('<b>實作案例</b>：全院 3,427 筆藥品清冊與抗生素報廢管理', body_style), Paragraph('<b>發布日期</b>：2026 年 09 月 13 日', body_style)],
    [Paragraph('<b>核心技術</b>：本地高傳真模擬 · PAC CLI · Power BI 串接', body_style), Paragraph('<b>版本狀態</b>：正式版 (v2.1 完整指南發行)', body_style)]
]
t_info = Table(info_data, colWidths=[240, 247])
t_info.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_info)
story.append(Spacer(1, 8))

# 執行摘要
story.append(Paragraph('【執行摘要：本地端模擬驗證與跨端整合】', h1_style))
story.append(Paragraph('在建置全院海量藥品（3,427 筆）報廢表單時，傳統雲端 Low-Code 拖拉易遇到版面歪斜、重疊灰底與循環參考等困擾。本標準流程導入 <b>「本地高傳真互動模擬」</b>：藥師直接在本機瀏覽器打英文字母搜尋、測試藥號連動與紅框警戒，滿意後由 Agent 透過微軟官方 PAC CLI 編譯打包輸出實體 .msapp 上傳 Power Apps。資料庫更進一步與 Microsoft Teams 自動審核推播及 <b>Power BI 醫療戰情儀表板</b> 全面串接，實現臨床填報、行政審查與數據分析之完整閉環。', body_style))

# 流程圖展示
story.append(Spacer(1, 4))
story.append(Paragraph('【全流程視覺化架構圖】', h1_style))
img_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PowerApps_Agent開發流程圖.png'
if os.path.exists(img_path):
    story.append(Image(img_path, width=487, height=270))
story.append(Spacer(1, 6))

# 換頁進入第 2 頁
story.append(PageBreak())

# ==================== 第 2 頁：本地端模擬驗證五大步驟 ====================
story.append(Paragraph('第一章：本地端即時模擬驗證手把手教學（從 Excel 到 Power Apps）', h1_style))
story.append(Paragraph('以下完整說明臨床藥師如何配合 AI Agent，從一份本機 Excel 藥品表開始，走完開發、測試與雲端載入：', body_style))

story.append(Paragraph('步驟一：準備藥品清冊 Excel 與口述需求', h2_style))
story.append(Paragraph('1. <b>資料檔準備</b>：藥庫提供 <code>藥品藥號.xlsx</code>，涵蓋全院 3,427 筆藥品（主要欄位為「藥號」與「藥品學名」）。', bullet_style))
story.append(Paragraph('2. <b>口述介面規格</b>：例如向 Agent 說：「我想做抗生素報廢管理 App，純白醫療風格無灰底。要有四個欄位：病房號碼（下拉選單）、藥品名稱（打英文字母搜尋）、藥品代碼（自動帶出）、報廢數量（若大於 50 顆要自動跳紅色警告）。」', bullet_style))

story.append(Paragraph('步驟二：AI Agent 在本地端建立「高傳真互動模擬器」', h2_style))
story.append(Paragraph('1. Agent 在背景自動解析 <code>藥品藥號.xlsx</code>，將 3,427 筆資料轉換為本機高效率資料結構。', bullet_style))
story.append(Paragraph('2. Agent 生成等同 Power Apps 畫面規格的本機模擬環境，注入英文字母即時快篩、LookUp 藥號連動與紅框警訊。', bullet_style))

story.append(Paragraph('步驟三：臨床人員在本地端直接點選「實機驗收」', h2_style))
story.append(Paragraph('藥師本機直接開啟測試畫面（如 <code>抗生素報廢管理App_方法二本地驗收模擬器.html</code>）進行四大臨床驗證：', body_style))
story.append(Paragraph('• <b>A / AD 字母過濾驗證</b>：在藥品名稱輸入「A」，即時列出開頭為 A 的藥品；再鍵入「D」變成「AD」，清單瞬間收窄，反應時間 0.01 秒！', bullet_style))
story.append(Paragraph('• <b>藥號即時帶出驗證</b>：點選任一藥品（如 <code>ADI-PEG20 (40.25mg/V)針</code>），右側「藥品代碼」欄位瞬間自動填入 <code>10A000</code>，杜絕人工抄錯。', bullet_style))
story.append(Paragraph('• <b>超量防呆警戒驗證</b>：在報廢數量輸入「60」，邊框瞬間變紅並彈出「⚠️ 數量超過 50 顆，請確認是否須提報專案審核」警示。', bullet_style))
story.append(Paragraph('• <b>排版滿意度確認</b>：確認整體為純白醫療極簡風、無灰色重疊陰影、元件對齊方正。', bullet_style))

story.append(Paragraph('步驟四：驗收滿意 ➔ Agent 執行微軟官方 PAC CLI 一次打包', h2_style))
story.append(Paragraph('1. 藥師向 Agent 確認：「本地測試很順暢，可以打包！」', bullet_style))
story.append(Paragraph('2. Agent 將本地驗收成功的邏輯轉換為微軟標準 <code>Src/App.fx.yaml</code> 與 <code>Src/MainScreen1.fx.yaml</code>。', bullet_style))
story.append(Paragraph('3. 於終端機執行微軟官方打包指令：', bullet_style))
story.append(Paragraph('<code>pac canvas pack --sources [原始碼目錄] --msapp 抗生素報廢管理App.msapp</code>', bullet_style))
story.append(Paragraph('輸出微軟標準實體應用程式檔（約 62 KB），內部已封裝好完整的幾何排版與連動定義。', body_style))

story.append(Paragraph('步驟五：Power Apps 雲端載入與發布', h2_style))
story.append(Paragraph('藥師開啟微軟 Power Apps 網頁，點選 <b>「開啟」➔「瀏覽這部電腦」</b> 選取 <code>抗生素報廢管理App.msapp</code>：', body_style))
story.append(Paragraph('• 整套雙欄排版、藥名下拉、藥號自動連動與數量警戒邏輯 <b>1 秒瞬間完整還原在雲端</b>！', bullet_style))
story.append(Paragraph('• 藥師無需在網頁上手動微調任何像素，直接點擊「儲存」並「發布」給全院同仁使用。', bullet_style))

story.append(Spacer(1, 6))

# 第二章：Teams 審核流程
story.append(Paragraph('第二章：Microsoft Teams 主管審核與自適應卡片流程', h1_style))
story.append(Paragraph('表單送出後，後端透過 Power Automate 串接奇美醫院 Teams 審核機制：', body_style))
story.append(Paragraph('1. <b>自動化觸發</b>：當 SharePoint「報廢網頁」新增一筆報廢資料時，觸發流程。', bullet_style))
story.append(Paragraph('2. <b>Teams 自適應卡片 (Adaptive Card) 推播</b>：系統向藥庫主管發送專屬卡片，清晰呈現申請人、藥名、藥號、數量及原因。', bullet_style))
story.append(Paragraph('3. <b>一鍵快速簽核</b>：主管於手機或電腦 Teams 點擊「✅ 核准」或「❌ 退件」，審核狀態即時回寫 SharePoint。', bullet_style))
story.append(Paragraph('4. <b>雙平台權限隔離</b>：藥庫團隊具備完整管理權限，業務會議平台團隊則設定為純唯讀安全瀏覽。', bullet_style))

# 換頁進入第 3 頁
story.append(PageBreak())

# ==================== 第 3 頁：Power BI 完整串接手把手教學 ====================
story.append(Paragraph('第三章：如何將報廢資料庫完整串接到 Power BI？（手把手教學）', h1_style))
story.append(Paragraph('將 SharePoint「報廢網頁」與「藥品主檔」串接至 Power BI，能將單純的表單紀錄升級為<b>「全院藥事管理決策戰情室」</b>。以下為標準操作步驟：', body_style))

story.append(Paragraph('步驟一：在 Power BI Desktop 取得 SharePoint 清單資料', h2_style))
story.append(Paragraph('1. 開啟 Power BI Desktop，點擊頂部常用工具列的 <b>「取得資料」➔「更多...」</b>。', bullet_style))
story.append(Paragraph('2. 在搜尋框輸入「SharePoint」，選取 <b>「SharePoint 現代清單 (SharePoint Online List)」</b>，點擊「連線」。', bullet_style))
story.append(Paragraph('3. <b>輸入網站 URL</b>：輸入奇美醫院 Teams 關聯站台網址：', bullet_style))
story.append(Paragraph('<code>https://cmh2400.sharepoint.com/sites/msteams_d944ec</code>', bullet_style))
story.append(Paragraph('4. <b>驗證身分</b>：選擇左側「組織帳戶 (Microsoft 365)」，登入奇美醫院帳號（如 <code>B305W2@chimei.org.tw</code>）。', bullet_style))
story.append(Paragraph('5. <b>選取資料表</b>：勾選 <code>報廢網頁</code>（填報紀錄）與 <code>藥品主檔</code>（3,427 筆主檔），點擊「轉換資料」進入 Power Query。', bullet_style))

story.append(Paragraph('步驟二：Power Query 欄位清理與資料正規化', h2_style))
story.append(Paragraph('1. <b>展開關聯欄位</b>：在「報廢網頁」中，將藥品名稱、報廢原因等 Choice / LookUp 欄位點擊右上角展開圖示，選取 <code>Value</code>。', bullet_style))
story.append(Paragraph('2. <b>轉換資料型態</b>：', bullet_style))
story.append(Paragraph('• 將「報廢數量」設定為 <b>整數 (Int64)</b>。', bullet_style))
story.append(Paragraph('• 將「報廢日期」設定為 <b>日期 (Date)</b>。', bullet_style))
story.append(Paragraph('• 將「審核狀態」、「病房號碼」、「藥品代碼」維持 <b>文字 (Text)</b>。', bullet_style))
story.append(Paragraph('3. <b>建立主外鍵關聯</b>：點擊「關閉並套用」，在模型檢視中將「報廢網頁」的 <code>藥品代碼</code> 拖曳關聯至「藥品主檔」的 <code>Title (藥號)</code>，形成 1:N 星狀模型。', bullet_style))

story.append(Paragraph('步驟三：建立臨床報廢戰情儀表板三大核心指標', h2_style))

pbi_data = [
    [Paragraph('<b>視覺效果圖表</b>', body_style), Paragraph('<b>配置欄位與 DAX 公式</b>', body_style), Paragraph('<b>臨床管理價值</b>', body_style)],
    [
        Paragraph('<b>KPI 卡片：總報廢量</b>', body_style),
        Paragraph('<code>總報廢數量 = SUM(\'報廢網頁\'[報廢數量])</code>', body_style),
        Paragraph('即時掌握全院本月或各病房目前累積之藥品耗損總量。', body_style)
    ],
    [
        Paragraph('<b>條形圖：高耗損排行</b>', body_style),
        Paragraph('Y 軸：藥品名稱<br/>X 軸：報廢數量（依數量降冪排列 Top 10）', body_style),
        Paragraph('一眼看出全院耗損最嚴重的藥品品項，優先介入管控。', body_style)
    ],
    [
        Paragraph('<b>環形圖：報廢原因分析</b>', body_style),
        Paragraph('圖例：報廢原因<br/>值：項目計數（逾期/破損/換藥退回）', body_style),
        Paragraph('精準釐清是「逾期失效」多還是「臨床退藥」多，利於評鑑檢討。', body_style)
    ],
    [
        Paragraph('<b>矩陣表：超量專案清單</b>', body_style),
        Paragraph('列：病房、申請人、日期；篩選：報廢數量 > 50', body_style),
        Paragraph('列出所有單次報廢大於 50 顆之異常明細，供主任審核複查。', body_style)
    ]
]
t_pbi = Table(pbi_data, colWidths=[110, 230, 147])
t_pbi.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_pbi)
story.append(Spacer(1, 6))

story.append(Paragraph('步驟四：在 Power BI 內反向嵌入 Power Apps（作業與分析二合一）', h2_style))
story.append(Paragraph('1. 在 Power BI 視覺效果窗格點擊 <b>「Power Apps」</b> 圖示。', bullet_style))
story.append(Paragraph('2. 將資料表中的 <code>藥品代碼</code>、<code>ID</code> 拖入 PowerApps 資料欄位中。', bullet_style))
story.append(Paragraph('3. 於畫面內選擇已發布之「抗生素報廢管理 App」：', bullet_style))
story.append(Paragraph('• <b>雙向閉環神效</b>：主管在 Power BI 點選某一筆異常報廢藥品，嵌入的 Power Apps 畫面會 <b>「連動過濾出該筆申請」</b>，主管可直接在 Power BI 報表內點選「專案核准」或填寫意見，無需在系統間來回切換！', body_style))

story.append(Spacer(1, 6))
story.append(Paragraph('【總結】', h1_style))
story.append(Paragraph('從本地端 0.01 秒模擬驗證、PAC CLI 標準封裝，到 Teams 自適應卡片審核與 Power BI 視覺化儀表板串接，佳里奇美醫院藥劑科已完整實現<b>「前端填報敏捷化 · 中端審核自動化 · 後端分析智慧化」</b>的現代醫療資訊標準架構！', body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print('Comprehensive PDF with Power BI Integration generated successfully!')
