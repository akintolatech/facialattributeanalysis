import tkinter as tk
from tkinter import Frame, RAISED, Button, messagebox, Label, ttk, filedialog
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
from deepface.extendedmodels import Emotion
import os


def analyze_video(source):

    # Load the face cascade classifier
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

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


def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        analyze_video(file_path)


def analyze_webcam():
    analyze_video("webcam")


# UI Implementation
root = tk.Tk()
root.title("Facial Recognition")
#root.iconbitmap("fr.ico")
root.geometry("740x500")
root.resizable(0, 0)

# config
frame_width = 360
frame_height = 500
btn_color = "#514AF5"
sec_color = "#DDDCF2"

# left frame
left_frame = Frame(root, width=frame_width, height=frame_height, bg="white",
                   relief=RAISED, borderwidth=0)

video_feed = Label(left_frame, width=44, height=30, bg="#C9C9C9")
video_feed.place(x=20, y=20)

left_frame.place(x=0, y=0)

# right frame
right_frame = Frame(root, width=frame_width, height=frame_height, bg="white",
                    relief=RAISED, borderwidth=0)
right_frame.place(x=380, y=0)

app_info = Label(
    master=right_frame,
    text="Language Preference",
    bg="white"
)
app_info.place(x=20, y=270)

# Combobox for language reference
language = tk.StringVar()
language_ref = ttk.Combobox(master=right_frame, width=12, textvariable=language, state="readonly")
# language_ref = customtkinter.CTkComboBox(master=right_frame, width=12, textvariable=language)
language_ref["values"] = "English Spanish"
language_ref.current(0)
language_ref.place(x=20, y=300)

# App buttons
upload_btn = Button(
    master=right_frame,
    width=44,
    height=2,
    text="Upload Video File",
    bg=sec_color,
    fg="black",
    # fg_color="red",
    command=upload_video
)

upload_btn.place(x=20, y=376)

save_feed = Button(
    master=right_frame,
    width=44,
    height=2,
    text="Start Emotion Analysis",
    bg=btn_color,
    fg="white",
    command=analyze_webcam,
)

save_feed.place(x=20, y=436)

root.mainloop()
