from flask import Flask, request
import requests
import os

app = Flask(__name__)

DEEPSEEK_API_KEY = "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"

# ✅ 18+ abusive filter
abusive_words = ["gandu", "bhosdi", "madarchod", "chutiya", "lund", "bhenchod", "randi", "fuck", "sex"]

# ✅ Detect if message is study-related
def detect_intent(msg):
    msg = msg.lower()
    if any(word in msg for word in ["notes", "textbook", "book", "past paper", "paper", "guide", "guess"]):
        return "study"
    return "general"

# ✅ DeepSeek AI response
def ask_deepseek(query):
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
                    "Tum Ainotes.pk ke assistant ho. Har jawab choti Urdu mein do. Agar koi study-related info AI se mil jaye to do, "
                    "warna end mein bolo 'Mazid maloomat ke liye Ainotes.pk par jayein'."
                )
            },
            {"role": "user", "content": query}
        ]
    }
    res = requests.post(url, headers=headers, json=payload)
    data = res.json()
    return data["choices"][0]["message"]["content"]

# ✅ Google site search on Ainotes.pk
def search_ainotes(query):
    search_url = "https://www.google.com/search?q=site:ainotes.pk+" + "+".join(query.strip().split())
    return search_url

# ✅ Check if abusive message
def is_abusive(msg):
    msg = msg.lower()
    return any(word in msg for word in abusive_words)

# ✅ Twilio webhook
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()

    if is_abusive(incoming_msg):
        reply = "⛔ Ghalat alfaaz ka istemal na karein."
    else:
        intent = detect_intent(incoming_msg)

        if intent == "study":
            link = search_ainotes(incoming_msg)
            # Simulate search check: You can later improve by scraping (optional)
            reply = f"📘 Yeh notes shayad yahan mil jayein:\n{link}\n\nAgar yahan na milen to admin se request karne ke liye Ainotes.pk par jayein."
        else:
            response = ask_deepseek(incoming_msg)
            reply = f"{response}\n\nMazid maloomat ke liye Ainotes.pk par jayein."

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{reply}</Message>
</Response>"""

@app.route("/")
def home():
    return "✅ Ainotes WhatsApp Bot is Live!"
