# chatgpt generated
from setuptools import setup, find_packages

# Read the requirements.txt file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="inventory_system",
    version="1.0.0",
    author="Nikki La",
    description="Inventory management system with tracking.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NikkiLa1/inventory_system",
    packages=find_packages(),
    install_requires=requirements,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
