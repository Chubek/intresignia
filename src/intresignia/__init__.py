import os
import sys

sys.path.append(os.path.basename(os.path.dirname(__file__)))


globals()['Settings'] = __import__("settings.Settings")
globals()['intresignia_detect'] = __import__("detect.intresignia_detect")


all = ["settings.Settings", "detect.intresignia_detect"]