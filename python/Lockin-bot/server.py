#!/usr/bin/env python3
"""
Local alert server for the focus detector.
Serves a webpage that plays a noise and tells the user to get back to work.
"""

from flask import Flask, render_template
import threading
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Focus Alert Server</h1><p>Server is running. Go to /alert to test.</p>"

@app.route('/alert')
def alert():
    return render_template('alert.html')

def start_server():
    """Start the Flask server in a background thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    )
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Wait for server to start
    print("Alert server started at http://127.0.0.1:5000")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)