from pydantic import BaseModel
from typing import Tuple, Optional


class Settings(BaseModel):
    color_low: Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = (
        (0, 50, 50), (10, 255, 255))
    color_high: Optional[Tuple[Tuple[int, int, int], Tuple[int, int, int]]] = (
        (170, 50, 50), (180, 255, 255))
    dp: Optional[float] = 2.5
    min_dist_circle: Optional[int] = 180
    min_radius: Optional[int] = 15
    max_radius: Optional[int] = 60
    edge_low_threshold: Optional[int] = 50
    edge_high_threshold: Optional[int] = 150
    rho: Optional[int] = 1
    theta: Optional[float] = 0.785398
    line_threshold: Optional[int] = 15
    min_line_Length: Optional[int] = 20
    max_line_gap: Optional[int] = 20
