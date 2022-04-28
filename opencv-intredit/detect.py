import cv2
from cv2 import imshow
import numpy as np
from scipy import rand

import color
import shape

from settings import Settings


def detect_intredit_signs(img_path: str, settings: Settings, pyrd=True) -> np.array:
    img = cv2.imread(img_path)

    if pyrd:
        img = cv2.pyrDown(img)
        img = cv2.resize(img, (1024, 768))

    color_isolated = color.enclose_red(
        img, settings.color_low, settings.color_high, settings.red_thresh)
    
    circles = shape.detect_circle(
        color_isolated,
        settings.dp,
        settings.min_dist_circle,
        settings.min_radius,
        settings.max_radius,
        settings.param_1,
        settings.param_2)

    if circles is None:
        raise ValueError("No circle-like shapes found")

    output = img.copy()
    for circle in circles:
        x, y, r = circle

        if y >= r:
            y_left, y_right = y - r, y + r
        else:
            y_left, y_right = y, y + r

        if x >= r:
            x_left, x_right = x - r, x + r
        else:
            x_left, x_right = x, x + r

        img_cropped = color_isolated[y_left:y_right, x_left:x_right, :]

        cv2.imshow(f"{np.random.randint(0, 1999)}", img_cropped)

        if img[y_left:y_right, x_left:x_right, :].shape[1] == 0:
            continue

        detect_line = shape.detect_line(
                img_cropped,
                settings.edge_low_threshold,
                settings.edge_high_threshold,
                settings.rho,
                settings.theta,
                settings.line_threshold,
                settings.min_line_Length,
                settings.max_line_gap)

        detect_rectangle = shape.detect_rectangle(
                img_cropped,
                settings.kernel_size,
                settings.w_extrema,
                settings.h_extrema)

        
        detect_circle = shape.detect_circle(
                    img_cropped,
                    settings.dp,
                    settings.min_dist_circle,
                    settings.min_radius,
                    settings.max_radius,
                    settings.param_1,
                    settings.param_2)

        detect_triangle = shape.detect_triangle(img_cropped, settings.epps)

        if detect_triangle:
            continue

        if detect_circle is None:
            has_no_circle = True
        elif len(circle) == 0:
            has_no_circle = True
        else:
            has_no_circle = False

        if not detect_rectangle and detect_line:
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)
            cv2.putText(output, "General Intredit", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (10, 250, 50), 1, 2)

        if not detect_line and has_no_circle and detect_rectangle:
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)
            cv2.putText(output, "Entry Intredit", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (10, 250, 50), 1, 2)

        if not has_no_circle:
            cv2.circle(output, (x, y), r + 10, (0, 255, 0), 4)
            cv2.putText(output, "Ring Intredit", (x, y),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (10, 250, 50), 1, 2)
    
    return output
