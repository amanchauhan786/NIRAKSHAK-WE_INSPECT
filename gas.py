import os
import csv
import requests
import time
from flask import Flask, jsonify
from datetime import datetime

# Flask setup
app = Flask(__name__)

# ESP32 Web Server IP
ESP32_IP = "192.168.132.124"
DATA_URL = f"http://{ESP32_IP}/sensor_data"

# CSV File to store sensor data
CSV_FILE = "sensor_data.csv"

# Function to initialize or clear the CSV file
def initialize_csv():
    if os.path.isfile(CSV_FILE):
        os.remove(CSV_FILE)  # Delete existing file
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)", "CO2 Status", "Flame Sensor", "GPS Data"])

# Function to append sensor data to CSV
def append_to_csv(timestamp, temperature, humidity, co2_status, flame_status, gps_data):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temperature, humidity, co2_status, flame_status, gps_data])

# Function to fetch sensor data from ESP32
def fetch_data():
    while True:
        try:
            print(f"Fetching data from {DATA_URL}...")
            response = requests.get(DATA_URL, timeout=2)

            if response.status_code == 200:
                data = response.json()
                print(f"Raw Data: {data}")

                # Extract sensor values
                temperature = float(data.get("temperature", 0))
                humidity = float(data.get("humidity", 0))
                co2_status = data.get("co2_status", "Unknown")
                flame_status = data.get("flame_sensor", "Unknown")
                gps_data = data.get("gps", "No Data")

                # Timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Store data in CSV
                append_to_csv(timestamp, temperature, humidity, co2_status, flame_status, gps_data)
                print(f"Logged Data: {temperature}°C, {humidity}%, {co2_status}, {flame_status}, {gps_data}")

            else:
                print(f"ESP32 Response Error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"🚨 Connection Error: {e}")

        time.sleep(2)  # Fetch data every 2 seconds

# API Endpoint to retrieve stored sensor data
@app.route("/get_sensor_data")
def get_sensor_data():
    sensor_data = []
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                sensor_data.append({
                    "timestamp": row[0],
                    "temperature": row[1],
                    "humidity": row[2],
                    "co2_status": row[3],
                    "flame_sensor": row[4],
                    "gps_data": row[5]
                })
    return jsonify(sensor_data)

# Initialize CSV and start fetching data
initialize_csv()

if __name__ == "__main__":
    from threading import Thread
    fetch_thread = Thread(target=fetch_data, daemon=True)
    fetch_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
