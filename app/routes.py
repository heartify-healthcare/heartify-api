from flask import Flask

def register_routes(app: Flask):
    """
    Register all API blueprints/routes with the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Import blueprints
    from app.prediction.controller import prediction_bp
    
    # Register blueprints
    app.register_blueprint(prediction_bp)
    
    # Note: auth and users blueprints will be implemented later