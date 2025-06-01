from flask import Flask, request
import requests
import re

app = Flask(__name__)

# ✅ Your working DeepSeek API Key
API_KEY = "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"

# ✅ Abuse Filter (block 18+ messages)
def is_abusive(text):
    abuse_keywords = ['gandu', 'bhosdi', 'chutiya', 'madarchod', 'lund', 'sex']
    return any(bad in text.lower() for bad in abuse_keywords)

# ✅ Check if query is about notes/textbooks/etc
def is_study_related(text):
    keywords = ['notes', 'textbook', 'past paper', 'class', 'guess', 'short', 'long question']
    return any(k in text.lower() for k in keywords)

# ✅ Real-time Google Search for Ainotes.pk
def search_ainotes(query):
    base = "https://www.google.com/search?q=site:ainotes.pk+"
    search_url = base + "+".join(query.split())
    return f"📘 Aap yahan check kar sakte hain:\n{search_url}"

# ✅ DeepSeek smart Urdu response
def ask_deepseek(query):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Aap ek Urdu AI assistant hain Ainotes.pk ke liye. Sawal ka chhota, simple, aur Urdu mein jawab dein. "
                    "Agar study ya education ka sawal ho to seedha jawab dein. Agar notes chahiyein to search na karen, "
                    "balki Ainotes.pk ka link dein."
                )
            },
            {"role": "user", "content": query}
        ]
    }
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200:
        return res.json()['choices'][0]['message']['content'].strip()
    else:
        return "❌ AI se jawab nahi mila. Mazeed info ke liye Ainotes.pk par jayein."

# ✅ Home route
@app.route("/")
def home():
    return "✅ Ainotes WhatsApp Bot is Live!"

# ✅ Webhook for Twilio WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()

    # ❌ Abuse filter
    if is_abusive(incoming_msg):
        return respond("⚠️ Aapka paighaam naamunasib tha. Barah-e-karam tameez se baat karein.")

    # 📘 Study notes/textbook/paper request
    if is_study_related(incoming_msg):
        link = search_ainotes(incoming_msg)
        return respond(f"{link}\n\nAgar yeh notes available nahi, to aap request bhej sakte hain admin ko.\n🔗 https://ainotes.pk")

    # 💬 General question → AI response
    answer = ask_deepseek(incoming_msg)
    return respond(f"{answer}\n\n🔎 Mazeed info: https://ainotes.pk")

# ✅ Twilio-compatible XML response
def respond(text):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>{text}</Message>
</Response>"""

# ✅ Run server (comment this if using Render)
# if __name__ == "__main__":
#     app.run(debug=True)
