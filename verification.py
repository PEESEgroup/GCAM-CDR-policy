import pandas as pd
import math
import data_manipulation
import process_GCAM_data
import utilities
import constants


def main(scenario_name):
    """
    verify GCAM model outputs
    :param scenario_name: name of the scenario for verification
    :return: N/A
    """
    # get a list of files that need verification
    files = scenario_name.split("_")
    xml_files_to_build = []
    for i in files:
        xml_files_to_build.extend(utilities.build_from_scenario(str(i)))

    # location of output data
    directory = str(scenario_name).replace("_", "/")
    prefix = "./data/gcam_out/"
    fpath = prefix + directory

    # clear log file
    with open(fpath + "/log.txt", "w+") as f:
        f.write("")

    # don't do data analysis on years with errors
    error_years = []

    # group certain types of files (i.e. CDR demand) together
    csvs = {}
    CDR = {}
    links = {}
    for xml in xml_files_to_build:
        for file in xml.data_files:
            csv = xml.data_files[file]
            if "verify" in file:
                if "CDR" in file:
                    CDR[file] = csv
                else:
                    csvs[file] = csv
            if "link" in file:
                links_ground_truth = pd.read_csv(csv, skiprows=2)
                if "sector" in links_ground_truth.columns:
                    links[file] = links_ground_truth
                else:
                    links[file] = links_ground_truth[["region", "market"]]

    # verify CDR demand
    error_years.extend(verify_cdr(CDR, links, fpath))

    for csv in csvs:
        ground_truth = pd.read_csv(csvs[csv], skiprows=2)
        if "RES_markets" in csv:
            error_years.extend(verify_beccs(csvs[csv], fpath))
        if "ghg_constraint" in csv:
            error_years.extend(verify_ghg_constraint(ground_truth, links["ghg_CDR_market_link"], fpath))
        if "ghg_tax" in csv:
            # query co2 prices
            results = pd.read_csv(fpath+"/CO2_prices.csv")
            error_years.extend(verify_ghg_tax(ground_truth, results, fpath))
        if "subsidy" in csv:
            error_years.extend(verify_subsidy(ground_truth, links, fpath))
        # TODO: add more file types

    # update output .csv files based on years with errors
    process_GCAM_data.masking(scenario_name, error_years)


def verify_non_input_tech_costs(ground_truth, links, fpath):
    """
    verifies the data for the non-input costs for CDR technologies
    :param ground_truth: data used for configuration
    :param links: links between markets and ground truths
    :param fpath: link to the directory where output data is stored
    :return: list of years that have errors
    """
    # format results
    results = pd.read_csv(fpath + "/costs_by_tech_and_input.csv")
    years_with_error = []

    # format ground truth
    for i in constants.GCAMConstants.plotting_x:
        ground_truth[str(i)] = ground_truth[str(i)] * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC
    ground_truth["Units"] = "1975$/kg C"
    results = results[results["input"] == "non-energy"]

    # merge results and ground truth
    merge = pd.merge(results, ground_truth, "inner", on="technology", suffixes=("_l", "_r"))
    for i in constants.GCAMConstants.plotting_x:
        # check that minimum price is satisfied with converted units
        merge[str(i)] = merge[str(i) + "_l"] - merge[str(i) + "_r"]
        if not ((merge[str(i)] <= 1e-4) & (merge[str(i)] >= -1e-4)).all():
            errors = merge[~((merge[str(i)] <= 1e-4) & (merge[str(i)] >= -1e-4))]
            years_with_error.append(str(i))
            #TODO: find out what is going on with OEW lime prices
            log(fpath, str(i), "Non-input energy costs are invalid for " + str(errors["sector"].unique()))

    return years_with_error


def verify_subsidy(ground_truth, links, fpath):
    """
    verifies the presences of subsidies on technologies
    :param ground_truth: data in the config files
    :param links: links of ground truth data to technologies
    :param fpath: filepath of gcam output data
    :return: list of years with error
    """
    # format results
    product = ground_truth["stub-technology"].unique()[0] + "_subsidy"
    link = links[product+"_link"]
    results = pd.read_csv(fpath + "/prices_of_all_markets.csv")
    results = results[results["product"] == product]
    years_with_error = []

    # format ground truth
    ground_truth = ground_truth.pivot(index='market', columns='year')['fixedTax'].reset_index()
    ground_truth.columns = ground_truth.columns.astype(str)
    ground_truth["Units"] = "Mt"

    # merge results and ground truth
    merge = pd.merge(results, ground_truth, "left", left_on="GCAM", right_on="market", suffixes=("_l", "_r"))
    for i in constants.GCAMConstants.plotting_x:
        # check that minimum price is satisfied with converted units
        merge[str(i)] = merge[str(i)+"_l"] - (merge[str(i)+"_r"] * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC)
        if not ((merge[str(i)] <= 1e-4) & (merge[str(i)] >= -1e-4)).all():
            years_with_error.append(str(i))
            log(fpath, str(i), "Subsidy for " + str(product) + " is incorrect in " + str(i))

    return years_with_error


def verify_ghg_constraint(ground_truth, regions_map, fpath):
    """
    verifies ghg constraints
    :param ground_truth: the data used in the gcam config file
    :param regions_map: maps regions to gcam emissions markets
    :param fpath: location of the output data in the directory
    :return: list of years with errors
    """
    years_with_error = []
    results = pd.read_csv(fpath + "/CO2_emissions_by_sector.csv")

    # reformat ground truth
    ground_truth = ground_truth.pivot(index='market', columns='year')['constraint'].reset_index()
    ground_truth.columns = ground_truth.columns.astype(str)
    ground_truth["Units"] = "Mt"

    # regional CDR does not count toward C pricing, but it does count towards emissions in the economy

    # categorize by market
    results = pd.merge(results, regions_map, "left", left_on="GCAM", right_on="region")
    ground_truth = pd.merge(ground_truth, regions_map, "left", left_on="market", right_on="region", suffixes=("_x", ""))
    results = results.groupby(["market", "scenario", "baseline", "Units"]).sum(min_count=1).reset_index()

    # merge dataframes
    comparison = pd.merge(ground_truth, results, "left", on="market", suffixes=("_g", "_r"))

    for index, row in comparison.iterrows():
        df = comparison.iloc[index].copy(deep=True)
        for i in constants.GCAMConstants.plotting_x:
            # unit conversion
            df[str(i) + "_g"] = df[str(i) + "_g"] * constants.GCAMConstants.CO2_to_C
            # if the estimated value is not close to the reported value
            if .99 * df[str(i) + "_r"] < df[str(i) + "_g"]:
                print("GHG constraint for " + df["market"] + " in " + str(i) + " meets the constraint by " + str(df[str(i) + "_g"] - df[str(i) + "_r"]))
            else:
                years_with_error.append(str(i))
                log(fpath, str(i),
                    "GHG constraint for " + df["market"] + " in " + str(i) + " fails the constraint by" + str(df[str(i) + "_r"] - df[str(i) + "_g"]))
    return years_with_error


def verify_beccs(csv, fpath):
    """
    verifies the minimum price of beccs technologies
    :param csv: csv filepath containing the location of the ground truth data
    :param fpath: filepath to the output data
    :return: list of years with errors
    """
    # process results
    results = pd.read_csv(fpath + "/prices_of_all_markets.csv")
    results = results[results["product"] == "BECCS"]
    ground_truth = pd.read_csv(csv, skiprows=2)
    years_with_error = []

    # merge results and ground truth
    merge = pd.merge(results, ground_truth, "left", left_on="GCAM", right_on="region")
    for i in constants.GCAMConstants.plotting_x:
        # check that minimum price is satisfied
        merge[str(i)] = merge[str(i)] - merge["min-price"]
        if not (merge[str(i)] >= -1e-4).all():
            years_with_error.append(str(i))
            errors = merge[merge[str(i)] <= -1e-4]
            log(fpath, str(i),"BECCS is lower than minimum price in the following regions: " + str(errors["GCAM"].unique()))

    return years_with_error


def verify_cdr(CDR, links, fpath):
    """
    verify ghg tax values
    :param CDR: a list of files necessary to validate CDR output
    :param links: a dictionary of links between config data and gcam technologies and locations
    :param fpath: location to the output data in the directory
    :return: a list of years in which an error was detected
    """
    results = pd.read_csv(fpath + "/CDR_by_tech.csv")
    years_with_error = []
    exo_CDR_demand = pd.DataFrame()
    elastic_CDR_demand = pd.DataFrame()
    region_market = links["ghg_CDR_market_link"]

    # split up CDR dictionary
    for i in CDR:
        if "exo_CDR" in i:
            exo_CDR_demand = pd.read_csv(CDR[i], skiprows=2)
            exo_CDR_demand = exo_CDR_demand.pivot(index='region', columns='year')['demand'].reset_index()
            exo_CDR_demand.columns = exo_CDR_demand.columns.astype(str)
            for j in constants.GCAMConstants.plotting_x:
                # convert from CO2-eq to C
                exo_CDR_demand[str(j)] = exo_CDR_demand[str(j)] * constants.GCAMConstants.CO2_to_C
            exo_CDR_demand["Units"] = "Mt C"
            exo_CDR_demand = exo_CDR_demand.groupby(["Units"]).sum(min_count=1).reset_index()
        if "elastic_CDR" in i:
            elastic_CDR_demand = get_elastic_CDR_demand(CDR, fpath, i, region_market)
        if "CDR_non-input_tech_costs" in i:
            ground_truth = pd.read_csv(CDR[i], skiprows=2).T
            ground_truth.columns = ground_truth.iloc[0].astype(int).astype(str)
            ground_truth = ground_truth[1:].reset_index().rename(columns={'index': 'technology'})
            years_with_error.extend(verify_non_input_tech_costs(ground_truth, links, fpath))

    # combine CDR sources to get estimated CDR demand
    if exo_CDR_demand.empty:
        CDR_demand = elastic_CDR_demand
    elif elastic_CDR_demand.empty:
        CDR_demand = exo_CDR_demand
    else:
        elastic_CDR_demand["Units"] = "Mt C"
        CDR_demand = pd.merge(exo_CDR_demand, elastic_CDR_demand, on=["Units"], suffixes=("_l", "_r"))
        for i in constants.GCAMConstants.plotting_x:
            CDR_demand[str(i)] = CDR_demand[str(i) + "_l"] + CDR_demand[str(i) + "_r"]
    CDR_demand["product"] = "CDR"

    # process ground truth CDR numbers
    if not region_market.empty:
        # move unsatisfied CDR demand to its own output .csv file
        results = results[results["GCAM"] != "Global"]
        unsatisfied_CDR = results[results["subsector"] == "unsatisfiedDemand"]
        satisfied_CDR = results[results["subsector"] != "unsatisfiedDemand"]
        unsatisfied_CDR.to_csv(fpath + "/unsatisfied_CDR_demand.csv")

        # add market information to the results
        satisfied_CDR = pd.merge(satisfied_CDR, region_market, "left", left_on="GCAM", right_on="region")

        # group by market and technology
        data_manipulation.group(satisfied_CDR, ["GCAM"]).to_csv(fpath + "/satisfied_CDR_demand_by_region.csv")
        data_manipulation.group(satisfied_CDR, ["technology"]).to_csv(fpath + "/satisfied_CDR_demand_by_tech.csv")
        satisfied_CDR = data_manipulation.group(satisfied_CDR, ["scenario", "baseline"])
        satisfied_CDR["product"] = "CDR"

        # compare ground truths with results
        df = pd.merge(CDR_demand, satisfied_CDR, "left", ["product"], suffixes=("_left", "_right"))
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
    """
    get information pertaining to the elastic cdr demand based on the carbon prices and formulat
    :param CDR: dict containing cdr config information
    :param fpath: location to gcam output data directory
    :param i: key for cdr dict
    :param region_market: link between cdr markets and regions
    :return: dataframe containing the elastic cdr demand
    """
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

    for j in constants.GCAMConstants.plotting_x:
        elastic_ground_truth[str(j)] = elastic_ground_truth.apply(lambda row: get_elastic_demand(row, str(j)),
                                                                  axis=1)
    return elastic_ground_truth


def get_elastic_demand(row, i):
    # s-curve calculation
    if row[str(i)] < row["min-price"] * constants.GCAMConstants.USD2025_tCO2_to_1990_tC + 0.001:
        return 0
    else:
        return row["max-demand"] * constants.GCAMConstants.CO2_to_C / (1 + math.exp((0-row["steepness"]) * (row[str(i)] - (row["midpoint"]* constants.GCAMConstants.USD2025_tCO2_to_1990_tC))))


def verify_ghg_tax(ground_truth, results, fpath):
    """
    verify ghg tax values
    :param ground_truth: the values in the input file
    :param results: the values in the GCAM model output
    :param fpath: filepath used to verify outputs
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
    """
    log errors to the error log
    :param fpath: fpath to output data
    :param year: year in which an error occured
    :param reason: reason for the error occuring as calculated in the verification
    :return: N/A
    """
    # open log file and add reason for masking a year
    with open(fpath + "/log.txt", "a+") as f:
        print("Verification fails in " + year + " because " + reason)
        f.write("Verification fails in " + year + " because " + reason + "\n")


if __name__ == '__main__':
    main("default_ndc")
