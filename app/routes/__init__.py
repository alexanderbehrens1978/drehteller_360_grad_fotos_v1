from app.routes.main_routes import main_bp
from app.routes.api_routes import api_bp
from app.routes.device_routes import device_bp
from app.routes.photo_routes import photo_bp
from app.routes.diagnostic_routes import diagnostic_bp

__all__ = ['main_bp', 'api_bp', 'device_bp', 'photo_bp', 'diagnostic_bp']
