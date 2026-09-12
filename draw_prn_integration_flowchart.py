import os
from PIL import Image, ImageDraw, ImageFont

# 畫布尺寸：3800 x 2300
W, H = 3800, 2300
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

title_font = ImageFont.truetype(font_path, 76)
subtitle_font = ImageFont.truetype(font_path, 38)
step_num_font = ImageFont.truetype(font_path, 40)
box_title_font = ImageFont.truetype(font_path, 42)
box_sub_font = ImageFont.truetype(font_path, 28)
box_desc_font = ImageFont.truetype(font_path, 29)
badge_font = ImageFont.truetype(font_path, 28)

# 頂部標題列
draw.rectangle([0, 0, W, 210], fill='#005A9E')
draw.rectangle([0, 210, W, 220], fill='#0078D4')

draw.text((W//2, 75), "醫院 PRN 系統與微軟五大自動化工具完整串接架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 155), "佳里奇美醫院 藥劑科 · 臨床需要時醫囑/常備藥與報廢、審核、戰情全流程閉環", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 6 個核心節點：PRN 系統 + 5 大工具
steps = [
    {
        "num": "核心 01",
        "title": "院內 PRN 系統",
        "sub": "角色：臨床醫囑與常備庫源頭",
        "color_top": "#E11D48", # 醫療紅
        "border": "#E11D48",
        "lines": [
            "• 記錄病房 PRN 常備藥存量",
            "• 產生逾期、破損或退藥事件",
            "• 提供藥號、病患、病房辨識",
            "• 串接觸發後續報廢換藥申請"
        ],
        "tag": "🏥 臨床業務發起端"
    },
    {
        "num": "核心 02",
        "title": "Power Apps 前端",
        "sub": "角色：PRN 報廢填報與防呆",
        "color_top": "#742774", # Power Apps 紫
        "border": "#742774",
        "lines": [
            "• 快速帶入 PRN 藥號與病房",
            "• A/AD 英文字母秒搜 3,427 筆藥名",
            "• 自動預設當日報廢填表時間",
            "• 數量 > 50 顆即時跳紅框警戒"
        ],
        "tag": "📱 智慧防呆填報前台"
    },
    {
        "num": "核心 03",
        "title": "SharePoint 資料庫",
        "sub": "角色：PRN 報廢與主檔儲存",
        "color_top": "#0078D4", # SharePoint 藍
        "border": "#0078D4",
        "lines": [
            "• 儲存報廢網頁（業務申請紀錄）",
            "• 對照藥品主檔（3,427 筆學名）",
            "• 記載 PRN 報廢原因與審核狀態",
            "• 雙團隊權限隔離（藥庫/會議）"
        ],
        "tag": "💾 結構化資料庫中心"
    },
    {
        "num": "核心 04",
        "title": "Power Automate",
        "sub": "角色：審核水管與狀態流轉",
        "color_top": "#0066FF", # Automate 藍
        "border": "#0066FF",
        "lines": [
            "• 捕捉 PRN 報廢單新增事件",
            "• 判斷超量/管制藥主管路由",
            "• 自動組裝卡片送至主管 Teams",
            "• 簽核完畢回寫 SharePoint 與 PRN"
        ],
        "tag": "⚡ 自動化流程引擎"
    },
    {
        "num": "核心 05",
        "title": "Microsoft Teams",
        "sub": "角色：主管卡片審核與頻道",
        "color_top": "#464EB8", # Teams 紫
        "border": "#464EB8",
        "lines": [
            "• 主管手機/電腦即時彈出自適應卡",
            "• 一鍵點擊「✅ 核准」或「❌ 退件」",
            "• 釘選 Power Apps 於病房頻道",
            "• 推播 PRN 補藥/換藥完成通知"
        ],
        "tag": "💬 協作與即時簽核"
    },
    {
        "num": "核心 06",
        "title": "Power BI 戰情室",
        "sub": "角色：PRN 耗損分析與決策",
        "color_top": "#D97706", # Power BI 金橙
        "border": "#D97706",
        "lines": [
            "• 分析各病房 PRN 報廢頻次與原因",
            "• 統計高損耗 PRN 藥品排行 Top 10",
            "• 監控 PRN 常備量過剩或囤積現象",
            "• 報表內反向操作核准，達成閉環"
        ],
        "tag": "📊 醫療戰情決策中心"
    }
]

# 卡片幾何配置 (6 張卡片橫排，每張 570px，間距 45px)
card_w = 570
card_h = 1520
top_y = 330
gap = 48
start_x = 55

for i, step in enumerate(steps):
    x1 = start_x + i * (card_w + gap)
    y1 = top_y
    x2 = x1 + card_w
    y2 = y1 + card_h
    
    # 陰影
    draw.rounded_rectangle([x1+8, y1+8, x2+8, y2+8], radius=22, fill='#E2E8F0')
    # 白色主體
    draw.rounded_rectangle([x1, y1, x2, y2], radius=22, fill='#FFFFFF', outline=step["border"], width=4)
    
    # 頂部彩條
    banner_h = 210
    draw.rounded_rectangle([x1, y1, x2, y1+banner_h], radius=22, fill=step["color_top"])
    draw.rectangle([x1, y1+banner_h-30, x2, y1+banner_h], fill=step["color_top"])
    
    # 頂部文字
    draw.text((x1 + card_w//2, y1 + 50), step["num"], fill='#FFFFFF', font=step_num_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 115), step["title"], fill='#FFFFFF', font=box_title_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 170), step["sub"], fill='#F1F5F9', font=box_sub_font, anchor='mm')
    
    # 標籤
    tag_y = y1 + banner_h + 40
    draw.rounded_rectangle([x1+30, tag_y, x2-30, tag_y+60], radius=14, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 30), step["tag"], fill=step["color_top"], font=badge_font, anchor='mm')
    
    # 說明條列
    text_start_y = tag_y + 110
    line_spacing = 135
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 35, ly), line, fill='#1E293B', font=box_desc_font)
        if j < len(step["lines"]) - 1:
            draw.line([x1+35, ly+90, x2-35, ly+90], fill='#F1F5F9', width=2)
            
    # 底部卡片裝飾
    draw.rounded_rectangle([x1+35, y2-105, x2-35, y2-45], radius=12, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-75), "全流程串接關鍵點", fill='#FFFFFF', font=badge_font, anchor='mm')
    
    # 箭頭
    if i < 5:
        arrow_x = x2 + gap // 2
        arrow_y = y1 + card_h // 2
        draw.polygon([
            (arrow_x - 14, arrow_y - 30),
            (arrow_x + 16, arrow_y),
            (arrow_x - 14, arrow_y + 30)
        ], fill='#0078D4')
        draw.rectangle([arrow_x - 24, arrow_y - 7, arrow_x - 10, arrow_y + 7], fill='#0078D4')

# 底部狀態列
draw.rectangle([0, H-130, W, H], fill='#0F172A')
draw.text((80, H-65), "PRN 系統串接核心：PRN 發起醫囑與損耗 ➔ Power Apps 智慧防呆 ➔ SharePoint 安全儲存 ➔ Automate 路由 ➔ Teams 審核 ➔ Power BI 決策閉環", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-65), "奇美醫療財團法人 佳里奇美醫院 藥劑科", fill='#94A3B8', font=subtitle_font, anchor='rm')

output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PRN系統與微軟五大工具串接架構圖.png'
img.save(output_path, quality=95)
print("PRN Integration Flowchart generated successfully!")
