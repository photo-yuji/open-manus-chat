from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("AIzaSyCpskddn_uvMSTE_VM0hutJbaBSFn920WE")

def query_gemini(user_input):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [{"text": user_input}]
            }
        ]
    }
    params = {
        "key": API_KEY
    }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        candidates = response.json().get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
        else:
            return "（Geminiから返答がありませんでした）"
    except Exception as e:
        return f"エラー: {e}"

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        response = query_gemini(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
