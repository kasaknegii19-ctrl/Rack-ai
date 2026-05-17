from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

GEMINI_API_KEY = "YAHAN_APNI_NAYE_GEMINI_KEY_DALO"
ACCESS_KEYS = ["rack2714851332"]
CONTACT = "@racksun19"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

SYSTEM_PROMPT = """You are an extremely intelligent and helpful AI assistant.
You can help with:
- Coding in any programming language (Python, JavaScript, C++, Java, etc.)
- Answering any general knowledge question
- Solving math and science problems
- Writing stories, essays, or any creative content
- Giving advice and helping people with their problems
- Explaining complex topics in simple words
- Any other topic the user asks about

Always give clear, detailed, accurate and helpful responses.
If the user writes in Hindi, reply in Hindi.
If the user writes in English, reply in English.
Match the language of the user automatically."""


@app.route("/")
def home():
    return jsonify({"status": "online", "contact": CONTACT})


@app.route("/api/rack")
def chat():
    key = request.args.get("key", "")
    message = request.args.get("message", "")

    if key not in ACCESS_KEYS:
        return jsonify({"error": "Invalid API key", "contact": CONTACT}), 403

    if not message:
        return jsonify({"error": "message parameter is required", "contact": CONTACT}), 400

    try:
        full_prompt = SYSTEM_PROMPT + "\n\nUser: " + message
        response = model.generate_content(full_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e), "contact": CONTACT}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
