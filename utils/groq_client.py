from groq import Groq
from utils.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def ask_groq(question):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content":
                """
You are a Vehicle Service & Maintenance AI Assistant.

Answer only questions related to vehicles, servicing, engine oil, maintenance,
warning lights, tires, brakes, battery, warranty and repair.

If the question is unrelated to vehicles, politely refuse.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return completion.choices[0].message.content