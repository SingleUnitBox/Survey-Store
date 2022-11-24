#MAIN needs to be changed after renaming
from __main__ import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(20), unique=True, nullable=False)
    items = relationship("Item", back_populates="location")

    def __repr__(self):
        return f"User({self.name}, {self.password})"


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(20), nullable=False, default=datetime.now().strftime("%d/%m/%y %H:%M"))

    location_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location = relationship("User", back_populates="items")


# with app.app_context():
#     db.create_all()
#     db.session.commit()