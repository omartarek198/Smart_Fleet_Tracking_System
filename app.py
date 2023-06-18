import flask
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'kodqwpjdqwodOIWJDnqDIOJ209E019'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
            <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
            </form>
        '''

    email = flask.request.form['email']
    print(f'{users=}')
    print(f'{email=}')
    print(f'{flask.request.form["password"]=}')

    if email in users and flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    if isinstance(user,):
        pass
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if flask.request.method == 'GET':
        return """
        <form action='signup' method='POST'>
            <input type='text' name='email' id='email' placeholder='email'/>
            <input type='password' name='password' id='password' placeholder='password'/>
            <input type='password' name='password' id='password' placeholder='password'/> 
            <input type='submit' name='submit'/>
        </form>
        """
    

    email = flask.request.form['email']
    password = flask.request.form['password']
    users[email] = {'password': password}

    print(f'{users=}')
    return flask.redirect(flask.url_for('login'))

@app.route('/')
def index():
    return flask.redirect(flask.url_for('signup'))