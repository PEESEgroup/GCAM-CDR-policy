import pandas as pd
import utilities


def main(scenario_name):
    # get a list of files that need verification
    xml_files_to_build = utilities.build_from_scenario(scenario_name)
    files_to_verify = {}

    # location of output data
    directory = str(scenario_name).replace("_", "/")
    prefix = "./data/gcam_out/"
    fpath = prefix + directory

    # don't do data analysis on years with errors
    error_years = []

    # TODO: may need to group certain types of files (i.e. CDR demand) together
    for file in xml_files_to_build:
        data = utilities.open_csv(file.data_files)
        for key in data:
            if "verify" in key:
                # TODO: replace with pd.read_csv
                ground_truth = pd.DataFrame.from_dict(data[key]).transpose().reset_index()
                if "exo_CDR_demand" in key:
                    pass
                if "elastic_CDR_demand" in key:
                    pass
                if "RES_markets" in key:
                    pass
                if "ghg_constraint" in key:
                    pass
                if "ghg_tax" in key:
                    # query co2 prices
                    results = pd.read_csv(fpath+"/CO2_prices.csv")
                    error_years.extend(verify_ghg_tax(ground_truth, results))
                # TODO: add more file types

    # TODO: update output .csv files based on years with errors


def verify_ghg_tax(ground_truth, results):
    # TODO: compare ground_truth with the results and identify if any of the years have an error
    years_with_error = []
    return years_with_error


if __name__ == '__main__':
    main("BECCSRESTest_default")
