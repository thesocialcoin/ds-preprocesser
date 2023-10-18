from setuptools import find_packages, setup

import cbpreprocessing

DISTNAME = "cbpreprocessing"

MAINTAINER = "Citibeats"
MAINTAINER_EMAIL = "administration@citibeats.com"

DESCRIPTION = "A preprocessing library that given a text and its language returns the cleaned version of the text."
with open('./README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

URL = "https://www.citibeats.com/"

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/thesocialcoin/ds-preprocessing/issues",
    "Documentation": "https://github.com/thesocialcoin/ds-preprocessing/tree/main/src",
    "Source Code": "https://github.com/thesocialcoin/ds-preprocessing/tree/main",
}

VERSION = cbpreprocessing.__version__

with open("./requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

PACKAGES = find_packages(exclude=["tests"])

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',              # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: <audience>',          # Define your audience
    'Topic :: <topic>'
    'License :: OSI Approved :: MIT License',       # Again, pick a license
    'Programming Language :: Python :: 3.10.13']       # Specify which python versions that you want to suppor


setup(
    name=DISTNAME,
    author=MAINTAINER,
    author_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    project_urls=PROJECT_URLS,
    version=VERSION,
    install_requires=REQUIREMENTS,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    package_data={DISTNAME: ['data/stop-words/*']}
)
