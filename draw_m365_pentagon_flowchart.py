import os
from PIL import Image, ImageDraw, ImageFont

# 畫布尺寸：3800 x 2200
W, H = 3800, 2200
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

title_font = ImageFont.truetype(font_path, 76)
subtitle_font = ImageFont.truetype(font_path, 38)
step_num_font = ImageFont.truetype(font_path, 42)
box_title_font = ImageFont.truetype(font_path, 44)
box_sub_font = ImageFont.truetype(font_path, 30)
box_desc_font = ImageFont.truetype(font_path, 31)
badge_font = ImageFont.truetype(font_path, 30)

# 頂部標題列
draw.rectangle([0, 0, W, 210], fill='#005A9E')
draw.rectangle([0, 210, W, 220], fill='#0078D4')

draw.text((W//2, 75), "微軟醫療自動化五大核心工具（五星閉環）串接架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 155), "佳里奇美醫院 藥劑科 · 醫院 IT 新手從零上手專案全流程圖解指南", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 5 大核心角色卡片
steps = [
    {
        "num": "模組 01",
        "title": "SharePoint 清單",
        "sub": "角色：雲端資料庫（地基）",
        "color_top": "#0078D4", # SharePoint Blue
        "border": "#0078D4",
        "lines": [
            "• 建立儲存庫：新增報廢網頁清單",
            "• 設定欄位：藥名、藥號、數量、日期",
            "• 權限隔離：藥庫編輯 / 會議唯讀",
            "• 做為全系統唯一真實資料來源"
        ],
        "tag": "💾 結構化資料儲存中心"
    },
    {
        "num": "模組 02",
        "title": "Power Apps",
        "sub": "角色：前端操作介面（前台）",
        "color_top": "#742774", # Power Apps Purple
        "border": "#742774",
        "lines": [
            "• 臨床防呆介面：純白雙欄醫療風",
            "• 智慧快篩：A/AD 字母秒搜藥品",
            "• 自動帶出：選取藥名即時帶出藥號",
            "• 超量警示：數量 > 50 顆外框變紅"
        ],
        "tag": "📱 智慧填報與防呆前端"
    },
    {
        "num": "模組 03",
        "title": "Power Automate",
        "sub": "角色：自動化流程神經（傳送帶）",
        "color_top": "#0066FF", # Automate Blue
        "border": "#0066FF",
        "lines": [
            "• 事件監聽：當 SharePoint 新增項目",
            "• 邏輯路由：判斷是否需主任專案複核",
            "• 觸發推播：打包表單資料送至 Teams",
            "• 狀態回寫：審核結果更新回資料庫"
        ],
        "tag": "⚡ 後端神經自動流轉"
    },
    {
        "num": "模組 04",
        "title": "Microsoft Teams",
        "sub": "角色：溝通與簽核中心（站點）",
        "color_top": "#464EB8", # Teams Purple/Blue
        "border": "#464EB8",
        "lines": [
            "• 釘選表單：病房頻道隨開隨填",
            "• 自適應卡片：推播主管專屬通知",
            "• 行動簽核：手機/電腦一鍵按核准",
            "• 雙團隊頻道：藥庫溝通與會議隔離"
        ],
        "tag": "💬 協作與即時簽核介面"
    },
    {
        "num": "模組 05",
        "title": "Power BI",
        "sub": "角色：戰情儀表板（大腦）",
        "color_top": "#F2C811", # Power BI Gold
        "border": "#D4A017",
        "lines": [
            "• 雲端排程：自動同步 SharePoint 資料",
            "• 戰情指標：耗損 Top 10 與報廢原因",
            "• 異常監控：追蹤超量報廢發生頻次",
            "• 雙向操作：在報表內直接反向核准"
        ],
        "tag": "📊 醫療決策戰情室"
    }
]

# 卡片幾何配置
card_w = 680
card_h = 1480
top_y = 330
gap = 55
start_x = 65

for i, step in enumerate(steps):
    x1 = start_x + i * (card_w + gap)
    y1 = top_y
    x2 = x1 + card_w
    y2 = y1 + card_h
    
    # 陰影
    draw.rounded_rectangle([x1+10, y1+10, x2+10, y2+10], radius=24, fill='#E2E8F0')
    # 白色主體
    draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill='#FFFFFF', outline=step["border"], width=5)
    
    # 頂部彩條
    banner_h = 220
    draw.rounded_rectangle([x1, y1, x2, y1+banner_h], radius=24, fill=step["color_top"])
    draw.rectangle([x1, y1+banner_h-30, x2, y1+banner_h], fill=step["color_top"])
    
    # 頂部文字
    draw.text((x1 + card_w//2, y1 + 55), step["num"], fill='#FFFFFF', font=step_num_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 125), step["title"], fill='#FFFFFF', font=box_title_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 180), step["sub"], fill='#FFFFFF' if step["color_top"] != "#F2C811" else "#1E293B", font=box_sub_font, anchor='mm')
    
    # 標籤
    tag_y = y1 + banner_h + 45
    draw.rounded_rectangle([x1+40, tag_y, x2-40, tag_y+65], radius=16, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 32), step["tag"], fill=step["color_top"] if step["color_top"] != "#F2C811" else "#B45309", font=badge_font, anchor='mm')
    
    # 說明條列
    text_start_y = tag_y + 115
    line_spacing = 135
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 45, ly), line, fill='#1E293B', font=box_desc_font)
        if j < len(step["lines"]) - 1:
            draw.line([x1+45, ly+92, x2-45, ly+92], fill='#F1F5F9', width=3)
            
    # 底部卡片裝飾
    draw.rounded_rectangle([x1+45, y2-110, x2-45, y2-45], radius=14, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-77), "專案串接定位", fill='#FFFFFF' if step["color_top"] != "#F2C811" else "#1E293B", font=badge_font, anchor='mm')
    
    # 箭頭
    if i < 4:
        arrow_x = x2 + gap // 2
        arrow_y = y1 + card_h // 2
        draw.polygon([
            (arrow_x - 16, arrow_y - 35),
            (arrow_x + 18, arrow_y),
            (arrow_x - 16, arrow_y + 35)
        ], fill='#0078D4')
        draw.rectangle([arrow_x - 28, arrow_y - 8, arrow_x - 12, arrow_y + 8], fill='#0078D4')

# 底部狀態列
draw.rectangle([0, H-130, W, H], fill='#0F172A')
draw.text((80, H-65), "醫院 IT 新手串接心法：SharePoint 是地基 · Power Apps 是門面 · Automate 是水管 · Teams 是對講機 · Power BI 是儀表板", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-65), "奇美醫療財團法人 佳里奇美醫院 藥劑科", fill='#94A3B8', font=subtitle_font, anchor='rm')

output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/微軟五大工具串接架構圖.png'
img.save(output_path, quality=95)
print("Pentagon Flowchart generated successfully!")
