Thank you for considering to contribute to **"BEE Package Maker"**

## Starting development

We recommend [PyCharm Community](https://www.jetbrains.com/pycharm) to edit our code base.
In order to get started testing the application, you need to install [Python 3.8](https://www.python.org/downloads).
Open the terminal, cd to the directory you have cloned "BEE Package Maker" to and run `pip install -r requirements.txt`. Afterwards, you can use `py BEEPackageMaker.py --dev` to start the
development version of BPM.
Note: Its suggested to put the BPM packages and enviroment in a Virtual Enviroment (like venv or pipenv), to divide the packages.

## Code Rules

### Verified as working

All code contributed to this repository should be verified as working, meaning you've tested the
functionality at least once and didn't encounter unexpected behaviour. Building the application also may not contain errors inside the console.

### Code Style
#### Imports
All imports should happen at the start of the file, there's should be no empty lines between import statements.
Don't "minimize" imports (`import module0, module1`), every module should have its own line and import keyword

#### Names
Variable, constant and parameter names should all be camelCase.

```python
# Example
myVar = 'Hello World!'
```

Method and function names are prefered to be CamelCase.

#### Strings
All strings should use `''` if the string doesn't contain a `'`, else, use `""`.

```python
# Example
'Hello World!'  # ok
"Hello world!"  # no
"you're a dev!"  # ok
'you\'re a dev!'  # no
```

If you need to concat a value to a string o vice versa, is preferred to use `f''` instead of `+` or `.join()`. This is for concatenating more than two values too.

```python
# Example
yourVar = 'Hello'
myVar = f'{yourVar} World!'
```

### Opening a Pull Request

Please make sure that you have been working with the "dev" branch. Pull request should use the "dev" branch as their base.
(as 13/01/2021 the dev branch isn't available yet, it will be created when BEE Package Maker v.1.0 is released)
