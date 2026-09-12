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

pdf_filename = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/醫院PRN系統整合指南_微軟自動化工具串接全流程.pdf'

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
            self.drawString(54, 800, '佳里奇美醫院 藥劑科 智慧藥事自動化專題手冊')
            self.drawRightString(541, 800, '醫院 PRN 系統與本地 AI Agent 防火牆穿透整合指南')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        self.drawString(54, 38, '機密等級：院內專案指南 · 智慧醫療自動化教材')
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
    fontSize=17,
    leading=23,
    textColor=colors.HexColor('#0F172A'),
    alignment=1,
    spaceAfter=5
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    fontName='ArialUnicode',
    fontSize=10.5,
    leading=15,
    textColor=colors.HexColor('#0284C7'),
    alignment=1,
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'SectionH1',
    fontName='ArialUnicode',
    fontSize=11.5,
    leading=16,
    textColor=colors.HexColor('#005A9E'),
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    fontName='ArialUnicode',
    fontSize=9.8,
    leading=13.8,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=6,
    spaceAfter=2.5,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyDark',
    fontName='ArialUnicode',
    fontSize=8.6,
    leading=13,
    textColor=colors.HexColor('#334155'),
    spaceAfter=3.5
)

bullet_style = ParagraphStyle(
    'BulletText',
    fontName='ArialUnicode',
    fontSize=8.4,
    leading=12.5,
    textColor=colors.HexColor('#334155'),
    leftIndent=14,
    spaceAfter=2
)

story = []

# ==================== 第 1 頁：PRN 定位與全流程架構圖 ====================
story.append(Spacer(1, 4))
story.append(Paragraph('佳里奇美醫院 藥劑科 智慧藥事專題指南', subtitle_style))
story.append(Paragraph('醫院 PRN 系統整合與筆電 AI Agent 協同作戰手冊<br/>突破防火牆限制：本地模擬、微軟自動化串接與 Power BI 全流程閉環', title_style))
story.append(Spacer(1, 4))

info_data = [
    [Paragraph('<b>手冊代號</b>：CMH-PHARM-PRN-AGENT', body_style), Paragraph('<b>編製小組</b>：藥劑科智慧藥事小組 / Google Antigravity', body_style)],
    [Paragraph('<b>整合範疇</b>：院內 PRN 系統 · 本地 AI Agent · 醫療防火牆', body_style), Paragraph('<b>發布日期</b>：2026 年 09 月 13 日', body_style)],
    [Paragraph('<b>技術架構</b>：PRN + 本地 Agent + Power Platform + Teams + BI', body_style), Paragraph('<b>版本狀態</b>：正式版 (v2.0 旗艦發行)', body_style)]
]
t_info = Table(info_data, colWidths=[240, 247])
t_info.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_info)
story.append(Spacer(1, 6))

story.append(Paragraph('【核心解析：PRN 在整個系統中到底是什麼角色？】', h1_style))
story.append(Paragraph('在醫療實務中，<b>PRN（pro re nata，需要時使用）</b>是病房最常見但也是管理最棘手的醫囑類型（如退燒止痛針、緊急抗生素、氣喘吸入劑或鎮靜安眠藥）。病房通常會備妥一定數量的「PRN 常備藥」。<br/>'
                       '在整套自動化架構中，<b>PRN 扮演「業務發起的火車頭（起點）」與「藥品帳料核銷的終點」</b>：<br/>'
                       '1. <b>源頭產生事件</b>：病房 PRN 藥品因「過期、開瓶破損、病人出院停藥未拆封但已退回」產生報廢需求。<br/>'
                       '2. <b>串接 Power Apps</b>：護理師或藥師直接調用 PRN 藥號與病房資訊，免手動重複登打。<br/>'
                       '3. <b>貫穿審核與戰情</b>：經 Teams 主管核准後，自動回扣 PRN 常備庫存，並由 Power BI 監控各病房 PRN 備藥是否過剩！', body_style))

story.append(Spacer(1, 4))
story.append(Paragraph('【PRN 系統與微軟五大工具串接架構圖】', h1_style))
flow_img = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PRN系統與微軟五大工具串接架構圖.png'
if os.path.exists(flow_img):
    story.append(Image(flow_img, width=487, height=270))
story.append(Spacer(1, 6))

story.append(PageBreak())

# ==================== 第 2 頁：筆電 AI Agent 突破防火牆的四大超能力 ====================
story.append(Paragraph('第一章：自己的筆電有 AI Agent，如何突破醫院防火牆輕鬆搞定 PRN 整合？', h1_style))
story.append(Paragraph('醫院網路具備極高規格的<b>「醫療內外網實體隔離與資安防火牆」</b>，院外筆電無法直接連入醫院 HIS 資料庫。此時，您個人筆電上的 <b>AI Agent 正是完美的「中繼智慧外掛」</b>！以下詳解 Agent 究竟能為您做什麼：', body_style))

story.append(Paragraph('超能力一：離線無感沙盒（在筆電建立 3,427 筆真實資料的高傳真模擬器）', h2_style))
story.append(Paragraph('• <b>痛點</b>：在院內連線慢，被資安限制無法隨意安裝工具，直接在線上改 Power Apps 容易當機或改壞。', bullet_style))
story.append(Paragraph('• <b>Agent 作法</b>：您只需從院內匯出一次 Excel 脫敏清冊（如 <code>藥品藥號.xlsx</code>），Agent 在您的個人筆電本機建立完全一模一樣的 HTML 互動環境。您在完全斷網/無防火牆限制下，打 A/AD 驗收秒搜、測試藥號帶出與紅框防呆，測試滿意再上線！', bullet_style))

story.append(Paragraph('超能力二：口述轉 Code-First（您動口、Agent 寫 YAML 與公式）', h2_style))
story.append(Paragraph('• <b>痛點</b>：醫院同仁要記住 <code>LookUp</code>、<code>Sort</code>、<code>Distinct</code> 等複雜語法非常痛苦，且極易引發循環參考。', bullet_style))
story.append(Paragraph('• <b>Agent 作法</b>：您只要用口述：「我要增加一個 PRN 切換紐，點選 PRN 只顯示該病房的常備退藥」，Agent 在 10 秒內自動在筆電寫好精準的 <code>App.fx.yaml</code> 原始碼，杜絕任何人為語法失誤。', bullet_style))

story.append(Paragraph('超能力三：微軟官方工具鏈本機打包（輸出合規實體 .msapp 檔案）', h2_style))
story.append(Paragraph('• <b>痛點</b>：醫院防火牆會阻擋未授權的雲端傳輸與外掛安裝。', bullet_style))
story.append(Paragraph('• <b>Agent 作法</b>：Agent 透過微軟官方 <code>PAC CLI (Power Platform CLI)</code>，在您的個人筆電本地端直接將寫好的原始碼編譯封裝成微軟官方標準的 <code>.msapp</code> 實體檔案。這個檔案完全合規、無毒，您只要用隨身碟或院內 Teams 一傳，進院內點擊「開啟」就能瞬間上線！', bullet_style))

story.append(Paragraph('超能力四：Power Automate 審核流程包自動建構（.zip 一鍵匯入）', h2_style))
story.append(Paragraph('• <b>痛點</b>：在院內點選 Power Automate 幾十個節點、排版 Teams 自適應卡片 JSON 容易眼花撩亂。', bullet_style))
story.append(Paragraph('• <b>Agent 作法</b>：Agent 在筆電直接生成標準 JSON 流程定義檔，並自動打包成 <code>.zip 流程匯入包</code>。您進院內點擊「匯入流程」，整套「主管審核卡推播、核准回寫 SharePoint、Teams 公告」幾秒鐘全自動組裝完畢！', bullet_style))

story.append(Spacer(1, 6))

story.append(Paragraph('第二章：突破防火牆的「四步跨網實作法」', h1_style))

agent_table = [
    [Paragraph('<b>步驟</b>', body_style), Paragraph('<b>在外網（您自己的個人筆電）</b>', body_style), Paragraph('<b>在內網（醫院辦公室電腦）</b>', body_style)],
    [
        Paragraph('<b>1. 需求與資料</b>', body_style),
        Paragraph('口述需求給 Agent，載入本地藥品清冊。', body_style),
        Paragraph('自 PRN 系統匯出藥品 Excel 清冊。', body_style)
    ],
    [
        Paragraph('<b>2. 模擬與驗收</b>', body_style),
        Paragraph('Agent 生成高傳真模擬器，您在本機親自測試連動。', body_style),
        Paragraph('免受院內網路延遲干擾，專注於臨床體驗確認。', body_style)
    ],
    [
        Paragraph('<b>3. 編譯與打包</b>', body_style),
        Paragraph('Agent 執行 PAC CLI，輸出實體 <code>.msapp</code> 與流程包。', body_style),
        Paragraph('透過院內合規通道（Teams/隨身碟）帶入內網。', body_style)
    ],
    [
        Paragraph('<b>4. 雲端一鍵上線</b>', body_style),
        Paragraph('由 Agent 產出操作手冊與指引。', body_style),
        Paragraph('Power Apps 點選「瀏覽」，1 秒載入全院正式發布！', body_style)
    ]
]
t_agent = Table(agent_table, colWidths=[90, 200, 197])
t_agent.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_agent)

story.append(PageBreak())

# ==================== 第 3 頁：PRN 臨床作業閉環與 Power BI 戰情 ====================
story.append(Paragraph('第三章：PRN 藥品報廢全院業務閉環（Teams + SharePoint + Power BI）', h1_style))
story.append(Paragraph('透過 Agent 在筆電打包完成並上傳院內後，PRN 報廢流程將完整串通微軟醫療生態系：', body_style))

# 業務流程表格
biz_flow = [
    [Paragraph('<b>階段流程</b>', body_style), Paragraph('<b>執行角色與工具</b>', body_style), Paragraph('<b>自動化處理與技術核心</b>', body_style)],
    [
        Paragraph('<b>1. 填報申請</b>', body_style),
        Paragraph('病房/藥庫藥師<br/>(Power Apps / Teams)', body_style),
        Paragraph('同仁在 Teams 索引標籤開啟 App，選取 PRN 藥名即時帶出藥號與預設今日日期，送出寫入 SharePoint 清單。', body_style)
    ],
    [
        Paragraph('<b>2. 主管審核</b>', body_style),
        Paragraph('護理長 / 藥庫主任<br/>(Teams 自適應卡片)', body_style),
        Paragraph('Power Automate 偵測 PRN 報廢單，若數量 > 50 顆啟動專案複核，向主管 Teams 機器人發送 Adaptive Card，主管一鍵簽核。', body_style)
    ],
    [
        Paragraph('<b>3. 帳料核銷</b>', body_style),
        Paragraph('HIS PRN 常備庫存<br/>(自動反向沖帳)', body_style),
        Paragraph('簽核通過後，自動將審核結果更新回 SharePoint，並推播通知護理站「已核准，明日補發 PRN 常備品項」。', body_style)
    ],
    [
        Paragraph('<b>4. 戰情分析</b>', body_style),
        Paragraph('科主任 / 品保小組<br/>(Power BI 儀表板)', body_style),
        Paragraph('串接 SharePoint 資料庫，統計各病房 PRN 耗損 Top 10 與過期原因，主管可在報表內反向操作 App 觸發補藥！', body_style)
    ]
]
t_biz = Table(biz_flow, colWidths=[90, 130, 267])
t_biz.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_biz)
story.append(Spacer(1, 8))

story.append(Paragraph('第四章：Power BI PRN 專屬三大戰情指標', h1_style))

pbi_data = [
    [Paragraph('<b>戰情圖表</b>', body_style), Paragraph('<b>配置欄位與 DAX 公式</b>', body_style), Paragraph('<b>臨床管理與評鑑價值</b>', body_style)],
    [
        Paragraph('<b>PRN 耗損週轉率<br/>(折線圖)</b>', body_style),
        Paragraph('X 軸：月份；Y 軸：報廢數量加總<br/>圖例：各病房（5A/6B/ICU）', body_style),
        Paragraph('一眼看出哪些病房的 PRN 常備藥常放到過期，及時調降核准配額，杜絕浪費。', body_style)
    ],
    [
        Paragraph('<b>高額損耗藥品 Top 10<br/>(橫條圖)</b>', body_style),
        Paragraph('Y 軸：藥品學名<br/>X 軸：報廢總金額（數量 × 單價）', body_style),
        Paragraph('揪出耗損金額最高的 PRN 藥品（如昂貴針劑），優先介入改用小包裝。', body_style)
    ],
    [
        Paragraph('<b>退藥原因深度剖析<br/>(樹狀結構圖)</b>', body_style),
        Paragraph('類別：逾期失效 / 開瓶破損 / 停藥退回<br/>數值：報廢項目筆數', body_style),
        Paragraph('若「停藥退回」頻次異常偏高，藥師可主動輔導臨床醫師開立 PRN 之適應症。', body_style)
    ]
]
t_pbi = Table(pbi_data, colWidths=[110, 190, 187])
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

story.append(Paragraph('【總結：AI Agent 賦能醫療人員】', h1_style))
story.append(Paragraph('透過<b>「個人筆電 AI Agent 本地先行開發 ➔ PAC CLI 合規打包 ➔ 穿透防火牆至院內發布」</b>的敏捷模式，醫療人員完全不再受限於內網封閉環境與繁瑣語法。您只要專注於臨床邏輯與病患照護，所有複雜的架構、程式碼編寫與流程串接，全部由 AI Agent 在幕後為您輕鬆搞定！', body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print('Updated PRN & AI Agent Guide PDF generated successfully at:', pdf_filename)
