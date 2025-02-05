import os
import csv
import requests  # <-- Add this line to import the requests library
from flask import Flask, render_template, jsonify
import numpy as np
import threading
import time
from datetime import datetime

# Flask setup
app = Flask(__name__)

# ESP32 Web Server IP
ESP32_IP = "192.168.132.113"
DATA_URL = f"http://{ESP32_IP}/data"

# Store real-time data
data_store = {"x_vals": [], "y_vals": [], "distances": [], "angles": []}

# Function to initialize or clear the CSV file
def initialize_csv():
    if os.path.isfile("lidar_data.csv"):
        os.remove("lidar_data.csv")  # Delete the old file if it exists
    # Create the CSV file and write headers
    with open("lidar_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "X (mm)", "Y (mm)", "Distance (mm)", "Angle (°)"])  # Write headers

# Function to append data to the CSV file
def append_to_csv(timestamp, x, y, distance, angle):
    with open("lidar_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, f"{x:.2f}", f"{y:.2f}", f"{distance:.2f}", f"{angle:.2f}"])  # Format data and append

def fetch_data():
    """Continuously fetch data from ESP32 and emit via WebSocket."""
    while True:
        try:
            print(f"Fetching data from {DATA_URL}...")  # Debug: Indicate fetching start

            response = requests.get(DATA_URL, timeout=2)  # Timeout for quick failure
            if response.status_code == 200:
                data = response.text.strip()
                print(f"Raw data received: {data}")  # Debug: Print raw data

                parts = data.split("|")

                # Ensure the format matches expectations (length should be 3)
                if len(parts) == 3:
                    try:
                        # Extract distance and angle
                        distance = float(parts[1].split(":")[1].strip().replace(" mm", ""))
                        angle = float(parts[2].split(":")[1].strip())

                        # Convert polar to Cartesian coordinates
                        angle_rad = np.radians(angle)
                        x = distance * np.cos(angle_rad)
                        y = distance * np.sin(angle_rad)

                        # Get the timestamp
                        timestamp = datetime.now().strftime("%H:%M:%S")

                        # Store data
                        data_store["x_vals"].append(x)
                        data_store["y_vals"].append(y)
                        data_store["distances"].append(distance)
                        data_store["angles"].append(angle)

                        # Keep only the latest 500 values
                        for key in data_store:
                            if len(data_store[key]) > 500:
                                data_store[key].pop(0)

                        # Print formatted output in terminal
                        print(f"Logged: Point ({x:.2f}, {y:.2f}), Distance {distance} mm, Angle {angle}°")

                        # Append the data to CSV file
                        append_to_csv(timestamp, x, y, distance, angle)

                    except ValueError as e:
                        print(f"❌ Error processing data: {e}")
                else:
                    print(f"⚠️ Data format mismatch: {data}")
            else:
                print(f"❌ ESP32 Response Error ({response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"🚨 Connection Error: {e}")

        time.sleep(0.3)  # Fetch every 300ms

# Endpoint to get the data from the CSV file
@app.route("/get_lidar_data")
def get_lidar_data():
    # Read the data from the CSV file
    lidar_data = {"x_vals": [], "y_vals": [], "distances": [], "angles": []}
    if os.path.isfile("lidar_data.csv"):
        with open("lidar_data.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                timestamp, x, y, distance, angle = row
                lidar_data["x_vals"].append(float(x))
                lidar_data["y_vals"].append(float(y))
                lidar_data["distances"].append(float(distance))
                lidar_data["angles"].append(float(angle))

    return jsonify(lidar_data)

@app.route("/")
def home():
    return render_template("index.html")

# Initialize or clear the CSV file when the app starts
initialize_csv()

# Run the data fetcher in a separate thread
threading.Thread(target=fetch_data, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)



# from flask import Flask, render_template
# from flask_socketio import SocketIO
# import pandas as pd
# import numpy as np
# import threading
# import time
# from datetime import datetime
#
# # Flask setup
# app = Flask(_name_)
# socketio = SocketIO(app, cors_allowed_origins="*")
#
# # Load CSV data
# CSV_FILE = "lidar_data.csv"  # Ensure this file exists in the correct path
# try:
#     df = pd.read_csv(CSV_FILE)
# except FileNotFoundError:
#     print(f"🚨 Error: CSV file '{CSV_FILE}' not found!")
#     exit(1)
# except Exception as e:
#     print(f"🚨 Error reading CSV file: {e}")
#     exit(1)
#
# # Store real-time data
# data_store = {"x_vals": [], "y_vals": [], "distances": [], "angles": []}
#
# def simulate_data():
#     """Simulate real-time data fetching from CSV."""
#     for _, row in df.iterrows():
#         try:
#             distance = float(row["Distance_mm"])  # Corrected column name
#             angle = float(row["Angle_deg"])  # Corrected column name
#
#             # Convert polar to Cartesian
#             angle_rad = np.radians(angle)
#             x = distance * np.cos(angle_rad)
#             y = distance * np.sin(angle_rad)
#
#             # Store data
#             data_store["x_vals"].append(x)
#             data_store["y_vals"].append(y)
#             data_store["distances"].append(distance)
#             data_store["angles"].append(angle)
#
#             # Keep only the latest 500 values
#             for key in data_store:
#                 if len(data_store[key]) > 500:
#                     data_store[key].pop(0)
#
#             # Emit data via WebSocket
#             socketio.emit("update_data", data_store)
#
#             time.sleep(0.3)  # Simulate real-time behavior with delay
#         except KeyError as e:
#             print(f"🚨 Missing column in CSV: {e}")
#             exit(1)
#         except ValueError as e:
#             print(f"🚨 Data conversion error: {e}")
#             continue
#         except Exception as e:
#             print(f"🚨 Unexpected error: {e}")
#             continue
#
# @app.route("/")
# def home():
#     return render_template("index.html")
#
# # Run the data simulator in a separate thread
# threading.Thread(target=simulate_data, daemon=True).start()
#
# if _name_ == "_main_":
#     print("🚀 Starting Flask server...")
#     try:
#         socketio.run(app, debug=True, host="127.0.0.1", port=5000)  # Use 127.0.0.1 for local access
#     except Exception as e:
#         print(f"🚨 Flask failed to start: {e}")
