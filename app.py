from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = "YAHAN_APNA_NAYA_GROQ_KEY_DALO"
ACCESS_KEYS = ["rack2714851332"]
CONTACT = "@racksun19"
OWNER = "@kihoerack"

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
        "owner": OWNER,
        "contact": CONTACT,
        "usage": "/api/rack?key=YOUR_KEY&message=YOUR_QUESTION"
    })


@app.route("/api/rack")
def chat():
    key = request.args.get("key", "")
    message = request.args.get("message", "")

    if key not in ACCESS_KEYS:
        return jsonify({"error": "Invalid API key", "owner": OWNER, "contact": CONTACT}), 403

    if not message:
        return jsonify({"error": "message parameter is required", "owner": OWNER, "contact": CONTACT}), 400

    try:
        headers = {
            "Authorization": "Bearer " + GROQ_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        text = data["choices"][0]["message"]["content"]
        return jsonify({"response": text, "owner": OWNER})
    except Exception as e:
        return jsonify({"error": str(e), "owner": OWNER, "contact": CONTACT}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
