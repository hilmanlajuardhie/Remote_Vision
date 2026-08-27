import cv2 as cv
import torch
import numpy as np
from ultralytics import YOLO
import time

def Record():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running YOLO11 on device: {device}")
    model = YOLO("model/yolo11m.pt")

    cap = cv.VideoCapture(0, cv.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv.CAP_PROP_FPS, 60)

    dummy_input = np.zeros((720, 1280, 3), dtype=np.uint8)
    for _ in range(3):
        model.predict(
            source=dummy_input, 
            device=device, 
            verbose=False, 
            quantize=16
            )

    frame_count = 0
    fps_display = 0.0
    last_time = time.time()

    with torch.inference_mode():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(
                source=frame, 
                device=device, 
                verbose=False, 
                quantize=16
                )
            annotated_frame = results[0].plot()
            
            frame_count += 1
            current_time = time.time()
            elapsed_time = current_time - last_time

            if elapsed_time >= 1.0:
                fps_display = frame_count / elapsed_time
                frame_count = 0
                last_time = current_time
                print(f"FPS: {fps_display:.2f}")

            fps_text = f"FPS:{fps_display:.2f}"
            cv.putText(annotated_frame, fps_text, (10, 20), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (235,150,0), 2, cv.LINE_AA)
            print(f"FPS: {fps_display:.2f}")

            cv.imshow("Record: YOLOv11", annotated_frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    Record()