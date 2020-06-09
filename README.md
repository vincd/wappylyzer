# Wappylyzer

Implementation of [Wappalyzer](https://www.wappalyzer.com/) in Python.


## Installation

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Update the Wappalyzer database (`apps.json`):
```
$ python main.py update
```

## How to use

```
$ python main.py analyze -u <url>
```

This will output a json list of applications.
