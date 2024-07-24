import tkinter as tk
import customtkinter
from tkinter import Frame, RAISED, Button, messagebox, Label, ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os
import numpy as np

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

# Store true labels and predicted scores for each emotion
true_labels = {emotion: [] for emotion in emotion_counts.keys()}
predicted_scores = {emotion: [] for emotion in emotion_counts.keys()}


def analyze_video(source):
    global emotion_counts, true_labels, predicted_scores
    # Reset emotion counts and data storage
    for key in emotion_counts.keys():
        emotion_counts[key] = 0
        true_labels[key] = []
        predicted_scores[key] = []

    # Update the chart
    update_chart()

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
            print("No faces detected in the frame.")
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

                        # Store true labels and predicted scores for ROC curve
                        for emotion, score in analyze[0]['emotion'].items():
                            true_labels[emotion].append(1 if emotion == dominant_emotion else 0)
                            predicted_scores[emotion].append(score)

                        if language_reference == "Spanish":
                            if dominant_emotion == "happy".casefold():
                                dominant_emotion = "Feliz"
                            elif dominant_emotion == "sad".casefold():
                                dominant_emotion = "Triste"
                            elif dominant_emotion == "angry".casefold():
                                dominant_emotion = "Enojada"
                            elif dominant_emotion == "surprise".casefold():
                                dominant_emotion = "Sorpresa"
                            elif dominant_emotion == "disgust".casefold():
                                dominant_emotion = "Asco"
                            elif dominant_emotion == "fear".casefold():
                                dominant_emotion = "Miedo"
                            else:
                                dominant_emotion = "Neutral"

                        # Display the dominant emotion text
                        cv2.putText(frame, dominant_emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 26), 3)

                    # Update the chart and ROC curve
                    update_chart()
                    update_roc_curve()
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

        # Check for key press
        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' key to exit
            break

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def calculate_roc(true_labels, predicted_scores):
    thresholds = sorted(set(predicted_scores), reverse=True)
    tpr_list = []
    fpr_list = []
    for thresh in thresholds:
        tp = fp = tn = fn = 0
        for true, score in zip(true_labels, predicted_scores):
            if score >= thresh:
                if true == 1:
                    tp += 1
                else:
                    fp += 1
            else:
                if true == 1:
                    fn += 1
                else:
                    tn += 1
        tpr = tp / (tp + fn) if (tp + fn) != 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) != 0 else 0
        tpr_list.append(tpr)
        fpr_list.append(fpr)
    return fpr_list, tpr_list


def update_chart():
    # Clear the axis
    axis1.clear()

    # Update the bar chart
    axis1.bar(emotion_counts.keys(), emotion_counts.values(), color=pry_color)

    # Redraw the canvas
    canvas.draw()


def update_roc_curve():
    axis2.clear()
    for emotion in emotion_counts.keys():
        if len(true_labels[emotion]) > 0 and len(predicted_scores[emotion]) > 0:
            fpr, tpr = calculate_roc(true_labels[emotion], predicted_scores[emotion])
            axis2.plot(fpr, tpr, lw=2, label=emotion)
    axis2.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    axis2.set_xlim([0.0, 1.0])
    axis2.set_ylim([0.0, 1.05])
    axis2.set_xlabel('False Positive Rate')
    axis2.set_ylabel('True Positive Rate')
    axis2.set_title('Receiver Operating Characteristic')
    axis2.legend(loc="lower right")
    canvas.draw()


def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        analyze_video(file_path)


def analyze_webcam():
    analyze_video("webcam")


pry_color = "#514AF5"
sec_color = "#DDDCF2"
_2nd_bgcolor = "white"

# --------------------------------------------------------------
fig = Figure(figsize=(6.5, 4), facecolor=_2nd_bgcolor, tight_layout=True)
axis1 = fig.add_subplot(211)
axis2 = fig.add_subplot(212)
axis1.bar(emotion_counts.keys(), emotion_counts.values(), color=pry_color)
axis1.grid(linestyle='-')  # solid grid lines

# UI Implementation
root = tk.Tk()
root.title("Facial Attribute Analysis Software v.0.2")
root.iconbitmap("fr.ico")
root.geometry("1080x600")
root.resizable(0, 0)

# left frame
left_frame = Frame(root, width=360, height=600, bg="white",
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
right_frame = Frame(root, width=700, height=600, bg="white",
                    relief=RAISED, borderwidth=0)
right_frame.place(x=380, y=0)

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().place(x=20, y=20, width=660, height=460)

# Combobox for language reference
app_info = Label(master=right_frame, text="Language Preference", bg="white")
app_info.place(x=20, y=490)

language = tk.StringVar()
language_ref = ttk.Combobox(master=right_frame, width=12, textvariable=language, state="readonly")
language_ref.place(x=20, y=520)
language_ref["values"] = ("English", "Spanish")
language_ref.current(0)

# statistical analysis
total_feed_time = Label(right_frame, text="Live Time: 2:00", bg=_2nd_bgcolor)
total_feed_time.place(x=20, y=570)

max_emotion = Label(right_frame, text="Most detected Emotion: Angry", bg=_2nd_bgcolor)
max_emotion.place(x=400, y=570)

ROC_curve_label = Label(right_frame, text="ROC Curve: Updated", bg=_2nd_bgcolor)
ROC_curve_label.place(x=20, y=600)

total_detected_emotions = Label(right_frame, text="Emotion: 46", bg=_2nd_bgcolor)
total_detected_emotions.place(x=400, y=600)

root.mainloop()
