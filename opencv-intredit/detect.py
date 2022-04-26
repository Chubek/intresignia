import cv2
import numpy as np

import color
import shape

from settings import Settings


def detect_intredit_signs(img_path: str, settings: Settings) -> np.array:
    img = cv2.imread(img_path)

    color_isolated = color.enclose_red(
        img, settings.color_low, settings.color_high)

    circles = shape.detect_circle(
        color_isolated,
        settings.dp,
        settings.min_dist_circle,
        settings.min_radius,
        settings.max_radius)

    if circles is None:
        raise ValueError("No circle-like shapes found")

    output = img.copy()

    for circle in circles:
        x, y, r = circle
        if shape.detect_line(img[y - r:y + r, x - r:x + r, :]):
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)

    return output
