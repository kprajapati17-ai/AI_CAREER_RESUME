import io
import os
import datetime
from flask import Flask, render_template, request, redirect, session, send_file
import PyPDF2
import docx
from config import Config
from services.ai_service import analyze_resume
from services.pdf_service import generate_resume_report_pdf

# Initialize Flask App.
# Templates and static files are located in the project root directory.
app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = Config.SECRET_KEY


@app.route("/")
def home():
    """Redirect root path to the dashboard."""
    return redirect("/dashboard")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Main page for resume uploading and on-the-fly Gemini AI analysis."""
    result = None
    has_report = False
    
    if request.method == "POST":
        user_goal = request.form.get("role")
        # Support both 'resyme' (from HTML form) and 'resume' field name
        resume_text = request.form.get("resume") or request.form.get("resyme") or ""

        file = request.files.get("file")

        # In Flask, checking if file.filename is non-empty tells if a file was selected.
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                try:
                    # PyPDF2 requires a file-like stream; wrap file bytes in BytesIO
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    pdf_text = ""
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text() or ""
                    resume_text = pdf_text
                except Exception as e:
                    return f"Error reading PDF: {str(e)}"
            
            elif file.filename.endswith(".docx"):
                try:
                    # python-docx reads docx files from a stream via docx.Document
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    return f"Error reading docx: {str(e)}"

        # If we have both target role and resume contents, trigger analysis
        if resume_text and user_goal:
            try:
                # Call the reusable Google Gemini AI Service
                result = analyze_resume(resume_text, user_goal)
                
                # Store the analysis details in Flask session for PDF generation
                session["last_analysis"] = {
                    "role": user_goal,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "analysis": result
                }
                has_report = True
            except Exception as e:
                return f"Error analyzing resume: {str(e)}"
                
    return render_template("dashbord.html", result=result, has_report=has_report)


@app.route("/download_pdf")
def download_pdf():
    """Generates and downloads the report as a PDF from the session data."""
    report = session.get("last_analysis")
    if not report:
        return "No analysis report found in your session. Please analyze a resume first.", 400
        
    try:
        # Generate the PDF bytes in memory
        pdf_bytes = generate_resume_report_pdf(report)
        
        # Serve the file directly using io.BytesIO without writing anything to disk
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="CareerMind_Report.pdf"
        )
    except Exception as e:
        return f"Error generating PDF report: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)