import pandas as pd

import utilities


def main(scenario_name, config_fname):
    # get a list of files that need verification
    xml_files_to_build = utilities.build_from_scenario(scenario_name)
    files_to_verify = {}
    dir = str(config_fname).replace("_", "/")
    prefix = "./data/gcam_out/"
    fpath = prefix+dir

    # TODO: may need to group certain types of files (i.e. CDR demand) together
    for file in xml_files_to_build:
        for key, value in file.data_files:
            if "verify" in str(value).lower():
                files_to_verify[key] = value

    # for each file to verify, open the original .csv file and extract relevant data
    for key, value in files_to_verify:
        ground_truth = utilities.open_csv(value)
        # TODO: convert from dict to pd dataframe

        if key == "exo_CDR_demand":
            pass
        if key == "elastic_CDR_demand":
            pass
        if key == "RES_markets":
            pass
        if key == "ghg_constraint":
            pass
        if key == "ghg_tax":
            # TODO: query CO2 results
            results = pd.read_csv(fpath+"CO2_prices.csv")
            verify_ghg_tax(ground_truth, results)
        # TODO: add more file types


def verify_ghg_tax(ground_truth, results):
    # TODO: compare ground_truth with the results and identify if any of the years have an error
    years_with_error = []
    return years_with_error


if __name__ == '__main__':
    main("alteredTest_default")