Template
===


# Build

```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install poetry==1.1.12
$ poetry install
$ pip install -e .
$ pre-commit install
$ mypy
```

# Test

Noclist server should not be up.

```shell
$ pytest
```

# Using

```shell
python -m src.noclist 2>/dev/null
```
