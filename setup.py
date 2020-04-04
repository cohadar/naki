from setuptools import setup, find_packages
setup(
    name="naki",
    packages=find_packages("код"),
    package_dir={"": "код"},
    install_requires=[
        "attrs>=19.3",
        "blessings>=1.7",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
)
