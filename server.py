# the "re" module will let us perform some regular expression operations
import re
# import Flask
from flask import Flask, render_template, redirect, request, session, flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL


# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"



# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('login_registration')


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/register", methods=['POST'])
def submit():
    # adding validation rules:        

    if len(request.form['firstname']) < 1:
        flash("Name cannot be blank!", 'name')

    elif len(request.form['lastname']) <= 2:
        flash("Name must be 2 or more characters", 'name')

    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')

    elif not EMAIL_REGEX.match(request.form['email']):    
        flash("Invalid Email Address!", 'email')

    elif len(request.form['password']) < 7 and len(request.form['password']) > 25:
        flash("Password must be at least 7 and less than 25 characters", 'password')
            
    if '_flashes' in session.keys():
        print(session['_flashes'])
        return redirect("/")

    else:
        mysql = connectToMySQL("login_registration")
        query = "INSERT INTO customers (firstname, lastname, email, password, created_at, updated_at) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s, NOW(), NOW());"
        data = {
            'firstname': request.form['firstname'],
            'lastname':  request.form['lastname'],
            'email': request.form['email'],
            'password': request.form['password']
            }
        mysql.query_db(query, data)
        return render_template("/success.html")


@app.route("/login", methods=['POST'])
def login():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')

    elif not EMAIL_REGEX.match(request.form['email']):    
        flash("Invalid Email Address!", 'email')

    elif len(request.form['password']) < 7 and len(request.form['password']) > 25:
        flash("Password must be at least 7 and less than 25 characters", 'password')
    else:
        return render_template("/success.html")    


# now, we may invoke the query_db method
print("all the customers", mysql.query_db("SELECT * FROM customers"))


if __name__=="__main__":
    app.run(debug=True)