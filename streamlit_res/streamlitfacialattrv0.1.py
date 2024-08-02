import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoProcessorBase
import av
import cv2
import numpy as np
import os
from deepface import DeepFace


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


# Define a function to capture video from the webcam
def video_capture():
    global emotion_counts
    cap = cv2.VideoCapture(0)  # Capture video from the default webcam (index 0)

    stframe = st.empty()

    # Get the absolute path to the Haar cascade file to be used during packaging
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cascade_file = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cascade_file)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video")
            break

        # Apply some processing to the frame (example: brighten the image)
        # matrix = np.ones(frame.shape, dtype="uint8") * 100
        # b_frame = cv2.add(frame, matrix)

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

                    # Check if emotions are detected
                    if 'dominant_emotion' in analyze[0]:
                        # Get the dominant emotion
                        dominant_emotion = analyze[0]['dominant_emotion']

                        # Update emotion count
                        emotion_counts[dominant_emotion] += 1

                        # if language_reference == "Spanish":
                        #     dominant_emotion = emotion_translations.get(dominant_emotion, dominant_emotion)

                        # Display the dominant emotion text
                        cv2.putText(frame, dominant_emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 26), 3)

                    # # Update the chart
                    # update_chart()

                except:
                    pass
                    # messagebox.showerror("Error", "Analysis Error")

        # Display the processed frame in Streamlit
        stframe.image(frame, channels="BGR")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


st.title("Facial Attribute Analysis Software")
st.write("Local Version")

# Initialize session state for capturing
if 'capturing' not in st.session_state:
    st.session_state['capturing'] = False

# Define start and stop buttons
if st.button('Start'):
    st.session_state['capturing'] = True
    video_capture()

if st.button('Stop'):
    st.session_state['capturing'] = False
