# Manure Pyrolysis IAM

This study uses the Global Change Analysis Model (GCAM) integrated assessment model (IAM) to analyze the cost and CDR potential of various CDR technologies under many policy scenarios in the US from 2020 to 2050. The main folders include
    data
    gcam
    xml

## Locations

Global (32 GCAM regions) and USA (50 GCAM regions). This study, while it has global results, are only analyzed in the context of the US

## Files overview

The root folder contains the Python scripts used in the study. There are ten Python scripts and three folders. Details of each file or folder is provided below:

- data/: This folder contains three folders
  - data_analysis/: contains excel files for results calculations
    - images/: contains images used in results plotting and in the supplemental information
    - supplementary_tables/: contains supplementary data tables for measures of CDR policy
  - gcam_out/ contains the extracted data from the gcam xml db. 
    - /<policy-scenario-name>/<baseline-pathway> contains the results from a given policy scenario based on the baseline pathway assumptions.
    - /masked/ contains the masked data where years with model errors are removed from data analysis, the raw data is in .csv files labeled by xmldb query
    - ref.csv is the output from the database query
    - log.txt contains the list of errors found in the model output
  - maps/ contains map shapefiles for plotting
- gcam/: contains the modified files in the GCAM model. These consist of .xml files generated based on input data (gcamdata is not used, so we wrote code to directly write to .xml files is the `building_xml` folder) and updates to the gcam .bat files to create a unique config and .bat file for each policy scenario. Not all .bat files that are created are relevant to the analysis in the paper.
- building_xml/code/: contains code to map input data files to .xml files.
- building_xml/inputs/: contains input data files modified for the various scenarios, as well as lists of parameters duplicated in the supplemental information.
- xml/ contains a list of xml queries used to query the GCAM xml db. These only need to be modified if you have a different output folder name.
- build_xml_config.py builds the xml configurations necessary to run a given policy scenario
- 
- constants.py contains a list of constants for use in the project, including the locations for extracting data from the gcam xml db
- data_manipulation.py contains common data manipulation functions for the project output
- data_preprocessing.py will query the xmldb, process data, and verify it against he assumptions
- plotting.py contains code for standard formatting of figures
- plotting_script.py contains the script for processing the data to be plotted and then calling functions from plotting.py to plot the code
- process_GCAM_data.py splits the single .csv file returned from the gcam xml db and splits it by query
- produce_regional_queries.py converts an .xml file with global queries for the gcam model and makes a query for every region. the gcam xml db does not disaggregate global queries by region
- read_GCAM_DB.py reads data from the gcam xml db.
- run_GCAM_scenarios.py automates the entire process, enabling the running of a GCAM scenario, automatic querying of outputs and verification with the push of a single button and a scenario name
- supplementary_figures.py conducts additional analysis, much like plotting_script.py
- utilities.py contains a list of the various input data needed to create each scenario's input files
- verification.py verifies the GCAM model outputs against the inputs to check for model errors.

## Requirements

To run the codes in this repository, the following Python and core package versions must be installed:

    pandas~=2.2.1
    geopandas~=0.14.3
    matplotlib~=3.8.3
    numpy~=1.26.4
    scipy~=1.12.0

    Python ~ 3.11
    GCAM model version 5.4
    GCAM-CDR model version 1.0.0

## Installation Guide and Running a Demo

Recommended installation is from the zenodo link here: TBD.

The GCAM model was run on a HP Pavilion Desktop TP01-3xxx using Microsoft Windows 11 Home, with 64GB of RAM. A typical model run will take ~2 hours to run. Model errors in intermediate steps are common, and may require rerunning the scenario to avoid errors.

Users are expected to be proficient in computer software, include the Python programming languages, as well as the structure of xml files.

To reproduce the GCAM model config xml files that are not altered by policy scenarios, download the GCAM model (http://jgcri.github.io/gcam-doc/index.html) and GCAM-CDR (https://github.com/icrlp/gcam-cdr/tree/main). Then, copy over the modified config files contained in this repository to the same location in the JCGRI GCAM project directory.

Once the GCAM xml files have been built, run gcam/exe/run-gcam-<scenario-name>.bat

The expected output will be a ~3GB .xmldb file. This file will need to be named something like "database_basexdb-<scenario-name>_<baseline pathway>", which are required inputs in constants.py, if the data is to processed properly into .csv format for additional analysis.

The .csv output files can be further processed using data_preprocessing.py to yield the example data in the data folder.

The whole process can be automated by setting a scenario name in run_GCAM_scenarios.py.

## Citation

Please use the following citation when using the data, methods or results of this work:

TBD

## Overview of Global Change Analysis Model (GCAM)

https://github.com/JGCRI/gcam-core

The Joint Global Change Research Institute (JGCRI) is the home and primary development institution for GCAM, an integrated assessment tool for exploring consequences and responses to global change. Climate change is a global issue that impacts all regions of the world and all sectors of the global economy. Thus, any responses to the threat of climate change, such as policies or international agreements to limit greenhouse gas emissions, can have wide ranging consequences throughout the energy system as well as on land use and land cover. Integrated assessment models endeavor to represent all world regions and all sectors of the economy in an economic framework in order to explore interactions between sectors and understand the potential ramifications of climate mitigation actions.

GCAM has been developed at PNNL for over 20 years and is now a freely available community model and documented online (See below). The team at JGCRI is comprised of economists, engineers, energy experts, forest ecologists, agricultural scientists, and climate system scientists who develop the model and apply it to a range of science and policy questions and work closely with Earth system and ecosystem modelers to integrate the human decision components of GCAM into their analyses.
Model Overview

GCAM is a dynamic-recursive model with technology-rich representations of the economy, energy sector, land use and water linked to a climate model that can be used to explore climate change mitigation policies including carbon taxes, carbon trading, regulations and accelerated deployment of energy technology. Regional population and labor productivity growth assumptions drive the energy and land-use systems employing numerous technology options to produce, transform, and provide energy services as well as to produce agriculture and forest products, and to determine land use and land cover. Using a run period extending from 1990 – 2100 at 5 year intervals, GCAM has been used to explore the potential role of emerging energy supply technologies and the greenhouse gas consequences of specific policy measures or energy technology adoption including; CO2 capture and storage, bioenergy, hydrogen systems, nuclear energy, renewable energy technology, and energy use technology in buildings, industry and the transportation sectors. GCAM is an Representative Concentration Pathway (RCP)-class model. This means it can be used to simulate scenarios, policies, and emission targets from various sources including the Intergovernmental Panel on Climate Change (IPCC). Output includes projections of future energy supply and demand and the resulting greenhouse gas emissions, radiative forcing and climate effects of 16 greenhouse gases, aerosols and short-lived species at 0.5×0.5 degree resolution, contingent on assumptions about future population, economy, technology, and climate mitigation policy.

“The Global Change Analysis Model (GCAM) is a multisector model developed and maintained at the Pacific Northwest National Laboratory’s Joint Global Change Research Institute (JGCRI, 2023) <include additional citations to previous GCAM studies as relevant>. GCAM is an open-source community model. In this study, we use GCAM v NN. The documentation of the model is available at the GCAM documentation page (http://jgcri.github.io/gcam-doc) and the description below is a summary. GCAM includes representations of: economy, energy, agriculture, and water supply in 32 geopolitical regions across the globe; their GHG and air pollutant emissions and global GHG concentrations, radiative forcing, and temperature change; and the associated land allocation, water use, and agriculture production across 384 land sub-regions and 235 water basins.
JGCRI, 2023. GCAM Documentation (Version 5.4). https://github.com/JGCRI/gcam-doc. Joint Global Change Research Institute. https://zenodo.org/doi/10.5281/zenodo.11377813.
