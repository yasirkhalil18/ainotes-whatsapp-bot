# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from googlesearch import search  # pip install googlesearch-python

app = Flask(__name__)

# ✅ Keyword Normalizer Function
def normalize_keywords(text):
    replacements = {
        # Classes
        "class 9": "class 9", "9th class": "class 9", "ninth class": "class 9",
        "class 10": "class 10", "10th class": "class 10", "tenth class": "class 10",
        "class 11": "class 11", "first year": "class 11", "1st year": "class 11",
        "class 12": "class 12", "second year": "class 12", "2nd year": "class 12",

        # Subjects
        "urdu": "urdu", "eng": "english", "english": "english", "islamiat": "islamiyat", 
        "isl": "islamiyat", "islamiyaat": "islamiyat", "math": "mathematics", 
        "chem": "chemistry", "phy": "physics", "bio": "biology", "computer": "computer science",

        # Boards
        "fbise": "fbise", "federal": "fbise", "punjab": "punjab board", "kpk": "kpk board",

        # Resources
        "notes": "notes", "notez": "notes", "notz": "notes",
        "past paper": "past papers", "model paper": "model papers",
        "guess paper": "guess papers", "textbook": "textbook", "book": "textbook",
        "important question": "important questions", "sawal": "questions",
        "mcqs": "mcqs", "short": "short questions", "long": "long questions",
        "kitab": "textbook", "papr": "papers"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

# ✅ Home Route (Health Check)
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

# ✅ Twilio Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    # Normalize user query
    clean_query = normalize_keywords(incoming_msg)

    # Build Google search query
    query = f"{clean_query} site:ainotes.pk"
    print(f"🔍 Searching Google for: {query}")

    try:
        results = list(search(query, num_results=1))
        if results:
            link = results[0]
            msg.body(f"🔗 Here's what I found for:\n*{incoming_msg}*\n👉 {link}")
        else:
            msg.body("❌ Sorry! I couldn't find your request. Visit https://ainotes.pk or try again with more details.")
    except Exception as e:
        msg.body("⚠️ Something went wrong. Please try again later.")
        print("Error:", e)

    return str(resp)

# ✅ Run App
if __name__ == "__main__":
    app.run(debug=True)
