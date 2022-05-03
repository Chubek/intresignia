import cv2
import numpy as np
from cv2 import line
from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim

from . import color
from . import settings

img_temp_no_entry = cv2.imread("./data/no_entry.png")
img_temp_no_wait = cv2.imread("./data/no_waiting.png")
img_temp_ring = cv2.imread("./data/ring.png")
img_temp_line = cv2.imread("./data/line.png")


st = settings.Settings()

color_no_entry = img_as_float(cv2.resize(color.enclose_red(img_temp_no_entry, st.color_low,
                                                           st.color_high, st.red_thresh), (400, 400)))

color_no_wait = img_as_float(cv2.resize(color.enclose_red(img_temp_no_wait, st.color_low,
                                                          st.color_high, st.red_thresh), (400, 400)))


color_line = img_as_float(cv2.resize(color.enclose_red(img_temp_line, st.color_low,
                                                       st.color_high, st.red_thresh), (400, 400)))


color_ring = img_as_float(cv2.resize(color.enclose_red(img_temp_ring, st.color_low,
                                                       st.color_high, st.red_thresh), (400, 400)))


def get_max_sim(img: np.array, thresh=0.7) -> bool:
    """
    This functions purpose is to make sure signs are signs.

    Param
    -----
        img: np.ndarray
            The image numpy array
        thresh:
            The threshold for maximum SSIM score

    Returns
    -------
        max_score: int
        score_dict: Dict
    """

    img = cv2.resize(img, (400, 400))

    img = img_as_float(img)
    comp_line = ssim(color_no_entry, img,
                     data_range=img.max() - img.min(), channel_axis=2)
    comp_nw = ssim(color_no_wait, img,
                   data_range= img.max() -  img.min(), channel_axis=2)
    comp_ring = ssim(
        color_line, img, data_range= img.max() -  img.min(), channel_axis=2)
    comp_ne = ssim(color_ring, img,
                   data_range=img.max() - img.min(), channel_axis=2)

    dct = {
        "No Entry": comp_ne,
        "Line Intredit": comp_line,
        "No Wait": comp_nw,
        "Ring Intredit":  comp_ring
    }

    mx = max(dct, key=dct.get)

    if dct[max(dct, key=dct.get)] < thresh:
        return -1, None

    return mx, dct
