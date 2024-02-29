# original-metaplex-python
Python port of Metaplex JS SDK - https://github.com/metaplex-foundation/js

## Tools & IDE

### black: code formatter

https://black.readthedocs.io/  
config: pyproject.toml  
pre-commit & pre-push: enabled

```bash
black .
pre-commit run black --all-files
```


### flake8: linter

https://flake8.pycqa.org/  
config: .flake8  
pre-commit & pre-push: enabled  

```bash
flake8 .
pre-commit run flake8 --all-files
```

### isort: import sorting

https://pycqa.github.io/isort/  
config: pyproject.toml  
pre-commit & pre-push: enabled

```bash
isort .
pre-commit run isort --all-files
```

### mypy: type checking

https://mypy.readthedocs.io/  
config: mypy.ini  
pre-commit & pre-push: enabled

```bash
mypy .
pre-commit run mypy --all-files
```