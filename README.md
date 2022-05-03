# Intresignia

[![CircleCI](https://circleci.com/gh/Chubek/intresignia/tree/master.svg?style=shield)](https://circleci.com/gh/Chubek/intresignia/tree/master)

## Status
* **Verson 0.0.1beta** [Current]-> Detection done.
* **Verson 0.0.2beta** [Upcoming]-> Recognition and Classification TBA.


## What is this?

This is a Python package that uses color thresholding and other classical vision methods through OpenCV to detect a subset of intredit (prohibition) traffic signs. It will detect and classify any sign that is red.


## How to Use?

1. This package is not hosted on PyPi so don't try installing it with pip like that. Just do this:

```bash
python3.10 virtualenv venv
source venv/bin/activate (on Linux) or venv/vin/activate.ps1 (Windows)
python3.10 pip install git+https://github.com/chubek/intresignia.git
```

This will install the package. Mind you that you need to install Python 3.10. It does not use any of its feaures yet but it will pretty soon.

2. Create a new Python file and:

```python
from intresignia.detect import detect_intredit_signs
from intresignia.settings import Settings
import cv2
from pprint import pprint

st = Settings()

det, ssim_scores, coords = detect_intredit_signs("/path/to/img.png", st)

pprint(ssim_scores)
pprint(coords)


cv2.imshow('Detected Signs', det)
cv2.waitKey(0)
cv2.destroyAllWindows()

```
An exhaustive list of settings + grid search to find the best params using `grid_search.py` will be added to this readme pretty soon. Meanwhile please use the `help(Settings)`.


Any questions regarding this library should be directed at Chubak#7400.