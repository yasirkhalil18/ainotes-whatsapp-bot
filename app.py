# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Keywords mapping
boards = {
    'fbise': 'FBISE',
    'punjab': 'Punjab',
    'kpk': 'KPK',
    'balochistan': 'Balochistan',
    'ajk': 'AJK',
    'sindh': 'Sindh'
}

classes = {
    'class 9': 'Class 9',
    'class 10': 'Class 10',
    'class 11': 'Class 11',
    'class 12': 'Class 12',
}

subjects = {
    'physics': 'Physics',
    'phy': 'Physics',
    'chemistry': 'Chemistry',
    'chem': 'Chemistry',
    'biology': 'Biology',
    'bio': 'Biology',
    'math': 'Mathematics',
    'computer': 'Computer',
    'english': 'English',
    'urdu': 'Urdu',
    'islamiat': 'Islamiat',
    'pak': 'Pakistan Studies',
    'p.s.t': 'Pakistan Studies',
}

# Website base URL
BASE_URL = "https://ainotes.pk"

@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')

    print(f"📩 Message from {from_number}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    found_class = None
    found_board = None
    found_subject = None

    # Matching logic
    for key in classes:
        if key in incoming_msg:
            found_class = classes[key]
            break

    for key in boards:
        if key in incoming_msg:
            found_board = boards[key]
            break

    for key in subjects:
        if key in incoming_msg:
            found_subject = subjects[key]
            break

    # Response logic
    if found_class and found_board and found_subject:
        msg.body(f"📘 Here's your {found_class} {found_board} {found_subject} Notes:\n👉 {BASE_URL}/notes/{found_board.lower()}/{found_class.replace(' ', '-').lower()}/{found_subject.lower()}")
    elif found_class and found_board:
        msg.body(f"📘 Here's your {found_class} {found_board} Notes:\n👉 {BASE_URL}/notes/{found_board.lower()}/{found_class.replace(' ', '-').lower()}")
    elif found_class:
        msg.body(f"📘 Here's your {found_class} Notes:\n👉 {BASE_URL}/notes/{found_class.replace(' ', '-').lower()}")
    else:
        msg.body("❌ Sorry! I couldn't find your request.\n💡 Try something like: 'Class 9 FBISE Physics Notes'\nOr visit 🔗 https://ainotes.pk")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
