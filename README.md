# python-fastapi-sqlalchemy
Building a data API with python fastapi sqlalchemy

![lint-failure](https://raw.githubusercontent.com/gokhaneraslan/python-fastapi-sqlalchemy/main/Untitled.png)


## Installation

Install python 3.9.13 from python/downloads [Python 3.9.13](https://www.python.org/downloads/release/python-3913/).

Create a Python Virtual Environment
```bash
python3 -m venv venv
```

Activate a Python Virtual Environment for windows
```bash
venv/Scripts/activate
```
Activate a Python Virtual Environment for Linux
```bash
source venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```

## Usage
In Terminal
```python
uvicorn app.main:app --host 127.0.0.1 --port 5000
```


## License

[MIT](https://choosealicense.com/licenses/mit/)
