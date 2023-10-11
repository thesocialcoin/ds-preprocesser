from setuptools import find_packages, setup

import template

DISTNAME = "template"

MAINTAINER = "Citibeats"
MAINTAINER_EMAIL = "administration@citibeats.com"

DESCRIPTION = "<description>"
with open('./README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

URL = "https://www.citibeats.com/"

PROJECT_URLS = {
    "Bug Tracker": "<bug-tracker-url>",
    "Documentation": "<documentation-url>",
    "Source Code": "<source-code-url>",
}

VERSION = template.__version__

with open("./requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

PACKAGES = find_packages(exclude=["tests"])

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',              # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: <audience>',          # Define your audience
    'Topic :: <topic>'
    'License :: OSI Approved :: MIT License',       # Again, pick a license
    'Programming Language :: Python :: <python-version>']       # Specify which python versions that you want to suppor


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
    classifiers=CLASSIFIERS
)
