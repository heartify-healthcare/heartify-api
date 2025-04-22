import os

class Config:
    """Base configuration for the Flask application."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    DEBUG = False
    TESTING = False
    
    # Model paths
    MODEL_PATH = os.environ.get('MODEL_PATH', 'models/heart_cnn_lstm_model.keras')
    SCALER_PATH = os.environ.get('SCALER_PATH', 'models/scaler.save')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    # In production, ensure SECRET_KEY is set in environment variables
    pass

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    
# Configuration dictionary
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}