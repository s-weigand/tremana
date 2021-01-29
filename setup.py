#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages
from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.md") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
    "pandas>=1.2.0",
    "numpy>=1.19.5",
    "PyYAML>=5.4.0",
    "matplotlib>=3.0",
]

setup_requirements = ["pytest-runner"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Sebastian Weigand",
    author_email="s.weigand.phy@gmail.com",
    python_requires=">=3.6.1",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Medical tremore analysis package (e.g. for parkinsonian tremor)",
    entry_points={
        "console_scripts": [
            "tremana=tremana.cli:main",
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    project_urls={
        "Documentation": "https://tremana.readthedocs.io/en/latest/",
        "Source": "https://github.com/s-weigand/tremana",
        "Tracker": "https://github.com/s-weigand/tremana/issues",
    },
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="tremana",
    name="tremana",
    packages=find_packages(include=["tremana", "tremana.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/s-weigand/tremana",
    version="0.0.1",
    zip_safe=False,
)
