import tkinter as tk
from tkinter import Canvas


def draw_bar_chart(canvas, data, width=660, height=460):
    canvas.delete("all")  # Clear previous drawings

    max_value = max(data.values())
    num_bars = len(data)
    bar_width = width / num_bars

    for i, (emotion, count) in enumerate(data.items()):
        bar_height = (count / max_value) * height
        x0 = i * bar_width
        y0 = height - bar_height
        x1 = x0 + bar_width
        y1 = height

        canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
        canvas.create_text(x0 + bar_width / 2, y1 + 10, text=emotion, anchor=tk.N)
        canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(count), anchor=tk.S)


# Initialize the main window
root = tk.Tk()
root.title("Facial Attribute Analysis Software v.0.2")
root.geometry("1080x600")

# Create a canvas to draw the bar chart
chart_canvas = Canvas(root, width=660, height=460, bg="white")
chart_canvas.place(x=380, y=20)

# Dummy data for testing
emotion_counts = {
    "neutral": 549,
    "angry": 5,
    "fear": 2,
    "disgust": 3,
    "happy": 8,
    "sad": 1,
    "surprise": 4
}

# Draw the bar chart with the dummy data
draw_bar_chart(chart_canvas, emotion_counts)

root.mainloop()
