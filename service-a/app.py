from flask import Flask, jsonify, render_template_string
import os
import random
import time

app = Flask(__name__)

START_TIME = time.time()

# Simulated dependency status (DB / IoT broker / API)
DEPENDENCY_READY = True

# ---------- LIVENESS PROBE ----------
@app.route("/live")
def live():
    # Only check if app is running
    return "LIVE", 200


# ---------- READINESS PROBE ----------
@app.route("/ready")
def ready():
    # Check env-based failure
    if os.getenv("FAIL") == "true":
        return "NOT READY", 500

    # Check dependencies
    if not DEPENDENCY_READY:
        return "DEPENDENCY NOT READY", 500

    return "READY", 200


# ---------- METRICS (IoT-style) ----------
@app.route("/metrics")
def metrics():
    data = {
        "uptime_seconds": int(time.time() - START_TIME),
        "temperature": round(random.uniform(20.0, 40.0), 2),
        "humidity": round(random.uniform(30.0, 70.0), 2),
        "device_status": "ONLINE",
    }
    return jsonify(data), 200


# ---------- DASHBOARD UI ----------
@app.route("/")
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Service Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                text-align: center;
            }
            .card {
                background: #1e293b;
                padding: 20px;
                margin: 20px auto;
                width: 300px;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }
            h1 { color: #38bdf8; }
            .ok { color: #22c55e; }
        </style>
    </head>
    <body>
        <h1>📡 IoT Monitoring Dashboard</h1>

        <div class="card">
            <p class="ok">Service Status: RUNNING</p>
            <p>Uptime: {{ uptime }} seconds</p>
            <p>Temperature: {{ temp }} °C</p>
            <p>Humidity: {{ humidity }} %</p>
        </div>
    </body>
    </html>
    """,
    uptime=int(time.time() - START_TIME),
    temp=round(random.uniform(20.0, 40.0), 2),
    humidity=round(random.uniform(30.0, 70.0), 2)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)