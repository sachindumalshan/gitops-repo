from flask import Flask, request, jsonify

app = Flask(__name__)

devices = []

# ── Health probes ──────────────────────────────────────────────
@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

# ── Device endpoints ───────────────────────────────────────────
@app.route("/devices", methods=["POST"])
def register_device():
    data = request.get_json()
    if not data or not data.get("device_id"):
        return jsonify({"error": "device_id is required"}), 400

    device = {
        "device_id": data.get("device_id"),
        "location":  data.get("location", "unknown")
    }
    devices.append(device)
    print(f"[service-a] Registered device: {device}", flush=True)
    return jsonify({"message": "Device registered", "device": device}), 201

@app.route("/devices", methods=["GET"])
def list_devices():
    print(f"[service-a] Listing {len(devices)} device(s)", flush=True)
    return jsonify(devices), 200

@app.route("/devices/<device_id>", methods=["GET"])
def get_device(device_id):
    device = next((d for d in devices if d["device_id"] == device_id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404
    return jsonify(device), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)