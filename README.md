# ADRM
ADRM - automatized data retrieval for microgrid and Water-Energy-Food polyservice system design

The purpose of the tool is the automatization of location-specific data retrieval for providing the input for site-tailored configuration of microgrids and water-energy-food polyservice systems. The information required for the system optimization is point-based (coordinates).

This repository is generated from rli_template. More information see below. 

## Overview

An Overview of input parameters including required temporal and spatial resolution, potential data sources and API can be found in the excel below: 

https://1drv.ms/x/s!AmPb5U21V6Xhh_Bv73yK-dlfHm8xXw?e=lg1egk

Feel free to update this excel by further parameters and data sources including their API. 

# rli_template
Template repository for creating new projects under the RLI's umbrella

## Get started

Simply click on the green `Use this template` button on the left of the `Clone or download` button.

The detailed instructions to create a new repository from this template can be found [here](https://help.github.com/en/articles/creating-a-repository-from-a-template).

## src folder

This folder is where you should place the code of your package (package name to be edited in `setup.py` under name)

You can install it locally for developing with

    python setup.py install
    
More details for packaging are available on [https://packaging.python.org](https://packaging.python.org/tutorials/packaging-projects/)


## Docs

To build the docs simply go to the `docs` folder

    cd docs

Install the requirements

    pip install -r docs_requirements.txt

and run

    make html

The output will then be located in `docs/_build/html` and can be opened with your favorite browser

## Code linting

In this template, 3 possible linters are proposed:
- flake8 only sends warnings and error about linting (PEP8)
- pylint sends warnings and error about linting (PEP8) and also allows warning about imports order
- black sends warning but can also fix the files for you

You can perfectly use the 3 of them or subset, at your preference. Don't forget to edit `.travis.yml` if you want to desactivate the automatic testing of some linters!
