from flask import Flask
import os

app = Flask(__name__)

@app.route("/health")
def health():
    if os.getenv("FAIL") == "true":
        return "FAIL", 500
    return "OK", 200

@app.route("/")
def home():
    return "Service A Running", 200

app.run(host="0.0.0.0", port=8080)
