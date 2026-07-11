from fpdf import FPDF
from typing import Dict, Any

class CareerReportPDF(FPDF):
    def header(self) -> None:
        # Title of the PDF
        self.set_font("helvetica", "B", 16)
        self.set_text_color(30, 41, 59)  # Dark slate gray
        self.cell(0, 10, "CareerMind-AI - Analysis Report", ln=1, align="C")
        
        # Subtitle decorative line
        self.set_draw_color(30, 41, 59)
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(8)

    def footer(self) -> None:
        # Position footer at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 116, 139)  # Slate gray
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def clean_text(text: Any) -> str:
    """
    Cleans text or lists of strings to ensure they are compatible with PDF Latin-1 encoding,
    preventing UnicodeEncodeErrors in standard Helvetica fonts.
    """
    if text is None:
        return ""
    
    if isinstance(text, list):
        text = "\n".join([f"- {item}" for item in text])
        
    # Map common non-Latin-1 unicode characters to standard ASCII/Latin-1 equivalents
    replacements = {
        "\u2013": "-",   # En dash
        "\u2014": "-",   # Em dash
        "\u2018": "'",   # Left single quote
        "\u2019": "'",   # Right single quote
        "\u201c": '"',   # Left double quote
        "\u201d": '"',   # Right double quote
        "\u2022": "*",   # Bullet point
        "\u2026": "...", # Ellipsis
        "\u2713": "[x]", # Checkmark
        "\u00a0": " ",   # Non-breaking space
    }
    
    text_str = str(text)
    for uni_char, ascii_char in replacements.items():
        text_str = text_str.replace(uni_char, ascii_char)
        
    # Strictly encode to latin-1 and ignore any remaining unmappable characters
    return text_str.encode("latin-1", errors="ignore").decode("latin-1")

def generate_resume_report_pdf(report_data: Dict[str, Any]) -> bytes:
    """
    Generates a beautifully formatted PDF report in-memory.
    
    Args:
        report_data (dict): The report dictionary containing role, timestamp, and analysis.
        
    Returns:
        bytes: The generated PDF file bytes.
    """
    role = report_data.get("role", "Target Role")
    timestamp = report_data.get("timestamp", "")
    analysis = report_data.get("analysis", {})
    
    # Initialize PDF object
    pdf = CareerReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Job Role & Timestamp
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(59, 130, 246)  # Accent Blue
    pdf.cell(0, 8, f"Target Job Role: {clean_text(role)}", ln=1)
    
    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(100, 116, 139)  # Gray
    pdf.cell(0, 6, f"Analyzed on: {clean_text(timestamp)}", ln=1)
    pdf.ln(5)
    
    # Helper to append sections
    def add_section(title: str, content: Any) -> None:
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(30, 41, 59)  # Dark slate gray
        pdf.cell(0, 8, title, ln=1)
        
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(51, 65, 85)  # Charcoal
        cleaned_content = clean_text(content)
        pdf.multi_cell(0, 6, cleaned_content)
        pdf.ln(4)
        
    # Render details from the schema
    add_section("Current Skills", analysis.get("current_skills", []))
    add_section("Missing Skills", analysis.get("missing_skills", []))
    add_section("Skill Gap Analysis", analysis.get("gap_analysis", ""))
    add_section("Learning Roadmap", analysis.get("roadmap", []))
    add_section("Resume Improvement Suggestions", analysis.get("suggestions", []))
    
    # Output directly to bytes (in-memory PDF data)
    pdf_bytes = pdf.output()
    return bytes(pdf_bytes)
