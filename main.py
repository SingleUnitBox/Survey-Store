import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.testing import db
from forms import AddNewItemForm, LoginForm, RegisterForm
from datetime import date, datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xfd{Hxe5<x95f9xe3x96.5xd1x01O<!xd5x'
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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///store.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

@app.route('/')
def home():
    items = Item.query.all()
    return render_template("index.html", all_items=items, logged_in=current_user.is_authenticated, user=current_user)

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
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated, title="Log in")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        with app.app_context():
            user = db.session.query(User).filter_by(name=name).first()
            if user:
                flash("You are registered already. Please Log In instead.")
                return redirect(url_for(("login")))
            elif password != confirm_password:
                flash("Passwords do not match. Please try again.")
                return redirect(url_for(("register")))
            else:
                flash(f"Account for {name} created.")
                return redirect(url_for(("home")))


    return render_template("register.html", form=form, title="Register")

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
            #date=datetime.now().strftime("%d/%m/%y %H:%M")
        )
        with app.app_context():
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_new_item.html", form=form, logged_in=current_user.is_authenticated, title="Add")

@app.route('/store/<int:item_id>', methods=["GET", "POST"])
def take_items(item_id):
    item = Item.query.get(item_id)
    #print(item.location.name)
    if item.location.name == "Bilsthorpe":
        item.location_id = 4
        #item.location_id = current_user.id
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('home'))
    elif item.location_id == current_user.id:
        item.location_id = 5
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('home'))
    elif item.location_id == 4:
        item.location_id = current_user.id
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete/<int:item_id>')
@admin_only
def delete(item_id):
    item_to_delete = Item.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)