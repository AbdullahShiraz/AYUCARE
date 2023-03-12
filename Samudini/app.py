from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/signup')
def signup():  # put application's code here
    return render_template("signup.html")

@app.route('/register')
def register():  # put application's code here
    return render_template("register.html")

@app.route('/service')
def service():  # put application's code here
    return render_template("service.html")

@app.route('/med_service')
def med_service():  # put application's code here
    return render_template("med_service.html")

@app.route('/doc_service')
def doc_service():  # put application's code here
    return render_template("doc_service.html")

if __name__ == '__main__':
    app.run()
