import pandas as pd
import utilities
import constants


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
    for xml in xml_files_to_build:
        for file in xml.data_files:
            csv = xml.data_files[file]
            if "verify" in file:
                ground_truth = pd.read_csv(csv, skiprows=2)
                if "exo_CDR_demand" in file:
                    pass
                if "elastic_CDR_demand" in file:
                    pass
                if "RES_markets" in file:
                    pass
                if "ghg_constraint" in file:
                    pass
                if "ghg_tax" in file:
                    # query co2 prices
                    results = pd.read_csv(fpath+"/CO2_prices.csv")
                    error_years.extend(verify_ghg_tax(ground_truth, results))
                # TODO: add more file types

    # TODO: update output .csv files based on years with errors


def verify_ghg_tax(ground_truth, results):
    # update ground truth to the results data format
    years_with_error = []
    ground_truth = ground_truth.transpose()
    ground_truth.columns = ground_truth.iloc[0]
    ground_truth.columns = ground_truth.columns.astype(str)
    ground_truth["GCAM"] = ground_truth.iloc[1].unique()[0]
    ground_truth["product"] = ground_truth.iloc[2].unique()[0]
    ground_truth = pd.DataFrame(ground_truth.iloc[3]).transpose()

    # compare ground truths with results
    df = pd.merge(ground_truth, results, "left", ["GCAM", "product"], suffixes=("_left", "_right"))
    for i in constants.GCAMConstants.plotting_x:
        df[str(i)] = df[str(i) + "_left"] - df[str(i) + "_right"]
        if df[str(i)].sum() != 0:
            years_with_error.append(str(i))

    return years_with_error


if __name__ == '__main__':
    main("exoTest_default")
