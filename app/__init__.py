"""
Flask Application Factory.
Web-only context - separado de la lógica de negocio.
"""
from flask import Flask
from config import config


def create_app(config_name='default'):
    """
    Factory pattern para crear la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a usar (development, production, testing)
    
    Returns:
        Aplicación Flask configurada
    """
    app = Flask(__name__)
    
    #  flask
    app.config.from_object(config[config_name])
    
    # blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app
