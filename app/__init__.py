from flask import Flask
import os

def create_app():
    """
    Erstellt und konfiguriert die Flask-App
    """
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # Stelle sicher, dass die erforderlichen Verzeichnisse existieren
    os.makedirs('../static/photos', exist_ok=True)
    os.makedirs('../static/test', exist_ok=True)
    
    # Registriere die Blueprints (Routen)
    from app.routes import main_bp, api_bp, device_bp, photo_bp, diagnostic_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(device_bp, url_prefix='/devices')
    app.register_blueprint(photo_bp, url_prefix='/photos')
    app.register_blueprint(diagnostic_bp, url_prefix='/diagnostics')
    
    return app
