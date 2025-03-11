from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes, restricted to your Netlify frontend URL
    CORS(app, resources={r"/*": {"origins": "https://your-personal-history.netlify.app"}})

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
