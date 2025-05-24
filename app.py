# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Load search data
with open("search-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Expanded keyword groups
keywords = {
    "books": [
        "book", "books", "kitab", "pdf", "textbook", "ebooks", "download book", "book of", "full book", "pura kitab", "chapter book"
    ],
    "notes": [
        "note", "notes", "helping", "handout", "short questions", "long questions", "chapter wise", "mcqs", "key points", "important questions", "full notes"
    ],
    "class": [
        "class", "grade", "matric", "inter", "ninth", "tenth", "eleventh", "twelfth", "9", "10", "11", "12", "class 9", "class 10", "class 11", "class 12"
    ],
    "subject": [
        "biology", "physics", "chemistry", "math", "mathematics", "computer", "computer science", "urdu", "english", "islamiat", "islamiyat", "pakistan studies",
        "pak studies", "science", "general science", "islamic studies", "education", "economics", "sindhi", "history", "geography", "civics", "pma", "css"
    ],
    "board": [
        "fbise", "punjab", "kpk", "balochistan", "ajk", "sindh", "federal board", "punjab board", "kpk board", "balochistan board", "ajk board", "sindh board"
    ]
}

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running with Full Smart Matching!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    matched_links = []

    for entry in data:
        title = entry.get("title", "").lower()

        # Matching by score
        score = 0
        for group in keywords.values():
            for word in group:
                if word in incoming_msg and word in title:
                    score += 1

        if score >= 2:
            matched_links.append(f"👉 {entry['title']}\n🔗 {entry['link']}")

        if len(matched_links) >= 3:
            break

    if matched_links:
        msg.body(f"🔍 Results for: *{incoming_msg}*\n\n" + "\n\n".join(matched_links))
    else:
        msg.body("❌ Sorry! I couldn't find anything. Try again using clear words like 'class 10 physics notes fbise'. Or visit: https://ainotes.pk")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
