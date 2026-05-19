from flask import Blueprint, request, jsonify
import sqlite3
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint('auth', __name__)
JWT_SECRET = os.environ.get("JWT_SECRET", "병아리2026")
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 회원가입
@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    hashed = bcrypt.hashpw(
        password.encode(), bcrypt.gensalt()
    ).decode()

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
            (email, hashed, name)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "회원가입 완료"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"message": "이미 사용중인 이메일입니다"}), 409

# 로그인
@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({"message": "이메일이 존재하지 않습니다"}), 404

    if not bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):
        return jsonify({"message": "비밀번호가 틀렸습니다"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return jsonify({
        "message": "로그인 성공",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
    }), 200

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "토큰이 없습니다"}), 401

        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = data["user_id"]
        except:
            return jsonify({"message": "유효하지 않은 토큰입니다"}), 401

        return f(*args, **kwargs)
    return decorated