# Python needs this to know that this directory is a project

from setuptools import setup, find_packages

# python -m pip install --editable ./

setup(
    name="AI-Project",
    version="0.1.0",
    description="Project 1 for the Comp3710 class",
    url="https://github.com/computerwizard1991/ai-project",
    packages=find_packages()
)
