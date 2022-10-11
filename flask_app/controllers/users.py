from flask_app import app
from flask_app.models.user import User
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def login_page():

    return render_template('login_page.html')

@app.route('/registration_processing', methods=['POST'])
def register_processing():
    is_valid = User.validate_user(request.form)
    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match!")
        is_valid = False

    if is_valid == False:
        return redirect('/')
    data ={}
    data['first_name'] = request.form['first_name']
    data['last_name'] = request.form['last_name']
    data['email'] = request.form['email']
    data['birthday'] = request.form['birthday']
    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    User.save(data)
    return redirect('/')

@app.route('/login_processing', methods=['POST'])
def login_processing():
    data = {
        'email':request.form['email']
    }
    userdata = User.get_by_email(data)
    
    if not userdata:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(userdata.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = userdata.id
    
    return redirect('/user_page')

@app.route('/user_page')
def user_page():
    if 'user_id' in session:
        data = {'id':session['user_id']}
        user = User.get_one(data)
        print(user)
        return render_template('user_page.html', user=user[0])
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')