import time
from tkinter.messagebox import NO

import cv2
import numpy as np
from cv2 import imshow
from scipy import rand

from . import color, matcher
from . import settings as st
from . import shape, template
from . import auto_brighten

KERNEL = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

def intresignia_detect(img_path: str, settings: st.Settings, pyrd=True) -> np.array:
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
    print("Isolating the color red based on your settings...")
    color_isolated = color.enclose_red(
        img, settings.color_low,
        settings.color_high, settings.red_thresh,
        op_brighten=settings.do_op,
        op_brighten_hsv=settings.do_op_hsv,
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

    dcts = {}
    coords = {}
    cropped = {}
    all_det = []

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

        img_cropped = img[y_left - 15:y_right + 15, 
                                        x_left - 15:x_right + 15, :]

        y_nonzero, x_nonzero, _ = np.nonzero(img_cropped)

        img_cropped = img_cropped[np.min(y_nonzero):np.max(
            y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

        if img[y_left:y_right, x_left:x_right, :].shape[1] == 0:
            continue

        img_cropped = cv2.resize(img_cropped, (400, 400))

        img_cropped = cv2.GaussianBlur(img_cropped, (5,5), 
                    cv2.BORDER_DEFAULT)
        img_cropped = cv2.filter2D(img_cropped, -1, KERNEL)
        img_cropped = cv2.detailEnhance(img_cropped)

        try:
            img_cropped, _, _ = auto_brighten.automatic_brightness_and_contrast(img_cropped)
        except:
            pass

        if settings.classifier == st.ClassifierType.ORB:
            temp, dct = matcher.orb_matcher(img_cropped,
                                            settings.classifier_threshold,
                                            settings.classifier_norm,
                                            settings.classifier_aggmode)
        else:
            temp, dct = template.get_max_sim(img_cropped, settings.thresh_temp)

        
        if temp == -1:
            print("Could not detect any of the sign shapes based on given templates...")
            continue

        print("Shape detected, adding to list...")
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)

        if settings.do_classify:
            print("DoClassify enabled, marking classification...")
            cv2.putText(output, temp,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1.5,
                        color=(0, 255, 0), thickness=2, org=(x - (r * 2), y - (r * 2)))
        
        temp = f"{i + 1} - {temp}"
        coords[temp] = (x, y, r)
        dcts[temp] = dct
        cropped[temp] = img_cropped
        all_det.append(temp)

    if len(coords) == 0:
        print("Warning: No signs detected, output image won't have any marks...")

    print("Done! Returning the output image, scores, sign coordinates and isolated color.")

    return output, dcts, coords, color_isolated, cropped, all_det
