from setuptools import setup, find_packages

setup(
    name="mrd",
    description="mouse-rna detection",
    version="0.0.1",
    author="Sander Bollen",
    author_email="a.h.b.bollen@lumc.nl",
    license="AGPLv3",
    packages=find_packages(),
    install_requires=[
        "click",
        "scikit-learn",
        "pysam"
    ],
    entry_points={
        "console_scripts": [
            "mrd-train = mrd.cli:train_cli"
        ]
    }
)
