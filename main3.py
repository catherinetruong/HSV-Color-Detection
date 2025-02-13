import cv2
import numpy as np
import sys
import adafruit_ssd1306
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont

# categorize color based on hsv values
def categorize_color(h, s, v):
    if v < 50:
        return "black / gray"
    elif s < 50 and v > 200:
        return "white"
    elif s < 100 and h > 15 and h < 30 and v > 100:
        return "brown"
    elif (h < 10 or h > 170) and s > 100:
        return "red"
    elif h > 10 and h < 30 and s > 100:
        return "orange"
    elif h > 30 and h < 60 and s > 100:
        return "yellow"
    elif h > 40 and h < 90 and s > 100 and v > 50:
        return "green"
    elif h > 100 and h < 140 and s > 100 and v > 50:
        return "blue"
    elif h > 140 and h < 180 and s > 100 and v > 50:
        return "indigo"
    elif h > 180 and h < 240 and s > 100 and v > 50:
        return "violet"
    else:
        return "unknown"

# initialize i2c for the oled display
def init_oled():
    i2c = busio.I2C(SCL, SDA)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.show()
    return oled

# display the color category and hsv values on the oled
def display_on_oled(oled, color_category, h, s, v):
    image = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()

    text = f"color: {color_category}\nhsv: ({h},{s},{v})"
    draw.text((0, 0), text, font=font, fill=255)

    oled.image(image)
    oled.show()

# open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("error: could not open camera.")
    exit()

# initialize the oled display
oled = init_oled()

while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to capture image.")
        break

    height, width, _ = frame.shape
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get the hsv value of the center pixel
    center_x, center_y = width // 2, height // 2
    h, s, v = hsv_frame[center_y, center_x]

    # categorize color based on hsv
    color_category = categorize_color(h, s, v)
    print(f"center pixel hsv: ({h}, {s}, {v}) - color category: {color_category}")

    # display on oled
    display_on_oled(oled, color_category, h, s, v)

    # small crosshair at the center
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

    # show the frame
    cv2.imshow("camera feed", frame)

    # exit if the enter key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # ascii code for enter key
        print("exit condition triggered: enter key pressed.")
        break

# release resources
cap.release()
cv2.destroyAllWindows()
