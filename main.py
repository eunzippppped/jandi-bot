from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GPTS_LINK = os.environ.get('GPTS_LINK')
JANDI_GUIDE_URL = os.environ.get('JANDI_GUIDE_URL') 
JANDI_HR_URL = os.environ.get('JANDI_HR_URL')

@app.route('/')
def home():
    return "I'm alive!"

@app.route('/jandi-guide-bot', methods=['POST'])
def handle_guide_request():
    data = request.json
    if data.get('keyword') == '증명서':
        writer_name = data.get('writerName', '요청자')
        if not GPTS_LINK:
            response_body = "오류: 관리자가 GPTs 링크를 아직 설정하지 않았습니다."
        else:
            response_body = f"""{writer_name}님, 증명서 발급 신청을 도와드릴게요.
아래 링크를 클릭하여 전용 챗봇과 대화를 시작해주세요.

▶ [증명서 신청 챗봇 바로가기]({GPTS_LINK})
            """
        headers = {'Accept': 'application/vnd.tosslab.jandi-v2+json', 'Content-Type': 'application/json'}
        payload = {
            "body": response_body,
            "connectColor": "#FAC11B",
            "connectInfo": [{"contentType": "text"}] # ★★★ 이 줄이 미리보기를 없애줍니다.
        }
        
        if JANDI_GUIDE_URL:
            requests.post(JANDI_GUIDE_URL, json=payload, headers=headers)
    return jsonify(success=True)

@app.route('/forward-to-jandi', methods=['POST'])
def forward_to_jandi():
    gpts_data = request.json
    if JANDI_HR_URL:
        requests.post(JANDI_HR_URL, json=gpts_data)
    return jsonify(success=True)
