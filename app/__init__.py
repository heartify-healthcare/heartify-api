"""
Main application factory module.
"""
from flask import Flask
from app.config import Config
from app.routes import register_routes

def create_app(config_class=Config):
    """
    Application factory that creates and configures a Flask application.
    
    Args:
        config_class: Configuration class to use for the application.
        
    Returns:
        Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register all routes and blueprints
    register_routes(app)
    
    @app.route('/health')
    def health_check():
        """Basic health check endpoint"""
        return {'status': 'ok'}
    
    return app