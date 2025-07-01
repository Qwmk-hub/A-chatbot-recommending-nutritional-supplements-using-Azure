# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, jsonify, make_response, send_from_directory
from openai import AzureOpenAI

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.supplement import Supplement
from src.routes.user import user_bp
from src.routes.supplement import supplement_bp

# Flask 앱 설정
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB 초기화
db.init_app(app)
with app.app_context():
    db.create_all()

# 블루프린트 등록
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(supplement_bp, url_prefix='/api/supplements')

# Azure OpenAI 설정
client = AzureOpenAI(
    api_key="DACG8zSfz6wi4BtnHPzaYYNkScF3jh1b5ZEoJ7MY0WQ0ZPeUIFHHJQQJ99BEACNns7RXJ3w3AAABACOGxCyB",
    api_version="2023-07-01-preview",
    azure_endpoint="https://leejunghyun.openai.azure.com/"
)

# 시스템 프롬프트
SYSTEM_PROMPT = (
    "너는 지금부터 영양제 박사야. 고객이 영양제 추천이나 상담을 요청하면, "
    "다음 정보(키, 몸무게, 나이, 성별)를 바탕으로 답변해. "
    "또한 복용하면 좋은 시간(아침, 점심, 저녁, 취침 전)과 "
    "공복 또는 식후 중 어떤 타이밍이 적절한지도 설명해줘."
)

# Chatbot API 엔드포인트
@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        height = data.get("height")
        weight = data.get("weight")
        age = data.get("age")
        gender = data.get("gender")
        message = data.get("message")

        user_prompt = f"사용자 정보: 키 {height}cm, 몸무게 {weight}kg, 나이 {age}세, 성별 {gender}. 질문: {message}"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )

        answer = response.choices[0].message.content
        flask_response = make_response(jsonify({"response": answer}))
        flask_response.headers["Content-Type"] = "application/json; charset=utf-8"
        return flask_response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 정적 파일 서빙
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# 서버 실행
if __name__ == '__main__':
    from add_sample_data import add_sample_supplements
    add_sample_supplements()
    app.run(port=5000, debug=True)