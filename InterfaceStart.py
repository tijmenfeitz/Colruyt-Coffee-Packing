import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Coffee")

# Set the size of the window
root.geometry("1080x920")

# Create a label to display the live feed
video_label = Label(root)
video_label.pack(pady=20)

# Create a label to display the selection
output_label = Label(root, text="", font=("Arial", 12), wraplength=180)
output_label.pack(pady=10)

# Video capture setup
cap = cv2.VideoCapture(1)  # Use the first webcam (ID = 0)

def update_video_feed():
    """Capture frames from the webcam and display them in the interface."""
    ret, frame = cap.read()  # Read a frame from the video capture
    if ret:
        # Convert the frame to RGB (tkinter uses RGB while OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to a PIL image, then to ImageTk for tkinter
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        # Update the label with the new image
        video_label.config(image=img)
        video_label.image = img
    # Schedule the next frame update
    root.after(10, update_video_feed)

def button_pressed(weight):
    """Handle button presses and display messages."""
    if weight == "250g":
        message = "You selected 250g!"
    elif weight == "500g":
        message = "The 500g selection is not yet supported."
    elif weight == "1kg":
        message = "The 1kg selection is not yet supported."
    elif weight == "2,5kg":
        message = "You selected 2,5kg!"
    else:
        message = "Unknown selection."

    print(message)
    output_label.config(text=message)

# Create buttons
button_250g = tk.Button(root, text="250g", command=lambda: button_pressed("250g"))
button_250g.pack(pady=10)

button_500g = tk.Button(root, text="500g", command=lambda: button_pressed("500g"))
button_500g.pack(pady=10)

button_1kg = tk.Button(root, text="1kg", command=lambda: button_pressed("1kg"))
button_1kg.pack(pady=10)

button_2_5kg = tk.Button(root, text="2,5kg", command=lambda: button_pressed("2,5kg"))
button_2_5kg.pack(pady=10)

# Start the live video feed update loop
update_video_feed()

# Run the application
root.mainloop()

# Release the video capture when the application closes
cap.release()