from flask import Flask, render_template, request, redirect, url_for, session as login_session
import pyrebase 
from googletrans import Translator

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "PASSWORD"

firebaseConfig = {
  "apiKey": "AIzaSyDm8MA87XdVcLU_a8OKC_02KnRwoOmcbJ4",
  "authDomain": "projectssssssssss.firebaseapp.com",
  "projectId": "projectssssssssss",
  "storageBucket": "projectssssssssss.appspot.com",
  "messagingSenderId": "50108558309",
  "appId": "1:50108558309:web:1dba5a57c240770f4b9d0c",
  "measurementId": "G-BG83JHK6HT",
  "databaseURL" : "https://projectssssssssss-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
      return render_template("signup.html")

    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    login_session['email'] = email
    login_session['password'] = password
    login_session['username'] = username
    try:
      login_session['user'] = auth.create_user_with_email_and_password(email, password)
      user_id = login_session['user']['localId']

      user = {
      'email': email,
      'username': username} 

      essays = {
      'essay_text': essay_text,
      'the_writer': the_writer,
      'uid' : uid,
      'reported_user': reported_user
    }
      login_session['essays'] = [] 
      return redirect(url_for('home'))
    except:
      print("w")
      return render_template("home.html")
      
@app.route("/signin", methods =["GET", "POST"])
def signin():
  if request.method == 'GET' :
    return render_template("signin")
  else :
    email = request.form['email']
    password = request.form['password']
    try:
      user = auth.sign_in_with_email_and_password(email, password)
      login_session['user'] = user
      return redirect(url_for('home'))
    except:
      return render_template("signin.html")
@app.route("/home", methods = ["GET", "POST"])
def home():
  if login_session.get('user'):
    if request.method == "GET":
        translator = Translator(service_urls=['http://127.0.0.1:5000/home' ])
        essays = db.child("essays").get().val() or {}
        return render_template("home.html", essay_data=essays)
    else:
          essay_text  = request.form['essay_text']
          return render_template("home.html")    

@app.route("/signout", methods = ["GET", "POST"])
def signout():
  login_session['user']=  None
  auth.current_user = None
  print("signed out user")
  return redirect(url_for('signout'))

@app.route("/essays", methods=["GET", "POST"])
def essays():
  if request.method == "POST":
    essay_text = request.form['essay_text']
    user_id = login_session['user']['localId']
    essay_data = {'essay_text': essay_text,'user_id': user_id}
    db.child("essays").push(essay_data)
    essays = db.child("essays").get().val()
    return render_template("essays.html", essays=essays)
  else:
    return render_template("essays.html")

        # return render_template("essays.html", essays=essays)
@app.route("/ai", methods=["GET", "POST"])
def ai():
   return render_template("ai.html")
@app.route("/report", methods=["GET", "POST"])
def report():
    return render_template("report.html")
if __name__ == '__main__':
  app.run(debug=True)