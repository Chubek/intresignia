from setuptools import setup

setup(
    name='opencv_intredit',
    version='0.0.1beta',
    packages=['opencv-intredit'],
    install_requires=[
        'opencv-python',
        'numpy',
        'pydantic',
        'scikit-image',
        'pillow',
    ],
)
