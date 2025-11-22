from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Anime Recommeder System",
    version="1.0",
    author="Rohit",
    packages=find_packages(),
    install_requires = requirements,
)