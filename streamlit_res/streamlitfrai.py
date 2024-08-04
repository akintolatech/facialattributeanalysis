import streamlit as st
import av
import cv2
import numpy as np
from deepface import DeepFace
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, ClientSettings
import matplotlib.pyplot as plt

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

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.emotion_counts = emotion_counts.copy()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def analyze_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_region = frame[y:y + h, x:x + w]
            
            try:
                analyze = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
                if 'dominant_emotion' in analyze[0]:
                    dominant_emotion = analyze[0]['dominant_emotion']
                    self.emotion_counts[dominant_emotion] += 1
                    cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            except:
                pass

        return frame

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = self.analyze_frame(img)
        return img

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

client_settings = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},  # Only request video, not audio
)

st.title("Facial Attribute Analysis Software v0.4")
st.write("Web version")

# Use webcam
st.header("Webcam Feed")
ctx = webrtc_streamer(key="example", client_settings=client_settings, video_transformer_factory=VideoTransformer)

if ctx.video_transformer:
    draw_bar_chart(ctx.video_transformer.emotion_counts)
