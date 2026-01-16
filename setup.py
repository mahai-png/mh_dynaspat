from setuptools import setup, find_packages

setup(
    name="mhmy-dynaspat",
    version="0.1.0",
    author="mhmy",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
    ],
)