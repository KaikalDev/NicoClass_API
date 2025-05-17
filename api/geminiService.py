import time
from google import generativeai as genai

GOOGLE_GEMINI_API_KEY = "AIzaSyC8ljufSCPDZ7JkaVWpyTsg1QckafEO5YI"
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

def enviar_prompt(prompt):
    try:
        response = model.generate_content(prompt)

        time.sleep(5)

        return {"resposta": response.text}

    except Exception as e:
        return e
