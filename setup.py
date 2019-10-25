"""Installation recipe for meintile."""

import os
from setuptools import find_packages, setup

# get version number
with open("meintile/__init__.py") as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip().strip("'").strip('"')
            break


# get dependencies from requirements file
def _parse_requirements(file):
    return sorted(
        set(
            line.partition("#")[0].strip()
            for line in open(os.path.join(os.path.dirname(__file__), file))
        )
        - set("")
    )


# use README.rst for project long_description
with open("README.rst") as f:
    readme = f.read()

setup(
    name="meintile",
    version=version,
    description="helps handling tile pyramids",
    long_description=readme,
    long_description_content_type="text/x-rst",
    author="Joachim Ungar",
    author_email="joachim.ungar@eox.at",
    url="https://github.com/EOX-A/meintile",
    license="MIT",
    packages=find_packages(),
    install_requires=_parse_requirements("requirements.txt"),
    extras_require={"dev": _parse_requirements("requirements-dev.txt")},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
