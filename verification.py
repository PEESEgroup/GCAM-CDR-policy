import pandas as pd
import utilities
import constants


def main(scenario_name):
    """
    verify GCAM model outputs
    :param scenario_name: name of the scenario for verification
    :return: N/A
    """
    # get a list of files that need verification
    xml_files_to_build = utilities.build_from_scenario(scenario_name)
    files_to_verify = {}

    # location of output data
    directory = str(scenario_name).replace("_", "/")
    prefix = "./data/gcam_out/"
    fpath = prefix + directory

    # don't do data analysis on years with errors
    error_years = []

    # group certain types of files (i.e. CDR demand) together
    csvs = {}
    CDR = {}
    for xml in xml_files_to_build:
        for file in xml.data_files:
            csv = xml.data_files[file]
            if "verify" in file:
                if "CDR" in file:
                    CDR[file] = csv
                else:
                    csvs[file] = csv

    verify_cdr(CDR, fpath)

    for csv in csvs:
        ground_truth = pd.read_csv(csvs[csv], skiprows=2)
        if "RES_markets" in csv:
            pass
        if "ghg_constraint" in csv:
            pass
        if "ghg_tax" in csv:
            # query co2 prices
            results = pd.read_csv(fpath+"/CO2_prices.csv")
            error_years.extend(verify_ghg_tax(ground_truth, results))
                # TODO: add more file types

    # TODO: update output .csv files based on years with errors


def verify_cdr(CDR, fpath):
    """
    verify ghg tax values
    :param CDR: a list of files necessary to validate CDR output
    :return: a list of years in which an error was detected
    """
    results = pd.read_csv(fpath + "/CDR_by_tech.csv")
    years_with_error = []
    exo_ground_truth = pd.DataFrame()
    elastic_ground_truth = pd.DataFrame()
    links_ground_truth = pd.DataFrame()

    # split up CDR dictionary
    for i in CDR:
        if "exo_CDR" in i:
            exo_ground_truth = pd.read_csv(CDR[i], skiprows=2)
        if "elastic_CDR" in i:
            elastic_ground_truth = pd.read_csv(CDR[i], skiprows=2)
        if "linked_ghg_CDR" in i:
            links_ground_truth = pd.read_csv(CDR[i], skiprows=2)

    # if there is exogenous demand, verify it
    if not exo_ground_truth.empty:
        config_regions = exo_ground_truth['region'].unique()
        gt_dfs = {}

        # sort GCAM regions by linkage file
        if not links_ground_truth.empty:
            region_market = links_ground_truth[["region", "market"]]

            # TODO: drop unsatisfied CDR demand
            # TODO: add market information to the results
            # TODO: group by market and sector

        # compare ground truths with results
        df = pd.merge(ground_truth, results, "left", ["GCAM", "product"], suffixes=("_left", "_right"))
        for i in constants.GCAMConstants.plotting_x:
            df[str(i)] = df[str(i) + "_left"] - df[str(i) + "_right"]
            if df[str(i)].sum() != 0:
                years_with_error.append(str(i))
                # TODO: add print statement and log to a file somewhere

    return years_with_error


def verify_ghg_tax(ground_truth, results):
    """
    verify ghg tax values
    :param ground_truth: the values in the input file
    :param results: the values in the GCAM model output
    :return: a list of years in which an error was detected
    """
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
            # TODO: add print statement and log to a file somewhere

    return years_with_error


def log(year, reason):
    pass



if __name__ == '__main__':
    main("test_default")
