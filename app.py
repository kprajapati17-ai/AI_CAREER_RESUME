from flask import Flask,render_template,request,redirect,session
from db import Base,engine,sessionmaker
import models
import PyPDF2
import docx
import json


app = Flask(__name__)
app.secret_key = "secret123"

Base.metadata.create_all(bind=engine)



@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# signup route
@app.route("/signup",methods=["GET","POST"])
def signup():
    db = SessionLocal()
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        Existing_user = db.query(models.User).filter_by(email=email).first()
        if Existing_user:
            return "User Alredy exists"
        
        user = models.User(email=email,password=password)
        db.add(user)
        db.commit()
        
        return redirect("/login")
    return render_template("signup.html")

#login
@app.route("/login",methods=["GET","POST"])
def login():
    db = SessionLocal()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.query(models.User).filter_by(email=email,password=password).first()

        if user:
            session["user"] = user.email
            return redirect("/dashboard")
        else:
            return "Invalid password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)