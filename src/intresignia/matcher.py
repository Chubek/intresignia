from ctypes import Union
from typing import Dict
import cv2
import numpy as np
from glob import glob

import inspect
import os


path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))


path_matchers = os.path.join(path, 'matchers')

imgs_temp = glob(os.path.join(path_matchers, "*.png"))

classes = {
    "bike_no_access_old.png": "No Acces for Bikes (Old)",
    "bike_no_access.png": "No Access for Bikes",
    "give_way.png": "Give Way",
    "no_access_axel_load_4_8.png": "No Axel Load Larger 4.8t",
    "no_access_bicycles_old.png": "No Access for Bicycles (Old)",
    "no_access_bicycles.png": "No Access for Bicycles",
    "no_access_bus_haulers.png": "No Access for Buses and Haulders",
    "no_access_bus.png": "No Access for Buses",
    "no_access_cars_bikes_old.png": "No Access for Cars and Bikes (Old)",
    "no_access_cars_bikes.png": "No Access for Bikes and Cars",
    "no_access_haulers_old.png": "No Access for Haulers (Old)",
    "no_access_haulers.png": "No Access for Haulers",
    "no_access_hazardous.png": "No Access for Hazard Carriers",
    "no_access_millue_zone.png": "Millue Zone",
    "no_access_mopeds_bicycles_old.png": "No Access for Mopeds and Bicycles (Old)",
    "no_access_mopeds_bicycles.png": "No Access for Mopeds and Bicycles",
    "no_access_mopeds_old.png": "No Acccess for Mopeds (Old)",
    "no_access_mopeds.png": "No Access for Mopeds",
    "no_access_more_two_old.png": "No Access for Vehicles with More than 2 Wheels (Old)",
    "no_access_more_two.png": "No Access for Vehicles with More than 2 Wheels",
    "no_access_ped_old.png": "No Pedesterians (Old)",
    "no_access_ped.png": "No Pedesterians",
    "no_access_slow_bicycle_bike_invalid.png": "No Access for Two-Wheeled Slow Vehicles",
    "no_access_slow_old.png": "No Access for Slow Vehicles (Old)",
    "no_access_slow.png": "No Access for Slow Vehicles",
    "no_access_trailers_old.png": "No Access for Trailer Cars (Old)",
    "no_access_trailers.png": "No Access for Trailer Cars",
    "no_access_weight_5_4.png": "No Access for Weights Larger than 5.4t",
    "no_access_wide_load.png": "No Access for Wide Length (min 10m)",
    "no_access_width_2_3.png": "No Acces for Wide Width (min 2.3m)",
    "no_access_wide_height.png": "No Acces for Wide Height (min 3.1m)",
    "no_entry.png": "No Entry",
    "no_overtaking_trucks.png": "No Overtaking Haulers",
    "no_overtaking.png": "No Overtaking",
    "no_parking_bikes_mopeds.png": "No Parking Bikes and Mopeds",
    "no_parking.png": "No Parking",
    "no_stopping.png": "No Stopping",
    "no_u_turn.png": "No U Turn",
    "road_closed.png": "Road Closed",
    "speed_limit_50.png": "Speed Limit (min 50)",
    "stop.png": "Stop"
}

orb = cv2.ORB_create()
m = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

queries_imgs = {k.split("/")[-1]: cv2.imread(k, 0) for k in imgs_temp}
queires_descriptors = {k: orb.detectAndCompute(
    v, None)[1] for k, v in queries_imgs.items()}


def orb_matcher(img: np.array, threshold=60) -> Union[str, Dict]:
    global orb
    global m

    _, img_descriptors = orb.detectAndCompute(img, None)

    scores_mean = {}

    for k, v in queires_descriptors.items():
        matches = m.match(img_descriptors, v)

        dists = [m.distance for m in matches]

        scores_mean[k] = np.mean(dists)

    max_ = max(scores_mean, key=scores_mean.get)

    if max_ < threshold:
        None, scores_mean

    return classes[k], scores_mean
