from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.testing import db
from forms import AddNewItemForm
from datetime import date, datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'czczcz'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    #posts = relationship("BlogPost", back_populates="author")
    #comments = relationship("Comment", back_populates="comment_author")

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(50))
    date = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def home():
    items = Item.query.all()
    return render_template("index.html", all_items=items)

@app.route('/add', methods=["GET", "POST"])
def add_new_item():
    form = AddNewItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            date=datetime.now().strftime("%d/%m/%y %H:%M")
        )
        with app.app_context():
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_new_item.html", form=form)




if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)