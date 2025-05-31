from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Get DeepSeek API key from environment
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Route for checking server status in browser
@app.route('/')
def index():
    return "✅ Flask bot server running! Visit /webhook for Twilio integration."

# Intent detection based on keywords
def detect_intent(message):
    message = message.lower()
    if any(greet in message for greet in ["hello", "hi", "salam", "assalamualaikum", "kia hall hai"]):
        return "greeting"
    elif any(q in message for q in ["result", "kab", "kb", "date", "announce"]):
        return "question"
    elif any(w in message for w in ["notes", "textbook", "guide", "past paper", "chapter"]):
        return "search"
    else:
        return "question"  # fallback to DeepSeek

# Ask DeepSeek API for general questions
def ask_deepseek(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You're an educational assistant for a Pakistani site Ainotes.pk. Give to-the-point, accurate, and helpful answers. Use Urdu if the question is in Urdu."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Search Ainotes.pk mock (update with real search later)
def search_ainotes(query):
    if "class 9" in query.lower():
        return "🔗 https://ainotes.pk/fbise-new-textbooks-for-class-9-2024-2025/"
    return "🔗 https://ainotes.pk/?s=" + query.replace(" ", "+")

# Webhook route for Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    intent = detect_intent(incoming_msg)

    if intent == "greeting":
        reply = "👋 Walikum Salam! Main Ainotes.pk ka assistant hoon. Aap ko kis cheez ki madad chahiye?"
    elif intent == "search":
        result = search_ainotes(incoming_msg)
        reply = f"📘 Yeh mila:\n{result}"
    else:
        reply = ask_deepseek(incoming_msg)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{reply}</Message>
</Response>"""

