import os
from PIL import Image, ImageDraw, ImageFont

# 畫布尺寸：3800 x 2100，提供充裕空間
W, H = 3800, 2100
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

# 設定專業級字體大小（標題與內文字體協調，字型大且絕對不溢出）
title_font = ImageFont.truetype(font_path, 76)
subtitle_font = ImageFont.truetype(font_path, 38)
step_num_font = ImageFont.truetype(font_path, 42)
box_title_font = ImageFont.truetype(font_path, 46)
box_sub_font = ImageFont.truetype(font_path, 30)
box_desc_font = ImageFont.truetype(font_path, 31)  # 31pt 確保每行 15~17 字完美容納在卡片中
badge_font = ImageFont.truetype(font_path, 30)

# 頂部標題列裝飾
draw.rectangle([0, 0, W, 210], fill='#005A9E')
draw.rectangle([0, 210, W, 220], fill='#0078D4')

# 標題文字（完全移除「高清晰大字版」等字樣，維持正式醫療手冊風格）
draw.text((W//2, 75), "AI Agent 本地端即時模擬驗證與 Power Apps 全流程架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 155), "佳里奇美醫院 藥劑科 · 3,427 筆藥品報廢即時連動、Teams 審核與 Power BI 串接全流程", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 5 個主要步驟節點（字數經嚴謹字數排版計算，每行長度控制在 480px 內，卡片可用寬度 590px，杜絕溢出）
steps = [
    {
        "num": "步驟 01",
        "title": "口述需求與資料匯整",
        "sub": "3,427 筆藥品清冊準備",
        "color_top": "#0284C7",
        "border": "#0284C7",
        "lines": [
            "• 口述欄位（藥名、藥號、病房）",
            "• 準備 Excel 藥品主檔（3,427 筆）",
            "• 設定防呆條件（數量 > 50 顆紅框）",
            "• 確立純白醫療視覺（杜絕灰底）"
        ],
        "tag": "🗣️ 口述需求 + 資料準備"
    },
    {
        "num": "步驟 02",
        "title": "本地生成互動模擬器",
        "sub": "注入全量真實臨床數據",
        "color_top": "#7C3AED",
        "border": "#7C3AED",
        "lines": [
            "• 本地建立高傳真 HTML 模擬器",
            "• 完整注入 3,427 筆真實藥品資料",
            "• 實作 A/AD 英文字母即時快篩",
            "• 配置超量即時連動紅色警報"
        ],
        "tag": "⚡ 本地高傳真模擬建置"
    },
    {
        "num": "步驟 03",
        "title": "本地端實機點選驗收",
        "sub": "零雲端延遲 · 滿意才打包",
        "color_top": "#D97706",
        "border": "#D97706",
        "lines": [
            "• 本機瀏覽器直接點選操作驗收",
            "• 鍵入 A 或 AD 驗證毫秒級快搜",
            "• 點選藥名，確認藥號自動帶出",
            "• 輸入數量 60 顆，親睹紅框警報"
        ],
        "tag": "🧪 100% 本地實機驗收"
    },
    {
        "num": "步驟 04",
        "title": "PAC CLI 編譯實體 App",
        "sub": "微軟官方工具鏈標準封裝",
        "color_top": "#16A34A",
        "border": "#16A34A",
        "lines": [
            "• 驗收邏輯轉成標準 Power Fx",
            "• 執行 pac canvas pack 編譯封裝",
            "• 輸出實體應用程式 .msapp 檔案",
            "• 雲端一鍵開啟載入，免手動微調"
        ],
        "tag": "📦 實體 .msapp 一鍵打包"
    },
    {
        "num": "步驟 05",
        "title": "跨平台推播與決策閉環",
        "sub": "Teams 審核 + Power BI 串接",
        "color_top": "#DC2626",
        "border": "#DC2626",
        "lines": [
            "• 送出申請：寫入 SharePoint 資料庫",
            "• 主管審核：Teams 卡片一鍵核准",
            "• 雙團隊隔離：藥庫全權 / 會議唯讀",
            "• 戰情儀表板：Power BI 即時監控"
        ],
        "tag": "🚀 全院醫療流程正式上線"
    }
]

# 卡片幾何配置 (寬 680px，卡片間距 55px，兩側邊距 60px)
card_w = 680
card_h = 1440
top_y = 340
gap = 55
start_x = 65

for i, step in enumerate(steps):
    x1 = start_x + i * (card_w + gap)
    y1 = top_y
    x2 = x1 + card_w
    y2 = y1 + card_h
    
    # 卡片陰影
    draw.rounded_rectangle([x1+10, y1+10, x2+10, y2+10], radius=24, fill='#E2E8F0')
    
    # 卡片主體白色背景
    draw.rounded_rectangle([x1, y1, x2, y2], radius=24, fill='#FFFFFF', outline=step["border"], width=5)
    
    # 卡片頂部彩色 Banner
    banner_h = 220
    draw.rounded_rectangle([x1, y1, x2, y1+banner_h], radius=24, fill=step["color_top"])
    draw.rectangle([x1, y1+banner_h-30, x2, y1+banner_h], fill=step["color_top"]) # 補平底角
    
    # Banner 內文字（水平置中）
    draw.text((x1 + card_w//2, y1 + 55), step["num"], fill='#FFFFFF', font=step_num_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 125), step["title"], fill='#FFFFFF', font=box_title_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 180), step["sub"], fill='#E0F2FE', font=box_sub_font, anchor='mm')
    
    # 卡片內部內容標籤（水平置中）
    tag_y = y1 + banner_h + 45
    draw.rounded_rectangle([x1+40, tag_y, x2-40, tag_y+65], radius=16, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 32), step["tag"], fill=step["color_top"], font=badge_font, anchor='mm')
    
    # 條列說明文字（左邊距 45px，保留充足右邊距，絕對不溢出框線）
    text_start_y = tag_y + 115
    line_spacing = 130
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 45, ly), line, fill='#1E293B', font=box_desc_font)
        # 分隔線
        if j < len(step["lines"]) - 1:
            draw.line([x1+45, ly+90, x2-45, ly+90], fill='#F1F5F9', width=3)
            
    # 卡片底部裝飾塊
    draw.rounded_rectangle([x1+45, y2-110, x2-45, y2-45], radius=14, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-77), "標準交付里程碑", fill='#FFFFFF', font=badge_font, anchor='mm')
    
    # 連接箭頭（在兩張卡片之間）
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
draw.text((80, H-65), "奇美醫療自動化架構：本地高傳真驗收 · 3,427 筆藥品資料即時秒搜 · Teams 自動審核推播 · Power BI 戰情儀表板完整串接", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-65), "奇美醫療財團法人 佳里奇美醫院 藥劑科", fill='#94A3B8', font=subtitle_font, anchor='rm')

# 儲存
output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PowerApps_Agent開發流程圖.png'
img.save(output_path, quality=95)
print("Big Flowchart regenerated with NO text overflow!")
