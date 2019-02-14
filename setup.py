from setuptools import setup, find_packages


setup(
    name="rna_cd",
    description="RNA contamination detection",
    version="0.1.0",
    author="Leiden University Medical Center",
    author_email="a.h.b.bollen@lumc.nl",
    license="AGPLv3+",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=[
        "click",
        "scikit-learn",
        "pysam",
        "matplotlib",
        "joblib"
    ],
    entry_points={
        "console_scripts": [
            "rna_cd-train = rna_cd.cli:train_cli",
            "rna_cd-classify = rna_cd.cli:classify_cli"
        ]
    }
)
