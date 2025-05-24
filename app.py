# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Load search data from JSON file
with open("search-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define keyword groups for matching
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

    results = []

    for entry in data:
        title = entry.get("title", "").lower()
        score = 0

        for group in keywords.values():
            for word in group:
                if word in incoming_msg:
                    score += 1
                if word in title:
                    score += 1

        if score >= 2:
            results.append((score, entry))

    # Sort matched results by score (highest first)
    results.sort(reverse=True, key=lambda x: x[0])
    top_matches = results[:3]  # Max 3 results

    if top_matches:
        matched_links = [f"👉 {entry['title']}\n🔗 {entry['url']}" for _, entry in top_matches]
        msg.body(f"🔍 Results for: *{incoming_msg}*\n\n" + "\n\n".join(matched_links))
    else:
        msg.body("❌ Sorry! I couldn't find anything. Try again using clear words like 'class 10 physics notes fbise'. Or visit: https://ainotes.pk")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
