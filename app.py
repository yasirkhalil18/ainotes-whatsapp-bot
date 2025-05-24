from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ----------------------
# Keyword to Link Mapping
# ----------------------
KEYWORD_MAP = {
    "fbise notes": "https://ainotes.pk/fbise-notes/",
    "class 9 notes": "https://ainotes.pk/fbise-notes/class-9/",
    "class 10 notes": "https://ainotes.pk/fbise-notes/class-10/",
    "class 11 notes": "https://ainotes.pk/fbise-notes/class-11/",
    "class 12 notes": "https://ainotes.pk/fbise-notes/class-12/",
    "fsc part 1 notes": "https://ainotes.pk/fbise-notes/class-11/",
    "fsc part 2 notes": "https://ainotes.pk/fbise-notes/class-12/",
    "mdcat notes": "https://ainotes.pk/mdcat-notes/",
    "css notes": "https://ainotes.pk/css-notes/",
    "pms notes": "https://ainotes.pk/pms-notes/",
    "army test notes": "https://ainotes.pk/army-test-notes/",
    "pak army": "https://ainotes.pk/army-test-notes/",
    "ai lab reports": "https://ainotes.pk/bs-ai-books-notes-and-lab-reports/",
    "bs ai": "https://ainotes.pk/bs-ai-books-notes-and-lab-reports/",
    "bs ai lab": "https://ainotes.pk/bs-ai-books-notes-and-lab-reports/",
    "java lab report": "https://ainotes.pk/bs-ai-books-notes-and-lab-reports/lab-report-oel-airplane-reservation-system-in-java/",
    "guess the word": "https://ainotes.pk/guess-the-word/",
    "mcqs": "https://ainotes.pk/mcqs/",
    "past papers": "https://ainotes.pk/past-papers/",
    "9th mcqs": "https://ainotes.pk/mcqs/class-9/",
    "10th mcqs": "https://ainotes.pk/mcqs/class-10/",
    "11th mcqs": "https://ainotes.pk/mcqs/class-11/",
    "12th mcqs": "https://ainotes.pk/mcqs/class-12/",
    "online earning": "https://ainotes.pk/earnings-skills-for-students/online-earning-in-pakistan-without-investment-2025-guide-for-students/",
    "motorway police jobs": "https://ainotes.pk/government-jobs/nhmp-jobs-2025-apply-online-for-2100-motorway-police-vacancies-salary-guide/",
    "notes": "https://ainotes.pk/"
}

# ----------------------
# Flask Route for Twilio
# ----------------------
@app.route("/sms", methods=["POST"])
def sms_reply():
    user_input = request.form.get("Body", "").lower().strip()
    resp = MessagingResponse()
    matched = False

    for keyword, link in KEYWORD_MAP.items():
        if keyword in user_input:
            reply = f"🔍 Result for: {keyword.title()}\n🔗 {link}"
            resp.message(reply)
            matched = True
            break

    if not matched:
        default_reply = (
            "❌ No exact match found.\n"
            "Try one of these keywords:\n"
            "- fbise notes\n- mdcat notes\n- css notes\n"
            "- class 9 notes\n- ai lab reports\n- army test notes\n"
            "- guess the word\n- past papers\n- online earning"
        )
        resp.message(default_reply)

    return str(resp)

# ----------------------
# Run Flask App
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
