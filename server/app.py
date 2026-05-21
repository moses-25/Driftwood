from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, mail
from routes import register_routes
from database.connection import test_database_connection

def test():
    is_connected = test_database_connection()

    if is_connected:
        print("Application started successfully.")
    else:
        print("Application could not start.")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Register routes
    register_routes(app)
    
    test()
    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
    