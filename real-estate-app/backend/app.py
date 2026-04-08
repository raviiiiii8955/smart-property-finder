"""PropFinder AI — Flask Backend"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import init_db
from routes.auth import auth_bp
from routes.properties import properties_bp
from routes.favorites import favorites_bp
from routes.live import live_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET', 'propfinder-secret-2024-xK9mP')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'flask-secret-2024-zR3vQ')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # tokens don't expire for dev

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(properties_bp, url_prefix='/api/properties')
app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
app.register_blueprint(live_bp, url_prefix='/api/live')

@app.route('/api/health')
def health():
    return {'status': 'ok', 'message': 'PropFinder API running'}

if __name__ == '__main__':
    init_db()
    print("✅ Database initialized")
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Server running at http://localhost:{port}")
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)
