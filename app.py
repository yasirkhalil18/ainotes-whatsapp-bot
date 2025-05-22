from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from os import environ

app = Flask(__name__)

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = environ.get('TWILIO_PHONE_NUMBER')

# Subject mapping for short forms
subject_map = {
    "bio": "biology",
    "chem": "chemistry",
    "phy": "physics",
    "math": "math",
    "maths": "math",
    "mathematics": "math"
}

# Static links dictionary (JSON method)
notes_links = {
    "class-9-chemistry-federal-board-fbise-notes": "https://ainotes.pk/class-9-notes-pdf-chemistry-federal-board-fbise/",
    "class-10-biology-federal-board-fbise-textbook": "https://ainotes.pk/10th-class-biology-textbook-federal-board-fbise/",
    "class-10-physics-federal-board-fbise-notes": "https://ainotes.pk/10th-class-physics-federal-board-fbise/",
    "class-9-chemistry-punjab-board-textbook": "https://ainotes.pk/9th-class-chemistry-punjab-board/"
}

# Fetch resource link from static dictionary
def get_resource_link(class_number, subject, board, resource_type="notes"):
    mapped_subject = subject_map.get(subject, subject)
    key = f"class-{class_number}-{mapped_subject}-{board}-{resource_type}"
    return notes_links.get(key)

# Main bot logic
def process_message(incoming_msg):
    incoming_msg = incoming_msg.lower()
    if "class" in incoming_msg:
        class_number = "9" if "class 9" in incoming_msg else "10" if "class 10" in incoming_msg else "9"
        subject = next((sub for sub in ["chemistry", "physics", "biology", "math", "bio", "chem", "phy", "maths"] if sub in incoming_msg), "")
        board = "federal-board-fbise" if "federal" in incoming_msg or "fbise" in incoming_msg else "punjab-board" if "punjab" in incoming_msg else ""
        resource_type = "textbook" if "textbook" in incoming_msg or "book" in incoming_msg else "notes"
        
        if subject:
            real_link = get_resource_link(class_number, subject, board, resource_type)
            return f"Yeh raha {resource_type} link 📚: {real_link}" if real_link else f"{resource_type.capitalize()} nahi mila 😔. Class: {class_number}, Subject: {subject}, Board: {board}"
        return "Subject nahi mila 😔. Example: Class 9 Bio Textbook Federal"
    else:
        if "kya haal" in incoming_msg or "hello" in incoming_msg or "hy" in incoming_msg:
            return "Sab theek, bhai! 😎 Kis class ke notes ya textbook chahiye?"
        return "Welcome to AiNotes.pk Bot! 📚 Kis class, subject, ya board ke notes/textbook chahiye? Example: Class 9 Bio Textbook Federal"

# Flask route for WhatsApp
@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    reply = process_message(incoming_msg)
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
