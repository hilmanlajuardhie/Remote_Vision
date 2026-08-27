import cv2 as cv

def playback_node():
    print("Starting Playback Stream ...")
    
    # GStreamer pipeline receiving from Port 5001
    gst_in = (
        "udpsrc port=5001 ! "
        "application/x-rtp, media=video, clock-rate=90000, encoding-name=JPEG, payload=26 ! "
        "rtpjpegdepay ! jpegdec ! videoconvert ! appsink"
    )
    
    cap = cv.VideoCapture(gst_in, cv.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Could not connect to Port 5001. Is the inference script running?")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Stream lost. Waiting...")
            cv.waitKey(1000)
            continue

        cv.imshow("User Playback: YOLOv11 Stream", frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    playback_node()