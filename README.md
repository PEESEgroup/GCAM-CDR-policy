# Manure Pyrolysis IAM

This study uses the Global Change Analysis Model (GCAM) integrated assessment model (IAM) to analyze the impact on food, energy, land use, and climate sectors from the introduction of pyrolysis of animal manures in 2050. The project has 2 folders:

    data
    xml

## Locations

Global (32 GCAM regions)

## Files overview

The root folder contains the Python scripts used in the study. There are nine Python scripts and two folders. Details of each file or folder is provided below:

- data/: This folder contains four folders
  - data_analysis/ contains the excel file for minor results calculations
  - gcam_out/ contains the extracted data from the gcam xml db. 
    - /released/ contains the results from the released version of the model. 
    - /pyrolysis/ contains the results from the pyrolysis versions of the model, with pyrolysis with land application modeled as an N fertilizer and bio-oil as a secondary output. 
    - /pyrolysis-nofert/ models bio-oil as primary output with no application of biochar 
      - /RCP/ is indicated in the next subfolder level
        - /masked/ contains the masked data with errors removed in data from 2025-2050
        - /original/ contains the original data extracted from the GCAM database
        - ref.csv is the output from the database query
        - mask_log.txt contains the list of errors found in the model output
  - maps/ contains map shapefiles for plotting
- gcam-sandbox contains all of the necessary files with modifications to the GCAM model. This is intended to supplement the v7 release, and does not contain all necessary files to run the GCAM model
- xml/ contains a list of xml queries used to query the GCAM xml db.
- check_IO_coef.py checks to ensure that primary and secondary output coefficients are valid to check post-hoc for modeling errors, and remove that data from any subsequent analysis
- constants.py contains a list of constants for use in the project, including the locations for extracting data from the gcam xml db
- data_manipulation.py contains common data manipulation function for the project
- plotting.py contains code for plotting the figures
- plotting_script.py contains the script for processing the data to be plotted and then calling functions from plotting.py to plot the code
- process_data.py is a short script to read data from the gcam xml db and write out .csv files to teh data/gcam_out/ folder
- process_GCAM_data.py splits the single .csv file returned from the gcam xml db and splits it by query
- produce_regional_queries.py converts an .xml file with global queries for the gcam model and makes a query for every region. the gcam xml db does not disaggregate global queries by region
- read_GCAM_DB.py reads data from the gcam xml db.
- stats.py conducts statistics on price linkages between sectors. This code is not used in any of the publications.

## Requirements

To run the codes in this repository, the following Python and core package versions must be installed:

    pandas~=2.2.1
    statsmodels~=0.14.1
    geopandas~=0.14.3
    matplotlib~=3.8.3
    scipy~=1.12.0
    numpy~=1.26.4
    GCAM model version 7.0

## Running the code

To reproduce the figures, run plotting_script.py. Feel free to use the existing data and methods as examples to draw new figures.

To reproduce the GCAM model results, download the GCAM model (http://jgcri.github.io/gcam-doc/index.html), follow the installation guide, replace the old files with the files found in /gcam-sandbox/, use /gcam-sandbox/input/<scenario>_R_files/<config>.R to update the GCAM input xml files, but some files may need to already exist), rebuild the project in R to update the GCAM xml files, and let the model solve. Different policy scenarios are available. Then, use process_data.py and the ModelInterface application (needs to be on the path) to extract the data from the database.

## Citation

Please use the following citation when using the data, methods or results of this work:

TBD

## Overview of Global Change Analysis Model (GCAM)

https://github.com/JGCRI/gcam-core

The Joint Global Change Research Institute (JGCRI) is the home and primary development institution for GCAM, an integrated assessment tool for exploring consequences and responses to global change. Climate change is a global issue that impacts all regions of the world and all sectors of the global economy. Thus, any responses to the threat of climate change, such as policies or international agreements to limit greenhouse gas emissions, can have wide ranging consequences throughout the energy system as well as on land use and land cover. Integrated assessment models endeavor to represent all world regions and all sectors of the economy in an economic framework in order to explore interactions between sectors and understand the potential ramifications of climate mitigation actions.

GCAM has been developed at PNNL for over 20 years and is now a freely available community model and documented online (See below). The team at JGCRI is comprised of economists, engineers, energy experts, forest ecologists, agricultural scientists, and climate system scientists who develop the model and apply it to a range of science and policy questions and work closely with Earth system and ecosystem modelers to integrate the human decision components of GCAM into their analyses.
Model Overview

GCAM is a dynamic-recursive model with technology-rich representations of the economy, energy sector, land use and water linked to a climate model that can be used to explore climate change mitigation policies including carbon taxes, carbon trading, regulations and accelerated deployment of energy technology. Regional population and labor productivity growth assumptions drive the energy and land-use systems employing numerous technology options to produce, transform, and provide energy services as well as to produce agriculture and forest products, and to determine land use and land cover. Using a run period extending from 1990 – 2100 at 5 year intervals, GCAM has been used to explore the potential role of emerging energy supply technologies and the greenhouse gas consequences of specific policy measures or energy technology adoption including; CO2 capture and storage, bioenergy, hydrogen systems, nuclear energy, renewable energy technology, and energy use technology in buildings, industry and the transportation sectors. GCAM is an Representative Concentration Pathway (RCP)-class model. This means it can be used to simulate scenarios, policies, and emission targets from various sources including the Intergovernmental Panel on Climate Change (IPCC). Output includes projections of future energy supply and demand and the resulting greenhouse gas emissions, radiative forcing and climate effects of 16 greenhouse gases, aerosols and short-lived species at 0.5×0.5 degree resolution, contingent on assumptions about future population, economy, technology, and climate mitigation policy.

