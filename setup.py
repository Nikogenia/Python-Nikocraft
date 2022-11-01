"""Setup Script"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="nikocraft",
    version="0.0.1",
    description="Nikocraft Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikocraft123/Python-Nikocraft",
    author="Nikocraft",
    author_email="nikocraft@gmx.net",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",

        "Topic :: Multimedia :: Graphics",
        "Topic :: Games/Entertainment",
        "Topic :: Utilities",
    ],
    keywords="python, pygame, utils, framework, development",
    packages=find_packages(),
    python_requires=">=3.11, <4",
    install_requires=["pygame"],
    extras_require={
        "cv": ["opencv-python"],
    },
    # package_data={
    #     "sample": ["package_data.dat"],
    # },
    project_urls={
        "Source": "https://github.com/Nikocraft123/Python-Nikocraft",
    },
)