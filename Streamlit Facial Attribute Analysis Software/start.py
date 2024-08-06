from tkinter import *
from tkinter import ttk
import socket
import subprocess
import os
import webbrowser
from PIL import Image, ImageTk

server_process = None

app_name = "app.py"


def run_server():
    # Get the current directory (where start.py is located)
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the app directory
    app_directory = os.path.join(current_directory, "app")
    os.chdir(app_directory)

    # Path to the virtual environment activation script
    activate_venv = os.path.join(app_directory, ".venv", "Scripts", "activate.bat")

    # Activate the virtual environment
    subprocess.call(activate_venv, shell=True)

    # Run the Streamlit server
    subprocess.Popen(["streamlit", "run", app_name], shell=True)


def quit_server():
    global server_process
    if server_process is not None:
        # Terminate the Streamlit process
        server_process.terminate()
        server_process.wait()
        server_process = None
    else:
        print("Server is not running.")


root = Tk()
root.title("Facial Attribute Analysis Software Daemon")
root.geometry("400x420")
root.resizable(0, 0)
# root.iconbitmap("C:\sbrsrp\static\img/afit.ico")

# img = ImageTk.PhotoImage(Image.open("C:\sbrsrp\static\img/afitx.png"))
# logo_label = ttk.Label(
#     root,
#     image=img,
#     width=40
# )
# logo_label.place(x=110, y=20)

app_label = Label(
    root,
    text="FACIAL ANALYSIS DAEMON",
    font=('Arial bold', 10),
    foreground="#1438fe"
)
app_label.place(x=100, y=200)

detected_label = Label(
    root,
    text="Detected IP Address",
)
detected_label.place(x=133, y=230)

ip_label = Label(
    root,
    text="",
    font=('Arial bold', 10),
    bg="#EBF1ED"

)
ip_label.place(x=130, y=280)

# updt_ip()

run_btn = Button(
    root,
    text="Run Server",
    command=run_server,
    height=2,
    width=15,
    fg="white",
    bg="#3F77F2"
)
run_btn.place(x=70, y=330)

quit_btn = Button(
    root,
    text="Quit Server",
    command=quit_server,
    height=2,
    width=15,
    fg="white",
    bg="red",

)
quit_btn.place(x=200, y=330)

root.mainloop()
