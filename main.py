import cv2
import math
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# Initialize key states to track keypresses
key_states = {key: False for row in keys for key in row}

# Utility functions
def calculateDistance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def isPointInsideRect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

def drawAll(img, buttonList, handLandmarks, key_states):
    finalText = ""
    last_key = ""
    
    if handLandmarks:
        index_finger_tip = handLandmarks[8][:2]
        middle_finger_tip = handLandmarks[4][:2]
        
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            rect = (x, y, w, h)
            is_inside = isPointInsideRect(index_finger_tip, rect)
            distance = calculateDistance(index_finger_tip, middle_finger_tip)
            
            # Check if middle and index fingers are close (less than 30 pixels apart)
            if is_inside and distance < 30:
                # Green when pressed
                color = (0, 255, 0)  # Green color
                if not key_states[button.text]:
                    key_states[button.text] = True
                    last_key = button.text
                    print(last_key, end = " ")  # Print the pressed key to the terminal
            elif is_inside:
                # 48 25 52
                color = (255, 0, 255)  # Magenta color
            else:
                color = (128, 0, 128)  # Dark purple color
            
            # Create a transparent key image with the same size as the key
            transparent_key = np.zeros((h, w, 3), dtype=np.uint8)
            
            # Fill the key with the specified color
            transparent_key.fill(0)
            transparent_key[:, :] = color

            # Set the text color based on the background color
            if np.mean(color) > 128:  # If the background is light, set text color to black
                text_color = (0, 0, 0)
            else:  # If the background is dark, set text color to white
                text_color = (255, 255, 255)
            
            # Overlay the transparent key on the frame with the updated text color
            cv2.putText(transparent_key, button.text, (20, 65),
                        cv2.FONT_HERSHEY_PLAIN, 4, text_color, 4)

            # Overlay the transparent key on the frame
            img[y:y+h, x:x+w] = cv2.addWeighted(transparent_key, 1, img[y:y+h, x:x+w], 1, 0)

    # Reset key states for keys that are no longer pressed
    for key in key_states:
        if key_states[key] and key != last_key:
            key_states[key] = False
            
    finalText += last_key
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
    return img

class Button():
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([100 * x + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    img = drawAll(img, buttonList, hands[0]['lmList'] if hands else [], key_states)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
