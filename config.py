import os


class FlaskConfig:
    """Configuración base de Flask."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    JSON_AS_ASCII = False
    
    DEBUG = False
    TESTING = False


class DevelopmentConfig(FlaskConfig):
    """Configuración para desarrollo."""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(FlaskConfig):
    """Configuración para producción."""
    DEBUG = False
    ENV = 'production'


class TestingConfig(FlaskConfig):
    """Configuración para testing."""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}