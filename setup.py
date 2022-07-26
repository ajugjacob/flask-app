import os
from setuptools import setup, find_packages

setup(
    name = "Url Shortener",
    version = "0.0.1",
    author = "Aju George Jacob",
    author_email = "ajugjacob@gmail.com",
    description = "Test Package",
    
    scripts=['start.sh'],

    packages=find_packages(),

    include_package_data = True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.6',
)
