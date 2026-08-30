import cv2 as cv
import torch
import numpy as np
from ultralytics import YOLO
import time
import os

def capture_inference_node():
    # 1. Initialize the Hardware Camera
    print("Starting Camera capture...")
    cap = cv.VideoCapture(0, cv.CAP_V4L2)
    # Check System: Camera
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    # Set requested resolution and FPS
    width, height = 640, 480
    fps = 60
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv.CAP_PROP_FPS, fps)

    # 2. Initialize YOLO Model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Starting Capture Node on {device}...")
    # Set the location of AI model
    dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(dir, "..", "model", "yolo11m.pt")
    model = YOLO(model_path)
    # Warmup the GPU
    dummy_input = np.zeros((480, 640, 3), dtype=np.uint8)
    for _ in range(3):
        model.predict(
            source=dummy_input, 
            device=device, 
            verbose=False, 
            quantize="fp16"
        )

    # 3. Initialize Sender Pipeline (Broadcasting straight to Port 5000)
    gst_out = (
        "appsrc is-live=true do-timestamp=true ! "
        "videoconvert ! video/x-raw, format=I420 ! "
        "jpegenc quality=85 ! rtpjpegpay ! "
        "udpsink host=127.0.0.1 port=5000 sync=false"
    )
    out = cv.VideoWriter(gst_out, cv.CAP_GSTREAMER, 0, fps, (width, height))
    # Check System: Pipeline
    if not out.isOpened():
        print("Error: VideoWriter failed to open GStreamer pipeline.")
        cap.release()
        return
    print("Broadcasting on UDP Port 5000... (Press Ctrl+C to stop)")

    # 4. Initialize FPS Counter
    frame_count = 0
    fps_display = 0.0
    last_time = time.time()


    try:
        with torch.inference_mode():
            while True:
                # Grab hardware frame directly
                ret, frame = cap.read()
                if not ret:
                    print("Error: Camera disconnected.")
                    break
                
                # Run YOLO Inference
                results = model.predict(
                    source=frame, 
                    device=device, 
                    verbose=False, 
                    quantize="fp16"
                )
                annotated_frame = results[0].plot()
                
                # FPS Calculation
                frame_count += 1
                current_time = time.time()
                elapsed_time = current_time - last_time
                
                if elapsed_time >= 1.0:
                    fps_display = frame_count / elapsed_time
                    frame_count = 0
                    last_time = current_time
                    print(f"Inference FPS: {fps_display:.2f}")
                    
                # Burn FPS text onto the image
                cv.putText(
                    annotated_frame, 
                    f"FPS: {fps_display:.2f}", (10, 30), 
                    cv.FONT_HERSHEY_COMPLEX_SMALL, 
                    1, (235, 150, 0), 2, cv.LINE_AA)
                           
                # Force resolution to 640x480
                annotated_frame = cv.resize(annotated_frame, (width, height))
                
                # Blast it out to Port 5000
                out.write(annotated_frame)
                
    except KeyboardInterrupt:
        print("\nStopping Capture Node.")
    finally:
        cap.release()
        out.release()

if __name__ == "__main__":
    capture_inference_node()