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


# functional
def analyze_video(source):
    global emotion_counts

    start_time = time.time()

    # Load the face cascade classifier
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # for keys in emotion_counts.keys():
    #     emotion_counts[keys] = 0

    # Get the absolute path to the Haar cascade file to be used during packaging
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_file = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cascade_file)

    if source == "webcam":
        # Open the webcam
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(source)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed to access webcam")
        return

    # Get the frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('analysed_vid.mp4', fourcc, 10.0, (frame_width, frame_height))

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
            # print("No faces detected in the frame.")
            continue
        else:
            # Iterate over detected faces
            for x, y, w, h in faces:
                # Draw rectangle around the face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 26), 3)

                # Extract the face region
                face_region = frame[y:y + h, x:x + w]

                try:
                    # Analyze emotions for the face region
                    analyze = DeepFace.analyze(face_region, actions=['emotion'])

                    # language translation
                    language_reference = language.get()

                    # Check if emotions are detected
                    if 'dominant_emotion' in analyze[0]:
                        # Get the dominant emotion
                        dominant_emotion = analyze[0]['dominant_emotion']
                        # Update emotion count
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

                    # Update the chart
                    update_chart()
                except:
                    pass

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


def update_chart():
    # Clear the axis
    axis1.clear()

    # Update the bar chart
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
root.resizable(0, 0)
# root.attributes('-fullscreen', True)
# root.overrideredirect(True)
# config
frame_width = 360
frame_height = 600

# left frame
left_frame = Frame(root, width=frame_width, height=frame_height, bg="white",
                   relief=RAISED, borderwidth=0)
left_frame.place(x=0, y=0)

video_feed = Label(left_frame, width=44, height=30, bg="#C9C9C9")
video_feed.place(x=20, y=20)

# App buttons
upload_btn = customtkinter.CTkButton(
    master=left_frame,
    width=320,
    height=40,
    text="Upload Video File",
    fg_color=sec_color,
    bg_color=pry_color,
    text_color="black",
    command=upload_video
)

upload_btn.place(x=20, y=490)

save_feed = customtkinter.CTkButton(
    master=left_frame,
    width=320,
    height=40,
    text="Start Live Feed",
    fg_color=pry_color,
    command=analyze_webcam
)

save_feed.place(x=20, y=542)

# right frame
right_frame = Frame(root, width=700, height=frame_height, bg="white",
                    relief=RAISED, borderwidth=0)
right_frame.place(x=380, y=0)

canvas = FigureCanvasTkAgg(fig, master=right_frame, )
canvas.draw()
# canvas.get_tk_widget().place(x=400, y=20, width=660, height=460)
canvas.get_tk_widget().place(x=20, y=20, width=660, height=600)
# canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

# Combobox for language reference
app_info = Label(
    master=right_frame,
    text="Language Preference",
    bg="white"
)
app_info.place(x=20, y=370)

language = tk.StringVar()
language_ref = ttk.Combobox(
    master=right_frame,
    width=12,
    textvariable=language,
    state="readonly"
)
# language_ref = customtkinter.CTkComboBox(master=right_frame, width=12, textvariable=language)
language_ref.place(x=20, y=400)
language_ref["values"] = "English Spanish"
language_ref.current(0)

# statistical analysis
# analytics_box = LabelFrame(right_frame, text="Statistical Sumarization")
# analytics_box.place(x=20, y=490)

total_feed_time = Label(
    right_frame,
    text="Live Time: 00:00",
    bg=_2nd_bgcolor,
    font=('Arial bold', 10)
)
total_feed_time.place(x=20, y=490)

max_emotion = Label(
    right_frame,
    text="Most detected Emotion: Angry",
    bg=_2nd_bgcolor,
    font=('Arial bold', 10),
)
max_emotion.place(x=400, y=490)

# ROC_curve = Label(
#     right_frame,
#     text="ROC Curve: 1.29",
#     bg=_2nd_bgcolor,
#     font=('Arial bold', 10),
# )
# ROC_curve.place(x=20, y=540)

total_detected_emotions = Label(
    right_frame,
    font=('Arial bold', 10),
    text="Total Emotions Detected: 0",
    bg=_2nd_bgcolor
)
total_detected_emotions.place(x=400, y=540)

root.mainloop()
