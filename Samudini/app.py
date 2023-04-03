from flask import Flask, render_template, request
import pickle
import numpy as np
from sqlalchemy import false
import joblib
import warnings
from sklearn.exceptions import DataConversionWarning
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import InputRequired, ValidationError

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DataConversionWarning)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
f = open("DecisionTree-Model.sav", "rb")
model_N = pickle.load(f)

f2 = open("drugTree.pkl", "rb")
model_med = pickle.load(f2)

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

class medForm(FlaskForm):
    gender = SelectField('gender', choices=[(1,'male'),(0,'female')])
    age = StringField(validators=[InputRequired()],render_kw={"placeholder": "age"})
    severity = SelectField('severity', choices=[(0,'few days'),(1,'a week'),(2,'few weeks or more')])
    disease = SelectField('disease', choices=[(0, 'diarrhea'), (1, 'gastritis'),
                                                (2, 'osteoarthritis'),
                                                (3, 'rheumatoid arthritis'),
                                                (4, 'migraine')])


class serviceForm(FlaskForm):
    symptom1 = SelectField('symptom1', choices=[('acidity','acidity'), ('indigestion','indigestion'),
                                                ('headache','headache'),
                                                 ('blurred_and_distorted_vision','blurred_and_distorted_vision'),
                                                 ('excessive_hunger','excessive_hunger'),
                                                 ('muscle_weakness','muscle_weakness'),
                                                 ('stiff_neck','stiff_neck'),
                                                 ('swelling_joints','swelling_joints'),
                                                 ('movement_stiffness','movement_stiffness'),
                                                 ('depression','depression'),
                                                 ('irritability','irritability'),
                                                 ('visual_disturbances','visual_disturbances'),
                                                 ('painful_walking','painful_walking'),
                                                 ('abdominal_pain','abdominal_pain'),
                                                 ('nausea','nausea'),
                                                 ('vomiting','vomiting'),
                                                 ('blood_in_mucus','blood_in_mucus'),
                                                 ('Fatigue','Fatigue'),
                                                 ('Fever','Fever'),
                                                 ('Dehydration','Dehydration'),
                                                 ('loss_of_appetite','loss_of_appetite'),
                                                 ('cramping','cramping'),
                                                 ('blood_in_stool','blood_in_stool'),
                                                 ('gnawing','gnawing'),
                                                 ('upper_abdomain_pain','upper_abdomain_pain'),
                                                 ('fullness_feeling','fullness_feeling'),
                                                 ('hiccups','hiccups'),
                                                 ('abdominal_bloating','abdominal_bloating'),
                                                 ('heartburn','heartburn'),
                                                 ('belching','belching'),
                                                 ('burning_ache','burning_ache')])
    symptom2 = SelectField('symptom2', choices=[('acidity', 'acidity'), ('indigestion', 'indigestion'),
                                                ('headache', 'headache'),
                                                ('blurred_and_distorted_vision', 'blurred_and_distorted_vision'),
                                                ('excessive_hunger', 'excessive_hunger'),
                                                ('muscle_weakness', 'muscle_weakness'),
                                                ('stiff_neck', 'stiff_neck'),
                                                ('swelling_joints', 'swelling_joints'),
                                                ('movement_stiffness', 'movement_stiffness'),
                                                ('depression', 'depression'),
                                                ('irritability', 'irritability'),
                                                ('visual_disturbances', 'visual_disturbances'),
                                                ('painful_walking', 'painful_walking'),
                                                ('abdominal_pain', 'abdominal_pain'),
                                                ('nausea', 'nausea'),
                                                ('vomiting', 'vomiting'),
                                                ('blood_in_mucus', 'blood_in_mucus'),
                                                ('Fatigue', 'Fatigue'),
                                                ('Fever', 'Fever'),
                                                ('Dehydration', 'Dehydration'),
                                                ('loss_of_appetite', 'loss_of_appetite'),
                                                ('cramping', 'cramping'),
                                                ('blood_in_stool', 'blood_in_stool'),
                                                ('gnawing', 'gnawing'),
                                                ('upper_abdomain_pain', 'upper_abdomain_pain'),
                                                ('fullness_feeling', 'fullness_feeling'),
                                                ('hiccups', 'hiccups'),
                                                ('abdominal_bloating', 'abdominal_bloating'),
                                                ('heartburn', 'heartburn'),
                                                ('belching', 'belching'),
                                                ('burning_ache', 'burning_ache')])
    symptom3 = SelectField('symptom3', choices=[('acidity', 'acidity'), ('indigestion', 'indigestion'),
                                                ('headache', 'headache'),
                                                ('blurred_and_distorted_vision', 'blurred_and_distorted_vision'),
                                                ('excessive_hunger', 'excessive_hunger'),
                                                ('muscle_weakness', 'muscle_weakness'),
                                                ('stiff_neck', 'stiff_neck'),
                                                ('swelling_joints', 'swelling_joints'),
                                                ('movement_stiffness', 'movement_stiffness'),
                                                ('depression', 'depression'),
                                                ('irritability', 'irritability'),
                                                ('visual_disturbances', 'visual_disturbances'),
                                                ('painful_walking', 'painful_walking'),
                                                ('abdominal_pain', 'abdominal_pain'),
                                                ('nausea', 'nausea'),
                                                ('vomiting', 'vomiting'),
                                                ('blood_in_mucus', 'blood_in_mucus'),
                                                ('Fatigue', 'Fatigue'),
                                                ('Fever', 'Fever'),
                                                ('Dehydration', 'Dehydration'),
                                                ('loss_of_appetite', 'loss_of_appetite'),
                                                ('cramping', 'cramping'),
                                                ('blood_in_stool', 'blood_in_stool'),
                                                ('gnawing', 'gnawing'),
                                                ('upper_abdomain_pain', 'upper_abdomain_pain'),
                                                ('fullness_feeling', 'fullness_feeling'),
                                                ('hiccups', 'hiccups'),
                                                ('abdominal_bloating', 'abdominal_bloating'),
                                                ('heartburn', 'heartburn'),
                                                ('belching', 'belching'),
                                                ('burning_ache', 'burning_ache')])
    symptom4 = SelectField('symptom4', choices=[('acidity', 'acidity'), ('indigestion', 'indigestion'),
                                                ('headache', 'headache'),
                                                ('blurred_and_distorted_vision', 'blurred_and_distorted_vision'),
                                                ('excessive_hunger', 'excessive_hunger'),
                                                ('muscle_weakness', 'muscle_weakness'),
                                                ('stiff_neck', 'stiff_neck'),
                                                ('swelling_joints', 'swelling_joints'),
                                                ('movement_stiffness', 'movement_stiffness'),
                                                ('depression', 'depression'),
                                                ('irritability', 'irritability'),
                                                ('visual_disturbances', 'visual_disturbances'),
                                                ('painful_walking', 'painful_walking'),
                                                ('abdominal_pain', 'abdominal_pain'),
                                                ('nausea', 'nausea'),
                                                ('vomiting', 'vomiting'),
                                                ('blood_in_mucus', 'blood_in_mucus'),
                                                ('Fatigue', 'Fatigue'),
                                                ('Fever', 'Fever'),
                                                ('Dehydration', 'Dehydration'),
                                                ('loss_of_appetite', 'loss_of_appetite'),
                                                ('cramping', 'cramping'),
                                                ('blood_in_stool', 'blood_in_stool'),
                                                ('gnawing', 'gnawing'),
                                                ('upper_abdomain_pain', 'upper_abdomain_pain'),
                                                ('fullness_feeling', 'fullness_feeling'),
                                                ('hiccups', 'hiccups'),
                                                ('abdominal_bloating', 'abdominal_bloating'),
                                                ('heartburn', 'heartburn'),
                                                ('belching', 'belching'),
                                                ('burning_ache', 'burning_ache')])
    #submit = SubmitField('Submit', render_kw={"class":"modal-open bg-black  text-white  font-bold py-2 px-4 rounded-full"})


def serviceValidation(selected_symptoms):
    # # put application's code here

    # Extract the selected symptoms from the form data

    #print(selected_symptoms)
    # Convert the selected symptoms to a 30-element list of 1s and 0s
    inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for symptom in selected_symptoms:
        if symptom:
            inputs[symptom_mapping[symptom]] = 1

    inputs = np.array(inputs)  # convert list to NumPy array
    inputs = inputs.reshape(1, -1)
    #print(inputs)

    # Pass the inputs to your machine learning model and retrieve the predicted result
    predicted_result = model_N.predict(inputs)
    print(predicted_result[0])
    return predicted_result[0]
    # Return the predicted result to the user

def medicineValidation(selected_symptoms):
    # # put application's code here

    #pre-processing required
    inputs = np.array(selected_symptoms)  # convert list to NumPy array
    inputs = inputs.reshape(1, -1)
    # Pass the inputs to your machine learning model and retrieve the predicted result
    predicted_result = model_med.predict(inputs)
    print(predicted_result)
    return predicted_result[0]
    # Return the predicted result to the user

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/signup')
def signup():  # put application's code here
    return render_template("signup.html")

predicted_result = ""
@app.route('/register')
def register():  # put application's code here
    return render_template("register.html")



@app.route('/service', methods=['GET','POST'])
def service():
    global predicted_result
    form = serviceForm()
    if form.validate_on_submit():
        selectedSymptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data]
        predicted_result = serviceValidation(selectedSymptoms)

        return render_template('service.html', form=form, predicted_result=predicted_result)
    return render_template('service.html', form=form)


@app.route('/med_service', methods=['GET','POST'])
def med_service():  # put application's code here
    global predicted_result
    form = medForm()
    # if predicted_result == "diarrhea":
    #     predicted_result = 0
    # elif predicted_result == "gastritis":
    #     predicted_result = 1
    # elif predicted_result == "osteoarthritis":
    #     predicted_result = 2
    # elif predicted_result == "rheumatoid arthritis":
    #     predicted_result = 3
    # else:
    #     predicted_result = 4

    if form.validate_on_submit():
        selectedSymptoms = [form.gender.data, form.age.data, form.severity.data, form.disease.data]
        predicted_result = medicineValidation(selectedSymptoms)
        return render_template('med_service.html', form=form, predicted_result=predicted_result)

    return render_template("med_service.html", form = form)


@app.route('/doc_service')
def doc_service():  # put application's code here
    return render_template("doc_service.html")


if __name__ == '__main__':
    app.run(debug=True)
