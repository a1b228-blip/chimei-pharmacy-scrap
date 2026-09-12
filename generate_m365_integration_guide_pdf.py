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

# 註冊字型
font_path = '/Library/Fonts/Arial Unicode.ttf'
pdfmetrics.registerFont(TTFont('ArialUnicode', font_path))

pdf_filename = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/醫院IT新手專案指南_微軟五大工具完整串接SOP.pdf'

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
        
        if self._pageNumber > 1:
            self.drawString(54, 800, '佳里奇美醫院 藥劑科 醫療自動化基礎建設手冊')
            self.drawRightString(541, 800, '醫院 IT 新手從零上手：微軟五大工具完整串接 SOP')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        self.drawString(54, 38, '機密等級：院內專案指南 · 醫療自動化教育訓練教材')
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

# ==================== 第 1 頁：五大工具定位與全流程串接圖 ====================
story.append(Spacer(1, 5))
story.append(Paragraph('佳里奇美醫院 藥劑科 醫療自動化教育手冊', subtitle_style))
story.append(Paragraph('醫院 IT 新手從零上手專案指南<br/>Power Apps · Automate · SharePoint · Power BI · Teams 串接全攻略', title_style))
story.append(Spacer(1, 4))

info_data = [
    [Paragraph('<b>手冊代號</b>：CMH-IT-GUIDE-001 (小白入門版)', body_style), Paragraph('<b>編製單位</b>：藥劑科智慧藥事小組 / Google Antigravity', body_style)],
    [Paragraph('<b>適用情境</b>：藥品報廢 / 盤點 / 醫材申請等各類表單', body_style), Paragraph('<b>發布日期</b>：2026 年 09 月 13 日', body_style)],
    [Paragraph('<b>串接核心</b>：五大工具角色分工與資料單向流轉', body_style), Paragraph('<b>閱讀對象</b>：臨床藥師、護理長、各單位專案同仁', body_style)]
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

story.append(Paragraph('【核心觀念：五大工具在醫院專案中到底扮演什麼角色？】', h1_style))
story.append(Paragraph('很多醫療同仁剛接觸微軟工具時，常被一堆「Power」搞混。其實只要記住這句<b>「蓋房子口訣」</b>，整個架構就一清二楚：<br/>'
                       '• <b>SharePoint 是「地基與倉庫」</b>：負責把所有資料一行一行整齊存好。<br/>'
                       '• <b>Power Apps 是「漂亮的大門與前台櫃檯」</b>：讓同仁舒服填寫，並在第一線防呆擋下錯誤。<br/>'
                       '• <b>Power Automate 是「水管與輸送帶」</b>：有人送單，它就默默在背後把資料送去給主管簽核。<br/>'
                       '• <b>Microsoft Teams 是「廣播站與辦公桌」</b>：主管在手機或電腦直接收到卡片通知，按一個鈕就核准。<br/>'
                       '• <b>Power BI 是「院長室的戰情大螢幕」</b>：將幾萬筆歷史紀錄變成漂亮的圖表與趨勢分析。', body_style))

story.append(Spacer(1, 4))
story.append(Paragraph('【微軟五大工具串接架構圖】', h1_style))
flow_img = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/微軟五大工具串接架構圖.png'
if os.path.exists(flow_img):
    story.append(Image(flow_img, width=487, height=270))
story.append(Spacer(1, 6))

story.append(PageBreak())

# ==================== 第 2 頁：從頭開始手把手四步串接法 ====================
story.append(Paragraph('第一章：醫院專案四大串接步驟（由底層到上層順序走）', h1_style))
story.append(Paragraph('IT 新手請務必按照<b>「先建倉庫 ➔ 再做前台 ➔ 接上水管 ➔ 擺上戰情螢幕」</b>的黃金順序進行，千萬不要倒著做！', body_style))

story.append(Paragraph('第 1 步：在 SharePoint 建置清單（建倉庫）', h2_style))
story.append(Paragraph('1. <b>建立清單</b>：進入院內 Teams 關聯站台，點選「+ 新增」➔「清單」，命名為 <code>報廢網頁</code>。', bullet_style))
story.append(Paragraph('2. <b>規劃標準欄位</b>（避免中文特殊字元作為內部名稱）：', bullet_style))
story.append(Paragraph('• <b>Title (單行文字)</b>：儲存「申請人」或「單號」。', bullet_style))
story.append(Paragraph('• <b>藥品代碼 (單行文字)</b>：儲存 6 碼藥號（例如 <code>10A000</code>）。', bullet_style))
story.append(Paragraph('• <b>藥品名稱 (單行文字)</b>：儲存完整藥品學名。', bullet_style))
story.append(Paragraph('• <b>報廢數量 (數字)</b>：設定為整數。', bullet_style))
story.append(Paragraph('• <b>報廢原因 (選項 Choice)</b>：逾期、破損、換藥退回、溫度異常。', bullet_style))
story.append(Paragraph('• <b>審核狀態 (選項 Choice)</b>：待審核、已核准、退件。', bullet_style))
story.append(Paragraph('3. <b>匯入輔助對照主檔</b>：點選「從 Excel 新增」，將 <code>藥品藥號.xlsx</code> 匯入建立 <code>藥品主檔</code>（3,427 筆），作為選單對照依據。', bullet_style))

story.append(Paragraph('第 2 步：在 Power Apps 綁定 SharePoint 並做出防呆介面（做前台）', h2_style))
story.append(Paragraph('1. <b>連接資料來源</b>：在 Power Apps 左側圓柱體圖示（資料），點選「新增資料」➔ 搜尋「SharePoint」➔ 選取 <code>報廢網頁</code> 與 <code>藥品主檔</code>。', bullet_style))
story.append(Paragraph('2. <b>配置智慧下拉與自動帶出</b>：', bullet_style))
story.append(Paragraph('• 藥品名稱 ComboBox Items：<code>Sort(Distinct(藥品主檔, 藥品學名), Value, Ascending)</code>。', bullet_style))
story.append(Paragraph('• 藥品代碼 TextInput Default：<code>LookUp(藥品主檔, 藥品學名 = ComboBox1.Selected.Value).Title</code>。', bullet_style))
story.append(Paragraph('• <b>超量警報</b>：數量框邊框顏色設為 <code>If(Value(Self.Text) > 50, Color.Red, RGBA(206,212,218,1))</code>。', bullet_style))
story.append(Paragraph('3. <b>送出按鈕公式</b>：', bullet_style))
story.append(Paragraph('<code>Patch(報廢網頁, Defaults(報廢網頁), { 藥品代碼: CodeInput.Text, 藥品名稱: DrugCombo.Selected.Value, 報廢數量: Value(QtyInput.Text), 審核狀態: { Value: "待審核" } }); Notify("報廢單送出成功！", NotificationType.Success); ResetForm()</code>', bullet_style))

story.append(Paragraph('第 3 步：在 Power Automate 串接 Teams 自動化審核推播（接水管）', h2_style))
story.append(Paragraph('1. <b>建立雲端流程</b>：進入 Power Automate，建立「自動化雲端流程」。', bullet_style))
story.append(Paragraph('2. <b>設定觸發條件</b>：搜尋 SharePoint，選擇 <b>「建立項目時 (When an item is created)」</b>，選取網站與 <code>報廢網頁</code> 清單。', bullet_style))
story.append(Paragraph('3. <b>取得主管資訊</b>：新增動作「取得主管 (V2) (Get manager V2)」，User 填入觸發者的電子郵件 <code>Author Email</code>。', bullet_style))
story.append(Paragraph('4. <b>發送 Teams 自適應卡片並等候回應</b>：', bullet_style))
story.append(Paragraph('• 動作選取：<code>Post adaptive card and wait for a response</code>。', bullet_style))
story.append(Paragraph('• 收件者：填入主管信箱；卡片內文放入藥名、數量、原因與「✅ 核准」/「❌ 退件」按鈕。', bullet_style))
story.append(Paragraph('5. <b>更新審核結果回 SharePoint</b>：', bullet_style))
story.append(Paragraph('新增 SharePoint「更新項目」動作，將卡片回傳的結果更新回該筆資料的「審核狀態」欄位。', bullet_style))

story.append(Spacer(1, 6))

story.append(PageBreak())

# ==================== 第 3 頁：Teams 頻道整合與 Power BI 串接 ====================
story.append(Paragraph('第 4 步：在 Microsoft Teams 頻道發布並設定權限隔離', h2_style))
story.append(Paragraph('1. <b>將 App 發布至 Teams 頻道</b>：', bullet_style))
story.append(Paragraph('• 進入 Teams 的「藥庫溝通平台」頻道，點擊頂端「+」新增索引標籤。', bullet_style))
story.append(Paragraph('• 搜尋「Power Apps」，選取剛才做好的「抗生素報廢管理 App」並儲存。同仁打開 Teams 就能直接填報！', bullet_style))
story.append(Paragraph('2. <b>雙團隊權限隔離設計</b>：', bullet_style))
story.append(Paragraph('• <b>藥庫核心團隊</b>：在 SharePoint 賦予「編輯」權限，同仁能開單、主管能簽核。', bullet_style))
story.append(Paragraph('• <b>業務會議同仁</b>：在 SharePoint 賦予「檢視者 (Read-Only)」權限，僅供開會查閱紀錄，無法竄改資料。', bullet_style))

story.append(Paragraph('第 5 步：在 Power BI 串接資料庫製作全院戰情儀表板', h2_style))
story.append(Paragraph('1. <b>連線資料庫</b>：開啟 Power BI Desktop ➔ 取得資料 ➔ SharePoint Online 清單 ➔ 輸入站台網址並登入奇美醫院帳號。', bullet_style))
story.append(Paragraph('2. <b>資料型態設定</b>：將「報廢數量」轉為整數、「報廢日期」轉為日期。', bullet_style))
story.append(Paragraph('3. <b>三大經典儀表板實作</b>：', bullet_style))

dash_data = [
    [Paragraph('<b>戰情圖表</b>', body_style), Paragraph('<b>欄位設定</b>', body_style), Paragraph('<b>解決的醫療行政問題</b>', body_style)],
    [
        Paragraph('<b>高耗損藥品排行<br/>(橫條圖)</b>', body_style),
        Paragraph('Y 軸：藥品名稱<br/>X 軸：報廢數量加總 (Top 10)', body_style),
        Paragraph('揪出本月哪種抗生素報廢最多，針對高價品項檢討庫存安全存量。', body_style)
    ],
    [
        Paragraph('<b>報廢原因佔比<br/>(甜甜圈圖)</b>', body_style),
        Paragraph('圖例：報廢原因<br/>值：申請筆數計數', body_style),
        Paragraph('分析是「過期」多還是「病人退藥」多，做為評鑑改善方針。', body_style)
    ],
    [
        Paragraph('<b>反向操作審核<br/>(嵌入 Power Apps)</b>', body_style),
        Paragraph('插入 Power Apps 視覺效果<br/>傳遞選定藥品代碼', body_style),
        Paragraph('主任看報表發現異常，直接在 Power BI 點按鈕標記或退件，免開其他網頁！', body_style)
    ]
]
t_dash = Table(dash_data, colWidths=[110, 190, 187])
t_dash.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_dash)
story.append(Spacer(1, 8))

story.append(Paragraph('第二章：醫院 IT 新手避坑清單 (Top 4 常犯地雷)', h1_style))
story.append(Paragraph('1. <b>地雷一：SharePoint 欄位不要頻繁改內部名稱</b>：在 SharePoint 建立欄位時，先用英文命名儲存後，再改顯示名稱為中文，可杜絕 Power Apps 與 Automate 抓到亂碼內部名稱（如 <code>OData__x5831_</code>）。', bullet_style))
story.append(Paragraph('2. <b>地雷二：千萬不要把計算邏輯寫死在 Automate 裡面</b>：簡單防呆（如數量 > 50 變紅）在 Power Apps 前端做好；審核傳遞才交給 Automate，職責分明最穩健。', bullet_style))
story.append(Paragraph('3. <b>地雷三：Power Apps 下拉選單不要反向讀取文字框</b>：遵循單向資料流（選單驅動文字框），選單本身的 Default 留空，永遠不會引發循環參考。', bullet_style))
story.append(Paragraph('4. <b>地雷四：Power BI 排程重新整理權限</b>：發布至 Power BI 服務後，務必至資料集設定重新輸入奇美組織帳號 OAuth 憑證，報表才會每天自動更新。', bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph('【給新手的一句話鼓勵】', h1_style))
story.append(Paragraph('微軟五大工具的本質就是「各司其職」：資料歸 SharePoint、門面交 Power Apps、跑腿找 Automate、辦公在 Teams、決策看 Power BI。只要照著這份指南走，即使沒有資訊科系背景，您也能獨立打造出全院級的醫療自動化系統！', body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print('Beginner Guide PDF generated successfully at:', pdf_filename)
