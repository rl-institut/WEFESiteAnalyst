# WEFESiteAnalyst
automatized remote data collection tool for the site-tailored planning of integrated Water-Energy-Food-Environment Systems (iWEFEs).

The purpose of the tool is the automation of location-specific data collection for site-tailored planning and configuration of iWEFEs. The input to the WEFE Site Analyst are coordinates of the location to be analysed (point-based). Together with OWEFE and the iWEFE configurator, the WEFE Site Analyst contributes to the doctoral project "Facilitating the Planning of Integrated Water-Energy-Food-Environment Systems through Open Source Software".

This repository is generated from rli_template. More information see below. 

## Installation

### software
The currently supported Python Version is 3.9. For using the WEFESiteAnalyst clone the repository to your local machine. Then create a new virtual environment with Python Version 3.9. Activate the new virtual environment and move to the repository folder to install the requirements of WEFESiteAnalyst

     pip install -r requirements.txt

### required accounts
The WEFESiteAnalyst uses google earth engine and CDS API. Therefore, a Google Account and a Copernicus Climate Data Store Account are required. You can register for the Copernicus Climate Data Store [here](https://cds.climate.copernicus.eu/user/register). Instructions on how to use CDS API can be found [here](https://cds.climate.copernicus.eu/api-how-to).

## Get started

### Environmental data collection
After installation you can use the WEFESiteAnalyst. Therefore you have to run an anaconda prompt on your computer, move to the WEFESiteAnalyst repository and type "jupyter notebook". The repository will open in an jupyter notebook. In the folder examples, you can see applications of the WEFESiteAnalyst for various locations. For analyzing a new location you can use [WEFESiteAnalyst/examples/generic/WEFESiteAnalyst.ipynb](https://github.com/JulianBarinton/WEFESiteAnalyst/tree/master/examples/generic/WEFESiteAnalyst.ipynb). Here you can try out the WEFESiteAnalyst for any location on the globe. For storing the retrieved data for a new specific location in your repository, you can create a new folder "WEFESiteAnalyst/example/<new_location>/". Move the WEFESiteAnalyst.ipynb file to the newly created folder and run it to analyze the location and download site-specific WEFE data.

### Socio-economic data collection and WEF demand assessment
The WEFESiteAnalyst includes the collection of socio-economic data and WEF demand assessment. Therefore, find a Survey xml-file in [WEFESiteAnalyst/surveyWEFESiteAnalyst_survey.xml](https://github.com/JulianBarinton/WEFESiteAnalyst/blob/master/survey/WEFESiteAnalyst_survey.xml). You can deploy the xml-file in kobotoolbox and fill it (in case you are analyzing a location you are working or living) or send it to people living or working at the location to be analyzed. The results are made available as table. For deployment of the xml-file in kobotoolbox, please see their [documentation](https://support.kobotoolbox.org/). 
The WEF demand assessment tool (WEF DAT) is implemented by adding the water and food dimension to the exisitng energy demand asssessment tool [RAMP](https://github.com/RAMP-project/RAMP). Inputs to the WEF DAT are the survey results. Outputs of the WEF DAT are hourly demand time series related to the water, energy, and food dimensions.

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
