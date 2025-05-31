from flask import Flask, request
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# ✅ Root route to avoid "Not Found" error
@app.route("/")
def home():
    return "🤖 Ainotes WhatsApp Bot is Live and Running!"

# ✅ Intent Detection
def detect_intent(message):
    message = message.lower()
    if any(greet in message for greet in ["hello", "hi", "salam", "assalamualaikum", "kia hall hai"]):
        return "greeting"
    elif any(q in message for q in ["result", "kab", "kb", "date", "announce", "hoga", "ayega", "aa rah", "rha", "raha"]):
        return "question"
    elif any(w in message for w in ["notes", "textbook", "guide", "past paper", "chapter", "mcqs", "long", "short"]):
        return "search"
    else:
        return "question"  # fallback to DeepSeek

# ✅ DeepSeek for answering questions
def ask_deepseek(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are an educational assistant for a Pakistani website Ainotes.pk. Give helpful, short, and accurate answers in Urdu if user asks in Urdu."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    return data["choices"][0]["message"]["content"]

# ✅ Real-time Ainotes Search (simple Google fallback)
def search_ainotes(query):
    # 🔄 Customize this with your real search engine later
    search_url = "https://www.google.com/search?q=site:ainotes.pk+" + query.replace(" ", "+")
    return f"🔎 Ainotes.pk Search:\n{search_url}"

# ✅ Webhook for Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    intent = detect_intent(incoming_msg)

    if intent == "greeting":
        reply = "👋 Walikum Salam! Main Ainotes.pk ka assistant hoon. Aap ko kis cheez ki madad chahiye?"
    elif intent == "search":
        result = search_ainotes(incoming_msg)
        reply = f"{result}"
    else:
        result = ask_deepseek(incoming_msg)
        reply = f"📘 {result}"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{reply}</Message>
</Response>"""

