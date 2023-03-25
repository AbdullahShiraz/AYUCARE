import pyrebase

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

