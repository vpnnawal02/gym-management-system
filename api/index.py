from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Hello from Flask on Vercel!"})

handler = app  # Vercel looks for 'handler'
