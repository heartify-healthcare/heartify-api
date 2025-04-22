"""
Routes registration module for the application.
"""
from app.prediction.controller import prediction_bp

def register_routes(app):
    """
    Register all routes and blueprints for the application.
    
    Args:
        app: Flask application instance.
    """
    # Register blueprints
    app.register_blueprint(prediction_bp, url_prefix='/api/prediction')