from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # ✅ FIX: Ensure CORS allows Netlify and local development access
    CORS(app, resources={r"/*": {"origins": ["https://your-personal-history.netlify.app", "http://localhost:3000", "http://127.0.0.1:5000"]}})

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
