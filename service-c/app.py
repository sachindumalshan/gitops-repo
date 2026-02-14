from flask import Flask, request, jsonify

app = Flask(__name__)

alerts = []

THRESHOLD_TEMP = 30

@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

@app.route("/check-alert", methods=["POST"])
def check_alert():
    data = request.json
    temperature = data.get("temperature")
    device_id = data.get("device_id")

    if temperature > THRESHOLD_TEMP:
        alert = {
            "device_id": device_id,
            "message": "High temperature detected!"
        }
        alerts.append(alert)
        return jsonify({"alert": alert}), 200

    return jsonify({"message": "Temperature normal"}), 200

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
