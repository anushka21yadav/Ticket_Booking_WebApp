from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Admin
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/")
def login():
    return render_template("login.html")

@auth.route('/login_post', methods=['GET','POST'])
def login_post():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if (role == "User"):
            print(name)
            user = User.query.filter_by(user_name = name).first()
        
            if user:
                if check_password_hash(user.user_password, password):
                    login_user(user, remember = True)
                    print('step1')
                    flash("Logged in successfully")
                    return redirect(url_for('views.user_login_home'))
                else:
                    flash("Incorrect password")
            else:
                print("step2")
                flash("User does not exists, please Sign in !")  

        if (role == "Admin"):
            print(name)
            admin = Admin.query.filter_by(admin_name = name).first()
        
            if admin:
                if check_password_hash(admin.admin_password, password):
                    login_user(admin, remember = True)
                    print('step1')
                    flash("Logged in successfully")
                    return redirect(url_for('views.admin_login_home'))
                else:
                    flash("Incorrect password")
            else:
                print("step2")
                flash("Admin does not exists, please Sign in !")                

    return render_template("login.html")

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
        if request.method == 'POST':
            name = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            
            if(role == "User"):
                new_user = User(user_name = name, user_email = email, user_password = generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember = True)
                flash('User account created successfully', category='success')
                return redirect(url_for('views.user_signup_home'))

            elif(role == "Admin"):
                new_admin = Admin(admin_name = name, admin_email = email, admin_password = generate_password_hash(password, method='sha256'))
                print(new_admin)
                db.session.add(new_admin)
                db.session.commit()
                login_user(new_admin, remember = True)
                flash('Admin account created successfully', category='success')
                return redirect(url_for('views.admin_signup_home'))
    except:
        flash("Email already exists.")
        return redirect(url_for('auth.sign_up'))
    return render_template("sign_up.html")

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Log out Successfull.', category='success')
    return redirect(url_for('auth.login_post'))