class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    # TODO: check to ensure that the list of versions and their corresponding file names are the ones you want to
    #  process data for. The filename must be the same between the version and the GCAMDB_ filenames

    version = [["test", "baseline"]]
    GCAMDB_filenames = ["data/gcam_out/test/baseline/ref.csv"]

    # TODO: ensure that this strings points to the correct location of the gcam/output/* database
    #  directory names are of the form database_basexdb-<version-name>-<RCP>.
    #  This location should only need to be set once
    XML_DB_loc = "gcam/output/database_basexdb-"
    # TODO: get US state map
    processed_map_loc = "data/maps/simplified_world_map.shp"
    basin_map_loc = "data/maps/reg_glu_boundaries_moirai_combined_3p1_0p5arcmin.shp"

    # other relevant constants
    SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    RCPs = ["6p0", "4p5", "3p7", "2p6", "1p9"]
    GCAM_region = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                   "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                   "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    missing = "missing"
    column_order = ["1990", "2005", "2010", "2015", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "2055",
                    "2060", "2065", "2070", "2075", "2080", "2085", "2090", "2095", "2100", 'SSP', 'Version',
                    "GCAM", "sector", "subsector", "technology", "output", "concentration", "input", "product", "fuel",
                    "LandLeaf", "GHG", "Units"]
    csv_columns = ["1990", "2005", "2010", "2015", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "2055",
                    "2060", "2065", "2070", "2075", "2080", "2085", "2090", "2095", "2100", 'Version', "Units"]
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

