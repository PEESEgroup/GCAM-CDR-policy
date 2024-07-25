class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    # TODO: check to ensure that the list of versions and their corresponding file names are the ones you want to
    #  process data for. The filename must be the same between the version and the GCAMDB_ filenames
    version = [["test", "2p6"]]
    GCAMDB_filenames = ["data/gcam_out/test/2p6/released.csv"]

    # TODO: ensure that this strings points to the correct location of the gcam/output/* database
    #  directory names are of the form database_basexdb-<version-name>-<RCP>.
    #  This location should only need to be set once
    XML_DB_loc = "gcam/output/database_basexdb-"
    processed_map_loc = "data/maps/simplified_world_map.shp"

    combines_csv_fnames = ["refined liquids costs by tech", "refined liquids production by tech (new)", "refined liquids production by tech"]

    # other relevant constants
    SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    GCAM_region = ["USA", "Africa_Eastern", "Africa_Northern", "Africa_Southern", "Africa_Western", "Australia_NZ",
                   "Brazil", "Canada", "Central America and Caribbean", "Central Asia", "China", "EU-12", "EU-15",
                   "Europe_Eastern", "Europe_Non_EU", "European Free Trade Association", "India", "Indonesia", "Japan",
                   "Mexico", "Middle East", "Pakistan", "Russia", "South Africa", "South America_Northern",
                   "South America_Southern", "South Asia", "South Korea", "Southeast Asia", "Taiwan", "Argentina",
                   "Colombia"]
    missing = "missing"
    column_order = ["1990", "2005", "2010", "2015", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "2055",
                    "2060", "2065", "2070", "2075", "2080", "2085", "2090", "2095", "2100", 'SSP', 'Version',
                    "GCAM", "sector", "subsector", "technology", "output", "concentration", "input", "product",
                    "LandLeaf", "GHG", "Units"]
    world_columns = ['OBJECTID', 'geometry', 'GCAM']
    x = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
    plotting_x = [2025, 2030, 2035, 2040, 2045, 2050]
    future_x = [2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
    biochar_x = [2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
    skip_years = 5

    # constants to evaluate IO coefficients
    animal_manure_ratio = dict()
    animal_manure_ratio["pyrolysis", "beef"] = 1/2.589
    animal_manure_ratio["pyrolysis", "dairy"] = 1/0.878
    animal_manure_ratio["pyrolysis", "pork"] = 1/0.304
    animal_manure_ratio["pyrolysis", "poultry"] = 1/1.381
    animal_manure_ratio["pyrolysis", "goat"] = 1/3.101
    animal_manure_ratio["pyrolysis-nofert", "beef"] = 1/2.589
    animal_manure_ratio["pyrolysis-nofert", "dairy"] = 1/0.018
    animal_manure_ratio["pyrolysis-nofert", "pork"] = 1/0.304
    animal_manure_ratio["pyrolysis-nofert", "poultry"] = 1/1.381
    animal_manure_ratio["pyrolysis-nofert", "goat"] = 1/3.101
    animal_manure_ratio["biochar", "beef"] = 1/2.589
    animal_manure_ratio["biochar", "dairy"] = 1/0.878
    animal_manure_ratio["biochar", "pork"] = 1/0.304
    animal_manure_ratio["biochar", "poultry"] = 1/1.381
    animal_manure_ratio["biochar", "goat"] = 1/3.101
    animal_manure_ratio["test", "beef"] = 1/2.589
    animal_manure_ratio["test", "dairy"] = 1/0.018
    animal_manure_ratio["test", "pork"] = 1/0.304
    animal_manure_ratio["test", "poultry"] = 1/1.381
    animal_manure_ratio["test", "goat"] = 1/3.101

    manure_biochar_ratio = dict()
    manure_biochar_ratio["pyrolysis", "beef"] = 2.1815
    manure_biochar_ratio["pyrolysis", "dairy"] = 2.1052
    manure_biochar_ratio["pyrolysis", "pork"] = 2.136
    manure_biochar_ratio["pyrolysis", "poultry"] = 2.1276
    manure_biochar_ratio["pyrolysis", "goat"] = 2.055
    manure_biochar_ratio["biochar", "beef"] = 2.1815
    manure_biochar_ratio["biochar", "dairy"] = 2.1052
    manure_biochar_ratio["biochar", "pork"] = 2.136
    manure_biochar_ratio["biochar", "poultry"] = 2.1276
    manure_biochar_ratio["biochar", "goat"] = 2.055
    manure_biochar_ratio["test", "beef"] = 2.1815
    manure_biochar_ratio["test", "dairy"] = 2.1052
    manure_biochar_ratio["test", "pork"] = 2.136
    manure_biochar_ratio["test", "poultry"] = 2.1276
    manure_biochar_ratio["test", "goat"] = 2.055

    manure_biooil_ratio = dict()
    manure_biooil_ratio["pyrolysis", "beef manure"] = 0.00477
    manure_biooil_ratio["pyrolysis", "dairy manure"] = 0.00525
    manure_biooil_ratio["pyrolysis", "pork manure"] = 0.00525
    manure_biooil_ratio["pyrolysis", "poultry manure"] = 0.0039
    manure_biooil_ratio["pyrolysis", "goat manure"] = 0.00525
    manure_biooil_ratio["pyrolysis-nofert", "beef manure"] = 0.00124
    manure_biooil_ratio["pyrolysis-nofert", "dairy manure"] = 0.00137
    manure_biooil_ratio["pyrolysis-nofert", "pork manure"] = 0.00137
    manure_biooil_ratio["pyrolysis-nofert", "poultry manure"] = 0.00101
    manure_biooil_ratio["pyrolysis-nofert", "goat manure"] = 0.00137

    biochar_fert_ratio = dict()
    biochar_fert_ratio["pyrolysis", "beef"] = 1/90.9
    biochar_fert_ratio["pyrolysis", "dairy"] = 1/54.34
    biochar_fert_ratio["pyrolysis", "pork"] = 1/44.05
    biochar_fert_ratio["pyrolysis", "poultry"] = 1/12.98
    biochar_fert_ratio["pyrolysis", "goat"] = 1/51.54

    manure_C_ratio = dict()
    manure_C_ratio["pyrolysis", "beef"] = -0.927
    manure_C_ratio["pyrolysis", "dairy"] = -0.583
    manure_C_ratio["pyrolysis", "pork"] = -0.632
    manure_C_ratio["pyrolysis", "poultry"] = -1.073
    manure_C_ratio["pyrolysis", "goat"] = -1.376
    manure_C_ratio["pyrolysis-nofert", "beef"] = -0.273
    manure_C_ratio["pyrolysis-nofert", "dairy"] = -0.273
    manure_C_ratio["pyrolysis-nofert", "pork"] = -0.581
    manure_C_ratio["pyrolysis-nofert", "poultry"] = -.304
    manure_C_ratio["pyrolysis-nofert", "goat"] = -0.273
    manure_C_ratio["biochar", "beef"] = -0.147
    manure_C_ratio["biochar", "dairy"] = -0.147
    manure_C_ratio["biochar", "pork"] = -0.425
    manure_C_ratio["biochar", "poultry"] = -0.160
    manure_C_ratio["biochar", "goat"] = -0.425
    manure_C_ratio["test", "beef"] = -0.147
    manure_C_ratio["test", "dairy"] = -0.147
    manure_C_ratio["test", "pork"] = -0.425
    manure_C_ratio["test", "poultry"] = -0.160
    manure_C_ratio["test", "goat"] = -0.425

    secout = dict()
    secout[2025, "beef manure"] = 0.048325
    secout[2030, "beef manure"] = 0.21
    secout[2035, "beef manure"] = 0.53
    secout[2040, "beef manure"] = 0.95
    secout[2045, "beef manure"] = 1.377
    secout[2050, "beef manure"] = 1.738
    secout[2025, "dairy manure", "pyrolysis-nofert"] = 0.000336
    secout[2030, "dairy manure", "pyrolysis-nofert"] = 0.00146
    secout[2035, "dairy manure", "pyrolysis-nofert"] = 0.003689
    secout[2040, "dairy manure", "pyrolysis-nofert"] = 0.006622
    secout[2045, "dairy manure", "pyrolysis-nofert"] = 0.009577
    secout[2050, "dairy manure", "pyrolysis-nofert"] = 0.012089
    secout[2025, "dairy manure", "pyrolysis"] = 0.0163
    secout[2030, "dairy manure", "pyrolysis"] = 0.0712
    secout[2035, "dairy manure", "pyrolysis"] = 0.1799
    secout[2040, "dairy manure", "pyrolysis"] = 0.3229
    secout[2045, "dairy manure", "pyrolysis"] = 0.4671
    secout[2050, "dairy manure", "pyrolysis"] = 0.5896
    secout[2025, "goat manure"] = 0.0578
    secout[2030, "goat manure"] = 0.2415
    secout[2035, "goat manure"] = 0.635
    secout[2040, "goat manure"] = 1.14
    secout[2045, "goat manure"] = 1.64
    secout[2050, "goat manure"] = 2.08
    secout[2025, "pork manure"] = .00567
    secout[2030, "pork manure"] = 0.0246
    secout[2035, "pork manure"] = 0.0623
    secout[2040, "pork manure"] = 0.111
    secout[2045, "pork manure"] = 0.161
    secout[2050, "pork manure"] = 0.204
    secout[2025, "poultry manure"] = 0.0257
    secout[2030, "poultry manure"] = 0.112
    secout[2035, "poultry manure"] = 0.283
    secout[2040, "poultry manure"] = 0.508
    secout[2045, "poultry manure"] = 0.734
    secout[2050, "poultry manure"] = 0.927
    secout["Soybean"] = 110
    secout["OilCrop"] = 32
    secout["regional corn for ethanol"] = 30
