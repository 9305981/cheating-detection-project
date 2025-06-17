from flask import Flask, render_template, send_file, jsonify
import subprocess
import threading
import time
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["GET"])
def start_detection():
    # Run detect.py in a separate thread
    def run_script():
        subprocess.call(["python", "detect.py"])
    threading.Thread(target=run_script).start()
    return jsonify({"message": "Detection Started"})

@app.route("/get_logs")
def get_logs():
    try:
        with open("log.csv", "r") as f:
            logs = f.readlines()
        return jsonify({"logs": logs})
    except FileNotFoundError:
        return jsonify({"logs": ["No logs yet."]})

@app.route("/download")
def download_log():
    return send_file("log.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
