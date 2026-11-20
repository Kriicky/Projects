#!/usr/bin/env python3
"""
Webcam Focus Detector
Detects if a human is in front of the webcam and if they're focused on the computer.
If not focused, opens a local webpage with a noise and "get back to work" message.
"""

import cv2
import numpy as np
import subprocess
import time
import threading
from datetime import datetime

# Configuration
CAMERA_INDEX = 0
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
ALERT_URL = "http://127.0.0.1:5000/alert"
ALERT_COOLDOWN = 30  # seconds between alerts
FOCUS_THRESHOLD = 30  # degrees - if head turned more than this, not focused

class FocusDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
        self.last_alert_time = 0
        self.alert_active = False
        self.focus_score = 100  # 0-100, higher = more focused

    def detect_face(self, frame):
        """Detect face and estimate head orientation."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 0:
            return None, 0

        # Use the largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face

        # Estimate head orientation using face position in frame
        frame_center_x = frame.shape[1] // 2
        face_center_x = x + w // 2

        # Calculate horizontal offset (proxy for head turn)
        offset = face_center_x - frame_center_x
        # Normalize to -1 to 1 range
        normalized_offset = offset / (frame.shape[1] // 2)

        # Estimate rotation angle (simplified)
        rotation = normalized_offset * 60  # max ~60 degrees

        return face, rotation

    def calculate_focus(self, face, rotation):
        """Calculate focus score based on face position and orientation."""
        if face is None:
            return 0

        # Face not detected = not focused
        if face is None:
            return 0

        # More rotation = less focused
        abs_rotation = abs(rotation)
        if abs_rotation < 10:
            focus = 100
        elif abs_rotation < 20:
            focus = 80
        elif abs_rotation < 30:
            focus = 60
        elif abs_rotation < 40:
            focus = 40
        else:
            focus = 20

        return focus

    def should_alert(self, focus_score):
        """Determine if we should trigger an alert."""
        now = time.time()

        # Check cooldown
        if now - self.last_alert_time < ALERT_COOLDOWN:
            return False

        # Alert if focus is low
        if focus_score < 40:
            self.last_alert_time = now
            self.alert_active = True
            return True

        return False

    def trigger_alert(self):
        """Open the alert webpage."""
        try:
            subprocess.Popen(["xdg-open", ALERT_URL])
        except Exception as e:
            print(f"Error opening alert page: {e}")

    def process_frame(self, frame):
        """Process a single frame and return focus status."""
        face, rotation = self.detect_face(frame)
        focus = self.calculate_focus(face, rotation)
        self.focus_score = focus

        # Draw debug info
        cv2.putText(frame, f"Focus: {focus}%", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Rotation: {rotation:.1f}°", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if face is not None:
            x, y, w, h = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame, focus

def main():
    detector = FocusDetector()
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    print("Starting focus detector...")
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, focus = detector.process_frame(frame)

        # Check if we should alert
        if detector.should_alert(focus):
            print(f"Alert triggered at {datetime.now().strftime('%H:%M:%S')} - Focus: {focus}%")
            detector.trigger_alert()

        cv2.imshow("Focus Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Stopped focus detector")

if __name__ == "__main__":
    main()