# aind-python-library-template
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)


This is a repository template to quickly setup a python library project. This repository utilizes a tool called **uv** to handle all dependency and package management. For more information on this tool go to the [uv wiki](https://docs.astral.sh/uv/). 

##  Getting Started

```bash
pip install -e .
python -m sfm.main
```

## Documentation
To generate the rst files source files for documentation, run
```bash
sphinx-apidoc -o docs/source/ src
```
Then to create the documentation HTML files, run
```bash
sphinx-build -b html docs/source/ docs/build/html
```
