import tkinter as tk
import threading
import time
from tkinter import Frame, RAISED, Button, messagebox, Label, ttk, filedialog, Canvas, LabelFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os

# Initialize emotion count dictionary
emotion_counts = {
    "neutral": 0,
    "angry": 0,
    "fear": 0,
    "disgust": 0,
    "happy": 0,
    "sad": 0,
    "surprise": 0
}

# Function for video analysis
def analyze_video_thread(source):
    global emotion_counts

    start_time = time.time()

    # Load the face cascade classifier
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_file = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_file)

    if source == "webcam":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to access webcam")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            continue
        else:
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 26), 3)
                face_region = frame[y:y + h, x:x + w]

                try:
                    analyze = DeepFace.analyze(face_region, actions=['emotion'])
                    if 'dominant_emotion' in analyze[0]:
                        dominant_emotion = analyze[0]['dominant_emotion']
                        emotion_counts[dominant_emotion] += 1
                except:
                    pass

        # Display the processed frame or update UI as needed

        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Function for updating the chart
def update_chart_thread():
    while True:
        update_chart()
        time.sleep(1)  # Update the chart every 1 second

# Function to start video analysis thread
def start_analysis_thread(source):
    analysis_thread = threading.Thread(target=analyze_video_thread, args=(source,))
    analysis_thread.daemon = True  # Daemonize the thread to stop with the main program
    analysis_thread.start()

# Function to start chart update thread
def start_chart_thread():
    chart_thread = threading.Thread(target=update_chart_thread)
    chart_thread.daemon = True  # Daemonize the thread to stop with the main program
    chart_thread.start()

# UI Implementation
root = tk.Tk()
root.title("Facial Attribute Analysis Software")
root.geometry("1080x600")

# Create UI components and layout (left_frame, right_frame, etc.)

# Start the threads for video analysis and chart update
start_analysis_thread("webcam")  # Example for webcam, adjust as needed
start_chart_thread()

root.mainloop()
