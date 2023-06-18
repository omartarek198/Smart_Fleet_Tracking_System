import mysql.connector
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.Connect(
    host='localhost',
    user='root',
    password='',
    database='system'
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with db.cursor() as cursor:
            query = "SELECT user_type FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

        if user:
            user_type = user['user_type']
            if user_type == 'admin':
                return redirect('/admin')
            elif user_type == 'passenger':
                return redirect('/passenger')
            elif user_type == 'driver':
                return redirect('/driver')

    return render_template('login_page.html')

@app.route('/admin')
def admin():
    return render_template('admin_page.html')

@app.route('/passenger')
def passenger():
    return render_template('passenger_page.html')

@app.route('/driver')
def driver():
    return render_template('driver_page.html')

if __name__ == '__main__':
    app.run(debug=True)
