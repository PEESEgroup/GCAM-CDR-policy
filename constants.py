class GCAMConstants:
    """
    list of constants used in processing data from GCAM models
    """
    #  directory names are of the form database_basexdb-<version-name>-<baseline>.
    XML_DB_loc = "gcam/output/database_basexdb-"
    processed_map_loc = "data/maps/us_reprojected_shp.shp"
    basin_map_loc = "data/maps/reg_glu_boundaries_moirai_combined_3p1_0p5arcmin.shp"

    # other relevant constants
    GCAM_region = ["USA", "Africa_Eastern", "Africa_Northern", "Africa_Southern", "Africa_Western", "Australia_NZ",
                   "Brazil", "Canada", "Central America and Caribbean", "Central Asia", "China", "EU-12", "EU-15",
                   "Europe_Eastern", "Europe_Non_EU", "European Free Trade Association", "India", "Indonesia", "Japan",
                   "Mexico", "Middle East", "Pakistan", "Russia", "South Africa", "South America_Northern",
                   "South America_Southern", "South Asia", "South Korea", "Southeast Asia", "Taiwan", "Argentina",
                   "Colombia"]
    USA_region = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
                   "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                   "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    missing = "missing"
    column_order = ["1990", "2005", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "scenario", "baseline",
                    "GCAM", "sector", "subsector", "technology", "output", "concentration", "input",
                    "product", "fuel", "LandLeaf", "GHG", "Units"]
    csv_columns = ["1990", "2005", "2010", "2015", "2020", "2025", "2030", "2035", "2040", "2045", "2050", "2055",
                    "2060", "2065", "2070", "2075", "2080", "2085", "2090", "2095", "2100", 'Version', "Units"]
    world_columns = ['OBJECTID', 'geometry', 'GCAM']
    x = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085,
         2090, 2095, 2100]
    plotting_x = [2025, 2030, 2035, 2040, 2045, 2050]

    scenario_names = ["exoTest"]
    baseline_names = ["default"]
