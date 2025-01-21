
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
sudo apt install -y build-essential cmake libusb-1.0-0-dev libjpeg-dev libopencv-dev python3-pip libgtk2.0-dev libgtk-3-dev python3-venv
```

---

### Step 3: Activate the Virtual Environment

A virtual environment has already been created in the `python` directory of this repository. To activate it, run:

```bash
cd purethermal1-uvc-capture/python
source thermcam/bin/activate
```

This ensures all dependencies are properly installed and isolated for this project.

---

### Step 4: Use Included `libuvc`

The `libuvc` library is already included in this repository. You do not need to clone or build it separately. The precompiled version is ready to use.

If needed, you can rebuild it by navigating to the `libuvc` directory:

```bash
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

## Preliminary Exercises

### **Exercise 1: Verify Camera Connection**

Connect your PureThermal 2 to the computer via USB. Verify the system detects it as a video device:

```bash
ls /dev/video*
```

**Expected result:** If the camera is correctly connected, you should see something like:

```
/dev/video0
```

If no device appears:

- Check the USB connection.
- Ensure the cable is functioning.
- Restart your computer and retry the command.

---

### **Exercise 2: Test the Camera with `guvcview`**

Use `guvcview` to ensure the camera is working properly:

1. Install `guvcview`:
   ```bash
   sudo apt install guvcview
   ```
2. Run `guvcview`:
   ```bash
   guvcview
   ```

In the `guvcview` interface:

- Select the correct video device (e.g., `/dev/video0`).
- You should see the thermal image output.

**Note:** If no image appears, ensure the correct device is selected.

---

### **Exercise 3: Run `uvc-deviceinfo.py`**

Navigate to the `python` directory in the repository and activate the virtual environment by running:

```bash
cd purethermal1-uvc-capture/python
source thermcam/bin/activate
sudo python3 uvc-deviceinfo.py
```

**Expected result:** The script should display details about the camera, such as:

```
Version gpp: 3.3.26 dsp: 3.3.26
FLIR part #: b'500-0771-01'
FLIR serial #: b'^F'
```

---

### **Exercise 4: Test Basic Thermal Streaming**

Run the `uvc-radiometry.py` script to verify the thermal data stream. Navigate to the directory and activate the environment first:

```bash
cd purethermal1-uvc-capture/python
source thermcam/bin/activate
sudo python3 uvc-radiometry.py
```

**Expected result:** A window should open showing the thermal image in grayscale. If the data stream works correctly, you can proceed to the final project.

---

## Running the Final Project

### Step 5: Run the Final Script

The main script for the project is `uvc-radiometry-celsius.py`. Navigate to the directory and activate the environment before running:

```bash
cd purethermal1-uvc-capture/python
source thermcam/bin/activate
sudo python3 uvc-radiometry-celsius.py
```

**Expected result:**

- The thermal image will be displayed in real-time.
- The hottest and coldest points will be highlighted in **red** and **blue**, respectively.
- Their temperatures will be displayed in white.
- A color bar on the right will indicate the temperature range.

Press **`q`** to exit the program.

---

## Troubleshooting

### **Issue: `uvc_open error`**

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

Install the necessary GTK dependencies:

```bash
sudo apt install libgtk2.0-dev libgtk-3-dev
```

---

## Repository Structure

```
thermal-camera-project/
├── README.md                   # Documentation
├── LICENSE                     # License information
├── purethermal1-uvc-capture/   # Main directory for scripts and files
│   ├── README_original.md      # Original README from the PureThermal repository
│   ├── python/                 # Python scripts for thermal imaging
│   │   ├── thermcam/           # Virtual environment for the project
│   │   ├── uvc-deviceinfo.py   # Camera info script
│   │   ├── uvc-radiometry.py   # Basic thermal data stream
│   │   └── uvc-radiometry-celsius.py # Final project script
│   └── libuvc/                 # Library for camera communication
```

---

## Example Output

The final thermal video includes:

- **Real-time thermal visualization**.
- **Hottest (red)** and **coldest (blue)** points highlighted.
- A **color bar** on the right showing the temperature range:

![Thermal Camera Example](https://via.placeholder.com/800x400?text=Thermal+Camera+Example)

---

## Credits

- [libuvc](https://github.com/groupgets/libuvc)
- [OpenCV](https://opencv.org/)
- [purethermal1-uvc-capture](https://github.com/groupgets/purethermal1-uvc-capture)

## Authors
  - [Name](insert linkedin/webpage link) - role

## References
- [K. Albee et al., “A robust observation, planning, and control pipeline for autonomous rendezvous with tumbling targets,” Frontiers in Robotics and AI, vol. 8, p. 234, 2021, doi: 10.3389/frobt.2021.641338.](https://www.frontiersin.org/articles/10.3389/frobt.2021.641338/full)

## Credits
  - [Name](insert linkedin/webpage link) - role

<!--  DO NOT REMOVE
-->
#### Acknowledgements

- Creation of GitHub template: [Marita Georganta](https://www.linkedin.com/in/marita-georganta/) - Robotic Sensing Expert
- Creation of MRAC-IAAC GitHub Structure: [Huanyu Li](https://www.linkedin.com/in/huanyu-li-457590268/) - Robotic Researcher


