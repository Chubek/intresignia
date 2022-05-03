from setuptools import setup

setup(
    name='opencv-intredit',
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
