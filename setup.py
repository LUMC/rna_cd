from setuptools import setup, find_packages

from mrd import VERSION

setup(
    name="mrd",
    description="mouse-rna detection",
    version=str(VERSION),
    author="Sander Bollen",
    author_email="a.h.b.bollen@lumc.nl",
    license="AGPLv3",
    packages=find_packages(),
    install_requires=[
        "click",
        "scikit-learn",
        "pysam",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "mrd-train = mrd.cli:train_cli"
        ]
    }
)
