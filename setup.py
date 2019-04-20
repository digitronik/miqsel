from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()

install_requirements = ["Click>=5.0", "docker>=3.1", "PyYAML>=3.0"]

setup_requirements = ["setuptools_scm"]

setup(
    author="Nikhil Dhandre",
    author_email="nik.digitronik@live.com",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Miq Selenium Server for local testing",
    entry_points={"console_scripts": ["miqsel=miqsel.miqsel:cli"]},
    install_requires=install_requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    setup_requires=setup_requirements,
    keywords="miqsel",
    name="miqsel",
    packages=find_packages(include=["miqsel"]),
    url="https://github.com/digitronik/miqsel",
    version="1.4",
    license="GPLv3",
    zip_safe=False,
)
