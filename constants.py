class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    # TODO: check to ensure that the list of versions and their corresponding file names are the ones you want to
    #  process data for. The filename must be the same between the version and the GCAMDB_ filenames
    version = [["pyrolysis-nofert", "6p0"]] #TODO: updated data is grabbed for 4p5 only
    GCAMDB_filenames = ["data/gcam_out/pyrolysis-nofert/6p0/ref.csv"]

    # TODO: ensure that this strings points to the correct location of the gcam/output/* database
    #  directory names are of the form database_basexdb-<version-name>-<RCP>.
    #  This location should only need to be set once
    XML_DB_loc = "../gcam-sandbox/output/database_basexdb-"
    processed_map_loc = "data/maps/simplified_world_map.shp"

    combines_csv_fnames = ["refined liquids costs by tech", "refined liquids production by tech (new)", "refined liquids production by tech"]

    # other relevant constants
    SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    scenario_names = []
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
    skip_years = 5

    # constants to evaluate IO coefficients
    animal_manure_ratio = dict()
    animal_manure_ratio["pyrolysis", "beef"] = 1/2.589
    animal_manure_ratio["pyrolysis", "dairy"] = 1/0.878
    animal_manure_ratio["pyrolysis", "pork"] = 1/0.304
    animal_manure_ratio["pyrolysis", "poultry"] = 1/1.381
    animal_manure_ratio["pyrolysis", "goat"] = 1/3.101

    manure_biochar_ratio = dict()
    manure_biochar_ratio["pyrolysis", "beef"] = 2.1815
    manure_biochar_ratio["pyrolysis", "dairy"] = 2.1052
    manure_biochar_ratio["pyrolysis", "pork"] = 2.136
    manure_biochar_ratio["pyrolysis", "poultry"] = 2.1276
    manure_biochar_ratio["pyrolysis", "goat"] = 2.055

    manure_biooil_ratio = dict()
    manure_biooil_ratio["pyrolysis", "beef"] = 3.143
    manure_biooil_ratio["pyrolysis", "dairy"] = 2.857
    manure_biooil_ratio["pyrolysis", "pork"] = 2.857
    manure_biooil_ratio["pyrolysis", "poultry"] = 3.846
    manure_biooil_ratio["pyrolysis", "goat"] = 2.857

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
