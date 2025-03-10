from app import create_app
from flask_cors import CORS  # ✅ Import CORS

app = create_app()
CORS(app)  # ✅ Enable CORS globally

if __name__ == '__main__':
    app.run(debug=True)
