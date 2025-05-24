from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Helper: generate URL based on keywords
def generate_note_url(message):
    message = message.lower()
    
    boards = ['fbise', 'punjab', 'kpk', 'sindh', 'balochistan', 'ajk']
    classes = ['9', '10', '11', '12']
    content_types = ['notes', 'keybook', 'textbook', 'past paper', 'pma', 'issb', 'css', 'mdcat', 'army']
    
    subject_keywords = {
        'physics': 'physics',
        'chemistry': 'chemistry',
        'biology': 'biology',
        'math': 'mathematics',
        'english': 'english',
        'urdu': 'urdu',
        'islamiat': 'islamiat',
        'pak studies': 'pak-studies',
        'computer': 'computer',
        'general science': 'general-science'
    }

    board = next((b for b in boards if b in message), None)
    class_level = next((c for c in classes if c in message), None)
    subject = next((s for s in subject_keywords if s in message), None)
    content = next((ct for ct in content_types if ct in message), None)

    if 'pma' in message or 'issb' in message:
        return "https://ainotes.pk/army-tests/pma-issb-notes/"

    if 'css' in message:
        return "https://ainotes.pk/css/"

    if 'mdcat' in message:
        return "https://ainotes.pk/mdcat/"

    if 'army' in message:
        return "https://ainotes.pk/army-tests/"

    if board and class_level and subject:
        return f"https://ainotes.pk/{board}/{class_level}th-class/{subject_keywords[subject]}-{content if content else 'notes'}/"

    return None

# Routes
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running on Render!"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    
    print(f"📩 Message from {from_number}: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()

    url = generate_note_url(incoming_msg)

    if url:
        msg.body(f"✅ Here is the link: {url}")
    else:
        msg.body("❌ Sorry! I couldn't find your request. Visit https://ainotes.pk or type e.g. 'Class 9 FBISE Physics Notes'.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
