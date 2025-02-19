#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uvctypes import *
import time
import cv2
import numpy as np
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import platform

BUF_SIZE = 2
q = Queue(BUF_SIZE)

def py_frame_callback(frame, userptr):
    array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
    data = np.frombuffer(
        array_pointer.contents, dtype=np.dtype(np.uint16)
    ).reshape(
        frame.contents.height, frame.contents.width
    )  # no copy

    if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
        return

    if not q.full():
        q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def ktoc(val):
    """Converts Kelvin to Celsius."""
    return (val - 27315) / 100.0

def apply_thermal_color(data, min_abs_temp=-2, max_abs_temp=50):
    """Generates the thermal image without normalizing, based on absolute temperature range."""
    # Convert raw values to Celsius
    temp_celsius = ktoc(data)

    # Define min and max temperatures for color scaling
    min_temp = min_abs_temp  # Minimum temperature to be mapped (adjustable)
    max_temp = max_abs_temp  # Maximum temperature to be mapped (adjustable)

    # Clip temperature values to the defined rangels /dev/video*
    temp_celsius = np.clip(temp_celsius, min_temp, max_temp)

    # Convert temperature values to 8-bit grayscale (0-255 range)
    img_gray = np.uint8(255 * (temp_celsius - min_temp) / (max_temp - min_temp))

    # Apply thermal colormap
    img_color = cv2.applyColorMap(img_gray, cv2.COLORMAP_VIRIDIS)

    return img_color

def add_colorbar(img, min_abs_temp=-50, max_abs_temp=100):
    """Adds a color bar on the right side of the image with fixed temperature values."""
    height, width, _ = img.shape
    colorbar_width = 50  # Width of the color bar

    # Create a vertical gradient
    gradient = np.linspace(255, 0, height, dtype=np.uint8).reshape((height, 1))
    colorbar = cv2.applyColorMap(gradient, cv2.COLORMAP_VIRIDIS)

    # Resize and append the color bar to the image
    colorbar = cv2.resize(colorbar, (colorbar_width, height))
    img_with_bar = np.hstack((img, colorbar))

    # Add text for constant min and max temperature values
    cv2.putText(img_with_bar, f"{max_abs_temp:.1f}C", (width + 10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 225, 0), 1)
    cv2.putText(img_with_bar, f"{min_abs_temp:.1f}C", (width + 10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 15, 192), 1)

    return img_with_bar


def display_temperature(img, val_k, loc, color=(255, 255, 255)):
    """Displays the temperature in Celsius at the highlighted points with white text."""
    val = ktoc(val_k)
    cv2.putText(img, "{0:.1f}C".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    x, y = loc
    cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
    cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

def main():
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    ctrl = uvc_stream_ctrl()

    res = libuvc.uvc_init(byref(ctx), 0)
    if res < 0:
        print("uvc_init error")
        exit(1)

    try:
        res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
        if res < 0:
            print("uvc_find_device error")
            exit(1)

        try:
            res = libuvc.uvc_open(dev, byref(devh))
            if res < 0:
                print("uvc_open error")
                exit(1)

            print("Device opened!")

            print_device_info(devh)
            print_device_formats(devh)

            frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
            if len(frame_formats) == 0:
                print("Device does not support Y16")
                exit(1)

            libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
                frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
            )

            res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
            if res < 0:
                print("uvc_start_streaming failed: {0}".format(res))
                exit(1)

            try:
                while True:
                    data = q.get(True, 500)
                    if data is None:
                        break
                    data = cv2.resize(data[:, :], (640, 480))
                    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
                    img = apply_thermal_color(data)  # Generate thermal image
                    display_temperature(img, minVal, minLoc)
                    display_temperature(img, maxVal, maxLoc)
                    img_with_bar = add_colorbar(img, min_abs_temp=-50, max_abs_temp=100)
                    cv2.imshow('Lepton Radiometry with Highlights and Colorbar', img_with_bar)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("Exiting program...")
                        break

                cv2.destroyAllWindows()
            finally:
                libuvc.uvc_stop_streaming(devh)
        finally:
            libuvc.uvc_unref_device(dev)
    finally:
        libuvc.uvc_exit(ctx)

if __name__ == '__main__':
    main()