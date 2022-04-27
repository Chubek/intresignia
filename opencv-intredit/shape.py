import cv2
import numpy as np
from typing import List
import random

def detect_circle(
        img: np.array,
        dp: float,
        min_dist: int,
        min_radius: int,
        max_radius: int,
        param_1: int,
        param_2: int) -> np.array and np.array:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp,
        min_dist,
        minRadius=min_radius,
        maxRadius=max_radius,
        param1=param_1,
        param2=param_2)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        return circles

    return None


def detect_line(img: np.array,
                edge_low_threshold=50,
                edge_high_threshold=150,
                rho=1,
                theta=45 * (np.pi / 180),
                threshold=15,
                min_line_length=20,
                max_line_gap=20) -> bool:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    edges = cv2.Canny(blur_gray, edge_low_threshold, edge_high_threshold)

    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    if lines is not None:
        return True

    return False


def detect_rectangle(img, kernel_size=(3, 3), w_extrema=(20, 50), h_extrema=(10, 20)) -> bool:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    normed = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=kernel_size)
    opened = cv2.morphologyEx(normed, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(opened, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        bbox = cv2.boundingRect(cnt)

        x, y, w, h = bbox

        if w_extrema[0] <= w < w_extrema[1] and h_extrema[0] <= h < h_extrema[1]:
            return True


    return False
