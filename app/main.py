import os
import sys
from flask import Flask, jsonify

app = Flask(__name__)

PORT = os.getenv("APP_PORT")

if not PORT:
    print("ERROR: APP_PORT environment variable not set")
    sys.exit(1)

@app.route("/")
def home():
    return jsonify({
        "app": "port-demo-app",
        "port": PORT
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(PORT))
