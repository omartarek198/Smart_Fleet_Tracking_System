import flask
import mysql.connector
from flask import Flask, request, redirect, render_template
import flask_login
from forms import UserForm
from models import User
from flask import Flask, render_template, redirect, url_for, request, flash

import models

app = Flask(__name__)
app.secret_key = "kodqwpjdqwodOIWJDnqDIOJ209E019"
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# Configure MySQL connection
db_config = mysql.connector.Connect(
    host="localhost",
    user="me",
    # user='root',
    password="",
    database="system",
)
db = db_config


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user_app/<int:user_id>")
def user_app(user_id):
    user = User.get(user_id, db_config)
    if not user:
        return redirect("/user")
    return redirect(f"/{user.user_type}")

# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["email"]
#         password = request.form["password"]

#         # with db.cursor() as cursor:
#         #     query = "SELECT user_type FROM user WHERE email=%s AND passwd=%s"
#         #     cursor.execute(query, (username, password))
#         #     user = cursor.fetchone()
#         user = models.User(0, 'admin', 'someone@something.com', 'adbasj', 'Admin', 'Admin')

#         if user:
#             user_type = user["user_type"]
#             if user_type == "admin":
#                 return redirect("/admin")
#             elif user_type == "passenger":
#                 return redirect("/passenger")
#             elif user_type == "driver":
#                 return redirect("/driver")

#     return redirect(flask.url_for("signup"))


@app.route("/user", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        connection = db_config
        # connection = mysql.connector.connect(**db_config)
        user = User(
            id=None,
            user_type=form.user_type.data,
            email=form.email.data,
            passwd=form.passwd.data,
            fname=form.fname.data,
            lname=form.lname.data,
        )
        print('hi')
        user.insert(connection)
        flash("User created successfully!", "success")
        return redirect(url_for('user_app', user_id=user.id))
        # return redirect(url_for(f"update_user", user_id=user.id))

    return render_template("user_form.html", form=form)


@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    form = UserForm()
    # connection = mysql.connector.connect(**db_config)
    connection = db_config

    if request.method == "GET":
        user = User.get(user_id, connection)
        form.id.data = user.id
        form.user_type.data = user.user_type
        form.email.data = user.email
        form.passwd.data = user.passwd
        form.fname.data = user.fname
        form.lname.data = user.lname

    if form.validate_on_submit():
        user = User(
            id=form.id.data,
            user_type=form.user_type.data,
            email=form.email.data,
            passwd=form.passwd.data,
            fname=form.fname.data,
            lname=form.lname.data,
        )
        user.update(connection)
        flash("User updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("user_form.html", form=form)


@app.route("/admin")
def admin():
    return render_template("admin_page.html")


@app.route("/passenger")
def passenger():
    return render_template("passenger_page.html")


@app.route("/driver")
def driver():
    return render_template("driver_page.html")


# @login_manager.user_loader
# def user_loader(email):
#     return models.User.get_by_email(email)


# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get("email")
#     connection = mysql.connector.connect(**db_config)
#     return models.User.get_by_email(email, connection)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return "Unauthorized", 401


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# # TODO: Add region selection
# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     if flask.request.method == "GET":
#         return """
#         <form action='signup' method='POST'>
#             <input type='text' name='fname' id='fname' placeholder='First Name'/>
#             <input type='text' name='lname' id='lname' placeholder='Last Name'/>
#             <input type='text' name='email' id='email' placeholder='email'/>
#             <input type='password' name='password' id='password' placeholder='password'/>
#             <input type='password' name='password' id='password' placeholder='confirm password'/>
#             <select name="user_type">
#                 <option value="passenger">Passenger</option>
#                 <option value="driver">Driver</option>
#                 <option value="admin">Admin</option>
#             </select>
#             <input type='submit' name='submit'/>
#         </form>
#         """

#     email = flask.request.form["email"]
#     password = flask.request.form["password"]
#     fname = flask.request.form["fname"]
#     lname = flask.request.form["lname"]
#     user_type = flask.request.form["user_type"]
#     models.User(-1, user_type, email, password, fname, lname).insert(connection=db)
#     return flask.redirect(flask.url_for("login"), code=307)


if __name__ == "__main__":
    app.run(debug=True)
