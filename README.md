# Colruyt Coffee Packing System

Welcome to the **Colruyt Coffee Packing System**! This repository contains code and resources for automating the packaging process for coffee bags using a UR robot, an UP Board, and Python-based control scripts.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements File](#requirements-file)

## Introduction

This project focuses on automating coffee bag packaging with a robotic arm, ensuring efficiency and quality. The system uses Python for managing robot commands, handling sensor data, and providing a user-friendly interface.

## Features

- **Automated Packaging Process**: Streamlines the workflow to reduce manual labor.
- **Real-time Communication**: Utilizes sockets for efficient communication between the UP Board and the UR robot.
- **Computer Vision Integration**: Employs OpenCV and YOLO for advanced object detection tasks.
- **Interactive Interface**: Built using Tkinter for ease of control and monitoring.

## System Requirements

### Hardware
- **UR Robot**: Set up with a preloaded URScript.
- **UP Board**: Used for running the Python control scripts.
- **Camera**: For object detection and quality control (e.g., Razer Kiyo or equivalent).
- **Network**: Ethernet or similar network connecting the UP Board and the UR robot.

### Software
- **Operating System**: Linux on the UP Board (e.g., Ubuntu, Debian).
- **Python**: Version 3.6 or higher.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tijmenfeitz/Colruyt-Coffee-Packing.git
   cd Colruyt-Coffee-Packing
   ```

2. **Install Dependencies**:
   Use the `requirements.txt` file to install the necessary libraries:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set Up the Environment**:
   Ensure the robot and UP Board are on the same network, and the robot is preloaded with the required URScript.

## Usage

### 1. Prepare the Script on the Robot
- Open the URScript on the robot's interface but do not start it yet.

### 2. Navigate to the Program Directory on the UP Board
- Use the `cd` command in the terminal to go to the directory containing the `Coffee.py` script and other required files:
  ```bash
  cd /path/to/project/directory
  ```

### 3. Run the Python Script
- Start the Python script with the following command:
  ```bash
  sudo python3 Coffee.py
  ```
- Wait for the terminal to display:
  ```
  Waiting for robot connection...
  ```

### 4. Start the Robot Script
- Press the "Play" button on the robot interface to establish the connection.

### 5. Use the Interface
- The user interface (UI) will appear once the connection is active. Use it to control the packaging process, including options to start, stop, and monitor progress.

## Requirements File

The `requirements.txt` file includes:
```
time
periphery
tkinter
Pillow
socket
opencv-python
ultralytics
struct
threading
```

### Explanation of Key Libraries
- **time**: For managing delays and scheduling tasks.
- **periphery**: For hardware interaction and GPIO control.
- **tkinter**: To build the graphical user interface.
- **Pillow**: For image handling, such as displaying logos in the UI.
- **socket**: For network communication between the UP Board and the robot.
- **opencv-python**: For image processing and camera integration.
- **ultralytics**: For object detection using YOLO.
- **struct**: For packing and unpacking binary data.
- **threading**: To manage parallel tasks, such as maintaining communication with the robot.


