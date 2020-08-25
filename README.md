# Wappylyzer

Implementation of [Wappalyzer](https://www.wappalyzer.com/) in Python.


## Installation

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Update the Wappalyzer database (`apps.json`):

```bash
python main.py update
```


## How to use

```bash
python main.py analyze -u <url>
```

This will output a JSON list of applications.

```bash
python main.py analyze -u https://google.com
[
    "Google Web Server"
]
```

Wappalyzer is a JavaScript application therefore some of the regex wont compile
in Python. You may see a message in the `stderr` with the faulty regex:

```bash
python main.py analyze -u https://google.com
Error with regex (?:<div class="sf-toolbar[^>]+?>[^]+<span class="sf-toolbar-value">([\d.])+|<div id="sfwdt[^"]+" class="[^"]*sf-toolbar)
[
    "Google Web Server"
]
```


## Why there is less results than the official application?

This Python implementation will returns less technologies than the official app
and here is why :

- The official Wappalyzer is written in JavaScript, so it analyze the global
variables from the JavaScript files. If you check my implementation, the
`analyze_js` method tries to look for global variables in Python but it cannot
find with accurately the patterns in minified code.
- Some website may returns different page based on your session cookie.
That why the browser extension may returns more accurate technologies than the
cli application.


## License

MIT
The `apps.json` comes from the official [Wappalyzer repository](https://github.com/AliasIO/wappalyzer)
