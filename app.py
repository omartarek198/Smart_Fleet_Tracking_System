import flask
import mysql.connector
from flask import Flask, request, redirect, render_template
import flask_login
import models

app = Flask(__name__)
app.secret_key = "kodqwpjdqwodOIWJDnqDIOJ209E019"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Configure MySQL connection
db = mysql.connector.Connect(
    host="localhost",
    user="me",
    # user='root',
    password="",
    database="system",
)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["email"]
        password = request.form["password"]

        # with db.cursor() as cursor:
        #     query = "SELECT user_type FROM user WHERE email=%s AND passwd=%s"
        #     cursor.execute(query, (username, password))
        #     user = cursor.fetchone()
        user = models.User(0, 'admin', 'someone@something.com', 'adbasj', 'Admin', 'Admin')

        if user:
            user_type = user["user_type"]
            if user_type == "admin":
                return redirect("/admin")
            elif user_type == "passenger":
                return redirect("/passenger")
            elif user_type == "driver":
                return redirect("/driver")

    return redirect(flask.url_for("signup"))


@app.route("/admin")
def admin():
    return render_template("admin_page.html")


@app.route("/passenger")
def passenger():
    return render_template("passenger_page.html")


@app.route("/driver")
def driver():
    return render_template("driver_page.html")


@login_manager.user_loader
def user_loader(email):
    return models.User.get_by_email(email)


@login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    return models.User.get_by_email(email)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized", 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# TODO: Add region selection
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "GET":
        return """
        <form action='signup' method='POST'>
            <input type='text' name='fname' id='fname' placeholder='First Name'/>
            <input type='text' name='lname' id='lname' placeholder='Last Name'/>
            <input type='text' name='email' id='email' placeholder='email'/>
            <input type='password' name='password' id='password' placeholder='password'/>
            <input type='password' name='password' id='password' placeholder='confirm password'/> 
            <select name="user_type">
                <option value="passenger">Passenger</option>
                <option value="driver">Driver</option>
                <option value="admin">Admin</option>
            </select>
            <input type='submit' name='submit'/>
        </form>
        """

    email = flask.request.form["email"]
    password = flask.request.form["password"]
    fname = flask.request.form["fname"]
    lname = flask.request.form["lname"]
    user_type = flask.request.form["user_type"]
    models.User(-1, user_type, email, password, fname, lname).insert(connection=db)
    return flask.redirect(flask.url_for("login"), code=307)


if __name__ == "__main__":
    app.run(debug=True)
