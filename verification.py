import pandas as pd
import math
import data_manipulation
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
    # TODO: why does CDR by tech only include info for the US states??? - might have to change results .csv - check model_interface
    results = pd.read_csv(fpath + "/CDR_by_tech.csv")
    years_with_error = []
    exo_CDR_demand = pd.DataFrame()
    elastic_CDR_demand = pd.DataFrame()
    links_ground_truth = pd.DataFrame()
    region_market = pd.DataFrame()

    # split up CDR dictionary
    for i in CDR:
        if "linked_ghg_CDR" in i:
            links_ground_truth = pd.read_csv(CDR[i], skiprows=2)
            region_market = links_ground_truth[["region", "market"]]
        if "exo_CDR" in i:
            exo_CDR_demand = pd.read_csv(CDR[i], skiprows=2)
            exo_CDR_demand = exo_CDR_demand.pivot(index='region', columns='year')['demand'].reset_index()
            exo_CDR_demand.columns = exo_CDR_demand.columns.astype(str)
            exo_CDR_demand["Units"] = "Mt"
            exo_CDR_demand = exo_CDR_demand.groupby(["Units"]).sum(min_count=1).reset_index()
        if "elastic_CDR" in i:
            elastic_CDR_demand = get_elastic_CDR_demand(CDR, fpath, i, region_market)

    # combine CDR sources to get estimated CDR demand
    if exo_CDR_demand.empty:
        CDR_demand = elastic_CDR_demand
    elif elastic_CDR_demand.empty:
        CDR_demand = exo_CDR_demand
    else:
        CDR_demand = pd.merge(exo_CDR_demand, elastic_CDR_demand)

    # process ground truth CDR numbers
    if not links_ground_truth.empty:
        # move unsatisfied CDR demand to its own output .csv file
        unsatisfied_CDR = results[results["subsector"] == "unsatisfiedDemand"]
        satisfied_CDR = results[results["subsector"] != "unsatisfiedDemand"]
        unsatisfied_CDR.to_csv(fpath + "/unsatisfied_CDR_demand.csv")

        # add market information to the results
        satisfied_CDR = pd.merge(satisfied_CDR, region_market, "left", left_on="GCAM", right_on="region")

        # group by market and technology
        data_manipulation.group(satisfied_CDR, ["GCAM"]).to_csv(fpath + "/satisfied_CDR_demand_by_region.csv")
        data_manipulation.group(satisfied_CDR, ["technology"]).to_csv(fpath + "/satisfied_CDR_demand_by_tech.csv")
        satisfied_CDR = data_manipulation.group(satisfied_CDR, ["market"])
        satisfied_CDR["product"] = "CDR"

        # compare ground truths with results
        df = pd.merge(CDR_demand, satisfied_CDR, "left", ["Units"], suffixes=("_left", "_right"))
        # because this is one line of data
        df = df.iloc[0]
        for i in constants.GCAMConstants.plotting_x:
            # if the estimated value is not close to the reported value
            if .97 * df[str(i) + "_right"] < df[str(i) + "_left"] < 1.03 * df[str(i) + "_right"]:
                print("CDR demand matches CDR supply by " + str(df[str(i) + "_left"] - df[str(i) + "_right"]))
            else:
                years_with_error.append(str(i))
                log(fpath, str(i),
                    "CDR demand does not match CDR supply by " + str(df[str(i) + "_left"] - df[str(i) + "_right"]))

    return years_with_error


def get_elastic_CDR_demand(CDR, fpath, i, region_market):
    elastic_ground_truth = pd.read_csv(CDR[i], skiprows=2)
    # read in carbon prices
    carbon_prices = pd.read_csv(fpath + "/CO2_prices.csv")
    # merge carbon prices into elastic demand df
    elastic_ground_truth = pd.merge(elastic_ground_truth, region_market, "left", left_on="region",
                                    right_on="region")
    elastic_ground_truth = pd.merge(elastic_ground_truth, carbon_prices, "left", left_on="market",
                                    right_on="GCAM")
    # only look at actual carbon prices
    elastic_ground_truth = elastic_ground_truth[elastic_ground_truth["product"] == "CO2"]
    elastic_ground_truth.columns = elastic_ground_truth.columns.astype(str)
    # calculate elastic ground truth
    # TODO: finish verifying elastic ground truth data
    for j in constants.GCAMConstants.plotting_x:
        elastic_ground_truth[str(j)] = elastic_ground_truth.apply(lambda row: get_elastic_demand(row, str(j)),
                                                                  axis=1)
    return elastic_ground_truth


def get_elastic_demand(row, i):
    # TODO: fix calculation
    if row[str(i)] < row["min-price"] + 0.001:
        return 0
    else:
        print((0-row["steepness"]))
        print((row[str(i)] - row["midpoint"]))
        print(1 + math.exp((0-row["steepness"]) * (row[str(i)] - row["midpoint"])))
        return row["max-demand"] / 1 + math.exp((0-row["steepness"]) * (row[str(i)] - row["midpoint"]))


def verify_ghg_tax(ground_truth, results, fpath):
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
        # TODO: update this log check
        if .97 * df[str(i) + "_right"] < df[str(i) + "_left"] < 1.03 * df[str(i) + "_right"]:
            years_with_error.append(str(i))
            log(fpath, str(i), "ghg taxes do not match")

    return years_with_error


def log(fpath, year, reason):
    with open(fpath + "/log.txt", "a+") as f:
        print("Verification fails in " + year + " because " + reason)
        f.write("Verification fails in " + year + " because " + reason + "\n")


if __name__ == '__main__':
    main("test_default")
