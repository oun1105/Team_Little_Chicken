from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.auth import auth, init_db

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth, url_prefix="/api")

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)