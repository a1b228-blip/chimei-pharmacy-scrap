import os
from PIL import Image, ImageDraw, ImageFont

# 圖片畫布尺寸 (3600 x 2000)
W, H = 3600, 2000
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

# 設定大字體尺寸
title_font = ImageFont.truetype(font_path, 80)
subtitle_font = ImageFont.truetype(font_path, 42)
step_num_font = ImageFont.truetype(font_path, 48)
box_title_font = ImageFont.truetype(font_path, 52)
box_desc_font = ImageFont.truetype(font_path, 38)
badge_font = ImageFont.truetype(font_path, 32)
arrow_font = ImageFont.truetype(font_path, 48)

# 頂部標題列裝飾
draw.rectangle([0, 0, W, 220], fill='#005A9E')
draw.rectangle([0, 220, W, 230], fill='#0078D4')

# 標題文字
draw.text((W//2, 80), "AI Agent 本地端 Code-First 開發 Power Apps 全流程架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 165), "佳里奇美醫院 藥劑科 · 醫療自動化標準作業流程 (SOP) · 高清大字版", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 5 個主要步驟節點
steps = [
    {
        "num": "步驟 01",
        "title": "臨床人員口述需求",
        "sub": "自然語言即時定義",
        "color_top": "#0284C7",
        "color_bg": "#FFFFFF",
        "border": "#0284C7",
        "lines": [
            "• 口述畫面排版與風格（純白無灰底）",
            "• 指定臨床欄位（藥名、藥號、病房）",
            "• 設定防呆規則（數量 > 50 顆跳紅框）",
            "• 掛載藥品清冊（3,427 筆藥品主檔）"
        ],
        "tag": "🗣️ 10 秒口述定義"
    },
    {
        "num": "步驟 02",
        "title": "Agent 本地代碼生成",
        "sub": "Code-First 精準架構",
        "color_top": "#7C3AED",
        "color_bg": "#FFFFFF",
        "border": "#7C3AED",
        "lines": [
            "• 像素級排版佈局運算（杜絕歪斜）",
            "• 生成標準 App.fx.yaml 結構代碼",
            "• 注入 ComboBox 首字母即時搜尋",
            "• 連動藥號 LookUp 杜絕循環參考"
        ],
        "tag": "⚡ 零代碼/全自動生成"
    },
    {
        "num": "步驟 03",
        "title": "PAC CLI 編譯打包",
        "sub": "微軟官方工具鏈驗證",
        "color_top": "#D97706",
        "color_bg": "#FFFFFF",
        "border": "#D97706",
        "lines": [
            "• 呼叫微軟官方 pac canvas pack",
            "• 靜態語法與型態相容性自動檢驗",
            "• 資源壓縮與架構打包封裝",
            "• 輸出實體抗生素報廢管理App.msapp"
        ],
        "tag": "📦 實體 .msapp 輸出"
    },
    {
        "num": "步驟 04",
        "title": "Power Apps 雲端載入",
        "sub": "免拖拉 · 一鍵無縫還原",
        "color_top": "#16A34A",
        "color_bg": "#FFFFFF",
        "border": "#16A34A",
        "lines": [
            "• 開啟 Power Apps Studio 雲端畫布",
            "• 點擊「開啟」➔「瀏覽這部電腦」",
            "• 1 秒瞬間載入整套雙欄排版與邏輯",
            "• 免手動微調、告別灰底與重疊痛點"
        ],
        "tag": "✅ 實機免調驗收"
    },
    {
        "num": "步驟 05",
        "title": "Power BI 與跨端發布",
        "sub": "醫療管理決策閉環",
        "color_top": "#DC2626",
        "color_bg": "#FFFFFF",
        "border": "#DC2626",
        "lines": [
            "• 嵌入 Power BI：報表點選即時核准",
            "• 釘選 Teams 頻道：病房同仁隨手開單",
            "• 整合 Power Automate 自適應審核卡",
            "• 實現雙團隊角色權限嚴密隔離"
        ],
        "tag": "🚀 全院雙向閉環"
    }
]

# 卡片幾何配置 (寬度大、間距適中、字體大)
card_w = 640
card_h = 1350
top_y = 360
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
    draw.rounded_rectangle([x1+40, tag_y, x2-40, tag_y+65], radius=16, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 32), step["tag"], fill=step["color_top"], font=box_desc_font, anchor='mm')
    
    # 條列說明文字
    text_start_y = tag_y + 120
    line_spacing = 115
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 45, ly), line, fill='#1E293B', font=box_desc_font)
        # 分隔虛線
        if j < len(step["lines"]) - 1:
            draw.line([x1+45, ly+75, x2-45, ly+75], fill='#F1F5F9', width=3)
            
    # 卡片底部裝飾塊
    draw.rounded_rectangle([x1+40, y2-100, x2-40, y2-40], radius=14, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-70), "核心交付指標", fill='#FFFFFF', font=badge_font, anchor='mm')
    
    # 連接箭頭（在兩張卡片之間）
    if i < 4:
        arrow_x = x2 + gap // 2
        arrow_y = y1 + card_h // 2
        # 繪製醒目的大箭頭
        draw.polygon([
            (arrow_x - 18, arrow_y - 35),
            (arrow_x + 18, arrow_y),
            (arrow_x - 18, arrow_y + 35)
        ], fill='#0078D4')
        draw.rectangle([arrow_x - 32, arrow_y - 8, arrow_x - 12, arrow_y + 8], fill='#0078D4')

# 底部狀態列
draw.rectangle([0, H-120, W, H], fill='#0F172A')
draw.text((80, H-60), "📌 奇美醫療架構特點：嚴禁雲端手拉失誤 · 100% 本地 YAML 程式碼定義 · 自動相容全院 SharePoint 3,427 筆藥品資料庫", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-60), "奇美醫療財團法人 佳里奇美醫院 藥劑科 版權所有", fill='#94A3B8', font=subtitle_font, anchor='rm')

# 儲存
output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PowerApps_Agent開發流程圖.png'
img.save(output_path, quality=95)
print("Big Flowchart generated successfully!")
