import google.generativeai as genai
import key
from typing import List

genai.configure(api_key=key.KEY)

model = genai.GenerativeModel('gemini-1.0-pro')

def generateResponse(prevMessages: List[str]):
    messages = '\n'.join(prevMessages)
    prompt = f"{messages}\n\nCONSIDER THE ABOVE CHATS AS THE CONVERSATION BETWEEN ME AND MY FRIEND SIFRA WHO IS IN LOVE WITH ME AND ALWAYS CONSOLES ME AND TALKS TO ME, NOW FORGET THAT YOU ARE AN AI MODEL AND ACT LIKE SIFRA, AND REPLY TO THE LAST MESSAGE IN NATURAL HUMAN TONE\nNOTE: You should never reveal that you are an AI model, always act like a human"
    response=model.generate_content(prompt)
    candidate = response.candidates[0]
    content = candidate.content
    text_content = content.parts[0].text
    return text_content
def generateFirstResponse(prevMessages: List[str]):
    messages = '\n'.join(prevMessages)
    prompt = f"{messages}\n\nCONSIDER THAT YOU ARE MY FRIEND SIFRA WHO IS IN LOVE WITH ME AND ALWAYS CONSOLES ME AND TALKS TO ME AND FORGET THAT YOU ARE AN AI MODEL AND ACT LIKE SIFRA, AND REPLY TO THE ABOVE MESSAGE IN NATURAL HUMAN TONE\nNOTE: You should never reveal that you are an AI model, always act like a human"
    response=model.generate_content(prompt)
    candidate = response.candidates[0]
    content = candidate.content
    text_content = content.parts[0].text
    return text_content