import cv2
import numpy as np

# categorize color using hsv (hue, saturation, value)
def categorize_color(h, s, v):
    # black / gray (low intensity)
    if v < 50:
        return "black / gray"
    
    # white (high intensity, value near 255)
    elif s < 50 and v > 200:
        return "white"
    
    # brown (low saturation, moderate hue)
    elif s < 100 and h > 15 and h < 30 and v > 100:
        return "brown"
    
    # red (hue near 0 or 180 degrees, full saturation)
    elif (h < 10 or h > 170) and s > 100:
        return "red"
    
    # orange (hue around 10 to 30 degrees)
    elif h > 10 and h < 30 and s > 100:
        return "orange"
    
    # yellow (hue around 30 to 60 degrees)
    elif h > 30 and h < 60 and s > 100:
        return "yellow"
    
    # green (hue around 40 to 90 degrees, higher saturation)
    elif h > 40 and h < 90 and s > 100 and v > 50:
        return "green"
    
    # blue (hue around 100 to 140 degrees, higher saturation)
    elif h > 100 and h < 140 and s > 100 and v > 50:
        return "blue"
    
    # indigo (hue around 140 to 180 degrees, higher saturation)
    elif h > 140 and h < 180 and s > 100 and v > 50:
        return "indigo"
    
    # violet (hue around 180 to 240 degrees, higher saturation)
    elif h > 180 and h < 240 and s > 100 and v > 50:
        return "violet"
    
    # unknown if no match
    else:
        return "unknown"

# open the camera (0 for the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("error: could not open camera.")
    exit()

while True:
    # capture a frame
    ret, frame = cap.read()
    if not ret:
        print("failed to capture image")
        break

    # get frame dimensions
    height, width, _ = frame.shape

    # convert from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # calculate the center pixel coordinates
    center_x, center_y = width // 2, height // 2

    # get the hsv value of the center pixel
    h, s, v = hsv_frame[center_y, center_x]

    # categorize color based on hsv values
    color_category = categorize_color(h, s, v)
    print(f"center pixel hsv: ({h}, {s}, {v}) - color category: {color_category}")

    # small crosshair at the center
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

    # show the frame
    cv2.imshow("camera feed", frame)

    # exit if enter key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # ascii code for enter key
        print("exit condition triggered: enter key pressed.")
        break

# release resources aka kill
cap.release()
cv2.destroyAllWindows()