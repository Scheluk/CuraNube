from gettext import install
from struct import pack
from setuptools import setup

setup(
    name="Curanube",
    packages=["Curanube"],
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)