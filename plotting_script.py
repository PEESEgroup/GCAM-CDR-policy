import os
import plotting
import data_manipulation
import constants as c
import pandas as pd
import utilities


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


def CDR_tech(config_fname, year):
    """
    plot CDR information by region and technology in bar and map
    :param config_fname: where to store output data
    :param year: year being analyzed
    :return: N/A
    """
    # data processing
    CDR = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech", "unmasked")
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

    # match subsidy market to the states
    # get the subsidy files
    files = config_fname.split("/")
    xml_files_to_build = []
    for i in files:
        xml_files_to_build.extend(utilities.build_from_scenario(str(i)))
    subsidy_df = pd.DataFrame()

    # get subsidy links and calculate subsidy name
    for xml in xml_files_to_build:
        for file in xml.data_files:
            csv = xml.data_files[file]
            if "link" in file:
                if "subsidy" in file:
                    links_ground_truth = pd.read_csv(csv, skiprows=2)
                    links_ground_truth = links_ground_truth[["region", "market"]]
                    links_ground_truth["GCAM"] = links_ground_truth["market"]
                    subsidy_name = file.split("_")
                    links_ground_truth["product"] = subsidy_name[0] + " " + subsidy_name[1]
                    subsidy_df = pd.concat([subsidy_df, links_ground_truth])

    # merge price data into the subsidy dataframe
    if not subsidy_df.empty:
        subsidy_df = pd.merge(subsidy_df, price, "left", on=["GCAM", "product"])

        # update columns of df to prepare for merger
        subsidy_df["GCAM"] = subsidy_df["region"]  # update GCAM to region information
        subsidy_df[['product', 'technology']] = subsidy_df['product'].str.split(' ', expand=True)
        price = pd.concat([price, subsidy_df])

    # update the price to $2025USD/t C  from $1975USD/kg C - then to a CO@-eq basis
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
    scenario_df = plotting.plot_marimekko(mari_df, c.GCAMConstants.plotting_x, "_supply", "_price", "product_price",
                            "sorted price and supply of CDR by technology", config_fname)

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

    # add exogenous policy costs to the CDR cost dataframes
    if os.path.exists("./data/gcam_out/" + config_fname + "/exogenous_subsector_investment" + ".csv"):
        investments = data_manipulation.get_sensitivity_data([config_fname], "exogenous_subsector_investment", source="not")
        investments["product"] = "Investment in " + investments["subsector"]
        dataframe = pd.concat([dataframe, investments])

    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "product", "policy cost by year", config_fname)
    dataframe.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/policy cost by technology.csv")

    # compare this bar plot with default one (if this is not a default scenario)
    if baseline != scenario:
        cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + baseline + "/" + baseline +
                         "/policy cost by technology.csv")
        cost_diff = pd.merge(cost_diff, dataframe, "outer", on=["product", "GCAM", "Units", "baseline"], suffixes=("_old", "_new"))
        for i in c.GCAMConstants.plotting_x:
            cost_diff[str(i)] = cost_diff[str(i)+"_new"].fillna(0) - cost_diff[str(i)+"_old"].fillna(0)
        plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product", "change in policy cost by year", config_fname)

        # add a total row
        cols = ["2025", "2030", "2035", "2040", "2045", "2050", "product", "scenario_new", "baseline", "Units"]
        cost_diff = cost_diff[cols]
        total = pd.DataFrame(cost_diff.sum(numeric_only=True)).T
        cost_diff = pd.concat([cost_diff, total])
        cost_diff.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                         "/change in policy cost by technology.csv")


if __name__ == '__main__':
    main("nothing_nothing", "2040")
