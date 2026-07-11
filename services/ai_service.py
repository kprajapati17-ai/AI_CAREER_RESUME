import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import Config

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Pydantic schema for structured output to guarantee exact key matches for our HTML templates
class ResumeAnalysis(BaseModel):
    current_skills: List[str] = Field(description="List of key skills found in the resume relevant to the target role.")
    missing_skills: List[str] = Field(description="List of missing skills required to succeed in the target role.")
    gap_analysis: str = Field(description="A brief analysis of the gap between current skills and target role requirements.")
    roadmap: List[str] = Field(description="A step-by-step, actionable learning roadmap to acquire missing skills.")
    suggestions: List[str] = Field(description="Concrete suggestions to improve the candidate's resume for the target role.")

def analyze_resume(resume_text: str, user_goal: str) -> Dict[str, Any]:
    """
    Analyzes a candidate's resume against their target career goal using Google Gemini.
    
    Args:
        resume_text (str): The extracted text from the user's resume.
        user_goal (str): The desired career role (e.g., Backend Engineer).
        
    Returns:
        Dict[str, Any]: A dictionary containing current_skills, missing_skills, gap_analysis, roadmap, and suggestions.
    """
    # 1. Retrieve the Gemini API key
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == "YOUR_GEMINI_FREE_API_KEY":
        raise ValueError(
            "Gemini API key is not configured. Please add your key to the GEMINI_API_KEY field in the .env file."
        )

    try:
        # 2. Initialize the Google GenAI Client
        client = genai.Client(api_key=api_key)
        
        # 3. Create the prompt for the analysis
        prompt = (
            f"Analyze the following resume in the context of the user's target career goal:\n\n"
            f"--- TARGET CAREER GOAL ---\n"
            f"{user_goal}\n\n"
            f"--- RESUME CONTENT ---\n"
            f"{resume_text}\n\n"
            f"Please identify the current skills, list the missing skills, write a gap analysis, "
            f"outline a learning roadmap, and list concrete suggestions for improving the resume."
        )

        # 4. Generate structured content
        # We use the free-tier model gemini-3.5-flash
        logger.info(f"Sending request to Gemini API for target role: {user_goal}")
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert career counselor, resume reviewer, and technical recruiter.",
                response_mime_type="application/json",
                response_schema=ResumeAnalysis,
                temperature=0.2,
            ),
        )

        # 5. Parse and return the JSON response
        if not response.text:
            raise ValueError("Empty response received from Gemini API.")
            
        result = json.loads(response.text)
        logger.info("Successfully analyzed resume and parsed Gemini response.")
        return result

    except APIError as api_err:
        logger.error(f"Gemini API Error: {api_err}")
        raise RuntimeError(f"Gemini API call failed: {api_err.message}") from api_err
    except json.JSONDecodeError as json_err:
        logger.error(f"Failed to parse JSON response from Gemini API: {json_err}")
        raise RuntimeError("Failed to parse the analysis result from the AI service.") from json_err
    except Exception as e:
        logger.error(f"Unexpected error in analyze_resume: {e}")
        raise
