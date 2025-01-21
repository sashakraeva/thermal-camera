# Thermal Camera Setup and Testing Guide

This repository provides **step-by-step instructions** to set up and use a thermal camera (e.g., FLIR Lepton) with the **PureThermal 2 interface board**. It also includes **preliminary exercises** to validate that the hardware and software are correctly configured before running the final project.

---

## Features

- Real-time thermal video visualization.
- Highlights the hottest and coldest points in the frame, displaying their temperatures.
- A side **color bar** shows the temperature range (red = hottest, blue = coldest).

---

## Requirements

### Hardware

- **PureThermal 2** interface board.
- **FLIR Lepton camera module**.
- A computer running **Linux** (tested on Ubuntu).

### Software

- **Python 3.x**.
- Required libraries:
  - `libuvc`.
  - `OpenCV`.
  - `numpy`.

---

## Step-by-Step Setup

### Step 1: Clone This Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/Clarrainl/thermal-camera.git
cd thermal-camera
```

---

### Step 2: Install System Dependencies

Install the required libraries and dependencies:

```bash
sudo apt update
sudo apt install -y build-essential cmake libusb-1.0-0-dev libjpeg-dev python3-pip libgtk2.0-dev libgtk-3-dev python3-opencv
```

---

### Step 3: Clone and Build `libuvc`

Clone the `libuvc` repository and build it on your machine:

```bash
git clone https://github.com/groupgets/libuvc.git
cd libuvc
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```

**Expected result:** The `make` command should complete without errors, showing output like:

```
[100%] Built target uvc
```

---

### Step 4: Activate the Virtual Environment

A virtual environment has already been created in the `file` directory of this repository. To activate it, run:

```bash
cd file
source thermcam/bin/activate
```

This ensures all dependencies are properly installed and isolated for this project.

---

## Running the Final Project

### Step 5: Run the Final Script

The main script for the project is `uvc-radiometry-celsius.py`. Navigate to the directory and activate the environment before running:

```bash
cd file
source thermcam/bin/activate
sudo python3 uvc-radiometry-celsius.py
```

**Expected result:**

- The thermal image will be displayed in real-time.
- The hottest and coldest points will be highlighted in **red** and **blue**, respectively.
- Their temperatures will be displayed in white.
- A color bar on the right will indicate the temperature range.

Press `q` to exit the program.

---

## Troubleshooting

### **Issue: **

1. Ensure the camera is properly connected.
2. Verify detection with:
   ```bash
   ls /dev/video*
   ```

If no device appears, check the USB connection.

---

### **Issue: OpenCV Errors**

If you encounter errors like:

- *The function is not implemented.*
- *Cannot query video position.*

Ensure OpenCV is installed via:

```bash
sudo apt update
sudo apt install python3-opencv
```

---

## Repository Structure

```
thermal-camera-project/
├── README.md                   # Documentation
├── LICENSE                     # License information
├── file/                       # Main directory for scripts and virtual environment
│   ├── thermcam/               # Virtual environment for the project
│   ├── uvc-deviceinfo.py       # Camera info script
│   ├── uvc-radiometry.py       # Basic thermal data stream
│   └── uvc-radiometry-celsius.py # Final project script
```

---


## Example Output

The final thermal video includes:

- **Real-time thermal visualization**.
- **Hottest (red)** and **coldest (blue)** points highlighted.
- A **color bar** on the right showing the temperature range:

![Screenshot from 2025-01-21 21-12-05](https://github.com/user-attachments/assets/4d4faacb-536e-4c89-9e9b-58b748790e7e)


---

## Credits

- [libuvc](https://github.com/groupgets/libuvc)
- [OpenCV](https://opencv.org/)

## Authors
  - [Clarrainl](https://github.com/Clarrainl)
  - [j-albo](https://github.com/j-albo)
  - [Mauweberla](https://github.com/Mauweberla)


<!--  DO NOT REMOVE
-->
#### Acknowledgements

- Creation of GitHub template: [Marita Georganta](https://www.linkedin.com/in/marita-georganta/) - Robotic Sensing Expert
- Creation of MRAC-IAAC GitHub Structure: [Huanyu Li](https://www.linkedin.com/in/huanyu-li-457590268/) - Robotic Researcher


