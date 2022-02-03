Template
===


# Build a Working Environment

```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install poetry==1.1.12
$ poetry install
$ pip install -e .
```

# Test

Noclist server should not be up and running during testing.

To test, just run pytest.

```shell
$ pytest
```

A coverage report is created in HTML format in the htmlcov folder.

# Using

Optionally set an environment variable for the timeout.  The default timeout is 2 seconds.

```shell
export NOCLIST_TIMEOUT=1.0
```

Start a BADLIST server.

```shell
docker run --rm -p 8888:8888 adhocteam/noclist
```

Send logging to /dev/null.

```shell
python -m src.noclist 2>/dev/null
```

# Developing

This project uses pre-commit with several checks:

* black
* commitizen
* isort
* pyupgrade
* pylint
* mypy
* pytest

These checks must pass before a developer can commit a change.

```shell
$ pre-commit install
$ mypy
```

The developer may also run mypy manually to make sure typing hints are followed.
