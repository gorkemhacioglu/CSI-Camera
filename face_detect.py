import time
import serial
import numpy as np
import cv2

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=6,
    flip_method=2,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def face_detect():
    face_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(
        "/usr/share/opencv4/haarcascades/haarcascade_eye.xml"
    )
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        prevtime = time.time()
        facedetectedtime = prevtime
        cv2.namedWindow("Face Detect", cv2.WINDOW_AUTOSIZE)
        while cv2.getWindowProperty("Face Detect", 0) >= 0:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
				facedetectedtime = time.time()
				if(x> 370):
					serial_port.write('1'.encode())
					print("Right")
				elif(x <290):
					serial_port.write('0'.encode())
					print("Left")
					
				if(y> 260):
					serial_port.write('2'.encode())
					print("Down")
				elif(y <190):
					serial_port.write('3'.encode())
					print("Up")
                
				cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
				roi_gray = gray[y : y + h, x : x + w]
				roi_color = img[y : y + h, x : x + w]
				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex, ey, ew, eh) in eyes:
					cv2.rectangle(
						roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
					)
			
            cv2.imshow("Face Detect", img)
            keyCode = cv2.waitKey(30) & 0xFF
            if(len(faces) == 0):
				now = time.time()
				if(now-prevtime > 2 and now-facedetectedtime >4):
					print("start scan")
					serial_port.write('9'.encode())
					prevtime = now
            # Stop the program on the ESC key
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
	serial_port = serial.Serial(
		port="/dev/ttyTHS1",
		baudrate=4800,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,)
	time.sleep(1)
	face_detect()
