from flask import Flask, render_template, request
import google.generativeai as palm
import os
import openai
from textblob import TextBlob

# Configure the API keys
palm_api_key = "YOUR_PALM_API_KEY"
palm.configure(api_key=palm_api_key)

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")

@app.route("/ai_agent_reply", methods=["POST"])
def ai_agent_reply():
    q = request.form.get("q")
    try:
        # OpenAI GPT-3.5 API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q}],
        )
        r = response.choices[0].message['content']
    except Exception as e:
        r = f"Error: {str(e)}"
    
    return render_template("ai_agent_reply.html", r=r)

@app.route("/singapore_joke", methods=["POST"])
def singapore_joke():
    # A common joke in Singapore
    joke = "When there is a long queue, we love to just queue blindly without knowing what the line is for."
    return render_template("joke.html", joke=joke)

@app.route("/financial_portal", methods=["GET", "POST"])
def financial_portal():
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            # Analyze text with TextBlob
            blob = TextBlob(text)
            sentiment = blob.sentiment
            return render_template("financial_portal.html", sentiment=sentiment)
    return render_template("financial_portal.html")

if __name__ == "__main__":
    app.run(debug=True)

