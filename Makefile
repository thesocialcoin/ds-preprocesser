#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Create new python environment with the dependencies
environment:
	conda env create -f environment.yml

## Install investigation Python dependencies
requirements:
	pip install -r ./src/requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	isort setup.py
	isort -rc src
	flake8 src

## Build package from source code
build:
	cd src/ && python3 -m build --wheel

## Upload wheel package to AWS (you need to be logged in and your keys need to be configured)
upload:
	cd src/ && twine upload -r codeartifact dist/*.whl

test:
	py.test tests/
