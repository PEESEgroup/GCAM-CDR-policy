PFAL-DRL

This study uses artificial intelligence and computational modeling to analyze the dynamic complexity of plant-environment interactions across ten diverse locations worldwide, each with distinct climate conditions, and the potential to reduce resource consumption in plant factories with artificial lighting (PFALs). There is one folder in this repository:

    codes

Locations

Miami (Florida), Phoenix (Arizona), Los Angeles (California), Seattle (Washington), Chicago (Illinois), Milwaukee (Wisconsin), Fargo (North Dakota), Ithaca (New York), Reykjavik (Iceland), and Dubai (United Arab Emirates).
Codes

This folder contains the Python scripts used in the study. There are six Python scripts and one folder. Details of each file or folder is provided below:

    log/: This folder contains the trained neural network model as well as the training results
    PFALEnv.py: This file contains the PFAL model, reward function, etc. and follows the gymnasium custom environment conventions
    baseline_test.py: This file runs a single outdoor condition case using the baseline
    conventional_control.py: This file is Baseline module configuration
    drl_based_control.py: This file is the DRL module configuration and contains the training and the online inference functions
    drl_test.py: This file runs a single outdoor condition case using DRL
    main_simulation.py: This file runs year long simulation for a particular location with either baseline or DRL. The outdoor weather information are provided in this file

Requirements

To run the codes in this repository, the following Python and core package versions must be installed:

    Python 3.10.9
    Pytorch 2.0.0
    Tianshou 0.5.0
    Gymnasium 0.28.1
    Scipy 1.10.1
    Numpy 1.23.5
    Matplotlib 3.7.2

Running the code
Running code for single growing period (28 days)

The files drl_test.py and baseline_test.py are used to run a simulation for a single growing period (28 days) using the DRL strategy and the baseline strategy respectively. To run either of the files, simply create an instance of the PFAL environment with the mean monthly outdoor temperature and outdoor relative humidity values, that is env = PFALEnv(23, 0.79), and run the respective file.
Running code for twelve growing periods (one year)

The file main_simulation.py is used to run a year-long simulation for a given location and environmental regulation system. The function simulate(a,b,c) where a is a LIST containing the monthly outdoor location data, b is a STRING indicating either 'drl' or 'baseline', and c is a STRING indicating the name of the location for data storage. An example usage is data = simulate(weather_conditions_ithaca, 'drl', 'ithaca').
Citation

Please use the following citation when using the data, methods or results of this work:

Decardi-Nelson, B., You, F. Harnessing AI to boost energy savings in plant factories for sustainable food production. Submitted to Nature Food.


Global Change Analysis Model (GCAM)

The Joint Global Change Research Institute (JGCRI) is the home and primary development institution for GCAM, an integrated assessment tool for exploring consequences and responses to global change. Climate change is a global issue that impacts all regions of the world and all sectors of the global economy. Thus, any responses to the threat of climate change, such as policies or international agreements to limit greenhouse gas emissions, can have wide ranging consequences throughout the energy system as well as on land use and land cover. Integrated assessment models endeavor to represent all world regions and all sectors of the economy in an economic framework in order to explore interactions between sectors and understand the potential ramifications of climate mitigation actions.

GCAM has been developed at PNNL for over 20 years and is now a freely available community model and documented online (See below). The team at JGCRI is comprised of economists, engineers, energy experts, forest ecologists, agricultural scientists, and climate system scientists who develop the model and apply it to a range of science and policy questions and work closely with Earth system and ecosystem modelers to integrate the human decision components of GCAM into their analyses.
Model Overview

GCAM is a dynamic-recursive model with technology-rich representations of the economy, energy sector, land use and water linked to a climate model that can be used to explore climate change mitigation policies including carbon taxes, carbon trading, regulations and accelerated deployment of energy technology. Regional population and labor productivity growth assumptions drive the energy and land-use systems employing numerous technology options to produce, transform, and provide energy services as well as to produce agriculture and forest products, and to determine land use and land cover. Using a run period extending from 1990 – 2100 at 5 year intervals, GCAM has been used to explore the potential role of emerging energy supply technologies and the greenhouse gas consequences of specific policy measures or energy technology adoption including; CO2 capture and storage, bioenergy, hydrogen systems, nuclear energy, renewable energy technology, and energy use technology in buildings, industry and the transportation sectors. GCAM is an Representative Concentration Pathway (RCP)-class model. This means it can be used to simulate scenarios, policies, and emission targets from various sources including the Intergovernmental Panel on Climate Change (IPCC). Output includes projections of future energy supply and demand and the resulting greenhouse gas emissions, radiative forcing and climate effects of 16 greenhouse gases, aerosols and short-lived species at 0.5×0.5 degree resolution, contingent on assumptions about future population, economy, technology, and climate mitigation policy.
Documentation

    GCAM Documentation
    Getting Started with GCAM
    GCAM Community
    GCAM Videos and Tutorial Slides
