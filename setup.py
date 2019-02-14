from setuptools import setup, find_packages


setup(
    name="rna_cd",
    description="RNA contamination detector",
    version="0.1.0",
    author="Leiden University Medical Center",
    author_email="a.h.b.bollen@lumc.nl",
    url="https://github.com/LUMC/rna_cd",
    license="AGPLv3+",
    packages=find_packages(),
    python_requires=">=3.5",
    zip_safe=False,
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
    },
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
