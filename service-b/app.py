from flask import Flask, request, jsonify

app = Flask(__name__)

sensor_data = []

# ── Health probes ──────────────────────────────────────────────
@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

# ── Sensor data endpoints ──────────────────────────────────────
@app.route("/sensor-data", methods=["POST"])
def receive_data():
    data = request.get_json()
    if not data or not data.get("device_id"):
        return jsonify({"error": "device_id is required"}), 400

    entry = {
        "device_id":   data.get("device_id"),
        "temperature": data.get("temperature"),
        "humidity":    data.get("humidity")
    }
    sensor_data.append(entry)
    print(f"[service-b] Stored reading: {entry}", flush=True)
    return jsonify({"message": "Data received", "data": entry}), 201

@app.route("/sensor-data", methods=["GET"])
def get_all_data():
    print(f"[service-b] Returning {len(sensor_data)} readings", flush=True)
    return jsonify(sensor_data), 200

@app.route("/sensor-data/<device_id>", methods=["GET"])
def get_data_by_device(device_id):
    """Called internally by service-c via Kubernetes DNS"""
    readings = [d for d in sensor_data if d["device_id"] == device_id]
    return jsonify(readings), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)