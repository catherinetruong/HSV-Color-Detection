import cv2
import numpy as np

# categorize rgb into roygbiv and other colors
def categorize_color(r, g, b):
    # black / gray (low intensity)
    if r < 50 and g < 50 and b < 50:
        return "black / gray"
    
    # white (high intensity, all channels near 255)
    elif r > 200 and g > 200 and b > 200:
        return "white"
    
    # brown (common for values near 101, 85, 78)
    elif r > 80 and r < 150 and g > 50 and g < 100 and b > 50 and b < 100:
        return "brown"
    
    # red (high red component, low blue and green)
    elif r > 120 and g < 80 and b < 80:
        return "red"
    
    # orange (higher red and green, low blue)
    elif r > 150 and g > 100 and b < 80:
        return "orange"
    
    # yellow (high red and green, low blue)
    elif r > 150 and g > 150 and b < 100:
        return "yellow"
    
    # green (higher green, low red and blue)
    elif g > 120 and r < 80 and b < 80:
        return "green"
    
    # blue (high blue, low red and green)
    elif b > 120 and r < 80 and g < 80:
        return "blue"
    
    # indigo (high blue and red, low green)
    elif r > 100 and b > 100 and g < 80:
        return "indigo"
    
    # violet (high red and blue, moderate green)
    elif r > 100 and b > 100 and g < 150:
        return "violet"
    
    # unknown if no match (but with a wider range for color flexibility)
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

    # calculate the center pixel coordinates
    center_x, center_y = width // 2, height // 2

    # get the rgb value of the center pixel (btw!!! opencv uses bgr format)
    (b, g, r) = frame[center_y, center_x]

    # convert np.uint8 to regular int and categorize the color
    color_category = categorize_color(int(r), int(g), int(b))
    print(f"center pixel rgb: ({r}, {g}, {b}) - color category: {color_category}")

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
