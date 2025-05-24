# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Synonym normalization function
def normalize_input(user_input):
    user_input = user_input.lower()
    synonyms = {
        'bio': 'biology',
        'phy': 'physics',
        'chem': 'chemistry',
        'maths': 'mathematics',
        'math': 'mathematics',
        'eng': 'english',
        'urduu': 'urdu',
        'islamiyat': 'islamiat',
        'islamic studies': 'islamiat',
        'pak studies': 'pakistan studies',
        'pakstudy': 'pakistan studies',
        'comp': 'computer science',
        'cs': 'computer science',
        'eco': 'economics',
        'econs': 'economics',
        'gen science': 'general science',
        'g science': 'general science',
        'fbise': 'federal board',
        'punjab board': 'punjab board',
        'kpk': 'kpk board',
        'kp': 'kpk board',
        'sindh': 'sindh board',
        'sd': 'sindh board',
        'balochistan': 'balochistan board',
        'bl': 'balochistan board',
        'ajk': 'ajk board',
        '9th': 'class 9',
        'ninth': 'class 9',
        '10th': 'class 10',
        'tenth': 'class 10',
        '11th': 'class 11',
        'eleventh': 'class 11',
        '1st year': 'class 11',
        'first year': 'class 11',
        '12th': 'class 12',
        'twelfth': 'class 12',
        '2nd year': 'class 12',
        'second year': 'class 12',
        'note': 'notes',
        'handouts': 'notes',
        'key book': 'keybooks',
        'key-book': 'keybooks',
        'text book': 'textbooks',
        'past paper': 'past papers',
        'previous papers': 'past papers',
        'old papers': 'past papers',
    }
    for key, value in synonyms.items():
        user_input = user_input.replace(key, value)
    return user_input

# URL generator
def generate_url(user_input):
    base_url = "https://ainotes.pk"
    
    boards = ["federal board", "punjab board", "kpk board", "sindh board", "balochistan board", "ajk board"]
    classes = ["class 9", "class 10", "class 11", "class 12"]
    subjects = [
        "physics", "chemistry", "biology", "mathematics", "english", "urdu",
        "islamiat", "pakistan studies", "computer science", "economics", "general science"
    ]
    types = ["notes", "keybooks", "textbooks", "past papers"]
    
    board = next((b for b in boards if b in user_input), "federal board")
    class_level = next((c for c in classes if c in user_input), None)
    subject = next((s for s in subjects if s in user_input), None)
    content_type = next((t for t in types if t in user_input), None)
    
    if class_level and subject and content_type:
        board_slug = board.replace(" ", "-")
        class_slug = class_level.replace("class ", "") + "th-class"
        subject_slug = subject.replace(" ", "-")
        content_slug = content_type.replace(" ", "-")
        return f"{base_url}/{board_slug}/{class_slug}/{subject_slug}-{content_slug}/"
    return None

# Health check route
@app.route("/", methods=["GET"])
def home():
    return "✅ WhatsApp Bot is Running Successfully!"

# Twilio webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    from_number = request.values.get('From', '')
    
    print(f"📩 Message from {from_number}: {incoming_msg}")
    
    normalized_msg = normalize_input(incoming_msg)
    response_url = generate_url(normalized_msg)

    resp = MessagingResponse()
    msg = resp.message()
    
    if response_url:
        msg.body(f"📚 Here is the link to your request:\n{response_url}")
    else:
        msg.body("❌ Sorry! I couldn't find your request. Visit https://ainotes.pk or type e.g. 'Class 9 FBISE Physics Notes'.")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
