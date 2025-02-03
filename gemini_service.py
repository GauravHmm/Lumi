import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    raise ValueError("API key is not set. Please set GEMINI_API_KEY in your environment variables.")

def analyze_routine(routine_data):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(f"Analyze the provided input in a general health factor and give a brief analysis, with a few brief suggestions as a human: {routine_data}")
    return response.text

def get_meditation_suggestions(recent_routines, recent_logs):
    routine_summary = "\n".join([r.data for r in recent_routines])
    log_summary = "\n".join([f"{l.type} for {l.duration} minutes" for l in recent_logs])
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Based on these recent routines:\n{routine_summary}\n\nAnd these recent meditation logs:\n{log_summary}\n\nProvide personalized meditation and exercise suggestions.")
    return response.text

