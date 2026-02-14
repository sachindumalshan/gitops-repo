from flask import Flask, request, jsonify

app = Flask(__name__)

sensor_data = []

@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

@app.route("/sensor-data", methods=["POST"])
def receive_data():
    data = request.json
    entry = {
        "device_id": data.get("device_id"),
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity")
    }
    sensor_data.append(entry)
    return jsonify({"message": "Data received", "data": entry}), 201

@app.route("/sensor-data", methods=["GET"])
def get_data():
    return jsonify(sensor_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)