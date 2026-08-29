import cv2 as cv
import torch
import numpy as np
from ultralytics import YOLO
import time
import os

def inference_node():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Starting Inference Node on {device}...")


    dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(dir, "..", "model", "yolo11m.pt")
    model = YOLO(model_path)

    # Warmup
    dummy_input = np.zeros((480, 640, 3), dtype=np.uint8)
    for _ in range(3):
        model.predict(
            source=dummy_input, 
            device=device, 
            verbose=False, 
            quantize="fp16"
        )

    # GStreamer pipeline receiving from Port 5000
    gst_in = (
        "udpsrc port=5000 caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG, payload=(int)26\" ! "
        "rtpjpegdepay ! jpegdec ! videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true sync=false"
    )
    cap = cv.VideoCapture(gst_in, cv.CAP_GSTREAMER)

    # GStreamer pipeline sending to Port 5001
    gst_out = (
        "appsrc ! video/x-raw,format=BGR,width=640,height=480,framerate=60/1 ! "
        "videoconvert ! jpegenc ! rtpjpegpay ! "
        "udpsink host=127.0.0.1 port=5001"
    )
    out = cv.VideoWriter(gst_out, cv.CAP_GSTREAMER, 0, 60, (640, 480))

    frame_count = 0
    fps_display = 0.0
    last_time = time.time()
    print("Start Calculation...")

    try:
        with torch.inference_mode():
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Waiting for camera data... (Is 1_capture.py running?)")
                    cap.release()
                    time.sleep(0.5)
                    cap = cv.VideoCapture(gst_in, cv.CAP_GSTREAMER)
                    continue # Keep trying if the stream drops for a microsecond
                # print(cap)
                
                # Run YOLO Inference
                # print("Inference running...)")
                results = model.predict(
                    source=frame, 
                    device=device, 
                    verbose=False, 
                    quantize="fp16"
                )
                annotated_frame = results[0].plot()
                print(annotated_frame)

                # FPS Calculation
                frame_count += 1
                current_time = time.time()
                elapsed_time = current_time - last_time

                if elapsed_time >= 1.0:
                    fps_display = frame_count / elapsed_time
                    frame_count = 0
                    last_time = current_time

                print(f"Inference FPS: {fps_display:.2f}")
                fps_text = f"FPS: {fps_display:.2f}"
                cv.putText(annotated_frame, fps_text, (10, 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (235, 150, 0), 2, cv.LINE_AA)

                # Push annotated frame to Port 5001
                out.write(annotated_frame)
                
    except KeyboardInterrupt:
        print("\nStopping Inference Node.")
    finally:
        cap.release()
        out.release()

if __name__ == "__main__":
    inference_node()