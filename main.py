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

        # [수정된 부분] responseUrl 방식에서는 connectInfo가 필요 없으므로 삭제합니다.
        response_url = data.get('responseUrl')
        if response_url:
            response_data = {"text": response_body}
            requests.post(response_url, json=response_data)

    return jsonify(success=True)

@app.route('/forward-to-jandi', methods=['POST'])
def forward_to_jandi():
    gpts_data = request.json
    if JANDI_HR_URL:
        requests.post(JANDI_HR_URL, json=gpts_data)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
