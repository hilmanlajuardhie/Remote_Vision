import cv2 as cv

def playback_node():
    print("Starting Playback node...")

    gst_in = (
        "udpsrc port=5000 buffer-size=524288 "
        "caps=\"application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)JPEG, payload=(int)26\" ! "
        "rtpjpegdepay ! jpegdec ! videoconvert ! "
        "video/x-raw, format=BGR ! "
        "appsink drop=true max-buffers=1 sync=false"
    )
    
    print("Waiting for video stream on Port 5000...")
    cap = cv.VideoCapture(gst_in, cv.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Could not open the GStreamer receiver pipeline.")
        return

    max_retries = 3
    retry_count = 0
    stream_connected = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                retry_count += 1
                print(f"Warning: No data on port 5000 ({retry_count}/{max_retries})...")

                if retry_count >= max_retries:
                    print("Error: No data stream detected on port 5000 after 3 attempts. Terminating program.")
                    break

                cv.waitKey(1000)
                continue
            retry_count = 0

            if not stream_connected:
                print("Stream connected!")
                print("Press 'q' in the video window to quit.")
                stream_connected = True
            
            cv.imshow("Live Stream Playback", frame)

            # Break the loop if the user presses 'q'
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nStopping Playback Node.")
    finally:
        cap.release()
        cv.destroyAllWindows()
        print("Resources released. Program closed.")

if __name__ == "__main__":
    playback_node()