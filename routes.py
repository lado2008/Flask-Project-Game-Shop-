from flask import render_template, redirect
from forms import AddProductForm, EditProductForm, RegistrForm, LoginForm, IsDisplayedForm
from os import path
from extensions import app, db
from models import Products, User
from flask_login import login_user, logout_user, login_required, current_user
from flask import flash


@app.route("/")
def home():
   products = Products.query.filter_by(is_displayed=True).all()
   return render_template("index.html", products=products)

@app.route("/notifications")
@login_required
def notifications():
    if current_user.role != "admin":
        return redirect("/")
    products = Products.query.filter_by(is_displayed=False).all()
    return render_template("notifications.html", products=products)

@app.route("/view_product/<int:index>", methods=["GET", "POST"])
def view_product(index):
   product = Products.query.get(index)
   form = IsDisplayedForm()

   if form.validate_on_submit():
       product.is_displayed = form.checkbox.data
       db.session.commit()

   return render_template("product.html", product=product, form=form)

@app.route("/about")
def about_us():
    return render_template("about.html")

@app.route("/upload_game", methods=["POST", "GET"])
@login_required
def upload_game():
    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Products(name=form.name.data, price=form.price.data, img=form.img.data.filename,
                               description=form.about_game.data, user_id=current_user.id, game=form.game.data.filename)
        db.session.add(new_product)
        db.session.commit()

        file_dir = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_dir)

        file_dir_2 = path.join(app.root_path, "static", form.game.data.filename)
        form.game.data.save(file_dir_2)
        flash("Product uploaded successfully. Wait for admin approval.", "info")
        return redirect("/")
    return render_template("upload_game.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("log_in.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/registration", methods=["POST", "GET"])
def registration():
    form = RegistrForm()
    error_message = None

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            error_message = "Username already exists. Please choose a different username."
        else:
            user = User(username=form.username.data, password=form.password.data, role="guest")
            user.create()
            return redirect("/login")

    return render_template("registration.html", form=form, error_message=error_message)

@app.route("/edit_products/<int:index>", methods=["POST", "GET"])
@login_required
def edit_products(index):
    product = Products.query.get(index)
    form = EditProductForm()

    if current_user.role == "admin" or (current_user.role == "guest" and current_user.id == product.user_id):
        if form.validate_on_submit():
            product.description = form.about_game.data
            product.name = form.name.data
            product.price = form.price.data

            if form.img.data:
                product.img = form.img.data.filename

                file_dir = path.join(app.root_path, "static", form.img.data.filename)
                form.img.data.save(file_dir)

            if form.game.data:
                product.game = form.game.data.filename

                file_dir_2 = path.join(app.root_path, "static", form.game.data.filename)
                form.game.data.save(file_dir_2)

            db.session.commit()
            flash("Product edited successfully.", "success")
            return redirect("/")

        form.about_game.data = product.description
        form.name.data = product.name
        form.price.data = product.price
        form.img.data = product.img
        form.game.data = product.game

        return render_template("edit_game.html", form=form, product=product)
    else:
        flash("You don't have permission to edit this product.", "danger")
        return redirect("/")

@app.route("/delete_products/<int:index>")
@login_required
def delete_product(index):
    if current_user.role == "admin" or current_user.role == "guest":
        product = Products.query.get(index)
        db.session.delete(product)
        db.session.commit()
        return redirect("/")

@app.route("/library")
@login_required
def library():
    user_products = Products.query.filter_by(user_id=current_user.id).all()
    return render_template("library.html", user_products=user_products)
