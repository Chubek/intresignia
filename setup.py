from setuptools import setup

setup(
    name='intresignia',
    version='0.0.1beta',
    packages=['intresignia'],
    install_requires=[
        'opencv-python',
        'numpy',
        'pydantic',
        'scikit-image',
        'pillow',
    ],
    package_data={'': ['intresignia/temp_img/*.png']},
)
