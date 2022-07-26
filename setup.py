import os
from setuptools import setup, find_packages

setup(
    name = "url_shortener",
    version = "0.0.1",
    author = "Aju George Jacob",
    author_email = "ajugjacob@gmail.com",
    description = "Test Package",
    
    scripts=['start.sh'],

    packages=find_packages(),
    
    install_requires=[
	'cachelib==0.9.0',
	'click==8.1.3',
	'Flask==2.1.3',
	'Flask-Login==0.6.1',
	'Flask-Session==0.4.0',
	'Flask-SQLAlchemy==2.5.1',
	'itsdangerous==2.1.2',
	'Jinja2==3.1.2',
	'MarkupSafe==2.1.1',
	'SQLAlchemy==1.4.39',
	'Werkzeug==2.0.0'
    ],

    include_package_data = True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.6',
)
