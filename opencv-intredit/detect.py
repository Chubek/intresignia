import color
import cv2
import shape
from .types import Settings
import numpy as np
import cv2


def detect_intredit_signs(img_path: str, settings: Settings) -> np.array:
    img = cv2.imread(img_path)

    color_isolated = color.enclose_red(
        img, settings.color_low, settings.color_high)

    circles = shape.detect_circle(
        img,
        settings.db,
        settings.min_dist_circle,
        settings.min_radius,
        settings.max_radius)

    if circles is None:
        raise ValueError("No circle-like shapes found")

    output = img.copy()

    for circle in circles:
        x, y, r = circle
        if shape.detect_line(img[y:y + r, x:x + r, :]):
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)

    return output
