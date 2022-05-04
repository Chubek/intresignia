import time
from tkinter.messagebox import NO

import cv2
import numpy as np
from cv2 import imshow
from scipy import rand

from . import color
from . import shape
from . import template
from . import settings


def detect_intredit_signs(img_path: str, settings: settings.Settings, pyrd=True) -> np.array:
    """
    This is the main detect function.

    Params
    ------
        img_path: str
            Path to img, relative or absolute, does not matter
        settings: Settigngs
            The settings object you created.
        pyrd: bool
            Whethet to pyrDown the image or not (derease qualiy and size.

    Returns
        Final image annotated: np.array    
        Score dict: List 
            final SSIM score dict
    """

    img = cv2.imread(img_path)

    if pyrd:
        print("Pyring down the image as pyrd=True...")
        img = cv2.pyrDown(img)
        img = cv2.resize(img, (1024, 768))

    color_isolated = color.enclose_red(
        img, settings.color_low, 
        settings.color_high, settings.red_thresh,
        op=settings.do_op,
        add_hue=settings.add_hue)

    circles = shape.detect_circle(
        color_isolated,
        settings.dp,
        settings.min_dist_circle,
        settings.min_radius,
        settings.max_radius,
        settings.param_1,
        settings.param_2,
        settings.do_op_circle
        )

    output = img.copy()

    dcts = []
    coords = []

    print(f"Found {len(circles)} circles...")

    for i, circle in enumerate(circles):
        print(f"Operating on circle {i + 1}/{len(circles)}...")

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

        y_nonzero, x_nonzero, _ = np.nonzero(img_cropped)

        img_cropped = img_cropped[np.min(y_nonzero):np.max(
            y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

        if img[y_left:y_right, x_left:x_right, :].shape[1] == 0:
            continue

        temp, dct = template.get_max_sim(img_cropped, settings.thresh_temp)
        dcts.append(dct)
        if temp == -1:
            print("Could not detect any of the sign shapes based on given templates...")
            continue
        
        print("Shape detected, adding to list...")
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        coords.append((x, y, r))
    
    if len(coords) == 0:
        print("Warning: No signs detected, output image won't have any marks...")

    print("Done! Returning the output image, scores, sign coordinates and isolated color.")
    
    return output, dcts, coords, color_isolated
