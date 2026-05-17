from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY = "YAHAN_APNI_NAYE_GEMINI_KEY_DALO"
ACCESS_KEYS = ["apni_secret_key_yahan_likho"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

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
    return jsonify({
        "status": "online",
        "message": "AI API is running",
        "usage": "/api?key=YOUR_KEY&q=YOUR_QUESTION"
    })


@app.route("/api")
def chat():
    key = request.args.get("key", "")
    q = request.args.get("q", "")

    if key not in ACCESS_KEYS:
        return jsonify({"success": False, "error": "Invalid API key"}), 403

    if not q:
        return jsonify({"success": False, "error": "Query parameter 'q' is required"}), 400

    try:
        full_prompt = SYSTEM_PROMPT + "\n\nUser: " + q
        response = model.generate_content(full_prompt)
        return jsonify({
            "success": True,
            "query": q,
            "response": response.text
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
