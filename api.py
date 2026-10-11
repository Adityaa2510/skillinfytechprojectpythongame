import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)

INSTANCE_ID = os.getenv("INSTANCE_ID", socket.gethostname())


@app.get("/")
def home():
    return jsonify(
        application="Snake Arena API",
        message="API is running",
        instance=INSTANCE_ID,
    )


@app.get("/health")
def health():
    return jsonify(
        status="healthy",
        instance=INSTANCE_ID,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)