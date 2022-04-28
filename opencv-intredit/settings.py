from pydantic import BaseModel
from typing import Tuple, Optional


class Settings(BaseModel):
    color_low: Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = (
        (120, 50, 50), (150, 255, 255))
    color_high: Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = (
        (175, 60, 50), (180, 255, 255))
    red_thresh: Optional[int] = 125
    dp: Optional[float] = 7.6
    min_dist_circle: Optional[int] = 400
    min_radius: Optional[int] = 2
    max_radius: Optional[int] = 50
    param_1: Optional[int] = 600
    param_2: Optional[int] = 20
    edge_low_threshold: Optional[int] = 50
    edge_high_threshold: Optional[int] = 150
    rho: Optional[int] = 1
    theta: Optional[float] = 0.785398
    line_threshold: Optional[int] = 25
    min_line_Length: Optional[int] = 20
    max_line_gap: Optional[int] = 20
    kernel_size: Optional[Tuple[int, int]] = (3, 3)
    w_extrema: Optional[Tuple[int, int]] = (5, 80)
    h_extrema: Optional[Tuple[int, int]] = (5, 30)
    epps: Optional[float] = 1.07
