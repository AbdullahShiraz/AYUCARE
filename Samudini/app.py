# Importing necessary Libraries
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import pickle
import numpy as np
import warnings
from sklearn.exceptions import DataConversionWarning
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt


# Ignoring User warnings and Data Conversion Warning
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DataConversionWarning)

# Establishing Flask Connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'

#
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Defining the table columns
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    address = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    pastcondition = db.Column(db.String(80), nullable=False)

#Defining a class called RegisterForm, which inherits from FlaskForm
class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    lastname = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Last Name", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    gender = SelectField('Gender', choices=[('Male','Male'),('Female','Female')], render_kw={"class": "text-sm mx-1"})
    email = StringField(validators=[InputRequired(), Length(min=10, max=40)], render_kw={"placeholder": "Email", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    address = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Enter your City", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})
    pastcondition = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Past Conditions", "class": "h-20 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})
    submit = SubmitField('Register', render_kw={"class": "bg-black w-full h-10 cursor-pointer text-white rounded-md text-sm"})

    # This is a validation method to check if a given email address already exists in the database.
    from flask import flash

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            flash('That email already exists. Please choose a different one.', 'error')
            raise ValidationError('That email already exists. Please choose a different one.')


# Creating a login form for users to enter their email and password information, and submit it to the server for authentication..
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Email", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent shadow-sm"})

    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "h-8 w-full rounded-md border border-slate-300 text-sm pl-2 bg-transparent  shadow-sm"})

    submit = SubmitField('Login', render_kw={"class": "bg-black w-full h-10 cursor-pointer text-white rounded-md text-sm"})

#Loading Diease Dectection Pickle File
f = open("DecisionTree-Model.sav", "rb")
model_N = pickle.load(f)

#loading Medicine Recommendation Pickle file
f2 = open("drugTree.pkl", "rb")
model_med = pickle.load(f2)


#Mapping Symptoms as indexes in dataset using dictionary
symptom_mapping = {
    'acidity': 0,
    'indigestion': 1,
    'headache': 2,
    'blurred_and_distorted_vision': 3,
    'excessive_hunger': 4,
    'muscle_weakness': 5,
    'stiff_neck': 6,
    'swelling_joints': 7,
    'movement_stiffness': 8,
    'depression': 9,
    'irritability': 10,
    'visual_disturbances': 11,
    'painful_walking': 12,
    'abdominal_pain': 13,
    'nausea': 14,
    'vomiting': 15,
    'blood_in_mucus': 16,
    'Fatigue': 17,
    'Fever': 18,
    'Dehydration': 19,
    'loss_of_appetite': 20,
    'cramping': 21,
    'blood_in_stool': 22,
    'gnawing': 23,
    'upper_abdomain_pain': 24,
    'fullness_feeling': 25,
    'hiccups': 26,
    'abdominal_bloating': 27,
    'heartburn': 28,
    'belching': 29,
    'burning_ache': 30
}
# Creating a Medical form to intergrate Medicine Recommendation Model
class medForm(FlaskForm):
    gender = SelectField('Gender :', render_kw={"style": "width: 170px;"},choices=[('', ' Select your gender'),(1,' Male'),(0,' Female')],default= None,validators=[DataRequired()])
    age = StringField(validators=[InputRequired()],render_kw={"style": "width: 60px;","placeholder": "Age"})
    severity = SelectField('Severity :',  render_kw={"style": "width: 220px;"},choices=[('', 'Select the level of severity'),(0,'Few days'),(1,'A week'),(2,'Few weeks or more')],default= None,validators=[DataRequired()])
    disease = SelectField('Disease :',  render_kw={"style": "width: 150px;"}, choices=[('', ' Select the diease'),(0, 'Diarrhea'), (1, 'Gastritis'),(2, 'Arthritis'),(3, 'Migraine')],default= None,validators=[DataRequired()])

# Creating Symptoms dropdown Menu for selecting Symptoms
class serviceForm(FlaskForm):
    choices = [('', ' Select a Symptom'), ('acidity', 'Acidity'), ('indigestion', 'Indigestion'),
               ('headache', 'Headache'), ('blurred_and_distorted_vision', 'Blurred and distorted vision'),
               ('excessive_hunger', 'Excessive hunger'), ('muscle_weakness', 'Muscle weakness'),
               ('stiff_neck', 'Stiff neck'), ('swelling_joints', 'Swelling joints'),
               ('movement_stiffness', 'Movement stiffness'), ('depression', 'Depression'),
               ('irritability', 'Irritability'), ('visual_disturbances', 'Visual disturbances'),
               ('painful_walking', 'Painful walking'), ('abdominal_pain', 'Abdominal pain'),
               ('nausea', 'Nausea'), ('vomiting', 'Vomiting'), ('blood_in_mucus', 'Blood in mucus'),
               ('Fatigue', 'Fatigue'), ('Fever', 'Fever'), ('Dehydration', 'Dehydration'),
               ('loss_of_appetite', 'Loss of appetite'), ('cramping', 'Cramping'),
               ('blood_in_stool', 'Blood in stool'), ('gnawing', 'Gnawing'),
               ('upper_abdomain_pain', 'Upper abdomain pain'), ('fullness_feeling', 'Fullness feeling'),
               ('hiccups', 'Hiccups'), ('abdominal_bloating', 'Abdominal bloating'),
               ('heartburn', 'Heartburn'), ('belching', 'Belching'), ('burning_ache', 'Burning ache')]
    symptom1 = SelectField('1st Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom2 = SelectField('2nd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom3 = SelectField('3rd Symptom', choices=choices, default= None,validators=[DataRequired()])
    symptom4 = SelectField('4th Symptom', choices=choices, default= None,validators=[DataRequired()])

#Defining a fucntion to convert user inputs and predict
def serviceValidation(selected_symptoms):

    # Convert the selected symptoms to a 30-element list of 1s and 0s
    inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for symptom in selected_symptoms:
        if symptom:
            inputs[symptom_mapping[symptom]] = 1

    # convert list to NumPy array
    inputs = np.array(inputs)
    inputs = inputs.reshape(1, -1)


    # Pass the inputs to your machine learning model and retrieve the predicted result
    predicted_result = model_N.predict(inputs)
    print(predicted_result[0])

    # Return the predicted result to the user
    return predicted_result[0]


def medicineValidation(selectedOptions):
    """Defining a function to recommend medicine"""
    inputs = np.array(selectedOptions)  # convert list to NumPy array
    inputs = inputs.reshape(1, -1)
    # Pass the inputs to your machine learning model and retrieve the predicted result
    recommend_Med = model_med.predict(inputs)
    # Return the predicted result to the user
    return recommend_Med[0]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('service'))
        else:
            # login failed, display error message
            flash('Invalid email or password. Please try again.', 'error')
    return render_template('signin.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.password.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User( firstname=form.firstname.data, lastname=form.lastname.data, age=form.age.data, gender=form.gender.data,email=form.email.data, address=form.address.data, password=hashed_password, pastcondition=form.pastcondition.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))

    return render_template('register.html', form=form)

@app.route('/service', methods=['GET','POST'])
@login_required
def service():
    global predicted_result
    user = User.query.filter_by(id=current_user.id).first()


    form = serviceForm()
    if form.validate_on_submit():
        selectedSymptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data]
        predicted_result = serviceValidation(selectedSymptoms)

        return render_template('service.html', form=form, predicted_result=predicted_result, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)
    return render_template('service.html', form=form, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)


@app.route('/med_service', methods=['GET','POST'])
@login_required
def med_service():

    form = medForm()
    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():
        selectedOptions = [form.disease.data, form.age.data, form.gender.data, form.severity.data]
        recommend_Med = medicineValidation(selectedOptions)
        return render_template("med_service.html", form=form, predicted_result=recommend_Med.upper(), id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)

    return render_template("med_service.html", form=form, id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)


@app.route('/doc_service')
def doc_service():  # put application's code here
    user = User.query.filter_by(id=current_user.id).first()

    return render_template("doc_service.html",id=user.id, name=user.firstname.upper(), age=user.age, gender=user.gender)

@app.route('/faq')
def faq():  # put application's code here
    return render_template("faq.html")

if __name__ == '__main__':
    app.run(debug=True)
