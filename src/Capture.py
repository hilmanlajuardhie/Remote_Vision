import cv2 as cv

def capture_node():
    print("Starting Camera capture...")
    cap = cv.VideoCapture(0, cv.CAP_V4L2)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv.CAP_PROP_FPS, 60)

    # GStreamer pipeline sending to Port 5000
    gst_out = (
        "appsrc ! videoconvert ! jpegenc ! rtpjpegpay ! "
        "udpsink host=127.0.0.1 port=5000"
    )
    
    out = cv.VideoWriter(gst_out, cv.CAP_GSTREAMER, 0, 60, (1280, 720))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            print(out)
    except KeyboardInterrupt:
        print("\nStopping Camera Node.")
    finally:
        cap.release()
        out.release()

if __name__ == "__main__":
    capture_node()