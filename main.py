from app import create_app
from flask_cors import CORS  # ✅ Import CORS

app = create_app()
CORS(app)  # ✅ Enable CORS globally

if __name__ == '__main__':
import os
port = int(os.environ.get("PORT", 10000))  # Render provides PORT dynamically
app.run(host="0.0.0.0", port=port, debug=True)

