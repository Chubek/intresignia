import cv2
import numpy as np
from typing import Tuple, List


def enclose_red(img: np.array,
                lower_thrershold: Tuple[Tuple[int, int], Tuple[int, int]],
                upper_thrershold: Tuple[Tuple[int, int], Tuple[int, int]]) -> np.array:
    """
    Detects and encloses red colors based on between threshold

    inputs:
        img: The image
        threshold: The red threshold tuple
    """
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_mask = cv2.inRange(hsv_img, lower_thrershold[0], lower_thrershold[1])
    upper_mask = cv2.inRange(hsv_img, upper_thrershold[0], upper_thrershold[1])

    return cv2.bitwise_and(img, img, mask=lower_mask + upper_mask)
