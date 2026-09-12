import os
from PIL import Image, ImageDraw, ImageFont

# 圖片畫布尺寸 (3600 x 2100)
W, H = 3600, 2100
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

# 設定超清晰大字體
title_font = ImageFont.truetype(font_path, 80)
subtitle_font = ImageFont.truetype(font_path, 42)
step_num_font = ImageFont.truetype(font_path, 48)
box_title_font = ImageFont.truetype(font_path, 52)
box_desc_font = ImageFont.truetype(font_path, 38)
badge_font = ImageFont.truetype(font_path, 32)

# 頂部標題列裝飾
draw.rectangle([0, 0, W, 220], fill='#005A9E')
draw.rectangle([0, 220, W, 230], fill='#0078D4')

# 標題文字
draw.text((W//2, 80), "AI Agent「方法二：本地端即時模擬驗證」全流程架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 165), "佳里奇美醫院 藥劑科 · 3,427 筆藥品報廢即時連動與微軟雲端一次發布 SOP", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 5 個主要步驟節點（依據方法二與實際藥品報廢流程）
steps = [
    {
        "num": "步驟 01",
        "title": "口述需求與資料準備",
        "sub": "3,427 筆藥品清冊對齊",
        "color_top": "#0284C7",
        "border": "#0284C7",
        "lines": [
            "• 口述欄位（藥名、藥號、數量、病房）",
            "• 準備 Excel 藥品主檔（3,427 筆學名）",
            "• 設定防呆條件（數量 > 50 顆亮紅框）",
            "• 確立純白醫療視覺（杜絕灰底與歪斜）"
        ],
        "tag": "🗣️ 臨床口述 + Excel 匯整"
    },
    {
        "num": "步驟 02",
        "title": "本地生成互動模擬器",
        "sub": "注入全量真實臨床數據",
        "color_top": "#7C3AED",
        "border": "#7C3AED",
        "lines": [
            "• Agent 於本地建立高傳真 HTML 模擬器",
            "• 完整注入 3,427 筆全院藥品學名與藥號",
            "• 實作 A/AD 英文字母動態遞進快篩",
            "• 配置超量即時連動紅框警報機制"
        ],
        "tag": "⚡ 本地高傳真環境建置"
    },
    {
        "num": "步驟 03",
        "title": "本地端實機點選驗收",
        "sub": "零雲端延遲 · 滿意才打包",
        "color_top": "#D97706",
        "border": "#D97706",
        "lines": [
            "• 在本機瀏覽器直接點選操作體驗",
            "• 鍵入「A」或「AD」驗證毫秒級秒搜",
            "• 點選藥品學名，確認右側藥號自動帶出",
            "• 輸入數量 60 顆，親睹即時紅色警報"
        ],
        "tag": "🧪 100% 本地實機驗收"
    },
    {
        "num": "步驟 04",
        "title": "PAC CLI 編譯實體 App",
        "sub": "微軟官方工具鏈無損轉換",
        "color_top": "#16A34A",
        "border": "#16A34A",
        "lines": [
            "• Agent 自動將驗收邏輯轉成 Power Fx",
            "• 執行 pac canvas pack 編譯壓縮封裝",
            "• 生成實體「抗生素報廢管理App.msapp」",
            "• 雲端一鍵開啟載入，免手動排版微調"
        ],
        "tag": "📦 實體 .msapp 一次打包"
    },
    {
        "num": "步驟 05",
        "title": "跨平台推播與決策閉環",
        "sub": "Teams 審核卡 + Power BI 報表",
        "color_top": "#DC2626",
        "border": "#DC2626",
        "lines": [
            "• 送出申請：SharePoint 雲端安全寫入",
            "• 主管審核：Teams 自適應卡片一鍵核准",
            "• 雙團隊權限隔離：藥庫全權 / 會議唯讀",
            "• 戰情儀表板：Power BI 即時監控耗損"
        ],
        "tag": "🚀 全院醫療流程上線"
    }
]

# 卡片幾何配置
card_w = 640
card_h = 1420
top_y = 350
gap = (W - 100 - (card_w * 5)) // 4
start_x = 50

for i, step in enumerate(steps):
    x1 = start_x + i * (card_w + gap)
    y1 = top_y
    x2 = x1 + card_w
    y2 = y1 + card_h
    
    # 卡片陰影
    draw.rounded_rectangle([x1+8, y1+8, x2+8, y2+8], radius=24, fill='#E2E8F0')
    
    # 卡片主體
    draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill='#FFFFFF', outline=step["border"], width=5)
    
    # 卡片頂部彩色 Banner
    banner_h = 220
    draw.rounded_rectangle([x1, y1, x2, y1+banner_h], radius=24, fill=step["color_top"])
    draw.rectangle([x1, y1+banner_h-30, x2, y1+banner_h], fill=step["color_top"]) # 補平底角
    
    # Banner 內文字
    draw.text((x1 + card_w//2, y1 + 55), step["num"], fill='#FFFFFF', font=step_num_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 130), step["title"], fill='#FFFFFF', font=box_title_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 185), step["sub"], fill='#E0F2FE', font=badge_font, anchor='mm')
    
    # 卡片內部內容標籤
    tag_y = y1 + banner_h + 45
    draw.rounded_rectangle([x1+30, tag_y, x2-30, tag_y+65], radius=16, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 32), step["tag"], fill=step["color_top"], font=box_desc_font, anchor='mm')
    
    # 條列說明文字
    text_start_y = tag_y + 120
    line_spacing = 125
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 40, ly), line, fill='#1E293B', font=box_desc_font)
        # 分隔線
        if j < len(step["lines"]) - 1:
            draw.line([x1+40, ly+85, x2-40, ly+85], fill='#F1F5F9', width=3)
            
    # 卡片底部裝飾塊
    draw.rounded_rectangle([x1+40, y2-110, x2-40, y2-45], radius=14, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-77), "標準交付里程碑", fill='#FFFFFF', font=badge_font, anchor='mm')
    
    # 連接箭頭（在兩張卡片之間）
    if i < 4:
        arrow_x = x2 + gap // 2
        arrow_y = y1 + card_h // 2
        draw.polygon([
            (arrow_x - 20, arrow_y - 40),
            (arrow_x + 22, arrow_y),
            (arrow_x - 20, arrow_y + 40)
        ], fill='#0078D4')
        draw.rectangle([arrow_x - 36, arrow_y - 10, arrow_x - 14, arrow_y + 10], fill='#0078D4')

# 底部狀態列
draw.rectangle([0, H-130, W, H], fill='#0F172A')
draw.text((80, H-65), "💡 方法二特色：本地完全零成本除錯 · 3,427 筆海量資料極速驗證 · 體驗滿意後 100% 無損封裝為微軟官方 .msapp 雲端發布", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-65), "奇美醫療財團法人 佳里奇美醫院 藥劑科", fill='#94A3B8', font=subtitle_font, anchor='rm')

# 儲存
output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PowerApps_Agent開發流程圖.png'
img.save(output_path, quality=95)
print("Flowchart with Method 2 updated successfully!")
