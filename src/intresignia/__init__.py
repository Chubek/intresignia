import os
import sys

sys.path.append(os.path.basename(os.path.dirname(__file__)))


from .settings import Settings
from .detect import intresignia_detect


all = [Settings, intresignia_detect]