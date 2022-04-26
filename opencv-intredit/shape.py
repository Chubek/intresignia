import cv2
import numpy as np

def detect_circle(img: np.array, original: np.array, dp: float, min_dist: int) -> np.array:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, min_dist)
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        output = original.copy()

        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)

        return output

    return None