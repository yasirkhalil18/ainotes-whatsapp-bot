from flask import Flask, request
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.route("/")
def home():
    return "✅ Ainotes WhatsApp Bot is Live!"

# Detect whether to search Ainotes or ask DeepSeek
def detect_intent(message):
    msg = message.lower()
    if "notes" in msg or "textbook" in msg or "past paper" in msg:
        return "search"
    return "question"

# Ask DeepSeek with error handling
def ask_deepseek(query):
    if not DEEPSEEK_API_KEY:
        return "❌ DeepSeek API key missing. Admin ko inform karein."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert assistant for Ainotes.pk. Answer in simple Urdu, be very short, direct, and helpful. "
                    "If it's a study-related question, answer to the point. If it’s a request for notes, refer to Ainotes.pk."
                )
            },
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ DeepSeek error:", e)
        return "⚠️ Maaf kijiye, abhi jawab dene mein masla ho raha hai."

# Google-based Ainotes.pk search
def search_ainotes(query):
    base_url = "https://www.google.com/search?q=site:ainotes.pk+"
    full_url = base_url + "+".join(query.strip().split())
    return f"📘 Ainotes.pk پر تلاش کریں:\n{full_url}"

# WhatsApp Twilio webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    print("📩 User:", incoming_msg)

    intent = detect_intent(incoming_msg)

    if intent == "search":
        reply = search_ainotes(incoming_msg)
    else:
        reply = ask_deepseek(incoming_msg)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{reply}</Message>
</Response>"""
