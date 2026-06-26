from flask import Flask, jsonify, render_template
import psutil, sqlite3, datetime
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("battery_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS battery_logs (
        date TEXT PRIMARY KEY,
        percent INTEGER,
        plugged INTEGER,
        health REAL
    )
    """)
    conn.commit()
    conn.close()

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery is None:
        return None
    return {
        "date": str(datetime.date.today()),
        "percent": battery.percent,
        "plugged": int(battery.power_plugged)
    }

def predict_health(charge_cycles):
    X = np.array([[100],[200],[300],[400],[500]])
    y = np.array([95, 90, 85, 80, 75])
    model = LinearRegression()
    model.fit(X, y)
    return float(model.predict([[charge_cycles]])[0])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/battery")
def battery_info():
    info = get_battery_info()
    if info is None:
        return jsonify({"error": "No battery detected"})
    health = predict_health(300)
    return jsonify({
        "percent": info["percent"],
        "plugged": bool(info["plugged"]),
        "health": round(health, 2)
    })

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

