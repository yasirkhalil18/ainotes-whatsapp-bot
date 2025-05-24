# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    print(f"📨 From {from_number} —> Message: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Expanded keyword mapping
    replacements = {
        # Subjects (shortcuts)
        "phy": "physics", "bio": "biology", "chem": "chemistry", "math": "mathematics",
        "isl": "islamiat", "comp": "computer", "eng": "english", "urdu": "urdu",
        "pak": "pak study", "g sci": "general science", "sci": "science",

        # Class identifiers
        "1st year": "class 11", "2nd year": "class 12", "ix": "class 9", "x": "class 10",
        "matric": "class 10", "inter": "class 11 class 12",

        # Boards
        "federal": "fbise", "fedral": "fbise", "punjab": "punjab board", "sind": "sindh board",
        "kpk": "kpk board", "bal": "balochistan board", "ajk": "ajk board",

        # Content types
        "keybook": "key book", "text book": "textbook", "past": "past papers",
        "model": "model papers", "guess": "guess papers", "solved": "solved papers",

        # Competitive
        "army": "army test", "pma": "pma long course", "issb": "issb preparation",
        "css": "css exam", "pms": "pms exam",
        
        # Common typos or chat language
        "fbse": "fbise", "fed": "fbise", "phyx": "physics", "biolgy": "biology",
        "key bk": "key book", "kitaab": "textbook", "kitab": "textbook",
    }

    # Apply replacements
    for key, value in replacements.items():
        if key in incoming_msg:
            incoming_msg = incoming_msg.replace(key, value)

    query = f"{incoming_msg} site:ainotes.pk"
    print(f"🔍 Searching Google for: {query}")

    try:
        results = list(search(query, num_results=1))
        if results:
            link = results[0]
            msg.body(f"🔗 Here's what I found for:\n*{incoming_msg}*\n👉 {link}")
        else:
            msg.body("❌ Sorry! No result found.\nVisit: https://ainotes.pk")
    except Exception as e:
        print("❌ Error:", str(e))
        msg.body("⚠️ Error fetching result. Please try again later.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
