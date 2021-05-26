from flask_sqlalchemy import SQLAlchemy
from app import db
class Urls():
    link = db.Column(db.String(80))
    redirect_url = db.Column(db.String(80))
