#!/usr/bin/env python
import os
import click
from flask.cli import FlaskGroup
from app import create_app
import shutil

# Create Flask application
app = create_app(os.environ.get('FLASK_CONFIG', 'dev'))

# Create CLI group
cli = FlaskGroup(create_app=lambda: app)

@cli.command('init')
def initialize():
    """Initialize the application with necessary directories and files."""
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    click.echo('Created models directory')
    
    # Check for model and scaler files in the current directory
    # and move them to the models directory if found
    if os.path.exists('heart_cnn_lstm_model.keras'):
        shutil.move('heart_cnn_lstm_model.keras', 'models/heart_cnn_lstm_model.keras')
        click.echo('Moved heart_cnn_lstm_model.keras to models directory')
    
    if os.path.exists('scaler.save'):
        shutil.move('scaler.save', 'models/scaler.save')
        click.echo('Moved scaler.save to models directory')
    
    click.echo('Initialization complete')

@cli.command('check-models')
def check_models():
    """Check if model files exist in the correct location."""
    model_path = os.path.join('models', 'heart_cnn_lstm_model.keras')
    scaler_path = os.path.join('models', 'scaler.save')
    
    if os.path.exists(model_path):
        click.echo(f"Model found: {model_path}")
    else:
        click.echo(f"Model not found: {model_path}")
    
    if os.path.exists(scaler_path):
        click.echo(f"Scaler found: {scaler_path}")
    else:
        click.echo(f"Scaler not found: {scaler_path}")

if __name__ == '__main__':
    cli()