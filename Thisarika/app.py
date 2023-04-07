from flask import Flask, session, render_template, request, redirect, flash
import sqlite3
import pyrebase


app = Flask(__name__)
app.secret_key = 'ayucare1'

conn = sqlite3.connect('ayucare.db')
conn.execute(
    "CREATE TABLE IF NOT EXISTS patients ( firstname TEXT NOT NULL, lastname TEXT NOT NULL, age INTEGER NOT NULL, gender VARCHAR NOT NULL, email VARCHAR UNIQUE NOT NULL, address VARCHAR NOT NULL, password VARCHAR NOT NULL, confirmpassword VARCHAR NOT NULL, pastconditions VARCHAR NOT NULL)")

conn.execute(
    "CREATE TABLE IF NOT EXISTS doctors ( doctor_id INTEGER PRIMARY KEY AUTOINCREMENT, doctor_name TEXT NOT NULL, specialized_field TEXT NOT NULL, contact_number VARCHAR NOT NULL)"
)

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
def signup():
    error_message = None  # Initialize error message as None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if both email and password are filled
        if email and password:
            # Check if the email and password are in the database
            with sqlite3.connect("ayucare.db") as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM patients WHERE email = ? AND password = ?", (email, password))
                row = c.fetchone()
                if row is not None:
                    # User is registered, redirect to service.html
                    session['email'] = email  # Store email in session for future use
                    return redirect('/service')
                else:
                    # User is not registered, set error message
                    error_message = 'Invalid email or password. Please check your credentials.'
        else:
            # Empty fields, set error message
            error_message = 'Please fill in all the fields before signing up.'

    return render_template("signup.html", error_message=error_message)



@app.route('/register', methods=['GET', 'POST'])
def register():
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

        # Check if all required fields are filled
        if not firstname or not lastname or not age or not gender or not email or not address or not password or not confirmpassword or not pastconditions:
            return "Please fill all the required fields"

        # Check if passwords match
        if password != confirmpassword:
            return "check your passwords again"

        with sqlite3.connect("ayucare.db") as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO patients(firstname,lastname,age,gender,email,address,password,confirmpassword,pastconditions) values (?,?,?,?,?,?,?,?,?)',
                (firstname, lastname, age, gender, email, address, password, confirmpassword, pastconditions))
            conn.commit()

        try:
            new_user1 = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(new_user1['idToken'])
            return render_template('index.html')
        except:
            existing_account1 = 'This email is already used'
            return render_template('index.html', exist_message=existing_account1)

    return render_template("register.html")

@app.route('/service')
def service():
    # Check if user is logged in by checking if email is stored in session
    if 'email' in session:
        return render_template("service.html")
    else:
        # User is not logged in, redirect to signup page
        flash('Please sign up to access the service.')
        return redirect('/signup')


if __name__ == '__main__':
    app.run()
