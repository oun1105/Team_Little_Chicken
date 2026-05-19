from flask import Blueprint, request, jsonify
import sqlite3
import os

team = Blueprint('team', __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_team_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            user_id INTEGER,
            role TEXT DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 팀 생성
@team.route("/team/create", methods=["POST"])
def create_team():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    deadline = data.get("deadline")
    user_id = data.get("user_id")

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO teams (name, description, deadline) VALUES (?, ?, ?)",
        (name, description, deadline)
    )
    team_id = cursor.lastrowid

    conn.execute(
        "INSERT INTO members (team_id, user_id, role) VALUES (?, ?, ?)",
        (team_id, user_id, 'leader')
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": "팀 생성 완료",
        "team_id": team_id
    }), 201

# 팀 목록 조회
@team.route("/team/list", methods=["GET"])
def get_teams():
    conn = get_db()
    teams = conn.execute("SELECT * FROM teams").fetchall()
    conn.close()

    return jsonify([dict(t) for t in teams]), 200

# 팀 참여
@team.route("/team/join", methods=["POST"])
def join_team():
    data = request.json
    team_id = data.get("team_id")
    user_id = data.get("user_id")

    conn = get_db()

    # 이미 참여한 팀인지 확인
    existing = conn.execute(
        "SELECT * FROM members WHERE team_id=? AND user_id=?",
        (team_id, user_id)
    ).fetchone()

    if existing:
        return jsonify({"message": "이미 참여한 팀입니다"}), 409

    conn.execute(
        "INSERT INTO members (team_id, user_id, role) VALUES (?, ?, ?)",
        (team_id, user_id, 'member')
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "팀 참여 완료"}), 201