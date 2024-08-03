import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

# Initialize emotion count dictionary
if 'emotion_counts' not in st.session_state:
    st.session_state.emotion_counts = {
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
    cap = cv2.VideoCapture(0)  # Capture video from the default webcam (index 0)

    stframe = st.empty()
    chart_placeholder = st.empty()

    # Get the absolute path to the Haar cascade file
    cascade_file = 'haarcascade_frontalface_default.xml'

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_file)

    while st.session_state.capturing:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture video")
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in faces:
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 26), 3)

            # Extract the face region
            face_region = frame[y:y + h, x:x + w]
            face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)

            try:
                # Analyze emotions for the face region
                analyze = DeepFace.analyze(face_region_rgb, actions=['emotion'], enforce_detection=False)

                # Get the dominant emotion
                dominant_emotion = analyze[0]['dominant_emotion']

                # Update emotion count
                st.session_state.emotion_counts[dominant_emotion] += 1

                # Display the dominant emotion text
                cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 26), 3)

            except Exception as e:
                st.write("Error in analyzing face region:", e)
                pass

        # Display the processed frame in Streamlit
        stframe.image(frame, channels="BGR")

        # Update the chart dynamically
        chart_placeholder.bar_chart(st.session_state.emotion_counts)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


st.title("Facial Attribute Analysis Software")
st.write("Local Version")

# Initialize session state for capturing
if 'capturing' not in st.session_state:
    st.session_state['capturing'] = False

# Display the emotion counts
# st.line_chart(st.session_state.emotion_counts)

# Define start and stop buttons
if st.button('Start'):
    st.session_state.capturing = True
    video_capture()

if st.button('Stop'):
    st.session_state.capturing = False
