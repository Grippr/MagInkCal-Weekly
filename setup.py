from setuptools import setup, find_packages

def read_requirements(fn):
    with open(fn) as req_file:
        return req_file.read().splitlines()

setup(
    name="MagInkCalPy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "maginkcalpy=MagInkCalPy.__main__:main",
        ],
    },
    author="Joel Kramer",
    author_email="joelkramer713@gmail.com",
    description="A Python package for displaying Google Calendar events on a Waveshare e-ink display",
    #long_description=open("README.md").read(),
    #long_description_content_type="text/markdown",
    url="https://github.com/Grippr/MagInkCalPy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: pache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',

    license='Apache License 2.0',
    license_files=('LICENSE',),
)