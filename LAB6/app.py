from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from models.database import db
from models.electro_scooter import ElectroScooter 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1111@localhost:5432/scooters'
    migrate = Migrate(app, db)
    db.init_app(app)
    

    return app


if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()