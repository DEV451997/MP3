import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Error handler for 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Home page and stats route
@app.route("/")
@app.route("/get_stats")
def get_stats():
    stats = list(mongo.db.stats.find())
    return render_template("stats.html", stats=stats)


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
    return render_template("register.html")


# User login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:

            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                            request.form.get("username")))
                return redirect(url_for(
                            "profile", username=session["user"]))
            else:

                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:

            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# User profile route
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    user_stats = list(mongo.db.stats.find({"created_by": session["user"]}))

    if session.get("user"):
        return render_template("profile.html",
                               username=username, user_stats=user_stats)

    return redirect(url_for("login"))


# User logout route
@app.route("/logout")
def logout():

    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add car route
@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        car = {
            "category_name": request.form.get("category_name"),
            "manufacturer": request.form.get("manufacturer"),
            "model": request.form.get("model"),
            "engine": request.form.get("engine"),
            "horsepower": request.form.get("horsepower"),
            "image_url": request.form.get("image_url"),
            "created_by": session.get("user")
        }
        mongo.db.stats.insert_one(car)
        flash("Car Successfully Added")
        return redirect(url_for("get_stats"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_car.html", categories=categories)


# Edit car route
@app.route("/edit_car/<stats_id>", methods=["GET", "POST"])
def edit_car(stats_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "manufacturer": request.form.get("manufacturer"),
            "model": request.form.get("model"),
            "engine": request.form.get("engine"),
            "horsepower": request.form.get("horsepower"),
            "image_url": request.form.get("image_url"),
        }
        mongo.db.stats.update_one({"_id": ObjectId(stats_id)},
                                  {"$set": submit})
        flash("Car Successfully Updated")

    stats_id_obj = ObjectId(stats_id)
    stat = mongo.db.stats.find_one({"_id": stats_id_obj})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_car.html", stat=stat, categories=categories)


# Delete car route
@app.route("/delete_car/<stats_id>")
def delete_car(stats_id):
    mongo.db.stats.delete_one({"_id": ObjectId(stats_id)})
    flash("Car Successfully Deleted")
    return redirect(url_for("get_stats"))


# Run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
