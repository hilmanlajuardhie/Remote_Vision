import cv2 as cv

def capture_node():
    print("Starting Camera capture...")
    # Open the default webcam
    cap = cv.VideoCapture(0, cv.CAP_V4L2)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Set requested resolution and FPS
    width, height = 640, 480
    fps = 30
    cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv.CAP_PROP_FPS, fps)

    # Sender Pipeline: 
    # Take raw frames (appsrc) -> convert for compression (I420) -> compress (jpegenc) -> 
    # package for network (rtpjpegpay) -> blast out of port 5000 (udpsink)
    gst_out = (
        "appsrc ! "
        "videoconvert ! video/x-raw, format=I420 ! "
        "jpegenc ! rtpjpegpay ! "
        "udpsink host=127.0.0.1 port=5000 sync=false"
    )
    
    out = cv.VideoWriter(gst_out, cv.CAP_GSTREAMER, 0, fps, (width, height))

    if not out.isOpened():
        print("Error: VideoWriter failed to open GStreamer pipeline.")
        cap.release()
        return

    print("Broadcasting on UDP Port 5000... (Press Ctrl+C to stop)")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Camera disconnected.")
                break
            
            # CRITICAL: Force the frame to match the VideoWriter resolution 
            # to prevent OpenCV from silently dropping frames
            frame = cv.resize(frame, (width, height))
            
            out.write(frame)
            
    except KeyboardInterrupt:
        print("\nStopping Camera Node.")
    finally:
        cap.release()
        out.release()

if __name__ == "__main__":
    capture_node()