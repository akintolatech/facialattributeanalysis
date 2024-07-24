import threading
import tkinter as tk
import customtkinter
from tkinter import Frame, RAISED, Button, messagebox, Label, ttk, filedialog, Canvas, LabelFrame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
# from deepface.extendedmodels import Emotion
import os
import time

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

# Lock for thread-safe updates
emotion_counts_lock = threading.Lock()


def analyze_video(source):
    global emotion_counts

    start_time = time.time()

    # Get the absolute path to the Haar cascade file to be used during packaging
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_file = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cascade_file)

    if source == "webcam":
        # Open the webcam using DirectShow backend
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(source)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to access webcam or video source")
        return

    # Get the frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('analysed_vid.mp4', fourcc, 10.0, (frame_width, frame_height))

    def process_frame():
        while True:
            # Read a frame from the webcam
            ret, frame = cap.read()

            # Check if the frame is read successfully
            if not ret:
                break

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            # Check if any faces are detected
            if len(faces) == 0:
                continue
            else:
                # Iterate over detected faces
                for x, y, w, h in faces:
                    # Draw rectangle around the face
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 26), 3)

                    # Extract the face region
                    face_region = frame[y:y + h, x:x + w]

                    # Start a new thread for emotion analysis
                    threading.Thread(target=analyze_frame, args=(frame, face_region, x, y)).start()

            # Write the frame into the output video
            out.write(frame)

            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to an ImageTk object
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)

            # Update the video feed label with the new frame
            video_feed.imgtk = img
            video_feed.configure(image=img, width=318, height=456)

            # Refresh the video feed label
            video_feed.update()

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            elapsed_minutes = int(elapsed_time // 60)
            elapsed_seconds = int(elapsed_time % 60)
            total_feed_time.config(text=f"Live Time: {elapsed_minutes:02d}:{elapsed_seconds:02d}")

            # Check for key press
            key = cv2.waitKey(1)
            if key == 27:  # Press 'Esc' key to exit
                break

        # Release everything when done
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # Start the frame processing in a new thread
    threading.Thread(target=process_frame).start()


def analyze_frame(frame, face_region, x, y):
    global emotion_counts

    try:
        # Analyze emotions for the face region
        analyze = DeepFace.analyze(face_region, actions=['emotion'])

        # language translation
        language_reference = language.get()

        # Check if emotions are detected
        if 'dominant_emotion' in analyze[0]:
            # Get the dominant emotion
            dominant_emotion = analyze[0]['dominant_emotion']

            # Lock the dictionary for thread-safe updates
            with emotion_counts_lock:
                emotion_counts[dominant_emotion] += 1

            if language_reference == "Spanish":
                if dominant_emotion == "happy".casefold():
                    dominant_emotion = "Feliz"
                elif dominant_emotion == "sad".casefold():
                    dominant_emotion = "Triste"
                elif dominant_emotion == "angry".casefold():
                    dominant_emotion = "Enojada"
                elif dominant_emotion == "surprise".casefold():
                    dominant_emotion = "Sorpresa"
                elif dominant_emotion == "disgusting".casefold():
                    dominant_emotion = "Asco"
                elif dominant_emotion == "fear".casefold():
                    dominant_emotion = "Miedo"
                else:
                    dominant_emotion = "Neutral"

            # Display the dominant emotion text
            cv2.putText(frame, dominant_emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 26), 3)

    except Exception as e:
        print(f"Error analyzing frame: {e}")


def update_chart():
    # Clear the axis
    axis1.clear()

    # Update the bar chart
    with emotion_counts_lock:
        axis1.bar(emotion_counts.keys(), emotion_counts.values(), color=pry_color)

    # Redraw the canvas
    canvas.draw()

    # update statistical variables
    total_detected_emotions_variable = sum(emotion_counts.values())
    total_detected_emotions.config(text=f"Total Emotions Detected: {total_detected_emotions_variable}")

    if total_detected_emotions_variable > 0:
        max_emotion_variable = max(emotion_counts, key=emotion_counts.get)
        max_emotion.config(text=f"Most Detected Emotion: {max_emotion_variable}")


def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        analyze_video(file_path)


def analyze_webcam():
    analyze_video("webcam")


pry_color = "#514AF5"
sec_color = "#DDDCF2"

_2nd_bgcolor = "white"

#--------------------------------------------------------------
fig = Figure(figsize=(6.5, 4), facecolor=_2nd_bgcolor, tight_layout=True)
# xValues = ["Neutral", "Angry", "Fear", "Disgust", "Happy", "Sad", "Angry"]
# yValues = [neutral_count, 7, 6, 8, 5, 6, 7]
#--------------------------------------------------------------
axis1 = fig.add_subplot(211)
# axis2 = fig.add_subplot(222, sharex=axis1, sharey=axis1)
# axis3 = fig.add_subplot(223, sharex=axis1, sharey=axis1)
# axis4 = fig.add_subplot(224, sharex=axis1, sharey=axis1)
#--------------------------------------------------------------
# axis1.plot(xValues, yValues)
# axis1.bar(xValues, yValues, color=pry_color, )
with emotion_counts_lock:
    axis1.bar(emotion_counts.keys(), emotion_counts.values(), color=pry_color)
# axis1.set_xlabel('Emotions')
# axis1.set_ylabel('Frequency')
axis1.grid(linestyle='-')  # solid grid lines
#--------------------------------------------------------------


# UI Implementation
root = tk.Tk()
root.title("Facial Attribute Analysis Software v.0.2")
root.iconbitmap("fr.ico")
root.geometry("1080x600")
# root.resizable(0, 0)
# root.attributes('-fullscreen', True)
# root.overrideredirect(True)
# config
frame_width = 360
frame_height = 480

#------------------------------------#---------------------------------------
#------------------------------------#---------------------------------------
frame1 = tk.Frame(root, bg=_2nd_bgcolor, width=frame_width, height=frame_height, highlightthickness=3, highlightbackground=sec_color)
frame1.grid(row=0, column=0, padx=10, pady=20)
#------------------------------------#---------------------------------------
frame2 = tk.Frame(root, bg=_2nd_bgcolor, width=frame_width, height=frame_height, highlightthickness=3, highlightbackground=sec_color)
frame2.grid(row=0, column=1, padx=10, pady=20)
#------------------------------------#---------------------------------------
frame3 = tk.Frame(root, bg=_2nd_bgcolor, width=frame_width, height=frame_height, highlightthickness=3, highlightbackground=sec_color)
frame3.grid(row=0, column=2, padx=10, pady=20)
#------------------------------------#---------------------------------------
chart = tk.LabelFrame(frame1, text="Emotional Analysis Graph", fg=pry_color, bg=_2nd_bgcolor, width=frame_width - 20, height=frame_height - 40)
chart.place(x=5, y=5)
#------------------------------------#---------------------------------------
canvas = FigureCanvasTkAgg(fig, chart)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
# canvas.draw()
#------------------------------------#---------------------------------------
statistical_info = tk.LabelFrame(frame2, text="Statistical Information", fg=pry_color, bg=_2nd_bgcolor, width=frame_width - 20, height=frame_height - 40)
statistical_info.place(x=5, y=5)
#------------------------------------#---------------------------------------
total_detected_emotions = tk.Label(statistical_info, text="Total Emotions Detected: 0", bg=_2nd_bgcolor, fg=pry_color, font=("TkdefaultFont", 10))
total_detected_emotions.place(x=20, y=20)
#------------------------------------#---------------------------------------
max_emotion = tk.Label(statistical_info, text="Most Detected Emotion: None", bg=_2nd_bgcolor, fg=pry_color, font=("TkdefaultFont", 10))
max_emotion.place(x=20, y=60)
#------------------------------------#---------------------------------------
video_feed_canvas = tk.LabelFrame(frame3, text="Real-Time Video Feed", fg=pry_color, bg=_2nd_bgcolor, width=frame_width - 20, height=frame_height - 130)
video_feed_canvas.place(x=5, y=5)
#------------------------------------#---------------------------------------
video_feed = tk.Label(video_feed_canvas, bg=_2nd_bgcolor)
video_feed.place(x=0, y=0)
#------------------------------------#---------------------------------------
language_frame = tk.LabelFrame(frame3, text="Language Translation", fg=pry_color, bg=_2nd_bgcolor, width=frame_width - 20, height=100)
language_frame.place(x=5, y=325)
#------------------------------------#---------------------------------------
lang = tk.StringVar()
lang.set("English")
language = ttk.Combobox(language_frame, textvariable=lang, state="readonly", values=["English", "Spanish"], width=20)
language.place(x=20, y=5)
language.set("English")
#------------------------------------#---------------------------------------
total_feed_time = tk.Label(video_feed_canvas, text="Live Time: 00:00", bg=_2nd_bgcolor, fg=pry_color, font=("TkdefaultFont", 10))
total_feed_time.place(x=20, y=405)
#------------------------------------#---------------------------------------
button_frame = tk.LabelFrame(root, text="", fg=pry_color, bg=_2nd_bgcolor, width=1040, height=50)
button_frame.grid(row=1, column=0, columnspan=3, pady=10)
#------------------------------------#---------------------------------------
upload_video_button = customtkinter.CTkButton(button_frame, text="Upload Video", width=200, height=30, fg_color=pry_color, hover_color=sec_color, command=upload_video)
upload_video_button.place(x=200, y=5)
#------------------------------------#---------------------------------------
webcam_analysis_button = customtkinter.CTkButton(button_frame, text="Webcam Analysis", width=200, height=30, fg_color=pry_color, hover_color=sec_color, command=analyze_webcam)
webcam_analysis_button.place(x=600, y=5)
#------------------------------------#---------------------------------------
update_chart_button = customtkinter.CTkButton(button_frame, text="Update Chart", width=200, height=30, fg_color=pry_color, hover_color=sec_color, command=update_chart)
update_chart_button.place(x=1000, y=5)
#------------------------------------#---------------------------------------

root.mainloop()
