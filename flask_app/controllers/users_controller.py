from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ? --------------------------------------
# READ all users, display on frontend
@app.route('/') 
def index():
    return render_template("index.html")  
# ? --------------------------------------



# ? --------------------------------------
# CREATE, validate, hash, redirect to success page
@app.route('/register', methods=['POST']) 
def register():

    if not user_model.User.registration(request.form):
        return redirect("/")

    data = {
        "password": bcrypt.generate_password_hash(request.form['password']),
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
    }

    user_model.User.save(data)

    return redirect('/success') 
# ? --------------------------------------



# ? --------------------------------------
# READ user by email, redirect to success page
@app.route('/login', methods=['POST']) 
def login():
    data = { 
        "email" : request.form["email"] 
    }

    user = user_model.User.get_by_email(data)

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']): 
        flash("Invalid Credentials", "login")
        return redirect('/')

    # to determine if someone is logged in
    # * confirmed, this key in session[] can be anything. Literally tested session['anything'], worked fine
    session['user_id'] = user.id

    return redirect("/success") 
# ? --------------------------------------



# ? --------------------------------------
# redirect successful registration to success page
@app.route('/success') 
def to_success_page():

    # ! this does not consistently work, no clue why.
    if 'user_id' not in session:
        return redirect('/')

    # if not session['user_id']:
    #     return redirect('/')

    return render_template("success.html") 
# ? --------------------------------------



# ? --------------------------------------
# logout, redirect to homepage
@app.route('/logout') 
def logout():
    session.clear()
    return redirect("/")
# ? --------------------------------------



# ? --------------------------------------
# add new user form page
# @app.route('/add/user') 
# def add_user():
#     return render_template("create.html")  

# CREATE new user, POST data
# @app.route('/create/user', methods=['POST']) 
# def create_user():
#     user_model.User.save(request.form)

#     return redirect('/') 
# ? --------------------------------------



# ? --------------------------------------
# READ one user, show on frontend in filled-out form
# @app.route('/update/user/<int:id>') 
# def update_user(id):   
#     data = { 
#         "id": id # id key, matches the column in the database, the name of the hidden input in the form
#     }

#     return render_template("update.html", user = user_model.User.get_one(data))  

# UPDATE user, collect form data
# need hidden input on the form with the user id
# @app.route('/update/user', methods=['POST']) 
# def update_user_form():
#     user_model.User.update_one(request.form)

#     return redirect("/")  
# ? --------------------------------------



# ? --------------------------------------
# READ user, show on frontend
# @app.route('/view/user/<int:id>') 
# def view_user(id):
#     data = { 
#         "id": id # id, the column in the database
#     }

#     return render_template("view.html", user = user_model.User.get_one(data))  
# ? --------------------------------------



# ? --------------------------------------
# DELETE user
# @app.route('/delete/user/<int:id>') 
# def delete_user(id):

#     data ={ 
#         "id": id # id, the column in the database
#     }

#     user_model.User.remove_one(data)

#     return redirect("/")  
# ? --------------------------------------
