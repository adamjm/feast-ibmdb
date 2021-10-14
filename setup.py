# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

INSTALL_REQUIRE = [
    "feast>=0.12.0",
]

TEST_REQUIRE = ["pytest==6.0.0", "pytest-xdist", "assertpy==1.1"]

DEV_REQUIRE = [
    "flake8",
    "black==19.10b0",
    "isort>=5",
    "mypy==0.790",
]

setup(
    name="feast-ibmdb",
    version="0.1",
    author="Adam Makarucha",
    author_email="adamjm@au1.ibm.com",
    description="IBM db2 support for Feast offline store",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.7.0",
    url="https://github.ibm.com/anz-tech-garage/feast-db2-warehouse.git",
    project_urls={
        "Bug Tracker": "https://github.ibm.com/anz-tech-garage/feast-db2-warehouse/issues",
    },
    packages=["feast_ibmdb"],
    install_requires=INSTALL_REQUIRE,
    extras_require={
        "dev": DEV_REQUIRE + TEST_REQUIRE,
        "test": TEST_REQUIRE,
    },
    keywords=("feast featurestore db2 ibmdb offlinestore"),
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #"License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
