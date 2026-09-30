import cv2
import os

def detect_motion(video_source=0, threshold=25, min_contour_area=500):
    """
    Automated data-processing tracking pipeline that parses real-time video frames,
    applies filtering algorithms, and tracks dynamic system changes.
    """
    # Initialize video capture stream (0 for webcam or pass a video file path)
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {video_source}.")
        return

    # Read the first frame as the reference background
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read initial frame from source.")
        cap.release()
        return

    # Preprocess background frame: convert to grayscale and apply Gaussian blur for filtering
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)
    
    frame_count = 0
    print("Motion detection pipeline active. Press 'q' to exit.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Convert current frame to grayscale and blur to remove high-frequency noise
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            # Compute absolute difference between current frame and reference frame
            delta_frame = cv2.absdiff(prev_gray, gray)
            
            # Apply thresholding parameters to isolate dynamic changes
            _, thresh = cv2.threshold(delta_frame, threshold, 255, cv2.THRESH_BINARY)
            
            # Dilate the thresholded image to fill in holes and find contours
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) < min_contour_area:
                    continue
                motion_detected = True
                
                # Draw bounding box around detected motion on the live frame
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
            if motion_detected:
                print(f"Frame {frame_count}: Motion detected!")

            # Update reference frame for continuous stream processing
            prev_gray = gray.gray if hasattr(gray, 'gray') else gray

    except KeyboardInterrupt:
        print("Pipeline manually interrupted.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Processed {frame_count} total frames. Pipeline closed safely.")

if __name__ == "__main__":
    # Run with default webcam stream
    detect_motion(video_source=0, threshold=25, min_contour_area=500)
