# app.py

import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, flash
from forms import UserForm
from models import User 
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

db_config = {
    "host":"localhost",
    "user":"root",
    "password":"",
    "database":"system"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        connection = mysql.connector.connect(**db_config)
        user = User(
            id=None,
            user_type=form.user_type.data,
            email=form.email.data,
            passwd=form.passwd.data,
            fname=form.fname.data,
            lname=form.lname.data
        )
        user.insert(connection)
        flash('User created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('user_form.html', form=form)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserForm()
    connection = mysql.connector.connect(**db_config)

    if request.method == 'GET':
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
            lname=form.lname.data
        )
        user.update(connection)
        flash('User updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('user_form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
