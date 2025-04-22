from app import create_app
import os

# Get configuration from environment or default to 'dev'
config_name = os.environ.get('FLASK_CONFIG', 'dev')

# Create the Flask application
app = create_app(config_name)

if __name__ == '__main__':
    # This is used when running the application directly with Python
    # For production, use a proper WSGI server (e.g., Gunicorn)
    app.run(host='0.0.0.0', port=5000)