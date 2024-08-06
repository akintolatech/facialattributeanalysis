import streamlit as st
import cv2
from deepface import DeepFace
# import numpy as np

# Export
import docx
from docx import Document
from openpyxl import Workbook
# from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.chart import BarChart, Reference

# Custom CSS to change the width of the Streamlit app
custom_css = """
<style>
    .main .block-container {
        max-width: 1200px;
        padding-left: 1rem;
        padding-right: 1rem;
        
    }
    
    .chart-wrapper .fit-x .fit-y {
        width:100% !important;
        height:100% !important;
    }
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

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


def export_data():
    # Update emotion count
    analytics_data = st.session_state.emotion_counts

    wb = Workbook()
    ws = wb.active

    # Add the table headers
    ws.append(["De serie", "emoción", "La emoción cuenta"])

    # Add data rows
    serial = 1
    for emotion, count in analytics_data.items():
        ws.append([serial, emotion_translations[emotion], count])
        serial += 1

    # Add data for the chart in Excel
    chart = BarChart()
    chart.title = "La emoción cuenta"
    chart.y_axis.title = "contar"
    chart.x_axis.title = "Emoción"
    chart.legend = None  # Disable the legend

    data = Reference(ws, min_col=3, min_row=1, max_row=1 + len(analytics_data))
    categories = Reference(ws, min_col=2, min_row=2, max_row=1 + len(analytics_data))

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    chart.shape = 4
    ws.add_chart(chart, "E5")

    # Save the workbook
    wb.save("results/datos-analíticos.xlsx")


# Define a function to capture video from the webcam
def video_capture():
    cap = cv2.VideoCapture(0)  # Capture video from the default webcam (index 0)

    with col1:
        stframe = st.empty()

    with col2:
        chart_placeholder = st.empty()

    # Get the absolute path to the Haar cascade file
    cascade_file = 'haarcascade_frontalface_default.xml'

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_file)

    # Get the frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('results/analysed_vid.mp4', fourcc, 10.0, (frame_width, frame_height))

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
                cv2.putText(frame, emotion_translations[dominant_emotion], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 26), 3)

            except Exception as e:
                st.write("Error in analyzing face region:", e)
                pass

        # Write the processed frame to the video file
        out.write(frame)

        # Display the processed frame in Streamlit
        stframe.image(frame, channels="BGR")

        # Update the chart dynamically
        # chart_placeholder.bar_chart(st.session_state.emotion_counts)

        # Update the chart dynamically
        chart_placeholder.bar_chart({emotion_translations[k]: v for k, v in st.session_state.emotion_counts.items()})

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


st.title("Software de análisis de atributos faciales v.0.5")
st.write("Una aplicación de reconocimiento de atributos faciales con un índice de confianza del 95 %")

# Initialize session state for capturing
if 'capturing' not in st.session_state:
    st.session_state['capturing'] = False

# Display the emotion counts
# st.line_chart(st.session_state.emotion_counts)


col1, col2 = st.columns(2)

col3, col4 = st.columns(2)

with col3:
    col5, col6 = st.columns(2)

    with col5:
        # Define start and stop buttons
        if st.button('iniciar y grabar análisis en vivo'):
            st.session_state.capturing = True
            video_capture()

    # with col6:
    #     if st.button('Export Data Analysis'):
    #         st.session_state.capturing = False

with col4:
    if st.button('Análisis de datos de exportación'):
        export_data()


