from app.prediction import prediction_bp
from app.users import user_bp

def register_routes(app):
    # Register blueprints
    app.register_blueprint(prediction_bp, url_prefix='/prediction')
    app.register_blueprint(user_bp, url_prefix='/users')