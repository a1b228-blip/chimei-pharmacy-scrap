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

pdf_filename = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PRN醫療自動化智慧導航版面整合指南.pdf'

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
            self.drawRightString(541, 800, 'PRN (Pro Re Nata) 智慧導航版面與本地 AI Agent 串接指南')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        self.drawString(54, 38, '機密等級：院內專案指南 · 醫療自動化教育手冊')
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

# ==================== 第 1 頁：PRN 智慧導航版面定位與架構圖 ====================
story.append(Spacer(1, 4))
story.append(Paragraph('佳里奇美醫院 藥劑科 醫療自動化專題指南', subtitle_style))
story.append(Paragraph('PRN 醫療自動化智慧導航版面整合手冊<br/>Pro Re Nata 智慧中樞、本地 AI Agent 突破防火牆與全流程閉環', title_style))
story.append(Spacer(1, 4))

info_data = [
    [Paragraph('<b>手冊代號</b>：CMH-PHARM-PRN-PORTAL', body_style), Paragraph('<b>編製小組</b>：藥劑科智慧藥事小組 / Google Antigravity', body_style)],
    [Paragraph('<b>系統全名</b>：PRN (Pro Re Nata) 醫療自動化智慧導航', body_style), Paragraph('<b>發布日期</b>：2026 年 09 月 13 日', body_style)],
    [Paragraph('<b>架構定位</b>：PRN 智慧門戶 + 本地 Agent + 醫療自動化鐵三角', body_style), Paragraph('<b>版本狀態</b>：正式版 (v3.0 正式發行)', body_style)]
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
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_info)
story.append(Spacer(1, 6))

story.append(Paragraph('【核心正名與定位：什麼是「PRN 醫療自動化智慧導航版面」？】', h1_style))
story.append(Paragraph('<b>PRN（全名：Pro Re Nata，拉丁文原意為「隨需要而生、因應需求而設」）</b>，在院內是專為同仁打造的<b>「醫療自動化智慧總導航入口（Portal Dashboard）」</b>！<br/>'
                       '很多同仁日常要填報廢、做盤點、查主檔、看審核，要在 Teams、網頁、HIS 間切換非常混亂。<b>PRN 智慧導航版面正是「全院單一服務入口（Single Entrance）」</b>：<br/>'
                       '1. <b>總指揮官角色</b>：同仁只需打開 PRN 導航首頁，就能一覽「藥品報廢、盤點申請、常備查驗」等所有自動化模組。<br/>'
                       '2. <b>智慧身分分流</b>：登入 PRN 版面時，系統依角色自動導航（護理師看到填報卡片；藥庫主管看到簽核匣；科主任看到戰情儀表板）。<br/>'
                       '3. <b>微軟自動化母港</b>：PRN 智慧導航作為頂層母架構，內部嵌入 Power Apps 填報表單、對接 SharePoint 資料庫，並將審核推至 Teams、戰情連回 Power BI，形成完美的智慧閉環！', body_style))

story.append(Spacer(1, 4))
story.append(Paragraph('【PRN 智慧導航中樞與微軟自動化工具串接架構圖】', h1_style))
flow_img = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PRN系統與微軟五大工具串接架構圖.png'
if os.path.exists(flow_img):
    story.append(Image(flow_img, width=487, height=270))
story.append(Spacer(1, 6))

story.append(PageBreak())

# ==================== 第 2 頁：筆電 AI Agent 突破防火牆的超能力 ====================
story.append(Paragraph('第一章：自己的筆電有 AI Agent，如何突破醫院防火牆輕鬆完成 PRN 系統整合？', h1_style))
story.append(Paragraph('奇美醫院為了資安嚴格實施<b>「醫療內外網隔離與防火牆」</b>，您的個人筆電無法直接觸碰院內伺服器，且院內辦公電腦通常無法隨意安裝 Python、CLI 或開發套件。此時，您個人筆電上的 <b>AI Agent 正是您的「外網智慧工程師」</b>，用最輕巧的方式跨越網閘：', body_style))

story.append(Paragraph('超能力一：離線無感沙盒（在筆電建立 3,427 筆真實資料的高傳真模擬器）', h2_style))
story.append(Paragraph('• <b>臨床痛點</b>：在院內線上修改 PRN 導航與 Power Apps 容易當機、卡在 99%，或因防火牆延遲引發錯誤。', bullet_style))
story.append(Paragraph('• <b>Agent 助攻</b>：您只需從院內帶出一份脫敏 Excel（如 <code>藥品藥號.xlsx</code>），Agent 在您的個人筆電建立 100% 還原的 HTML 互動版面。在完全離線、無防火牆限制下，打 A/AD 驗證 0.01 秒秒搜、測試藥號帶出與紅框防呆，測試到 100% 滿意才上線！', bullet_style))

story.append(Paragraph('超能力二：口述需求轉 Code-First（您動口、Agent 寫 YAML 與公式）', h2_style))
story.append(Paragraph('• <b>臨床痛點</b>：要在 PRN 導航中新增子功能，手動排版容易歪斜，記住 <code>LookUp</code>、<code>Sort</code> 語法極易踩中循環參考。', bullet_style))
story.append(Paragraph('• <b>Agent 助攻</b>：您只要對 Agent 說：「我想在 PRN 導航中加入一個抗生素報廢模組，要純白雙欄、數量超過 50 顆亮紅框」，Agent 10 秒內自動在筆電寫好精準的 <code>App.fx.yaml</code> 程式碼，完全免動手寫程式。', bullet_style))

story.append(Paragraph('超能力三：微軟官方工具鏈本機打包（輸出合規實體 .msapp 檔案）', h2_style))
story.append(Paragraph('• <b>臨床痛點</b>：醫院防火牆阻擋未經簽章的外部連線與第三方外掛。', bullet_style))
story.append(Paragraph('• <b>Agent 助攻</b>：Agent 透過微軟官方 <code>PAC CLI</code>，在您的個人筆電本地端直接編譯封裝成微軟官方標準的 <code>.msapp</code> 實體檔案（約 62 KB）。這份檔案完全合規、無資安風險，透過院內 Teams 或隨身碟傳入內網，於 Power Apps 點擊「開啟」，1 秒鐘在院內雲端完整還原！', bullet_style))

story.append(Paragraph('超能力四：Power Automate 流程包自動打包（.zip 一鍵匯入）', h2_style))
story.append(Paragraph('• <b>臨床痛點</b>：在院內手動拖拉 Power Automate 節點與自適應卡片 JSON 耗時費力。', bullet_style))
story.append(Paragraph('• <b>Agent 助攻</b>：Agent 在筆電直接生成標準 JSON 流程定義檔，並自動壓縮成 <code>.zip 流程匯入包</code>。您進院內點擊「匯入」，整套「Teams 主管審核卡推播、自動回寫 SharePoint」幾秒鐘全自動組裝就緒！', bullet_style))

story.append(Spacer(1, 6))

story.append(Paragraph('第二章：突破防火牆的「四步跨網實作法」（外網開發 ➔ 內網上線）', h1_style))

cross_net_table = [
    [Paragraph('<b>作業階段</b>', body_style), Paragraph('<b>在外網（您自己的個人筆電 + AI Agent）</b>', body_style), Paragraph('<b>在內網（醫院辦公室電腦）</b>', body_style)],
    [
        Paragraph('<b>1. 需求定義與資料</b>', body_style),
        Paragraph('口述 PRN 導航版面需求給 Agent，載入本地藥品清冊。', body_style),
        Paragraph('從院內匯出藥品 Excel 清冊（如 藥品藥號.xlsx）。', body_style)
    ],
    [
        Paragraph('<b>2. 本地模擬驗收</b>', body_style),
        Paragraph('Agent 生成高傳真互動模擬器，您在本機親自點選驗收。', body_style),
        Paragraph('免受院內網路延遲或防火牆干擾，本機秒搜驗證。', body_style)
    ],
    [
        Paragraph('<b>3. PAC CLI 編譯打包</b>', body_style),
        Paragraph('Agent 執行 PAC CLI，輸出合規實體 <code>.msapp</code> 與流程 zip。', body_style),
        Paragraph('透過院內合規通道（Teams/院內隨身碟）帶入內網。', body_style)
    ],
    [
        Paragraph('<b>4. 雲端一鍵發布</b>', body_style),
        Paragraph('由 Agent 產出清晰的單張操作步驟與對照圖。', body_style),
        Paragraph('Power Apps 點選「瀏覽」，1 秒還原並釘選至 PRN 版面！', body_style)
    ]
]
t_cross = Table(cross_net_table, colWidths=[90, 200, 197])
t_cross.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_cross)

story.append(PageBreak())

# ==================== 第 3 頁：PRN 智慧導航版面臨床全流程閉環 ====================
story.append(Paragraph('第三章：PRN (Pro Re Nata) 智慧導航版面全院作業閉環', h1_style))
story.append(Paragraph('透過 Agent 在筆電打包完成並上傳院內後，PRN 智慧導航將串聯起全院完整的醫療自動化生態系：', body_style))

# 業務流程表格
biz_flow = [
    [Paragraph('<b>階段流程</b>', body_style), Paragraph('<b>執行工具與平台</b>', body_style), Paragraph('<b>PRN 智慧導航之具體運作機制</b>', body_style)],
    [
        Paragraph('<b>1. 總導航入口</b>', body_style),
        Paragraph('PRN 智慧導航版面<br/>(Pro Re Nata 首頁)', body_style),
        Paragraph('同仁登入 PRN 智慧版面，首頁清晰展示各功能卡片。點擊「藥品報廢」即時開啟內嵌之 Power Apps 表單。', body_style)
    ],
    [
        Paragraph('<b>2. 智慧防呆填報</b>', body_style),
        Paragraph('Power Apps 模組<br/>(PRN 專屬表單)', body_style),
        Paragraph('同仁鍵入 A/AD 快速篩選 3,427 筆藥品，藥號自動帶出，自動預設當天日期；報廢數量 > 50 顆瞬間跳出紅框防呆。', body_style)
    ],
    [
        Paragraph('<b>3. 雲端結構儲存</b>', body_style),
        Paragraph('SharePoint 清單<br/>(雲端資料庫庫房)', body_style),
        Paragraph('送出單據安全寫入「報廢網頁」清單，嚴密區分「藥庫團隊（全權限）」與「會議同仁（唯讀瀏覽）」，杜絕誤改。', body_style)
    ],
    [
        Paragraph('<b>4. 主管行動審核</b>', body_style),
        Paragraph('Teams + Automate<br/>(自適應卡片水管)', body_style),
        Paragraph('後端捕捉新單據，向主管 Teams 推播 Adaptive Card。主管在手機或電腦上一鍵點選「核准/退件」，狀態即時回寫。', body_style)
    ],
    [
        Paragraph('<b>5. 戰情決策分析</b>', body_style),
        Paragraph('Power BI 戰情室<br/>(嵌入 PRN 主管頁)', body_style),
        Paragraph('在 PRN 導航的主管專區嵌入 Power BI 儀表板，即時監控全院報廢損耗排行與超量趨勢，並可於報表內反向操作核准！', body_style)
    ]
]
t_biz = Table(biz_flow, colWidths=[90, 125, 272])
t_biz.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_biz)
story.append(Spacer(1, 8))

story.append(Paragraph('第四章：PRN 智慧導航嵌入 Power BI 之三大決策指標', h1_style))

pbi_data = [
    [Paragraph('<b>戰情指標</b>', body_style), Paragraph('<b>分析圖表與維度</b>', body_style), Paragraph('<b>PRN 智慧導航之決策效益</b>', body_style)],
    [
        Paragraph('<b>各病房報廢損耗頻次<br/>(折線趨勢圖)</b>', body_style),
        Paragraph('X 軸：月份；Y 軸：報廢數量加總<br/>圖例：各病房（5A/6B/ICU）', body_style),
        Paragraph('即時監控哪些病房損耗頻繁，協助藥庫主動調整庫存與撥補頻率。', body_style)
    ],
    [
        Paragraph('<b>高金額損耗品項 Top 10<br/>(橫條排行圖)</b>', body_style),
        Paragraph('Y 軸：藥品學名<br/>X 軸：報廢總金額（數量 × 單價）', body_style),
        Paragraph('揪出報廢成本最高的藥品（如昂貴抗生素/針劑），列入重點管制防損項目。', body_style)
    ],
    [
        Paragraph('<b>報廢原因深度分析<br/>(環形佔比圖)</b>', body_style),
        Paragraph('分類：逾期失效 / 破損變色 / 換藥退回<br/>數值：申請項目筆數', body_style),
        Paragraph('分析損耗主因是否為「效期過期」，作為評鑑備查與臨床衛教改善依據。', body_style)
    ]
]
t_pbi = Table(pbi_data, colWidths=[115, 185, 187])
t_pbi.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 4.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t_pbi)
story.append(Spacer(1, 6))

story.append(Paragraph('【結語：PRN 智慧導航引領智慧藥事未來】', h1_style))
story.append(Paragraph('<b>PRN (Pro Re Nata) 醫療自動化智慧導航版面</b>，將各項原本孤立的表單工具收斂至單一智慧門戶；搭配您個人筆電上的 <b>AI Agent 突破防火牆之敏捷開發模式</b>，醫療人員完全不再受困於複雜技術。想加什麼功能，口述即可在筆電秒級生成、合規打包、雲端發布，真正實現「以臨床需求為核心、隨需應變」的頂尖智慧醫療！', body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print('PRN Portal Guide PDF generated successfully at:', pdf_filename)
