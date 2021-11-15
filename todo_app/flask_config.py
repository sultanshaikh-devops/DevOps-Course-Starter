import os
class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOGIN_DISABLED = os.environ.get('LOGIN_DISABLED') == "True"
    LOG_LEVEL = os.environ.get('LOG_LEVEL')
    LOGGLY_TOKEN=os.environ.get('LOGGLY_TOKEN')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
