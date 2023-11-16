import sys

from setuptools import find_packages
from setuptools import setup

assert sys.version_info >= (3, 6, 0), "miqsel requires Python 3.6+"


with open("README.md") as readme_file:
    readme = readme_file.read()

install_requirements = ["Click>=5.0"]

setup_requirements = ["setuptools_scm"]

setup(
    author="Nikhil Dhandre",
    author_email="nik.digitronik@live.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    description="Miq Selenium Server for local testing",
    entry_points={"console_scripts": ["miqsel=miqsel:main"]},
    install_requires=install_requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    setup_requires=setup_requirements,
    python_requires=">=3.6",
    use_scm_version=True,
    keywords="miqsel",
    name="miqsel",
    packages=find_packages(include=["miqsel"]),
    url="https://github.com/digitronik/miqsel",
    license="GPLv3",
    zip_safe=False,
)
