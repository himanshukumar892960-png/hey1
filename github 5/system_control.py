try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

import os
import subprocess

class SystemControl:
    def take_screenshot(self, filename="screenshot.png"):
        if not HAS_PYAUTOGUI:
            return "Screenshot functionality is not available in this environment."
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return filename
        except Exception as e:
            return f"Error taking screenshot: {e}"

    def open_app(self, app_name):
        try:
            # Simple implementation for Windows
            subprocess.Popen(f"start {app_name}", shell=True)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

    def capture_camera(self, filename="camera.jpg"):
        if not HAS_CV2:
            return "Camera capture is currently unavailable in this environment."
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
            cap.release()
            return filename
        cap.release()
        return "Failed to capture image"

    def get_screen_info(self):
        if not HAS_PYAUTOGUI:
            return "Screen info not available"
        return str(pyautogui.size())
