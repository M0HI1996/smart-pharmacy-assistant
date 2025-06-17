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
from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# CSV ফাইল লোড করুন
medicine_df = pd.read_csv("medicine_price_template.csv")

# HTML Template with mobile-friendly styling
html_template = """
<!doctype html>
<html>
<head>
  <title>Smart Pharmacy Assistant</title>
  <style>
    body { font-family: sans-serif; padding: 20px; background: #f4f4f4; }
    input[type=text] { width: 90%; padding: 10px; font-size: 18px; }
    input[type=submit] { padding: 10px 20px; font-size: 16px; }
    .result { margin-top: 20px; background: #fff; padding: 15px; border-radius: 5px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h2>💊 Smart Pharmacy Assistant</h2>
  <form method="post">
    <input type="text" name="query" placeholder="Enter medicine name..." required><br><br>
    <input type="submit" value="🔍 Search">
  </form>
  {% if result %}
  <div class="result">{{ result }}</div>
  {% endif %}
</body>
</html>
"""

# Matching function
def find_medicine_price(query):
    result = medicine_df[medicine_df["Medicine Name"].str.lower().str.contains(query.lower())]
    if not result.empty:
        rows = []
        for _, row in result.iterrows():
            rows.append(f"{row['Medicine Name']} ({row['Company']}) - {row['Price (BDT)']} BDT per {row['Unit']}")
        return "\n".join(rows)
    else:
        return "❌ Sorry, medicine not found."

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        user_input = request.form["query"]
        result = find_medicine_price(user_input)
    return render_template_string(html_template, result=result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)