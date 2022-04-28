from fileinput import close
import cv2
import numpy as np
from typing import Tuple, List


def enclose_red(img: np.array,
                lower_thrershold=((120, 50, 50), (150, 255, 255)),
                upper_thrershold=((175, 60, 50), (180, 255, 255)),
                red_thresh=125) -> np.array:

    img[:, :, 0] = img[:, :, 0] + 10
    normed = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    kernel = cv2.getStructuringElement(
        shape=cv2.MORPH_ELLIPSE, ksize=(5, 5))
    opened = cv2.morphologyEx(normed, cv2.MORPH_OPEN, kernel)
    img = cv2.GaussianBlur(opened, (5, 5), 0)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_mask = cv2.inRange(hsv_img, lower_thrershold[0], lower_thrershold[1])
    upper_mask = cv2.inRange(hsv_img, upper_thrershold[0], upper_thrershold[1])

    isolated = cv2.bitwise_and(img, img, mask=lower_mask + upper_mask)
    close = cv2.morphologyEx(isolated, cv2.MORPH_CLOSE, kernel)
    img = cv2.GaussianBlur(close, (5, 5), 0)

    return np.where(img > red_thresh, img, 0)
