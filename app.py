
from flask import Flask, request, jsonify
from fake_useragent import UserAgent
import requests
from flask_cors import CORS
from flask import Flask, render_template_string, request
app = Flask(__name__)
CORS(app)
ua = UserAgent()

HTML = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>MARWAN</title>
    <style>
        body {
            font-family: 'Arial';
            background: #121C2A;
            color: white;
            text-align: center;
            padding: 50px;
        }
        input[type="text"] {
            width: 80%;
            height: 80px;
            background-color: #2c3e50;
            color: white;
            border: 2px solid #3498db;
            border-radius: 10px;
            font-size: 20px;
            padding: 10px;
            margin: 10px;
            text-align: right;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 15px 30px;
            font-size: 24px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            margin-top: 25px;
        }
        button:hover {
            background-color: #2980b9;
        }
        #response {
            margin-top: 30px;
            background-color: white;
            color: #000000;
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
            white-space: pre-wrap;
            text-align: right;
            font-size: 18px;
            font-weight: bold;
        }
        .icon-btn {
            font-size: 22px;
            margin: 10px;
            padding: 10px 20px;
        }
        .social-links {
            margin-top: 30px;
            font-size: 18px;
        }
        .social-links a {
            margin: 0 10px;
            color: #3498db;
            text-decoration: none;
        }
        .social-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>DEV BY  <span style="color: #3498db;">MARWAN</span></h1>
    <input type="text" id="question" placeholder="اكتب سؤالك هنا"><br>
    <button onclick="ask()">📩</button>
    <div id="response"></div>
    <button id="copyBtn" class="icon-btn" style="display:none" onclick="copyResponse()">📋</button>
    <script>
        function ask() {
            const message = document.getElementById("question").value;
            if (message.trim() === '') {
                document.getElementById("response").innerText = "يرجى إدخال سؤال.";
                return;
            }
            document.getElementById("response").innerText = "جارٍ المعالجة...";
            fetch("/ask", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({message})
            })
            .then(res => res.text())
            .then(data => {
                document.getElementById("response").innerText = data;
                document.getElementById("copyBtn").style.display = "inline-block";
                document.getElementById("question").value = '';
            })
            .catch(err => {
                document.getElementById("response").innerText = "حصل خطأ: " + err;
            });
        }
        function copyResponse() {
            const responseText = document.getElementById("response").innerText;
            navigator.clipboard.writeText(responseText).then(() => {
                alert("تم نسخ الرد!");
            }).catch(err => {
                alert("فشل النسخ: " + err);
            });
        }
    </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    mess = data.get('message', '')
    headers = {
        'authority': 'www.blackbox.ai',
        'accept': '*/*',
        'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.blackbox.ai',
        'pragma': 'no-cache',
        'referer': 'https://www.blackbox.ai',
        'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random,
    }
    cookies = {
        'sessionId': '0b7edce6-c44b-45d2-8215-378b7679081d',
        'render_app_version_affinity': 'dep-d02fksadbo4c73ept6lg',
        '__Host-authjs.csrf-token': 'fake-token',
        '__Secure-authjs.callback-url': 'https%3A%2F%2Fwww.blackbox.ai',
        'intercom-id-x55eda6t': 'fake-id',
        'intercom-session-x55eda6t': '',
        'intercom-device-id-x55eda6t': 'fake-device-id',
    }
    json_data = {
        'messages': [{'id': 'kwlV6l6','content': mess,'role': 'user',}],
        'agentMode': {},'id': 'kwlV6l6','previewToken': None,'userId': None,
        'codeModelMode': True,'trendingAgentMode': {},'isMicMode': False,
        'userSystemPrompt': None,'maxTokens': 1024,'playgroundTopP': None,
        'playgroundTemperature': None,'isChromeExt': False,'githubToken': '',
        'clickedAnswer2': False,'clickedAnswer3': False,
        'clickedForceWebSearch': False,'visitFromDelta': True,
        'isMemoryEnabled': False,'mobileClient': False,'userSelectedModel': None,
        'validated': '00f37b34-a166-4efb-bce5-1312d87f2f94',
        'imageGenerationMode': True,'webSearchModePrompt': False,
        'deepSearchMode': False,'domains': None,'vscodeClient': False,
        'codeInterpreterMode': False,'customProfile': {'name': '','occupation': '','traits': [],'additionalInfo': '','enableNewChats': False,},
        'session': None,'isPremium': False,'subscriptionCache': None,
        'beastMode': False,'reasoningMode': False,
    }
    try:
        res = requests.post('https://www.blackbox.ai/api/chat', headers=headers, cookies=cookies, json=json_data)
        return res.text
    except Exception as e:
        return f"صار خطأ: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
