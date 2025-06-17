from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def ask_groq(user_input):
    headers = {
        "Authorization": "Bearer api-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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a helpful pharmacy assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        user_input = request.form["query"]
        result = ask_groq(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
