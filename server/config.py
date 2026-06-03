import os
from dotenv import load_dotenv
from datetime import timedelta

# Only load .env in development (when DATABASE_URL is not set)
if not os.environ.get('DATABASE_URL'):
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Debug: Print what DATABASE_URL we're getting
    db_url = os.environ.get('DATABASE_URL')
    print(f"🔍 DATABASE_URL from environment: {db_url[:50] if db_url else 'NOT SET'}")
    
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///driftwood_cafe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Payment configurations
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
    MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY')
    MPESA_INITIATOR_NAME = os.environ.get('MPESA_INITIATOR_NAME', 'testapi')
    MPESA_SECURITY_CREDENTIAL = os.environ.get('MPESA_SECURITY_CREDENTIAL', '')
    
    # Application URL (for callbacks)
    APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    OWNER_EMAIL = os.environ.get('OWNER_EMAIL')
    
    # Client origin for CORS
    CLIENT_ORIGIN = os.environ.get('CLIENT_ORIGIN', 'http://localhost:5173')
    
    # File upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size