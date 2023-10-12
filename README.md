# Data Science Template

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work._

## Requirements

- Conda or Miniconda

```bash
brew install --cask miniconda
```

- Make

```bash
brew install make
```

## Standarized directory structure

The directory structure of your new project looks like this:

```text
├── LICENSE
├── Makefile            <- Makefile with commands like `make environment` or `make build`
├── README.md          <- The top-level README for using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures         <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
│   └── template
|       ├── __init__.py    <- Makes template a Python module (PSS. make sure to rename it)
│       │
│       ├── data           <- Scripts to download or generate data
│       │   └── make_dataset.py
│       │
│       ├── features       <- Scripts to turn raw data into features for modeling
│       │   └── build_features.py
│       │
│       ├── models         <- Scripts to train models and then use trained models to make
│       │   │                 predictions
│       │   ├── predict_model.py
│       │   └── train_model.py
│       │
│       └── visualization  <- Scripts to create exploratory and results oriented visualizations
│           └── visualize.py
```

## Create environment

PSS. Before executing this command, deactivate the current environment `conda deactivate`.
After the make instruction, remember to activate the environment with `conda activate <environment-name>`.

------------

make environment

## Installing investigation requirements

------------

make requirements

### Running the tests

------------

make tests

### Lint code

------------

make lint

### Delete compiled Python files

------------

make clean

## Build package from source code

------------

make build (you need the `build` package, by default is installed when you make the environment with `make`.)

### Install package (wheel)

------------

1) Make sure you are in the correct environment
2) Move to the `src` directory
3) Install wheel using pip
   ```bash
   pip install dist/*
   ```

### Upload wheel package to AWS

------------

make upload
