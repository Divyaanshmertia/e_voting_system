import os

class Config:
    # Secret key for encrypting cookies
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')

    # Flask settings
    FLASK_APP = 'run.py'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

    # SQLAlchemy settings
    # For Cloud SQL (replace placeholders with your actual values)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root@/db?unix_socket=/cloudsql/securityproject-419120:us-central1:db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Google Cloud Storage settings
    GCS_BUCKET = os.environ.get('GCS_BUCKET', 'your_default_gcs_bucket_name')

    # Additional custom settings can be added here
    # For example, configuration for email server:
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Further configuration settings like logging, API keys, etc.
