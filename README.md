NIRAKSHAK - Autonomous Mine Inspection Robot
Note
A detailed document containing the project presentation, report, demo videos, and all relevant links can be found in our Project Master Document.

NIRAKSHAK (a name derived from the Sanskrit word for "Inspector") is an advanced robotics project designed for the autonomous inspection of mines. This system enhances safety in hazardous underground environments by using a robot to explore and assess areas that are too risky for human entry.

The project was created by Team Nirakshit and proudly secured 2nd Place at the Reboot Hackathon during Yantra Week at VIT Vellore.

The core of the solution is a ROS2-based robot capable of navigating mines, collecting real-time environmental data, and identifying structural weaknesses like cracks using a custom-trained machine learning model.

Key Features
Autonomous Navigation and Mapping: Utilizes LiDAR and the ROS2 Navigation Stack for precise, real-time mapping and navigation within complex mine layouts.

Real-time Hazard Detection: Equipped with multiple sensors, including flame and smoke detectors, to identify immediate dangers and report them to a central dashboard.

Machine Learning for Crack Detection: Implements a lightweight ML model to analyze tunnel surfaces and detect structural cracks, helping to prevent potential collapses.

High-Fidelity Simulation: The robot's algorithms were developed and tested in the Gazebo simulation environment, allowing for rapid prototyping and validation before hardware deployment.

Custom Hardware Controller: Built on a custom-designed PCB with an ESP32 microcontroller to manage the various sensors and actuators efficiently.

Web-Based Monitoring Dashboard: A user-friendly web interface for monitoring the robot's live status, viewing sensor data, and accessing automated risk assessment reports.

Technical Overview & Workflow
The system integrates hardware and software to create a complete inspection solution.

Hardware: A custom-built robot platform with an ESP32-based controller. Onboard sensors include LiDAR for mapping, a camera for visual data, and environmental sensors for gas and flame detection.

Software & Simulation: The robot's logic runs on ROS2, a flexible framework for robot software development. All navigation and sensor integration were first validated in a simulated mine environment in Gazebo.

Data & ML Processing: The data processing pipeline, including the machine learning model for crack detection, is handled by Python scripts.

Workflow: The robot autonomously navigates a mine shaft, streaming sensor and LiDAR data. This information is processed to build a map, detect hazards, and identify cracks. The findings are compiled into an automated report accessible via the web dashboard.

Repository Contents
This repository contains the source code and documentation for the NIRAKSHAK project.

File/Folder	Description
app.py	The main Python script for the web application backend (using a framework like Flask or FastAPI).
index.html	The main HTML file for the user interface of the web dashboard.
style.css	The CSS file for styling the web dashboard.
lidar.cpp	C++ source code for the ROS2 node responsible for interfacing with and processing data from the LiDAR sensor.
sensor_data.cpp	C++ source code for the ROS2 node that collects and publishes data from various environmental sensors.
gas.py	A Python script likely used for processing and interpreting data from gas sensors.
LiDAR_Report.pdf	A report document detailing the LiDAR integration, mapping algorithms, and results.
imagesnirakhshit.pdf	A document containing images of the hardware, team, and simulation.
Team and Acknowledgments
This project was brought to life by the dedicated members of Team Nirakshit.

Aman Chauhan - (LinkedIn / GitHub)

Aniket Singh - (LinkedIn / GitHub)

Tanmay Mishra - (LinkedIn / GitHub)

Robin Philip - (LinkedIn / GitHub)

Satvik Choudhary - (LinkedIn / GitHub)

Mentor: Dr. Tanmaya Kumar Das

This project was recognized for its innovation, winning 2nd Place at the Reboot Hackathon, Yantra Week, VIT Vellore.
