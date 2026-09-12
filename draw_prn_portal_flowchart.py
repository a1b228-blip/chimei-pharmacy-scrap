import os
from PIL import Image, ImageDraw, ImageFont

# 畫布尺寸：3800 x 2300
W, H = 3800, 2300
img = Image.new('RGB', (W, H), color='#F8FAFC')
draw = ImageDraw.Draw(img)

font_path = '/Library/Fonts/Arial Unicode.ttf'

title_font = ImageFont.truetype(font_path, 74)
subtitle_font = ImageFont.truetype(font_path, 36)
step_num_font = ImageFont.truetype(font_path, 40)
box_title_font = ImageFont.truetype(font_path, 42)
box_sub_font = ImageFont.truetype(font_path, 28)
box_desc_font = ImageFont.truetype(font_path, 29)
badge_font = ImageFont.truetype(font_path, 28)

# 頂部標題列
draw.rectangle([0, 0, W, 210], fill='#005A9E')
draw.rectangle([0, 210, W, 220], fill='#0078D4')

draw.text((W//2, 75), "PRN 智慧導航中樞與微軟醫療自動化生態串接架構圖", fill='#FFFFFF', font=title_font, anchor='mm')
draw.text((W//2, 155), "佳里奇美醫院 藥劑科 · Pro Re Nata 智慧導航版面、本地 AI Agent 與全院自動化閉環", fill='#BAE6FD', font=subtitle_font, anchor='mm')

# 6 個核心節點：PRN 智慧導航中樞 + 本地 Agent + 4大工具
steps = [
    {
        "num": "中樞 01",
        "title": "PRN 智慧導航",
        "sub": "角色：全院單一入口/總導航門面",
        "color_top": "#E11D48", # PRN 品牌深紅
        "border": "#E11D48",
        "lines": [
            "• Pro Re Nata 智慧首頁入口",
            "• 整合藥品報廢/盤點/常備模組",
            "• 依臨床身分動態分流導航",
            "• 嵌入式微軟 Power Apps 門戶"
        ],
        "tag": "🌐 全院單一智慧入口"
    },
    {
        "num": "中樞 02",
        "title": "本地端 AI Agent",
        "sub": "角色：突破防火牆之智慧引擎",
        "color_top": "#7C3AED", # Agent 紫
        "border": "#7C3AED",
        "lines": [
            "• 本機離線沙盒：3,427 筆藥品秒搜",
            "• 口述轉 Code-First：生成 YAML",
            "• PAC CLI 打包：輸出標準 .msapp",
            "• 免院內繁瑣安裝，安全跨網交付"
        ],
        "tag": "⚡ 防火牆穿透中繼外掛"
    },
    {
        "num": "中樞 03",
        "title": "Power Apps 前端",
        "sub": "角色：PRN 子模組表單與防呆",
        "color_top": "#742774", # Power Apps 紫紅
        "border": "#742774",
        "lines": [
            "• 嵌入 PRN 導航框架之臨床表單",
            "• 字母動態過濾 3,427 筆藥品主檔",
            "• 點選藥名自動秒出 6 碼藥號",
            "• 數量 > 50 顆即時跳紅框警戒"
        ],
        "tag": "📱 智慧防呆執行前台"
    },
    {
        "num": "中樞 04",
        "title": "SharePoint 資料庫",
        "sub": "角色：PRN 結構化儲存底座",
        "color_top": "#0078D4", # SharePoint 藍
        "border": "#0078D4",
        "lines": [
            "• 集中存放 PRN 導航遞交之數據",
            "• 3,427 筆藥品主檔安全對照",
            "• 雙團隊權限隔離（藥庫/會議）",
            "• 唯一合規雲端真實資料來源"
        ],
        "tag": "💾 雲端結構化儲存庫"
    },
    {
        "num": "中樞 05",
        "title": "Teams / Automate",
        "sub": "角色：PRN 審核水管與推播",
        "color_top": "#0066FF", # Automate 藍
        "border": "#0066FF",
        "lines": [
            "• 捕捉 PRN 送出單據自動路由",
            "• 發送主管手機/電腦自適應卡",
            "• 一鍵「核准/退件」即時回寫",
            "• 在 PRN 與 Teams 推播完成公告"
        ],
        "tag": "💬 流程流轉與行動審核"
    },
    {
        "num": "中樞 06",
        "title": "Power BI 戰情室",
        "sub": "角色：PRN 戰情儀表板大腦",
        "color_top": "#D97706", # Power BI 金
        "border": "#D97706",
        "lines": [
            "• 嵌入 PRN 智慧導航之主管儀表板",
            "• 即時統計各病房報廢損耗排行",
            "• 監控超量異常與審核時效 KPI",
            "• 報表內直接反向操作完成閉環"
        ],
        "tag": "📊 醫療決策數據中心"
    }
]

# 卡片幾何配置 (6 張卡片橫排，每張 570px，間距 48px)
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
    
    draw.rounded_rectangle([x1+8, y1+8, x2+8, y2+8], radius=22, fill='#E2E8F0')
    draw.rounded_rectangle([x1, y1, x2, y2], radius=22, fill='#FFFFFF', outline=step["border"], width=4)
    
    banner_h = 210
    draw.rounded_rectangle([x1, y1, x2, y1+banner_h], radius=22, fill=step["color_top"])
    draw.rectangle([x1, y1+banner_h-30, x2, y1+banner_h], fill=step["color_top"])
    
    draw.text((x1 + card_w//2, y1 + 50), step["num"], fill='#FFFFFF', font=step_num_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 115), step["title"], fill='#FFFFFF', font=box_title_font, anchor='mm')
    draw.text((x1 + card_w//2, y1 + 170), step["sub"], fill='#F1F5F9', font=box_sub_font, anchor='mm')
    
    tag_y = y1 + banner_h + 40
    draw.rounded_rectangle([x1+30, tag_y, x2-30, tag_y+60], radius=14, fill='#F1F5F9', outline='#CBD5E1', width=2)
    draw.text((x1 + card_w//2, tag_y + 30), step["tag"], fill=step["color_top"], font=badge_font, anchor='mm')
    
    text_start_y = tag_y + 110
    line_spacing = 135
    for j, line in enumerate(step["lines"]):
        ly = text_start_y + j * line_spacing
        draw.text((x1 + 35, ly), line, fill='#1E293B', font=box_desc_font)
        if j < len(step["lines"]) - 1:
            draw.line([x1+35, ly+90, x2-35, ly+90], fill='#F1F5F9', width=2)
            
    draw.rounded_rectangle([x1+35, y2-105, x2-35, y2-45], radius=12, fill=step["color_top"])
    draw.text((x1 + card_w//2, y2-75), "全流程定位指標", fill='#FFFFFF', font=badge_font, anchor='mm')
    
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
draw.text((80, H-65), "PRN 智慧導航體系：PRN 總入口 ➔ 本地 Agent 免安裝穿透防火牆 ➔ Power Apps 門戶嵌入 ➔ SharePoint 儲存 ➔ Teams 卡片審核 ➔ Power BI 儀表板", fill='#94A3B8', font=subtitle_font, anchor='lm')
draw.text((W-80, H-65), "奇美醫療財團法人 佳里奇美醫院 藥劑科", fill='#94A3B8', font=subtitle_font, anchor='rm')

output_path = '/Users/jiangruiyi/Documents/antigravity/藥劑科報廢流程表/PRN系統與微軟五大工具串接架構圖.png'
img.save(output_path, quality=95)
print("PRN Portal Flowchart regenerated successfully!")
