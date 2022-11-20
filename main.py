from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.testing import db
from forms import AddNewItemForm, LoginForm, TakeItem, EditForm
from datetime import date, datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'czczcz'
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    items = relationship("Item", back_populates="location")


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date = db.Column(db.String(250), nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location = relationship("User", back_populates="items")


# with app.app_context():
#     db.create_all()
#     db.session.commit()

@app.route('/')
def home():
    items = Item.query.all()
    return render_template("index.html", all_items=items, logged_in=current_user.is_authenticated)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        with app.app_context():
            user = db.session.query(User).filter_by(name=name).first()
            if not user:
                flash("That name does not exist, please try again.")
                return redirect(url_for("login"))
            elif user.password != password:
                flash("Wrong password, please try again.")
                return redirect(url_for("login"))
            else:
                login_user(user)
                return redirect(url_for(("home")))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add', methods=["GET", "POST"])
@admin_only
def add_new_item():
    form = AddNewItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            location=current_user,
            date=datetime.now().strftime("%d/%m/%y %H:%M")
        )
        with app.app_context():
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_new_item.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/store/<int:item_id>', methods=["GET", "POST"])
def take_items(item_id):


    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)