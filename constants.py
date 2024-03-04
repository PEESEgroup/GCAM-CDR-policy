class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    # TODO: check to ensure that the list of versions and their corresponding file names
    #  are the ones you want to process data for
    version = [["pyrolysis", "4p5"], ["released", "4p5"]] #TODO: updated data is grabbed for 4p5 only
    GCAMDB_filenames = ["data/gcam_out/pyrolysis/4p5/ref.csv", "data/gcam_out/released/4p5/ref.csv"]

    # TODO: ensure this list of products contains all products that we are interested in.
    #  More can be added to the list, but must reference the product name in GCAM
    products = ["beef manure", "dairy manure", "poultry manure", "pork manure", "goat manure", "manure fuel feedstock",
                "manure fuel", "beef_biochar", "dairy_biochar", "poultry_biochar", "pork_biochar", "goat_biochar",
                "Beef", "Dairy", "Pork", "Poultry", "SheepGoat", "regional beef", "regional dairy", "regional pork",
                "regional poultry", "regional sheepgoat", "N fertilizer", "refined liquids enduse", "CO2_LUC",
                "CO2_NearTerm", "CO2", "crude oil", "electricity", "natural gas"]

    # TODO: ensure that this strings points to the correct location of the gcam/output/* database
    #  directory names are of the form database_basexdb-<version-name>
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
