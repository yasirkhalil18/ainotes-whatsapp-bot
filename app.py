from flask import Flask, request
import requests
import os

app = Flask(__name__)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ---------- Step 1: Identify Intent -------------
def detect_intent(message):
    message = message.lower()
    if any(word in message for word in ["hello", "hi", "salam", "assalam", "kia hal", "how are you"]):
        return "greeting"
    elif any(word in message for word in ["notes", "textbook", "guide", "past paper", "chapter", "book", "send"]):
        return "search"
    else:
        return "question"

# ---------- Step 2: Use DeepSeek for smart answers -------------
def ask_deepseek(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You're an assistant for Ainotes.pk. Answer clearly and helpfully in Urdu or English, based on the user's question."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "Maaf kijiye, koi issue aa gaya hai. Thodi dair baad koshish kijiye."

# ---------- Step 3: Real-time Search Ainotes.pk -------------
def search_ainotes(query):
    formatted_query = query.replace(" ", "+")
    return f"🔎 Yeh mila: https://ainotes.pk/?s={formatted_query}"

# ---------- Step 4: Webhook for WhatsApp (Twilio) -------------
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    intent = detect_intent(incoming_msg)

    if intent == "greeting":
        reply = "👋 Walikum Salam! Main Ainotes.pk ka assistant hoon. Aap ko kis cheez ki madad chahiye? Example: 'Class 10 Chemistry notes' ya 'FBISE result kab aye ga?'"
    elif intent == "search":
        reply = search_ainotes(incoming_msg)
    else:
        reply = ask_deepseek(incoming_msg)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{reply}</Message>
</Response>"""

