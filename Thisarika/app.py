from flask import Flask, session, render_template, request, redirect
import mysql.connector
import pyrebase

app = Flask(__name__)

conn = mysql.connector.connect(host='localhost', user='root', password='', database='ayucare')

config = {
    'apiKey': "AIzaSyC2XqHQdB9Y0tNppfWAdKYThlOwHGV17cg",
    'authDomain': "authendicatepy-c0f50.firebaseapp.com",
    'projectId': "authendicatepy-c0f50",
    'storageBucket': "authendicatepy-c0f50.appspot.com",
    'messagingSenderId': "533819126801",
    'appId': "1:533819126801:web:4ae847258b1e6c6f25adb0",
    'measurementId': "G-H6KQ91415L",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # firebase authendication code
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            email = request.form['email']
            password = request.form['password']
            new_user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(new_user['idToken'])
            return render_template('index.html')
        except:
            existing_account = 'This email is already used'
            return render_template('signup.html', exist_message=existing_account)
    return render_template("signup.html")


@app.route('/register', methods=['GET', 'POST'])
def register():         # database connection
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        gender = request.form.get('gender')
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        pastconditions = request.form['pastconditions']
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO patient(firstname,lastname,age,gender,email,address,password,confirmpassword,pastconditions) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (firstname, lastname, age, gender, email, address, password, confirmpassword, pastconditions))
        conn.commit()

        # Firebase Authentication code
        if password == confirmpassword:
            try:
                new_user1 = auth.create_user_with_email_and_password(email, password)
                auth.send_email_verification(new_user1['idToken'])
                return render_template('index.html')
            except:
                existing_account1 = 'This email is already used'
                return render_template('register.html', exist_message=existing_account1)
        else:
            password_mismatch = 'Passwords do not match'
            return render_template('register.html', password_error=password_mismatch)
    return render_template("register.html")


@app.route('/service')
def service():  # put application's code here
    return render_template("service.html")


if __name__ == '__main__':
    app.run()
