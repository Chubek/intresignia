from struct import pack
from setuptools import setup


setup(
    name='intresignia',
    version='0.0.3beta',
    author = "Chubak Bidpaa",
    description = "Intredit traffic sign detection and classifier",
    url = "https://github.com/chubek/intresignia",
    packages=['intresignia'],
    install_requires=[
        'opencv-python',
        'numpy',
        'pydantic',
        'scikit-image',
        'pillow',
    ],
    package_dir={'intresignia': 'src/intresignia'},
    package_data = {"intresignia": ["data/*.png", "matchers/*.png"]}
)
