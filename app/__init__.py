from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # ✅ Fix: Explicitly Allow Netlify Requests
    CORS(app, resources={r"/*": {
        "origins": [
            "https://your-personal-history.netlify.app",
            "http://localhost:3000",
            "http://127.0.0.1:5000"
        ],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "OPTIONS"]
    }}, supports_credentials=True)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

