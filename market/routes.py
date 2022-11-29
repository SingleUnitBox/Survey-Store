from datetime import datetime
from functools import wraps
from market import app
from flask import render_template, redirect, url_for, flash, abort
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, AddItemForm
from market import db
from flask_login import login_user, logout_user, current_user


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route('/store')
#@login_required
def store_page():
    items = Item.query.all()
    return render_template("store.html", items=items, )


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              #email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! you are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for("store_page"))
    if form.errors != {}:
        for error_msg in form.errors.values():
            flash(f"There was an error with creating user: {error_msg}", category='danger')
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
            return redirect(url_for("store_page"))
        else:
            flash("Username and password are not match! Please try again", category="danger")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))


@app.route('/add', methods=["GET", "POST"])
@admin_only
def add_new_item():
    form = AddItemForm()
    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            location=current_user,
            #date=datetime.now().strftime("%d/%m/%y %H:%M")
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("store_page"))
    return render_template("add.html", form=form)


@app.route('/delete/<int:item_id>')
@admin_only
def delete(item_id):
    item_to_delete = Item.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('store_page'))


@app.route('/store/<int:item_id>', methods=["GET", "POST"])
def take_items(item_id):
    item = Item.query.get(item_id)
    #print(item.location_id)
    if item.location.username == "Bilsthorpe":
        item.location_id = 4
        #item.location_id = current_user.id
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('store_page'))
    elif item.location_id == current_user.id:
        item.location_id = 5
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('store_page'))
    elif item.location_id == 4:
        item.location_id = current_user.id
        item.date = datetime.now().strftime("%d/%m/%y %H:%M")
        db.session.commit()
        return redirect(url_for('store_page'))
    return redirect(url_for('store_page'))


@app.route('/scale')
def scale_page():
    pass
    return render_template("scale.html")
