import cv2 as cv
import numpy as np
import torch
from ultralytics import YOLO

camera = 1  # Set to 1 for your specific camera

# Ensure CUDA is available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if torch.cuda.is_available():
    print("CUDA is available and enabled.")

# Load the pre-trained YOLO OBB model
model = YOLO(r"C:/Users/gabri/Downloads/model_coffee.pt")  # Update with your model path

def main():
    # Initialize the video capture object
    cap = cv.VideoCapture(camera)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Camera not accessible.")
        return -1

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Run YOLO OBB inference on the frame
        results = model(frame, conf=0.8, verbose=False)

        # Check if results are available and handle them
        if results and hasattr(results[0], 'obb'):  # Check for OBB detections
            for obb in results[0].obb:
                # Extract OBB coordinates (e.g., 8-point vertices for an oriented box)
                vertices = obb.xyxyxyxy[0].cpu().numpy().astype(int)

                # Extract class label
                label = results[0].names[int(obb.cls[0])]

                # Draw the OBB using the vertices
                for i in range(len(vertices)):
                    cv.line(frame, tuple(vertices[i]), tuple(vertices[(i + 1) % len(vertices)]), (0, 255, 0), 2)

                # Draw the label near the first vertex
                cv.putText(frame, label, (vertices[0][0], vertices[0][1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Display the annotated frame
        cv.imshow("YOLO OBB Detection", frame)

        # Exit on 'q' key press
        if cv.waitKey(1) == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
