from setuptools import setup

setup(
    name='intresignia',
    version='0.0.1beta',
    author = "Chubak Bidpaa"
    description = "Intredit traffic sign detection and classifier"
    url = "https://github.com/chubek/intresignia"
    packages=['intresignia'],
    install_requires=[
        'opencv-python',
        'numpy',
        'pydantic',
        'scikit-image',
        'pillow',
    ],
    package_data={'': ['intresignia/temp_img/*.png']},
    include_dirs=["./intresignia/temp_img"]
)
