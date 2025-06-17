# ✅ detect.py — Main detection logic
import cv2
import mediapipe as mp
import datetime
import os
import csv
import pyttsx3

# Init speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Init face detection
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Logging function
def log_event(event):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, event])

speak("Initializing cheating detection. Please stay centered and alone.")

while True:
    success, frame = cap.read()
    if not success:
        break

    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(rgb_frame)

    if result.detections:
        num_faces = len(result.detections)

        if num_faces > 1:
            log_event("Multiple faces detected")
            speak("Warning! Multiple people detected. You are disqualified.")
            filename = f"screenshots/multiple_{datetime.datetime.now().strftime('%H%M%S')}.png"
            cv2.imwrite(filename, frame)

        for detection in result.detections:
            bbox = detection.location_data.relative_bounding_box
            x, y, w_box, h_box = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)
            cx = x + w_box // 2

            # Determine face position
            if cx < w * 0.3:
                position = "Left"
            elif cx > w * 0.7:
                position = "Right"
            else:
                position = "Center"

            if position != "Center":
                log_event(f"Face at {position}")
                speak(f"Warning. Your face is too much to the {position}. Please look at center.")
                filename = f"screenshots/face_{position}_{datetime.datetime.now().strftime('%H%M%S')}.png"
                cv2.imwrite(filename, frame)

            # Draw box
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (0, 255, 0), 2)
            cv2.putText(frame, position, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    else:
        log_event("No face detected")
        speak("No face detected. Please stay in camera view.")
        filename = f"screenshots/noface_{datetime.datetime.now().strftime('%H%M%S')}.png"
        cv2.imwrite(filename, frame)

    cv2.imshow("Cheating Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
