from google import genai
from src.config.settings import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

for m in client.models.list():
    print(m.name)

def call_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
