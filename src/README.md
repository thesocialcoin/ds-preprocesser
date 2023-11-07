# Py preprocesser

![](https://www.citibeats.com/hs-fs/hubfs/tmp_1677754011016.jpg?width=1600&height=278&name=tmp_1677754011016.jpg)


The **preprocesser** is a Python module for preprocess text in different languagues.

The project is maintained by the Data Science team of Citibeats started in 2023.

Website: https://www.citibeats.com/

## Installation

preprocesser requires:

- Python (>= 3.8)

### User installation

If you already have a working registration
to AWS the easiest way to install preprocesser is using ``pip``.

```sh
pip install preprocesser
```

The documentation includes more detailed [installation instructions](https://www.notion.so/citibeats/AWS-CodeArtifact-Tutorial-533ca93698ec4a1aa53e3f8d3830b075?pvs=4)

## Example of use

```python
>>> from preprocesser.models import PreProcesser

>>> p = PreProcesser()
>>> text = """Hola Como

va mi pana @user

Que tal"""

>>> text

'Hola Como\n\nva mi pana @user\n\nQue tal'

>>> p(text)

{'raw_text': 'Hola Como\n\nva mi pana @user\n\nQue tal',
 'urls': [],
 'successions': {'begin': None, 'end': None},
 'users': ['@user'],
 'tags': [],
 '#s': [],
 'emojis': [],
 'exclams': 0,
 'questions': 0,
 'stops': 0,
 'elongateds': 0,
 'numbers': {'dates': [], 'years': [], 'prices': [], 'other': []},
 'text': 'hola como va mi pana que tal'}

>>> p.preprocess(text)

{'raw_text': 'Hola Como\n\nva mi pana @user\n\nQue tal',
 'urls': [],
 'successions': {'begin': None, 'end': None},
 'users': ['@user'],
 'tags': [],
 '#s': [],
 'emojis': [],
 'exclams': 0,
 'questions': 0,
 'stops': 0,
 'elongateds': 0,
 'numbers': {'dates': [], 'years': [], 'prices': [], 'other': []},
 'text': 'hola como va mi pana que tal'}
``````

## Important links

- Official source code repo: https://github.com/thesocialcoin/ds-preprocesser
- Issue tracker: https://github.com/thesocialcoin/ds-preprocesser/issues

## Source code

You can check the latest sources with the command::

```sh
git clone https://github.com/thesocialcoin/ds-preprocesser.git
```
