import cv2 as cv

def playback_node():
    print("Starting Playback node...")

    # Receiver Pipeline:
    # Listen on port 5000 (udpsrc) -> declare incoming format (application/x-rtp...) -> 
    # unpack network data (rtpjpegdepay) -> decompress (jpegdec) -> 
    # format for OpenCV (videoconvert BGR) -> drop into Python (appsink)
    gst_in = (
        "udpsrc port=5000 caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG, payload=(int)26\" ! "
        "rtpjpegdepay ! jpegdec ! videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true sync=false"
    )
    
    print("Waiting for video stream on Port 5000...")
    cap = cv.VideoCapture(gst_in, cv.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Could not open the GStreamer receiver pipeline.")
        return

    print("Stream connected! Press 'q' in the video window to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # If no data is arriving, wait and try again (prevents silent infinite looping)
                print("Waiting for data... (Is Capture.py running?)")
                cv.waitKey(1000)
                continue

            cv.imshow("Live Stream Playback", frame)

            # Break the loop if the user presses 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nStopping Playback Node.")
    finally:
        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    playback_node()