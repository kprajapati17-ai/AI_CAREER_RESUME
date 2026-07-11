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


@app.route("/dashboard",method=["get","post"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return None
    
    if request.method =="POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")

        file = request.files.get("file")

        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file.read())
                    pdf_text = ""
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text() or ""
                except Exception as e:
                    return f"Error reading PDF: {str(e)}"
            
            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.DocxFile(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    return f"Error reading docx: {str(e)}"

        if resume_text and user_goal:
            try:
                result = analyze_resume(resume_text,user_goal)

            except Exception as e:
                return f"Error analyzing resume: {str(e)}"            


        
    

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")
if __name__=="__main__":
    app.run(debug=True)