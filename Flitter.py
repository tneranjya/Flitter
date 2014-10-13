__author__ = 'thihara'
#Entry point to the Flitter application and the controller functions.


import os
from flask import Flask, redirect, render_template, request, session, flash
from UserService import UserService
from PostService import PostService

#initialize the necessary classes
app = Flask(__name__)
userService = UserService()
postService = PostService()

#loads the application configurations from the app_config.py file
app.config.from_pyfile('app_configs.py')

#Redirects root to /flitter namespace
@app.route('/')
def index():
    return redirect("/flitter")


#Handles all login related controller functionality and populates the user details for display.
@app.route('/flitter/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if userService.validate_credentials(request.form['username'], request.form['password']):
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect('/flitter/home')
        else:
            error = 'Invalid username or password'

    return redirect_to_login(error)


#Log the user out and redirect to the login area.
@app.route('/flitter/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)

    flash('You were logged out')
    return redirect('/flitter/login')


#Register the user and display any errors. If registration is successful display a message and redirect to the login page.
@app.route('/flitter/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        confirm_password = request.form['confirmpassword']

        error = userService.register_user(fullname, username, password, confirm_password)
        if error is None:
            flash('Registration successful, please login')

    return redirect_to_login(error)


#Creates new posts and redirect to the home page
@app.route('/flitter/post/put', methods=['GET', 'POST'])
def create_new_post():
    if request.method == 'POST':
        logged_in_user = session['username']
        post_content = request.form['post_content']

        postService.save_post(logged_in_user, post_content)

    return redirect('flitter/home')


#Loads and displays posts by the logged in user
@app.route('/flitter/home', methods=['GET', 'POST'])
def view_home():
    posts = postService.get_posts_by_user(session['username'])
    return render_template('view_posts.html', posts=posts, is_own_posts=True)


#Loads and displays posts created by the user specified in the URL
@app.route('/flitter/user/<username>')
def view_user_post(username):

    posts = postService.get_posts_by_user(username)
    return render_template('view_posts.html', posts=posts, is_own_posts=False)


#Redirect the flitter landing URL to the login page.
@app.route('/flitter')
def view_public_users():
    return redirect('flitter/login')


#Loads the users for displaying in the login page, and return the redirect details for the login page..
def redirect_to_login(error=None):
    users = userService.get_users()
    return render_template('login.html', error=error, users=users)

#Start the application if being invoked from the command line
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

