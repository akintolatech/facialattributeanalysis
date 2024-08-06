"""
    Facial Attribute Analysis Software v0.4
    What's New
        More Performance optimization
        Export Analysis Data in Document and Excel
        Convert Chart Labels to Spanish
    All rights reserved Esteban Morales and Akintola Technologies @ 2024
"""

import streamlit as st
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from deepface import DeepFace

# Dictionary for emotion translations
emotion_translations = {
    "neutral": "Neutral",
    "angry": "Enojada",
    "fear": "Miedo",
    "disgust": "Asco",
    "happy": "Feliz",
    "sad": "Triste",
    "surprise": "Sorpresa"
}

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

st.title("Facial Attribute Analysis Software v0.4")
st.write("Web version")

def analyze_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) == 0:
        return frame, None

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face_region = frame[y:y + h, x:x + w]
        
        try:
            analyze = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
            if 'dominant_emotion' in analyze[0]:
                dominant_emotion = analyze[0]['dominant_emotion']
                emotion_counts[dominant_emotion] += 1
                cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        except:
            pass

    return frame, faces

def draw_bar_chart(emotion_counts, language="English"):
    emotions = list(emotion_counts.keys())
    counts = list(emotion_counts.values())

    if language == "Spanish":
        emotions = [emotion_translations[emotion] for emotion in emotions]

    plt.figure(figsize=(10, 6))
    plt.bar(emotions, counts, color='skyblue')
    plt.xlabel('Emotions')
    plt.ylabel('Counts')
    plt.title('Emotion Counts')
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Use webcam or upload video
source = st.sidebar.radio("Select source", ("Webcam", "Upload Video"))

if source == "Webcam":
    st.header("Webcam Feed")
    run = st.checkbox('Run')

    if run:
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to read frame from webcam")
                break
            
            frame, faces = analyze_frame(frame)
            current_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))

            st.image(frame, channels="BGR", caption=f"Live Feed - Time: {current_time}")
            draw_bar_chart(emotion_counts)

        cap.release()
else:
    uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi"])
    
    if uploaded_file is not None:
        st.header("Uploaded Video")
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        cap = cv2.VideoCapture(cv2.imdecode(file_bytes, cv2.IMREAD_COLOR))

        if st.button('Start Analysis'):
            start_time = time.time()
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame, faces = analyze_frame(frame)
                current_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))

                st.image(frame, channels="BGR", caption=f"Video Feed - Time: {current_time}")
                draw_bar_chart(emotion_counts)

            cap.release()
