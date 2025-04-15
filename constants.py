class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    # TODO: check to ensure that the list of versions and their corresponding file names are the ones you want to
    #  process data for. The filename must be the same between the version and the GCAMDB_ filenames

    version = [["Baseline", "baseline"],
               ["HighBiocharCost", "baseline"],
               ["HighBiocharNUE", "baseline"],
               #["HighBiocharNutrients", "baseline"],  # error
               ["HighBiocharSoilN2O", "baseline"],
               ["HighBiocharYield", "baseline"],
               ["HighCropYield", "baseline"],
               ["HighGCAMLandShare", "baseline"],
               ["HighGCAMManurePrice", "baseline"],
               ["LowBiocharNutrients", "baseline"],
               ["LowBiocharCost", "baseline"],
               ["LowBiocharNUE", "baseline"],
               ["LowBiocharSoilN2O", "baseline"],
               ["LowBiocharYield", "baseline"],
               ["LowCropYield", "baseline"],
               ["LowGCAMLandShare", "baseline"],
               ["LowGCAMManurePrice", "baseline"]]
    GCAMDB_filenames = ["data/gcam_out/Baseline/baseline/ref.csv",
                        "data/gcam_out/HighBiocharCost/baseline/ref.csv",
                        "data/gcam_out/HighBiocharNUE/baseline/ref.csv",
                        #"data/gcam_out/HighBiocharNutrients/baseline/ref.csv",  # error
                        "data/gcam_out/HighBiocharSoilN2O/baseline/ref.csv",
                        "data/gcam_out/HighBiocharYield/baseline/ref.csv",
                        "data/gcam_out/HighCropYield/baseline/ref.csv",
                        "data/gcam_out/HighGCAMLandShare/baseline/ref.csv",
                        "data/gcam_out/HighGCAMManurePrice/baseline/ref.csv",
                        "data/gcam_out/LowBiocharNutrients/baseline/ref.csv",
                        "data/gcam_out/LowBiocharCost/baseline/ref.csv",
                        "data/gcam_out/LowBiocharNUE/baseline/ref.csv",
                        "data/gcam_out/LowBiocharSoilN2O/baseline/ref.csv",
                        "data/gcam_out/LowBiocharYield/baseline/ref.csv",
                        "data/gcam_out/LowCropYield/baseline/ref.csv",
                        "data/gcam_out/LowGCAMLandShare/baseline/ref.csv",
                        "data/gcam_out/LowGCAMManurePrice/baseline/ref.csv"]

    # TODO: ensure that this strings points to the correct location of the gcam/output/* database
    #  directory names are of the form database_basexdb-<version-name>-<RCP>.
    #  This location should only need to be set once
    XML_DB_loc = "gcam/output/database_basexdb-"
    processed_map_loc = "data/maps/simplified_world_map.shp"

    # other relevant constants
    SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    RCPs = ["6p0", "4p5", "3p7", "2p6", "1p9"]
    GCAM_region = ["USA", "Africa_Eastern", "Africa_Northern", "Africa_Southern", "Africa_Western", "Australia_NZ",
                   "Brazil", "Canada", "Central America and Caribbean", "Central Asia", "China", "EU-12", "EU-15",
                   "Europe_Eastern", "Europe_Non_EU", "European Free Trade Association", "India", "Indonesia", "Japan",
                   "Mexico", "Middle East", "Pakistan", "Russia", "South Africa", "South America_Northern",
                   "South America_Southern", "South Asia", "South Korea", "Southeast Asia", "Taiwan", "Argentina",
                   "Colombia"]
    missing = "missing"
    column_order = ["1990", "2005", "2010", "2015", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "2055",
                    "2060", "2065", "2070", "2075", "2080", "2085", "2090", "2095", "2100", 'SSP', 'Version',
                    "GCAM", "sector", "subsector", "technology", "output", "concentration", "input", "product", "fuel",
                    "LandLeaf", "GHG", "Units"]
    world_columns = ['OBJECTID', 'geometry', 'GCAM']
    x = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085,
         2090, 2095, 2100]
    plotting_x = [2025, 2030, 2035, 2040, 2045, 2050]
    future_x = [2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
    biochar_x = [2040, 2045, 2050, 2055, 2060]
    skip_years = x.index(biochar_x[0])

    # constants to evaluate IO coefficients
    manure_C_ratio = dict()
    manure_C_ratio["beef"] = -0.459
    manure_C_ratio["dairy"] = -0.459
    manure_C_ratio["pork"] = -0.522
    manure_C_ratio["poultry"] = -0.522
    manure_C_ratio["goat"] = -0.526

