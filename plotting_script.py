import os
import plotting
import data_manipulation
import constants as c
import pandas as pd
import utilities
import numpy as np

import verification


def main(config_fname, reference_year):
    """
    Main method for scripts used to plot figures and information for the article
    :param config_fname: used to store information on where to save plots and tables
    :param reference_year: year to analyze outputs
    :return: N/A
    """
    config_fname = config_fname.replace("_", "/")
    os.makedirs("./data/data_analysis/images/" + config_fname + "/", exist_ok=True)
    os.makedirs("data/data_analysis/supplementary_tables/" + config_fname + "/", exist_ok=True)
    CDR_cost(config_fname, reference_year)
    CDR_tech(config_fname, reference_year)
    social_cost(config_fname, reference_year)


def social_cost(config_fname, reference_year):
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]
    # process USA emissions
    CO2_emissions = data_manipulation.get_sensitivity_data([config_fname], "CO2_emissions_by_sector")
    CO2_emissions = CO2_emissions[CO2_emissions["GCAM"].isin(c.GCAMConstants.USA_region)]
    CO2_emissions = CO2_emissions[CO2_emissions["sector"] != "CDR_regional"]
    # replace negative emissions with np.nan
    for i in c.GCAMConstants.plotting_x:
        CO2_emissions[str(i)] = CO2_emissions.apply(lambda row: np.nan if row[str(i)] < 0 else row[str(i)], axis=1)

    CO2_emissions = CO2_emissions.groupby(["scenario", "baseline", "Units"]).sum(min_count=1).reset_index()

    # process emissions prices
    CO2_prices = data_manipulation.get_sensitivity_data([config_fname], "CO2_prices")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_cost = pd.merge(CO2_emissions, CO2_prices, "left", "baseline", suffixes=("_supply", "_price"))
    for i in c.GCAMConstants.plotting_x:
        CO2_cost[str(i)+"_total_cost"] = (CO2_cost[str(i)+"_supply"] / c.GCAMConstants.CO2_to_C) * (CO2_cost[str(i)+"_price"]/c.GCAMConstants.USD2025_tCO2_to_1990_tC)

    # process total price of CDR
    CDR_cost = pd.read_csv(
        "data/data_analysis/supplementary_tables/" + scenario + "/" + baseline + "/sorted price and supply of CDR by technology.csv")
    for i in c.GCAMConstants.plotting_x:
        try:
            CDR_cost[str(i)+"_total_cost"] = CDR_cost[str(i)+"_supply"] * CDR_cost[str(i)+"_price"]
            CDR_cost = CDR_cost.drop([str(i)+"_supply", str(i)+"_price"], axis=1)
        except KeyError as e:
            print(e)
            CDR_cost[str(i) + "_total_cost"] = np.nan

    CDR_cost = CDR_cost.groupby(["Units_supply", "Units_price"]).sum(min_count=1).reset_index()
    CDR_cost["Units"] = "Million 2025USD"
    CO2_cost["Units"] = "Million 2025USD"

    costs = pd.concat([CDR_cost, CO2_cost])
    costs.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/CO2_CDR_social_costs.csv")


def CDR_tech(config_fname, year):
    """
    plot CDR information by region and technology in bar and map
    :param config_fname: where to store output data
    :param year: year being analyzed
    :return: N/A
    """
    # data processing
    CDR = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]

    # stacked bar plot
    plotting.plot_stacked_bar_product(CDR, year, "technology", "CDR by technology in " + str(year), config_fname)

    # choropleth map
    plotting.plot_world_by_products(CDR, "technology", [year], "plotting estimated CDR supply by technology in " + str(year),
                                    config_fname)


def CDR_cost(config_fname, year):
    """
    plot CDR costs (and policy costs from subsidies and R&D investment
    :param config_fname: retains information about where to save data
    :param year: year being analyzed
    :return: N/A
    """
    # check if it is a baseline scenario
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]

    # build and write out scenario policy cost
    supply = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    supply["Units"] = "Mt CO$_{2}$-eq"
    price = data_manipulation.get_sensitivity_data([config_fname], "prices_of_all_markets")
    price["product"] = price.apply(lambda row: data_manipulation.price_subsidy(row), axis=1)

    # get the amount of money spent on the C tax
    CO2_emissions = data_manipulation.get_sensitivity_data([config_fname], "CO2_emissions_by_sector")
    CO2_emissions = CO2_emissions[CO2_emissions["GCAM"].isin(c.GCAMConstants.USA_region)]
    CO2_emissions = CO2_emissions[CO2_emissions["sector"] != "CDR_regional"]
    # replace negative emissions with np.nan
    for i in c.GCAMConstants.plotting_x:
        CO2_emissions[str(i)] = CO2_emissions.apply(lambda row: np.nan if row[str(i)] < 0 else row[str(i)], axis=1)

    CO2_emissions = CO2_emissions.groupby(["scenario", "baseline", "Units"]).sum(min_count=1).reset_index()

    # process emissions prices
    CO2_prices = data_manipulation.get_sensitivity_data([config_fname], "CO2_prices")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_cost = pd.merge(CO2_emissions, CO2_prices, "left", "baseline", suffixes=("_supply", "_price"))
    for i in c.GCAMConstants.plotting_x:
        CO2_cost[str(i)] = (CO2_cost[str(i)+"_supply"] / c.GCAMConstants.CO2_to_C) * (CO2_cost[str(i)+"_price"]/c.GCAMConstants.USD2025_tCO2_to_1990_tC)
        CO2_cost = CO2_cost.drop([str(i)+"_supply", str(i)+"_price"], axis=1)
    CO2_cost["Units"] = "Million 2025USD"

    # match subsidy market to the states
    # get the subsidy files
    files = config_fname.split("/")
    xml_files_to_build = []
    for i in files:
        xml_files_to_build.extend(utilities.build_from_scenario(str(i)))
    xml_files_to_build.reverse()
    subsidy_df = pd.DataFrame()
    meko_subsidy = pd.DataFrame()

    # get subsidy links and calculate subsidy name
    for xml in xml_files_to_build:
        for file in xml.data_files:
            csv = xml.data_files[file]
            if "subsidy" in file and "countersubsidy" not in file and "link" not in file:
                ground_truth = pd.read_csv(csv, skiprows=2)
                meko_subsidy = ground_truth
                ground_truth["product"] = ground_truth["stub-technology"] + " subsidy"
                ground_truth = ground_truth[["product", "market"]].drop_duplicates()
                ground_truth["GCAM"] = [c.GCAMConstants.USA_region for i in ground_truth.index]
                ground_truth = ground_truth.explode("GCAM")
                if not subsidy_df.equals(ground_truth):
                    subsidy_df = pd.concat([subsidy_df, ground_truth])

    if not subsidy_df.empty:
        subsidy_df = pd.merge(subsidy_df, price, "left", on=["product"])

        # update columns of df to prepare for merger
        subsidy_df["GCAM"] = subsidy_df["GCAM_x"]
        subsidy_df[['product', 'technology']] = subsidy_df['product'].str.split(' ', expand=True)
        price = pd.concat([price, subsidy_df])

    # update the price to $2025USD/t C  from $1975USD/kg C - then to a CO2-eq basis
    price["Units"] = "2025USD/t CO$_{2}$-eq"
    for i in c.GCAMConstants.plotting_x:
        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=197501&year2=202501
        price[str(i)] = price[str(i)] / c.GCAMConstants.USD2025_tCO2_to_1975_kgC
        supply[str(i)] = supply[str(i)] / c.GCAMConstants.CO2_to_C

    # merge dataframes and constrain to US regions
    dataframe = pd.merge(supply, price, "left", left_on=["technology", "GCAM"], right_on=["product", "GCAM"],
                         suffixes=("_supply", "_price"))
    dataframe = dataframe[dataframe["GCAM"].isin(c.GCAMConstants.USA_region)]
    dataframe = dataframe[~dataframe["subsector_supply"].isin(["unsatisfiedDemand"])]

    # if there is supply less than 0.01 Mt CDR for a given tech and state, set supply and price to np.nan
    for i in c.GCAMConstants.plotting_x:
        dataframe[str(i) + "_price"] = dataframe.apply(lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        dataframe[str(i) + "_supply"] = dataframe.apply(lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)
    mari_df = dataframe[dataframe["technology_price"] != "subsidy"]

    # format ground truth
    meko_subsidy = meko_subsidy.pivot(index='stub-technology', columns='year')['fixedTax'].reset_index()
    meko_subsidy.columns = meko_subsidy.columns.astype(str)
    meko_subsidy["Units"] = "Mt"
    scenario_df = plotting.plot_marimekko(mari_df, c.GCAMConstants.plotting_x, "_supply", "_price", "product_price",
                            "sorted price and supply of CDR by technology", config_fname, meko_subsidy)

    # and compare tech costs to default
    if scenario != baseline:
        baseline_df = pd.read_csv("data/data_analysis/supplementary_tables/"+baseline+"/"+baseline+"/sorted price and supply of CDR by technology.csv")
        plotting.compare_marimekko(scenario_df, baseline_df, config_fname)

    # calculate the total cost and plot
    for i in c.GCAMConstants.plotting_x:
        # "Mt $CO_{2}$-eq"  "2025USD/t $CO_{2}$-eq" factor of a million is added to dollars
        dataframe[str(i)] = dataframe[str(i) + "_supply"] * dataframe[str(i) + "_price"]
    # sum by technology
    dataframe = dataframe.groupby(["product_price", "technology_price"]).sum(min_count=1)
    dataframe = dataframe.reset_index()
    dataframe["Units"] = "Million 2025$USD/yr"
    dataframe['scenario'] = scenario
    dataframe['baseline'] = baseline
    dataframe['product'] = dataframe.apply(lambda row: row["product_price"] + " " + row["technology_price"] if row["technology_price"] != "missing" else row["product_price"], axis=1)

    # avoid double counting cost
    for i in c.GCAMConstants.plotting_x:
        dataframe[str(i)] = dataframe.apply(lambda row: data_manipulation.substract_subsidy(row, str(i), subsidy_df), axis = 1)

    # add exogenous policy costs to the CDR cost dataframes
    if os.path.exists("./data/gcam_out/" + config_fname + "/exogenous_subsector_investment" + ".csv"):
        investments = data_manipulation.get_sensitivity_data([config_fname], "exogenous_subsector_investment", source="not")
        investments["product"] = "Investment in " + investments["subsector"]
        dataframe = pd.concat([dataframe, investments])

    # add CO2 costs into the dataframe
    CO2_cost["product"] = "CO$_{2}$ tax"
    dataframe = pd.concat([dataframe, CO2_cost])

    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "product", "policy cost by year", config_fname)
    dataframe.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/policy cost by technology.csv")

    # compare this bar plot with default one (if this is not a default scenario)
    if baseline != scenario:
        cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + baseline + "/" + baseline +
                         "/policy cost by technology.csv")
        cost_diff = pd.merge(cost_diff, dataframe, "outer", on=["product", "baseline"], suffixes=("_old", "_new"))
        cost_diff["Units"] = "Million 2025$USD/yr"
        for i in c.GCAMConstants.plotting_x:
            # if a year has been masked from the data, don't fill na`11`
            no_subsidy = cost_diff[cost_diff["scenario_new"] == scenario]
            if no_subsidy[str(i)+"_new"].isnull().all() or no_subsidy[str(i)+"_old"].isnull().all():
                cost_diff[str(i)] = cost_diff[str(i) + "_new"] - cost_diff[str(i) + "_old"]
            else:
                cost_diff[str(i)] = cost_diff[str(i)+"_new"].fillna(0) - cost_diff[str(i)+"_old"].fillna(0)
        plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product", "change in policy cost by year", config_fname)

        # add a total row
        cols = ["2025", "2030", "2035", "2040", "2045", "2050", "product", "scenario_new", "baseline", "Units"]
        cost_diff = cost_diff[cols]
        total = pd.DataFrame(cost_diff.sum(numeric_only=True)).T
        cost_diff = pd.concat([cost_diff, total])
        cost_diff.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                         "/change in policy cost by technology.csv")

    # verify procurement
    if scenario != baseline:
        verification.verify_procurement(scenario, baseline, "./data/gcam_out/"+config_fname)


if __name__ == '__main__':
    for i in ["low_low", "verify-2025_low"]:
        main(i, "2050")
