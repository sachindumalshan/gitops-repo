import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

alerts = []

THRESHOLD_TEMP = 30

# Kubernetes internal DNS: http://<service-name>.<namespace>.svc.cluster.local:<port>
# Since all services are in the same namespace (default), short name works:
SERVICE_B_URL = os.environ.get("SERVICE_B_URL", "http://service-b:80")

# ── Health probes ──────────────────────────────────────────────
@app.route("/live")
def live():
    return "OK", 200

@app.route("/ready")
def ready():
    return "READY", 200

# ── Alert endpoints ────────────────────────────────────────────
@app.route("/check-alert", methods=["POST"])
def check_alert():
    """
    Accepts: { "device_id": "...", "temperature": 35 }
    OR just { "device_id": "..." } → auto-fetches latest data from service-b
    """
    data = request.get_json()
    device_id   = data.get("device_id")
    temperature = data.get("temperature")

    # If temperature not provided, fetch latest reading from service-b
    if temperature is None and device_id:
        try:
            resp = requests.get(
                f"{SERVICE_B_URL}/sensor-data/{device_id}",
                timeout=3
            )
            readings = resp.json()
            if readings:
                temperature = readings[-1].get("temperature")
                print(f"[service-c] Fetched temp from service-b: {temperature}°C", flush=True)
            else:
                return jsonify({"message": "No sensor data found for this device"}), 404
        except requests.exceptions.RequestException as e:
            print(f"[service-c] Could not reach service-b: {e}", flush=True)
            return jsonify({"error": "Could not reach service-b", "detail": str(e)}), 503

    if temperature is None:
        return jsonify({"error": "temperature or device_id required"}), 400

    if temperature > THRESHOLD_TEMP:
        alert = {
            "device_id":   device_id,
            "temperature": temperature,
            "message":     f"🔥 High temperature! {temperature}°C exceeds limit of {THRESHOLD_TEMP}°C"
        }
        alerts.append(alert)
        print(f"[service-c] ALERT generated: {alert}", flush=True)
        return jsonify({"alert": alert}), 200

    print(f"[service-c] Temperature normal: {temperature}°C", flush=True)
    return jsonify({"message": f"Temperature normal ({temperature}°C)"}), 200

@app.route("/check-all-alerts", methods=["GET"])
def check_all_alerts():
    """
    Automatically fetch ALL sensor data from service-b
    and generate alerts for any high readings
    """
    try:
        resp = requests.get(f"{SERVICE_B_URL}/sensor-data", timeout=3)
        all_readings = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[service-c] Could not reach service-b: {e}", flush=True)
        return jsonify({"error": "Could not reach service-b", "detail": str(e)}), 503

    new_alerts = []
    for reading in all_readings:
        temp = reading.get("temperature")
        if temp and temp > THRESHOLD_TEMP:
            alert = {
                "device_id":   reading.get("device_id"),
                "temperature": temp,
                "message":     f"🔥 High temperature! {temp}°C exceeds limit of {THRESHOLD_TEMP}°C"
            }
            alerts.append(alert)
            new_alerts.append(alert)

    print(f"[service-c] Checked {len(all_readings)} readings, {len(new_alerts)} new alerts", flush=True)
    return jsonify({"checked": len(all_readings), "new_alerts": new_alerts}), 200

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)