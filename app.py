from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# .env 파일에서 환경변수 불러오기
load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase 클라이언트 초기화
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 서버 연결 확인용 테스트 라우트
@app.route("/")
def index():
    return {"message": "Little Chicken 서버 정상 작동 중 🐥"}, 200

@app.route("/ping")
def ping():
    results = {}
    tables = ["users", "teams", "team_members", "messages", "summaries", "schedules", "tasks"]
    for table in tables:
        try:
            supabase.table(table).select("*").limit(1).execute()
            results[table] = "✅"
        except Exception as e:
            results[table] = f"❌ {str(e)}"
    return {"tables": results}, 200
if __name__ == "__main__":
    app.run(debug=True, port=5000)