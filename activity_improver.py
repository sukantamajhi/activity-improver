from tkinter import *
from tkinter import messagebox
import threading
import time
import pyautogui


def center_window(window, width, height):
    # Get the dimensions of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be centered
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the position of the window
    window.geometry(f"{width}x{height}+{x}+{y}")


# Create root window
root = Tk()
root.title("Welcome to Activity Improver")
center_window(root, 350, 250)  # Adjusted the height for better spacing

# Global variable to control the thread
stop_thread_flag = threading.Event()


def clicked():
    interval = int(txt.get())  # interval in milliseconds
    stop_thread_flag.clear()  # Reset the stop flag
    try:
        while not stop_thread_flag.is_set():
            # print("Hello")
            pyautogui.press("enter")
            time.sleep(interval / 1000)
    except Exception as e:
        print(f"An error occurred: {e}")


def start_thread():
    global thread
    interval = txt.get()
    if not interval:
        messagebox.showerror("Error", "Please set the interval level")
        return
    if not thread.is_alive():
        stop_thread_flag.clear()
        thread = threading.Thread(target=clicked)
        thread.daemon = True
        thread.start()
        start_button.config(text="Running", state=DISABLED, bg="grey", fg="white")
        messagebox.showinfo("Started", "The activity improver has started.")


def stop_thread():
    # check if the thread is running
    if thread.is_alive():
        stop_thread_flag.set()  # Signal the thread to stop
        start_button.config(text="Start")  # Change button text back to "Start"
        start_button.config(text="Start", state=NORMAL, bg="green", fg="white")
        messagebox.showinfo("Stopped", "The activity improver has stopped.")
        return
    else:
        messagebox.showinfo("Stopped", "The activity improver is not running.")
        return


# Initialize the thread variable
thread = threading.Thread(target=clicked)

# Frame to hold all the widgets for better alignment
frame = Frame(root)
frame.pack(expand=True)  # Center the frame in the root window

# Add widgets to the frame
label = Label(frame, text="Welcome to Activity Improver", font=("Helvetica", 14))
label.grid(column=0, row=0, columnspan=2, pady=(10, 20))

interval_level = Label(
    frame, text="Select the interval level in milliseconds", font=("Helvetica", 12)
)
interval_level.grid(column=0, row=1, columnspan=2, pady=(0, 10))

txt = Entry(frame, width=30, font=("Helvetica", 12), relief="solid")
txt.grid(column=0, row=2, columnspan=2, pady=(0, 20))

start_button = Button(
    frame,
    text="Start",
    fg="white",
    bg="green",
    disabledforeground="white",
    command=start_thread,
    width=10,
    font=("Helvetica", 12),
    relief="flat",
)
start_button.grid(column=0, row=3, pady=(10, 5))

stop_button = Button(
    frame,
    text="Stop",
    bg="red",
    fg="white",
    command=stop_thread,
    width=10,
    font=("Helvetica", 12),
    relief="flat",
)
stop_button.grid(column=1, row=3, pady=(10, 5))

# Execute Tkinter
root.mainloop()
