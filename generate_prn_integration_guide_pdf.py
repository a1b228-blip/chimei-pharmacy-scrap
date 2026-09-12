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
            self.drawRightString(541, 800, '醫院 PRN 系統與 Power Platform / Teams / Power BI 串接全流程')
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        self.drawString(54, 38, '機密等級：院內專案指南 · 智慧醫療表單現代化教材')
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

# ==================== 第 1 頁：PRN 定位與全流程架構圖 ====================
story.append(Spacer(1, 5))
story.append(Paragraph('佳里奇美醫院 藥劑科 智慧藥事專題指南', subtitle_style))
story.append(Paragraph('醫院 PRN 系統與微軟自動化工具整合手冊<br/>從臨床醫囑/常備藥到報廢、審核與 Power BI 戰情全流程閉環', title_style))
story.append(Spacer(1, 4))

info_data = [
    [Paragraph('<b>手冊代號</b>：CMH-PHARM-PRN-001', body_style), Paragraph('<b>編製小組</b>：藥劑科智慧藥事小組 / Google Antigravity', body_style)],
    [Paragraph('<b>整合範疇</b>：PRN 醫囑系統 · 常備藥管理 · 報廢核銷', body_style), Paragraph('<b>發布日期</b>：2026 年 09 月 13 日', body_style)],
    [Paragraph('<b>技術架構</b>：PRN + Power Apps + Automate + Teams + BI', body_style), Paragraph('<b>版本狀態</b>：正式版 (v1.0 發行)', body_style)]
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

story.append(Paragraph('【核心解析：PRN 在醫院自動化系統中到底是什麼角色？】', h1_style))
story.append(Paragraph('在醫療實務中，<b>PRN（pro re nata，需要時使用）</b>是病房最常見但也是管理最棘手的醫囑類型（如退燒止痛針、緊急抗生素、氣喘吸入劑或鎮靜安眠藥）。病房通常會備妥一定數量的「PRN 常備藥」。<br/>'
                       '在整套自動化架構中，<b>PRN 是「業務觸發的火車頭（起點）」與「藥品帳料核銷的終點」</b>：<br/>'
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

# ==================== 第 2 頁：PRN 與微軟生態五步串接教學 ====================
story.append(Paragraph('第一章：PRN 系統與各工具串接操作指南（從源頭到簽核）', h1_style))
story.append(Paragraph('以下完整梳理 PRN 系統如何透過資料中介，與微軟四大自動化工具無縫對接：', body_style))

story.append(Paragraph('第 1 步：PRN 系統資料庫中介串接（對齊 SharePoint 主檔）', h2_style))
story.append(Paragraph('1. <b>匯出/介接 PRN 清冊</b>：從 HIS/NIS 的 PRN 模組匯出病房常備藥品清冊，與 <code>藥品藥號.xlsx</code>（3,427 筆藥品主檔）比對。', bullet_style))
story.append(Paragraph('2. <b>在 SharePoint 擴充 PRN 標記</b>：在「報廢網頁」與「藥品主檔」清單中，增加 <b>「醫囑類型 (Choice)」</b> 欄位（選項：<code>一般常規 (Regular)</code>、<code>需要時 (PRN)</code>、<code>高危險急救 (Stat)</code>），用以精準區分。', bullet_style))

story.append(Paragraph('第 2 步：在 Power Apps 前端介面打造 PRN 智慧快篩與防呆', h2_style))
story.append(Paragraph('1. <b>PRN 快速切換標籤</b>：在表單上方加入單選按鈕或切換開關 <code>[一般藥品 / PRN 藥品]</code>。', bullet_style))
story.append(Paragraph('2. <b>動態連動選單</b>：當同仁勾選 PRN 時，藥品 ComboBox 自動篩選出屬於該病房之 PRN 常備藥品清單：', bullet_style))
story.append(Paragraph('<code>Items: Filter(藥品主檔, IsPRN = true)</code>', bullet_style))
story.append(Paragraph('3. <b>PRN 劑量防呆規則</b>：PRN 藥品常為水劑、外用或單支針劑，設定若報廢數量超過該病房 PRN 核定基準量（如 50 顆/支），直接亮起紅色邊框與專案複核警訊。', bullet_style))

story.append(Paragraph('第 3 步：Power Automate 自動化路由：PRN 專案審核邏輯', h2_style))
story.append(Paragraph('1. <b>條件分支 (Condition)</b>：當 SharePoint 收到報廢申請時，流程讀取「醫囑類型」欄位。', bullet_style))
story.append(Paragraph('2. <b>若是 PRN 藥品且數量 > 50</b>：', bullet_style))
story.append(Paragraph('• 系統判定為「病房常備藥異常消耗」，審核卡片自動<b>同時發送給「病房護理長」與「藥庫主任」</b>進行雙簽。', bullet_style))
story.append(Paragraph('• 審核卡片清晰標註：<code>【PRN 異常耗損通報】病房：5A，品項：Augmentin，報廢量：60 顆</code>。', bullet_style))
story.append(Paragraph('3. <b>核准後自動觸發 PRN 補藥/沖帳</b>：審核通過後，Automate 不僅更新 SharePoint，更可透過 HTTP/Web API 反向將核銷紀錄拋轉回 HIS，自動扣減該病房 PRN 常備存量！', bullet_style))

story.append(Paragraph('第 4 步：在 Microsoft Teams 實現行動審核與 PRN 異動公告', h2_style))
story.append(Paragraph('1. 主管無需開電腦，手機 Teams 收到 Adaptive Card 即可查閱 PRN 病患退藥原因，一秒點擊核准。', bullet_style))
story.append(Paragraph('2. 簽核完畢後，機器人自動在 Teams「病房護理站頻道」推播公告：<code>5A 病房 PRN 報廢已完成審核，藥庫已排定明日補發常備藥品</code>。', bullet_style))

story.append(Spacer(1, 6))

story.append(PageBreak())

# ==================== 第 3 頁：Power BI PRN 戰情分析與管理價值 ====================
story.append(Paragraph('第二章：Power BI 醫療戰情室：PRN 專屬三大數據看板', h1_style))
story.append(Paragraph('將 PRN 報廢紀錄串入 Power BI，能協助藥劑科由「被動報廢」轉變為<b>「主動精準庫存管理」</b>：', body_style))

prn_table = [
    [Paragraph('<b>PRN 戰情指標</b>', body_style), Paragraph('<b>分析維度與圖表</b>', body_style), Paragraph('<b>臨床藥事改善效益</b>', body_style)],
    [
        Paragraph('<b>PRN 耗損週轉率<br/>(折線圖)</b>', body_style),
        Paragraph('X 軸：月份；Y 軸：報廢數量<br/>圖例：各病房（5A/6B/ICU）', body_style),
        Paragraph('監控哪些病房 PRN 藥品常放到過期，及時下修常備配額，減少浪費。', body_style)
    ],
    [
        Paragraph('<b>高頻報廢 PRN 藥品<br/>(橫條圖 Top 10)</b>', body_style),
        Paragraph('品名 vs 總耗損金額<br/>顏色深淺：報廢頻次', body_style),
        Paragraph('找出最常報廢的 PRN 品項（如抗生素水劑），評估改用單包裝或調整包裝規格。', body_style)
    ],
    [
        Paragraph('<b>退藥原因剖析<br/>(樹狀結構圖)</b>', body_style),
        Paragraph('分類：逾期 / 破損 / 換藥<br/>數值：報廢總量', body_style),
        Paragraph('若「換藥退回」佔比過高，臨床藥師可介入輔導醫師開立 PRN 之適應症。', body_style)
    ]
]
t_prn = Table(prn_table, colWidths=[110, 190, 187])
t_prn.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#005A9E')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_prn)
story.append(Spacer(1, 8))

story.append(Paragraph('第三章：PRN 系統串接之臨床常見問題與防呆要訣', h1_style))
story.append(Paragraph('1. <b>防呆一：PRN 批號與效期必須精確追蹤</b>：PRN 藥品因長期備於病房，最易發生「新藥先用、舊藥過期」的先進後出問題。在 Power Apps 表單中將「批號」與「有效期限」設為必填，利於 Power BI 提前 30 天跳出即期預警。', bullet_style))
story.append(Paragraph('2. <b>防呆二：雙重防呆避免重複報廢</b>：透過 SharePoint 欄位強制檢查 <code>藥號 + 批號 + 病房</code>，若 24 小時內已有相同申請單處於「待審核」，前端自動提示已在審查中，避免護理同仁重複提報。', bullet_style))
story.append(Paragraph('3. <b>防呆三：戰情反向補藥閉環</b>：在 Power BI 儀表板直接嵌入 Power Apps，主管在看 PRN 報廢報表時，點擊按鈕可當場觸發「PRN 自動補藥發單」，真正實現醫藥閉環運作。', bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph('【結語】', h1_style))
story.append(Paragraph('將 PRN 系統納入微軟自動化生態系，標誌著佳里奇美醫院藥劑科從單純的「行政表單數位化」，邁向<b>「臨床醫囑與後勤庫存一體化」</b>的高階智慧醫療里程碑！', body_style))

doc.build(story, canvasmaker=NumberedCanvas)
print('PRN Integration Guide PDF generated successfully at:', pdf_filename)
