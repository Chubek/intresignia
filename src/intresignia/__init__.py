import os
import sys

sys.path.append(os.path.basename(os.path.dirname(__file__)))


from .settings import Settings
from .detect import intresignia_detect, intresignia_detect_alt


all = [Settings, intresignia_detect, intresignia_detect_alt]