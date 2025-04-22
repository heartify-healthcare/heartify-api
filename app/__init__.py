from flask import Flask
from app.config import config_by_name
import os

def create_app(config_name='dev'):
    """
    Factory function to create and configure the Flask application.
    
    Args:
        config_name: Configuration to use ('dev', 'prod', 'test')
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Create model directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Import and register blueprints
    from app.routes import register_routes
    register_routes(app)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Simple health check endpoint."""
        return {'status': 'healthy'}, 200
    
    return app