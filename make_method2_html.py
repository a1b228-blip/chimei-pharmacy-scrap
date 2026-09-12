import pandas as pd
import json

df = pd.read_excel('藥品藥號.xlsx')
df = df.dropna(subset=['藥號', '藥品學名'])
drugs = df[['藥號', '藥品學名']].to_dict(orient='records')

drugs_json = json.dumps(drugs, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>佳里奇美醫院 藥劑科 - 抗生素報廢管理系統 (方法二本地驗收模擬器 · 3,427 筆藥品全量實測)</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background-color: #f8fafc; color: #1e293b; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }}
        .header {{ width: 100%; background-color: #005a9e; color: white; padding: 18px 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ font-size: 20px; font-weight: 600; }}
        .header-badge {{ background: rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 20px; font-size: 13px; }}
        .container {{ width: 980px; max-width: 95%; background: #ffffff; border-radius: 12px; margin-top: 36px; padding: 36px 44px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
        .method-banner {{ background: #eff6ff; border-left: 4px solid #0284c7; padding: 14px 18px; border-radius: 6px; margin-bottom: 24px; font-size: 13.5px; color: #0369a1; line-height: 1.6; }}
        .form-title {{ font-size: 18px; font-weight: 600; color: #0f172a; margin-bottom: 8px; }}
        .form-desc {{ font-size: 13px; color: #64748b; margin-bottom: 28px; border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; }}
        .grid-layout {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
        .form-group {{ display: flex; flex-direction: column; position: relative; }}
        .form-group label {{ font-size: 13px; font-weight: 600; color: #334155; margin-bottom: 8px; }}
        .form-control {{ height: 44px; border: 1px solid #cbd5e1; border-radius: 6px; padding: 0 14px; font-size: 14px; background-color: #ffffff; outline: none; transition: all 0.2s; width: 100%; }}
        .form-control:focus {{ border-color: #005a9e; box-shadow: 0 0 0 3px rgba(0,90,158,0.12); }}
        .form-control[readonly] {{ background-color: #f8fafc; color: #005a9e; font-weight: 700; cursor: not-allowed; }}
        .warning-text {{ color: #dc2626; font-size: 12.5px; font-weight: 600; margin-top: 6px; display: none; }}
        .warning-border {{ border-color: #dc2626 !important; box-shadow: 0 0 0 3px rgba(220,38,38,0.15) !important; }}
        .dropdown-list {{ position: absolute; top: 76px; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-radius: 6px; max-height: 240px; overflow-y: auto; z-index: 100; box-shadow: 0 8px 24px rgba(0,0,0,0.12); display: none; }}
        .dropdown-item {{ padding: 10px 14px; font-size: 13.5px; cursor: pointer; border-bottom: 1px solid #f1f5f9; }}
        .dropdown-item:hover {{ background-color: #f0f7ff; color: #005a9e; }}
        .dropdown-item b {{ color: #0284c7; }}
        .btn-submit {{ margin-top: 32px; height: 46px; background-color: #005a9e; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; }}
        .btn-submit:hover {{ background-color: #004578; }}
        .status-box {{ margin-top: 20px; padding: 14px; border-radius: 6px; background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; font-size: 13.5px; display: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 佳里奇美醫院 藥劑科 - 抗生素報廢管理系統</h1>
        <div class="header-badge">方法二：本地端即時模擬驗收（已載入 3,427 筆真實藥品）</div>
    </div>

    <div class="container">
        <div class="method-banner">
            <b>💡 方法二本地即時驗收說明：</b> 本畫面已直接掛載本機 <code>藥品藥號.xlsx</code> 內完整 <b>3,427 筆真實藥品清冊</b>。您可以在此親自驗收「英文字母動態快篩」、「藥名選取即時帶藥號」與「報廢數量大於 50 顆紅框警告」。本地完全滿意後，Agent 將一鍵打包上傳微軟 Power Apps！
        </div>

        <div class="form-title">抗生素報廢申請表單 (純白醫療風 · 雙欄排版)</div>
        <div class="form-desc">請填寫抗生素報廢品項。若報廢數量超過 50 顆將自動啟動專案複核程序。</div>

        <div class="grid-layout">
            <div class="form-group">
                <label>病房號碼 *</label>
                <select class="form-control" id="wardSelect">
                    <option value="5A 一般病房">5A 一般病房</option>
                    <option value="5B 一般病房">5B 一般病房</option>
                    <option value="6A 外科病房">6A 外科病房</option>
                    <option value="6B 骨科病房">6B 骨科病房</option>
                    <option value="7A 綜合病房">7A 綜合病房</option>
                    <option value="ICU 加護病房">ICU 加護病房</option>
                    <option value="急診醫學部">急診醫學部</option>
                    <option value="開刀房手術室">開刀房手術室</option>
                </select>
            </div>

            <div class="form-group">
                <label>報廢日期 (自動連動今天) *</label>
                <input type="date" class="form-control" id="scrapDate" readonly>
            </div>

            <div class="form-group">
                <label>藥品名稱 (打英文字母如 A、AD 即時篩選 3,427 筆藥品) *</label>
                <input type="text" class="form-control" id="drugSearch" placeholder="請輸入英文字母搜尋藥品 (例如 A 或 AD)..." autocomplete="off">
                <div class="dropdown-list" id="drugDropdown"></div>
            </div>

            <div class="form-group">
                <label>藥品代碼 (隨藥名選定自動帶出)</label>
                <input type="text" class="form-control" id="drugCode" placeholder="待選取藥品自動帶出" readonly>
            </div>

            <div class="form-group">
                <label>報廢數量 (超過 50 顆自動觸發紅色警告) *</label>
                <input type="number" class="form-control" id="qtyInput" placeholder="請輸入報廢數量 (例如 10)" min="1">
                <div class="warning-text" id="qtyWarning">⚠️ 注意：報廢數量大於 50 顆，依院內規定須提報科主任專案複核！</div>
            </div>

            <div class="form-group">
                <label>報廢原因 *</label>
                <select class="form-control" id="reasonSelect">
                    <option value="藥品逾期">藥品逾期</option>
                    <option value="外觀破損/變色">外觀破損/變色</option>
                    <option value="病人換藥/停藥退回">病人換藥/停藥退回</option>
                    <option value="冷藏溫度異常">冷藏溫度異常</option>
                </select>
            </div>
        </div>

        <button class="btn-submit" onclick="testSubmit()">🚀 本地模擬驗收確認無誤（準備由 Agent 打包至 Power Apps）</button>
        <div class="status-box" id="statusBox"></div>
    </div>

    <script>
        const drugData = {drugs_json};

        document.getElementById('scrapDate').valueAsDate = new Date();

        const searchInput = document.getElementById('drugSearch');
        const dropdown = document.getElementById('drugDropdown');
        const codeInput = document.getElementById('drugCode');
        const qtyInput = document.getElementById('qtyInput');
        const qtyWarning = document.getElementById('qtyWarning');
        const statusBox = document.getElementById('statusBox');

        searchInput.addEventListener('input', function() {{
            const val = this.value.trim().toLowerCase();
            if (!val) {{
                dropdown.style.display = 'none';
                return;
            }}
            const filtered = drugData.filter(d => d['藥品學名'].toLowerCase().startsWith(val)).slice(0, 50);
            if (filtered.length > 0) {{
                dropdown.innerHTML = filtered.map(d => 
                    `<div class="dropdown-item" onclick="selectDrug('${{d['藥號']}}', '${{d['藥品學名'].replace(/'/g, "\\\\'")}}')">
                        <b>${{d['藥號']}}</b> - ${{d['藥品學名']}}
                    </div>`
                ).join('');
                dropdown.style.display = 'block';
            }} else {{
                dropdown.innerHTML = '<div class="dropdown-item" style="color:#94a3b8;">查無匹配藥品，可直接手動輸入</div>';
                dropdown.style.display = 'block';
            }}
        }});

        document.addEventListener('click', function(e) {{
            if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {{
                dropdown.style.display = 'none';
            }}
        }});

        window.selectDrug = function(code, name) {{
            searchInput.value = name;
            codeInput.value = code;
            dropdown.style.display = 'none';
        }};

        qtyInput.addEventListener('input', function() {{
            const qty = parseFloat(this.value) || 0;
            if (qty > 50) {{
                this.classList.add('warning-border');
                qtyWarning.style.display = 'block';
            }} else {{
                this.classList.remove('warning-border');
                qtyWarning.style.display = 'none';
            }}
        }});

        window.testSubmit = function() {{
            const ward = document.getElementById('wardSelect').value;
            const drug = searchInput.value;
            const code = codeInput.value;
            const qty = qtyInput.value;
            const reason = document.getElementById('reasonSelect').value;
            const date = document.getElementById('scrapDate').value;

            if (!drug || !qty) {{
                alert('請先填寫藥品名稱與數量！');
                return;
            }}

            statusBox.innerHTML = `✅ <b>本地模擬驗收成功！</b><br/>已擷取完整資料：[${{date}}] ${{ward}} 申請報廢 <b>${{drug}}</b> (藥號: <b>${{code}}</b>)，數量：${{qty}}，原因：${{reason}}。<br/><b>下一步：</b>通知 Agent 執行 PAC CLI 打包成實體 .msapp 上傳 Power Apps 即可正式上線！`;
            statusBox.style.display = 'block';
        }};
    </script>
</body>
</html>"""

with open('抗生素報廢管理App_方法二本地驗收模擬器.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Method 2 HTML Simulator generated successfully!')
