from flask import Flask, request, jsonify

app = Flask(__name__)

devices = []

@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

@app.route("/devices", methods=["POST"])
def register_device():
    data = request.json
    device = {
        "device_id": data.get("device_id"),
        "location": data.get("location")
    }
    devices.append(device)
    return jsonify({"message": "Device registered", "device": device}), 201

@app.route("/devices", methods=["GET"])
def list_devices():
    return jsonify(devices), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
