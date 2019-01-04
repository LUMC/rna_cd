from setuptools import setup, find_packages

from rna_cd import VERSION

setup(
    name="rna_cd",
    description="RNA contamination detection",
    version=str(VERSION),
    author="Sander Bollen",
    author_email="a.h.b.bollen@lumc.nl",
    license="AGPLv3",
    packages=find_packages(),
    install_requires=[
        "click",
        "scikit-learn",
        "pysam",
        "matplotlib",
        "semver"
    ],
    entry_points={
        "console_scripts": [
            "rna_cd-train = rna_cd.cli:train_cli",
            "rna_cd-classify = rna_cd.cli:classify_cli"
        ]
    }
)
