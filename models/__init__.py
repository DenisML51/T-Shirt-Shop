from flask_sqlalchemy import SQLAlchemy
from models.models import db, TShirtModel, Color, Size, Print, TShirtCombination, PrintCompatibility


db = SQLAlchemy()
