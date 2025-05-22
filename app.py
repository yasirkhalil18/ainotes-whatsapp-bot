from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Subject mapping for short forms
subject_map = {
    "bio": "biology",
    "chem": "chemistry",
    "phy": "physics",
    "math": "math",
    "maths": "math",
    "mathematics": "math"
}

# Scrape links from AiNotes.pk
def get_resource_link(class_number, subject, board, resource_type="notes"):
    mapped_subject = subject_map.get(subject, subject)
    base_urls = []
    if resource_type == "textbook":
        base_urls = [f"https://ainotes.pk/fbise-new-textbooks-for-class-{class_number}-2024-2025/"]
    else:
        base_urls = [f"https://ainotes.pk/{'fbise' if 'fbise' in board else 'punjab-board'}-notes-class-9-to-12/"]
    
    for base_url in base_urls:
        try:
            res = requests.get(base_url)
            print(f"Scrape Status for {base_url}: {res.status_code}")
            if res.status_code != 200:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                href = link.get('href', '').lower()
                if (mapped_subject in href and class_number in href and 
                    (board in href or 'fbise' in href or 'punjab' in href) and 
                    resource_type in href):
                    return href
        except Exception as e:
            print(f"Scraping Error for {base_url}: {e}")
    return None

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
        if "kya haal" in incoming_msg or "hello" in incoming_msg:
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
