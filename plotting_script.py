import os
import constants
import plotting
import data_manipulation
import constants as c
import pandas as pd
import utilities
import numpy as np
import verification
import numpy_financial as npf


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
    # CDR_cost(config_fname, reference_year)
    # CDR_tech(config_fname, reference_year)
    # social_cost(config_fname, reference_year)
    # market_share(config_fname, reference_year)
    # subsidy_expiration(config_fname, reference_year)
    costs_and_benefits(config_fname, reference_year)


def costs_and_benefits(config_fname, reference_year):
    # process scenario data
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]
    npv_cols = [str(2025 + i) for i in range(0, 26)]
    npv_cols.append("cost_type")
    npv_cols.append("Units")

    # grab scenario config files
    xml_scenario_files = utilities.build_from_scenario(scenario)

    # get the costs of the scenario
    scenario_df = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario + "/" + baseline +
                            "/policy cost by technology.csv")
    # get the costs of the baseline
    baseline_df = pd.read_csv("data/data_analysis/supplementary_tables/" + baseline + "/" + baseline +
                                  "/policy cost by technology.csv")

    baseline_subsidy, baseline_deadweight, baseline_CTax, baseline_market, baseline_innovation_costs = get_CB_dfs(baseline_df, npv_cols)
    scenario_subsidy, scenario_deadweight, scenario_CTax, scenario_market, scenario_innovation_costs = get_CB_dfs(scenario_df, npv_cols)

    # calculate the procurement costs and remove that much money from the CDR market
    # get procurement dollar amounts, if they exist
    procurement_costs = pd.Series()
    for j in xml_scenario_files:
        if "exo_CDR_demand_verify" in j.data_files:
            # avoid double counting subsidies - doesn't overwrite baseline data
            scenario_subsidy_calc = scenario_subsidy[[str(k) for k in constants.GCAMConstants.plotting_x]]
            baseline_subsidy_calc = baseline_subsidy[[str(k) for k in constants.GCAMConstants.plotting_x]]
            double_subsidy = scenario_subsidy_calc - baseline_subsidy_calc

            # get CDR demand
            CDR_demand = utilities.open_csv(j.data_files)
            CDR_demand = CDR_demand["exo_CDR_demand_verify"]
            CDR_demand = pd.DataFrame(CDR_demand)

            # add in the double subsidy
            double_subsidy.columns = CDR_demand.columns
            double_subsidy.index = ["subsidy"]
            CDR_demand = pd.concat([CDR_demand, double_subsidy])
            CDR_demand = CDR_demand.T
            if "calc-avg-price" in CDR_demand.columns:
                # calculate the procurement costs
                CDR_demand["procurement_cost"] = CDR_demand['calc-avg-price'] * CDR_demand['govt-procurement'] - CDR_demand['subsidy']
                CDR_demand = CDR_demand.reset_index()
                CDR_demand["year"] = CDR_demand["level_0"].astype(str)
                CDR_demand = CDR_demand.set_index("year")
                procurement_costs = CDR_demand["procurement_cost"]
                procurement_costs = pd.DataFrame(pd.concat([procurement_costs, pd.Series(["procurement costs"], index=["cost_type"])])).T
                procurement_costs = data_manipulation.interpolate(procurement_costs, "truncated")
                procurement_costs["Units"] = "Million 2025$USD/yr"

                # remove procurement costs from the market
                remove_procure = pd.merge(scenario_market, procurement_costs, "inner", "Units", suffixes=("_market", "_procure"))
                for j in range(0, 26):
                    # subtract off the amount spent on procurement from the market
                    remove_procure[str(2025+j)] = remove_procure[str(2025+j)+ "_market"] - remove_procure[str(2025+j)+ "_procure"]
                # replace scenario market df
                remove_procure["cost_type"] = "CDR Market"
                scenario_market = remove_procure[npv_cols]

    # combine costs
    costs = pd.concat([scenario_subsidy, procurement_costs])
    total_costs = costs.groupby(["Units"]).sum(min_count=1)

    # combine the information that is relevant to meeting the net-zero 2050 mandate
    net_zero_mandate = pd.concat([scenario_subsidy, procurement_costs, scenario_innovation_costs, scenario_deadweight, scenario_CTax, scenario_market])
    net_zero_mandate = net_zero_mandate.fillna(0)
    net_zero_total_cost = net_zero_mandate.groupby(["Units"]).sum(min_count=1).reset_index()
    net_zero_total_cost["cost_type"] = "Total Cost"
    net_zero_mandate = pd.concat([net_zero_mandate, net_zero_total_cost])

    # get the NPV of the baseline scenario under 3 interest rates
    interest_rates = [0.03, 0.12, 0.20]
    npv_net_zero = {}
    NPV_CB = {}

    # calculate the npv
    for k in interest_rates:
        # remove identifying information from the dataframes
        net_zero_total_cost = net_zero_total_cost.drop(columns=['Units', 'cost_type', "0", 0], errors='ignore')
        total_costs = total_costs.drop(columns=['Units', 'cost_type', "0", 0], errors='ignore')
        scenario_market = scenario_market.drop(columns=['Units', 'cost_type', "0", 0], errors='ignore')
        baseline_market = baseline_market.drop(columns=['Units', 'cost_type', "0", 0], errors='ignore')

        npv_net_zero["NPV of Net Zero Mandate" + " | " + str(k*100) + "%"] = npf.npv(rate=k, values=net_zero_total_cost.values[0]) / 1000000
        costs = npf.npv(rate=k, values=total_costs.values[0])
        # benefits are defined as lower costs in the CDR market. these are compared to the baseline market
        benefits = npf.npv(rate=k, values=scenario_market.values[0]) - npf.npv(rate=k, values=baseline_market.values[0]) # benefits are negative, costs are positive

        # save cost benefit information
        NPV_CB["Benefits" + " | " + str(k * 100) + "%"] = benefits
        NPV_CB["Costs" + " | " + str(k * 100) + "%"] = costs
        NPV_CB["Benefits/Costs" + " | " + str(k*100) + "%"] = benefits/costs
        NPV_CB["Benefits-Costs" + " | " + str(k * 100) + "%"] = benefits - costs

    # write out information in .csv
    NPV_CB["Units"] = "Million $USD or unitless"
    npv = pd.DataFrame(NPV_CB, index= [0])
    npv_net_zero = pd.DataFrame(npv_net_zero, index=[0])
    npv_net_zero["Units"] = "Trillion $USD"
    npv.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
               "/cost-benefit-analysis.csv")
    npv_net_zero.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
               "/npv of achieving net zero.csv")
    net_zero_mandate.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                        "/interpolated costs of achieving net zero.csv")


def get_CB_dfs(baseline_market, npv_cols):
    # get subsidy information
    baseline_subsidy = baseline_market[baseline_market["technology_price"] == "subsidy"].copy(deep=True)
    baseline_subsidy = data_manipulation.interpolate(baseline_subsidy, "truncated")
    baseline_subsidy = baseline_subsidy.groupby(["technology_price", "Units"]).sum(min_count=1).reset_index()
    baseline_subsidy["cost_type"] = "Subsidy"
    baseline_subsidy = baseline_subsidy[npv_cols]

    # get C tax revenue and deadweight loss information
    baseline_deadweight = baseline_market[baseline_market["product"] == "Deadweight Loss"].copy(deep=True)
    baseline_deadweight = data_manipulation.interpolate(baseline_deadweight, "truncated")
    baseline_deadweight["cost_type"] = "Deadweight Loss"
    baseline_deadweight["Units"] = "Million 2025$USD/yr"
    baseline_deadweight = baseline_deadweight[npv_cols]

    baseline_CTax = baseline_market[baseline_market["product"] == "C Tax Revenue"].copy(deep=True)
    baseline_CTax = data_manipulation.interpolate(baseline_CTax, "truncated")
    baseline_CTax["cost_type"] = "C Tax Revenue"
    baseline_CTax["Units"] = "Million 2025$USD/yr"
    baseline_CTax = baseline_CTax[npv_cols]

    # get innovation information
    baseline_innovation_funding = baseline_market[(baseline_market["product"] == "Investment in R&D") |
                                                  (baseline_market["product"] == "Investment in DAC Hubs")].copy(deep=True)
    if len(baseline_innovation_funding) != 0:
        baseline_innovation_funding = data_manipulation.interpolate(baseline_innovation_funding, "extended")
        baseline_innovation_funding["cost_type"] = "Investment in R&D"
        baseline_innovation_funding = baseline_innovation_funding[npv_cols]
        baseline_innovation_funding["Units"] = "Million 2025$USD/yr"
    else:
        # empty df
        baseline_innovation_funding = pd.DataFrame(columns=npv_cols)

    # get market information
    baseline_market = baseline_market[
        (baseline_market["technology_price"] != "subsidy") & (baseline_market["product_price"] != "CO2") & (baseline_market["product"] != "Investment in R&D") & (baseline_market["product"] != "Investment in DAC Hubs")].copy(deep=True)
    baseline_market = data_manipulation.interpolate(baseline_market, "linear")
    baseline_market["cost_type"] = "CDR Market"
    baseline_market = baseline_market.groupby(["cost_type", "Units"]).sum(min_count=1).reset_index()
    baseline_market = baseline_market[npv_cols]

    # return files
    return baseline_subsidy, baseline_deadweight, baseline_CTax, baseline_market, baseline_innovation_funding


def subsidy_expiration(config_fname, reference_year):
    # get baseline info
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]
    # get market data at the state level
    CDR = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario + "/" + baseline +
                      "/sorted price and supply of CDR by technology.csv")

    list_of_subsidies = []
    # find out which years have subsidies
    for i in c.GCAMConstants.plotting_x:
        try:
            condition = CDR[str(i) + "_price"] > CDR[str(i) + "_subsidized"]
            if condition.any():
                list_of_subsidies.append(i)
        except KeyError as e:
            print(e)

    # get the last year without subsidies
    year_without_subsidies = list_of_subsidies[-1] + 5

    # calculate what happens when subsidies end
    if year_without_subsidies < 2051:
        CDR = CDR.fillna(0)
        columns = ["GCAM", "product_price"]
        for i in list_of_subsidies:
            CDR[str(i) + "_total_loss"] = CDR.apply(
                lambda row: -1*(row[str(i) + "_supply"] - row[str(year_without_subsidies) + "_supply"]) * row[
                    str(i) + "_price"]
                if row[str(i) + "_price"] > row[str(i) + "_subsidized"] else 0, axis=1)
            CDR[str(i) + "_CDR-Market_loss"] = CDR.apply(
                lambda row: -1* (row[str(i) + "_supply"] - row[str(year_without_subsidies) + "_supply"]) * row[
                    str(i) + "_subsidized"]
                if row[str(i) + "_price"] > row[str(i) + "_subsidized"] else 0, axis=1)
            CDR[str(i) + "_CDR-Subsidy_loss"] = CDR[str(i) + "_total_loss"] - CDR[str(i) + "_CDR-Market_loss"]
            columns.append(str(i) + "_CDR-Market_loss")
            columns.append(str(i) + "_CDR-Subsidy_loss")

        # refit df for histogram plotting
        CDR_df = CDR[columns]
        CDR_df = CDR_df.melt(id_vars=["GCAM", "product_price"], var_name='category', value_name='Change in market size')
        CDR_df["SSP"] = "na"
        CDR_df["Units"] = "Million USD/yr"
        # remove rows with no change
        CDR_df = CDR_df[CDR_df["Change in market size"]!= 0]

        plotting.plot_regional_hist_avg(CDR_df, 'Change in market size', "change in size of markets once the subsidy ends",
                                        "category", config_fname)

        # get only wasted and good spend
        CDR_wasted_subsidy = CDR.copy(deep=True)
        CDR_good_subsidy = CDR.copy(deep=True)

        for i in list_of_subsidies:
            CDR_wasted_subsidy[str(i)+"_CDR-Subsidy_loss"] = CDR_wasted_subsidy.apply(
                lambda row: 0 if row[str(i)+"_CDR-Subsidy_loss"] > 0 else row[str(i)+"_CDR-Subsidy_loss"], axis=1)
            CDR_wasted_subsidy[str(i)+"_CDR-Market_loss"] = CDR_wasted_subsidy.apply(
                lambda row: 0 if row[str(i)+"_CDR-Market_loss"] > 0 else row[str(i)+"_CDR-Market_loss"], axis=1)
            CDR_good_subsidy[str(i)+"_CDR-Subsidy_loss"] = CDR_good_subsidy.apply(
                lambda row: 0 if row[str(i)+"_CDR-Subsidy_loss"] < 0 else row[str(i)+"_CDR-Subsidy_loss"], axis=1)
            CDR_good_subsidy[str(i)+"_CDR-Market_loss"] = CDR_good_subsidy.apply(
                lambda row: 0 if row[str(i)+"_CDR-Market_loss"] < 0 else row[str(i)+"_CDR-Market_loss"], axis=1)

        CDR_wasted_subsidy = CDR_wasted_subsidy.groupby(["product_price"]).sum(min_count=1)
        CDR_wasted_subsidy = CDR_wasted_subsidy.reset_index()
        CDR_wasted_subsidy["Units"] = "Million 2025$USD/yr"
        CDR_wasted_subsidy["spend"] = "Wasted"
        CDR_good_subsidy = CDR_good_subsidy.groupby(["product_price"]).sum(min_count=1)
        CDR_good_subsidy = CDR_good_subsidy.reset_index()
        CDR_good_subsidy["Units"] = "Million 2025$USD/yr"
        CDR_good_subsidy["spend"] = "Good"
        CDR = pd.concat([CDR_wasted_subsidy, CDR_good_subsidy]).reset_index()
        CDR["product"] = CDR["product_price"] + " " + CDR["spend"]

        CDR.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                  "/subsidy-and-market-spend-on-subsidized-techs.csv")

        # remove market spend to focus on subsidies
        for i in list_of_subsidies:
            CDR[str(i)] = CDR[str(i)+"_CDR-Subsidy_loss"]
        plotting.plot_stacked_bar_product(CDR, list_of_subsidies, "product", "change in CDR market size from base year to year after subsidies end", config_fname)


def market_share(config_fname, reference_year):
    # get baseline info
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]

    # get market data from state
    CDR_market = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario + "/" + baseline +
                             "/sorted price and supply of CDR by technology.csv")

    # get supply
    CDR_market = CDR_market.groupby('product_price')[str(reference_year) + "_supply"].sum()

    # calculate percentage of market share
    percentages = (CDR_market / CDR_market.sum()) * 100

    # format data and output
    df = pd.concat([CDR_market, percentages], axis=1)
    df.columns = ["Mt", "%"]
    df.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
              "/market share in " + str(reference_year) + ".csv")


def social_cost(config_fname, reference_year):
    baseline = config_fname.split("/")[1]
    scenario = config_fname.split("/")[0]
    # process USA emissions
    costs = get_C_costs(baseline, config_fname, scenario)
    costs.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                 "/CO2_CDR_social_costs.csv")


def get_C_costs(baseline, config_fname, scenario):
    CO2_emissions = data_manipulation.get_sensitivity_data([config_fname], "CO2_emissions_by_sector")
    CO2_emissions = CO2_emissions[CO2_emissions["GCAM"].isin(c.GCAMConstants.USA_region)]
    CO2_emissions = CO2_emissions[CO2_emissions["sector"] != "CDR_regional"]  # excluded from the C tax
    CO2_emissions = CO2_emissions.groupby(["scenario", "baseline", "Units"]).sum(min_count=1).reset_index()
    # get a baseline CO2 emissions
    baseline_emissions = pd.read_csv("data/data_analysis/baseline_co2_emissions.csv")
    # process emissions revenue
    CO2_prices = data_manipulation.get_sensitivity_data([config_fname], "CO2_prices")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_tax_revenue = pd.merge(CO2_emissions, CO2_prices, "left", "baseline", suffixes=("_supply", "_price"))
    for i in c.GCAMConstants.plotting_x:
        # (Mt C * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        CO2_tax_revenue[str(i) + "_total_cost"] = (CO2_tax_revenue[str(i) + "_supply"] / c.GCAMConstants.CO2_to_C) * (
                CO2_tax_revenue[str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC)
    # process deadweight loss
    CO2_tax_price = pd.merge(CO2_emissions, CO2_prices, "left", "baseline", suffixes=("_supply", "_price"))
    CO2_tax_price["Units"] = "MTC"
    deadweight_loss = pd.merge(CO2_tax_price, baseline_emissions, "left", "Units", suffixes=("_actual", "_baseline"))
    for i in c.GCAMConstants.plotting_x:
        # ((Mt C - Mt C) * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        deadweight_loss[str(i) + "_total_cost"] = (
                0.5 * (deadweight_loss[str(i)] - deadweight_loss[str(i) + "_supply"]) / c.GCAMConstants.CO2_to_C *
                (deadweight_loss[str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC))

    # process total price of CDR
    CDR_cost = pd.read_csv(
        "data/data_analysis/supplementary_tables/" + scenario + "/" + baseline + "/sorted price and supply of CDR by technology.csv")
    for i in c.GCAMConstants.plotting_x:
        try:
            CDR_cost[str(i) + "_total_cost"] = CDR_cost[str(i) + "_supply"] * CDR_cost[str(i) + "_price"]
            CDR_cost = CDR_cost.drop([str(i) + "_supply", str(i) + "_price"], axis=1)
        except KeyError as e:
            print(e)
            CDR_cost[str(i) + "_total_cost"] = np.nan
    CDR_cost = CDR_cost.groupby(["Units_supply", "Units_price"]).sum(min_count=1).reset_index()
    CDR_cost["Units"] = "Million 2025$USD/yr"
    deadweight_loss["Units"] = "Million 2025$USD/yr"
    CO2_tax_revenue["Units"] = "Million 2025$USD/yr"
    CDR_cost["product"] = "CDR Market"
    deadweight_loss["product"] = "Deadweight Loss"
    CO2_tax_revenue["product"] = "C Tax Revenue"
    costs = pd.concat([CDR_cost, CO2_tax_revenue, deadweight_loss])
    return costs


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
    plotting.plot_world_by_products(CDR, "technology", [year],
                                    "plotting estimated CDR supply by technology in " + str(year),
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
        subsidy_df.drop_duplicates(inplace=True)
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
    dataframe.drop_duplicates(inplace=True)
    dataframe = dataframe[~dataframe["subsector_supply"].isin(["unsatisfiedDemand"])]

    # if there is supply less than 0.01 Mt CDR for a given tech and state, set supply and price to np.nan
    for i in c.GCAMConstants.plotting_x:
        dataframe[str(i) + "_price"] = dataframe.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        dataframe[str(i) + "_supply"] = dataframe.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)
    mari_df = dataframe[dataframe["technology_price"] != "subsidy"]

    # format ground truth
    meko_subsidy = meko_subsidy.pivot(index='stub-technology', columns='year')['fixedTax'].reset_index()
    meko_subsidy.columns = meko_subsidy.columns.astype(str)
    meko_subsidy["Units"] = "Mt"
    scenario_df = plotting.plot_marimekko(mari_df, c.GCAMConstants.plotting_x, "_supply", "_price", "product_price",
                                          "sorted price and supply of CDR by technology", config_fname, meko_subsidy)

    # and compare tech costs to default
    if scenario != baseline:
        baseline_df = pd.read_csv(
            "data/data_analysis/supplementary_tables/" + baseline + "/" + baseline + "/sorted price and supply of CDR by technology.csv")
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
    dataframe['product'] = dataframe.apply(
        lambda row: row["product_price"] + " " + row["technology_price"] if row["technology_price"] != "missing" else
        row["product_price"], axis=1)

    # avoid double counting cost
    for i in c.GCAMConstants.plotting_x:
        dataframe[str(i)] = dataframe.apply(lambda row: data_manipulation.substract_subsidy(row, str(i), subsidy_df),
                                            axis=1)

    # add exogenous policy costs to the CDR cost dataframes
    if os.path.exists("./data/gcam_out/" + config_fname + "/exogenous_subsector_investment" + ".csv"):
        investments = data_manipulation.get_sensitivity_data([config_fname], "exogenous_subsector_investment",
                                                             source="not")
        investments["product"] = "Investment in " + investments["subsector"]

        # remove nan rows
        investments = investments.dropna(subset=[str(i) for i in constants.GCAMConstants.plotting_x], how='all')
        dataframe = pd.concat([dataframe, investments])

    # add CO2 costs into the dataframe
    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "product",
                                      "policy cost by year (no C tax)", config_fname)
    dataframe.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/policy cost by technology_no co2.csv")

    # compare this bar plot with default one (if this is not a default scenario)
    if baseline != scenario:
        cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + baseline + "/" + baseline +
                                "/policy cost by technology_no co2.csv")
        cost_diff = pd.merge(cost_diff, dataframe, "outer", on=["product", "baseline"], suffixes=("_old", "_new"))
        cost_diff["Units"] = "Million 2025$USD/yr"
        for i in c.GCAMConstants.plotting_x:
            # if a year has been masked from the data, don't fill na
            no_subsidy = cost_diff[cost_diff["scenario_new"] == scenario]
            if no_subsidy[str(i) + "_new"].isnull().all() or no_subsidy[str(i) + "_old"].isnull().all():
                cost_diff[str(i)] = cost_diff[str(i) + "_new"] - cost_diff[str(i) + "_old"]
            else:
                cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
        plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                          "change in policy cost by year (no C tax)", config_fname)

        # add a total row
        cols = ["2025", "2030", "2035", "2040", "2045", "2050", "product", "scenario_new", "baseline", "Units"]
        cost_diff = cost_diff[cols]
        total = pd.DataFrame(cost_diff.sum(numeric_only=True)).T
        cost_diff = pd.concat([cost_diff, total])
        cost_diff.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                         "/change in policy cost by technology_no_C_tax.csv")

    C_costs = get_C_costs(baseline, config_fname, scenario)
    C_costs = C_costs[C_costs["product"] != "CDR Market"]

    for i in c.GCAMConstants.plotting_x:
        C_costs[str(i)] = C_costs[str(i) + "_total_cost"]

    dataframe = pd.concat([dataframe, C_costs])

    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "product", "policy cost by year",
                                      config_fname)
    dataframe.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/policy cost by technology.csv")

    # compare this bar plot with default one (if this is not a default scenario)
    if baseline != scenario:
        cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + baseline + "/" + baseline +
                                "/policy cost by technology.csv")
        cost_diff = pd.merge(cost_diff, dataframe, "outer", on=["product", "baseline"], suffixes=("_old", "_new"))
        cost_diff["Units"] = "Million 2025$USD/yr"
        for i in c.GCAMConstants.plotting_x:
            # if a year has been masked from the data, don't fill na
            no_subsidy = cost_diff[cost_diff["scenario_new"] == scenario]
            if no_subsidy[str(i) + "_new"].isnull().all() or no_subsidy[str(i) + "_old"].isnull().all():
                cost_diff[str(i)] = cost_diff[str(i) + "_new"] - cost_diff[str(i) + "_old"]
            else:
                cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
        plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                          "change in policy cost by year", config_fname)

        # add a total row
        cols = ["2025", "2030", "2035", "2040", "2045", "2050", "product", "scenario_new", "baseline", "Units"]
        cost_diff = cost_diff[cols]
        total = pd.DataFrame(cost_diff.sum(numeric_only=True)).T
        cost_diff = pd.concat([cost_diff, total])
        cost_diff.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                         "/change in policy cost by technology.csv")

    # verify procurement
    if scenario != baseline:
        verification.verify_procurement(scenario, baseline, "./data/gcam_out/" + config_fname)


if __name__ == '__main__':
    for i in ["s1-procureScaling-n_nothing", "s1-procure3B-n_nothing", "s1-procureRhodium-n_nothing",
              "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
              "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
              "nothing_nothing","nzn_nzn", "low_low", "high_high", "excess_excess", "4gt_4gt",
              "45Q-2040_low", "45Q-2050_low","CDRIA-2035_low", "CDRIA-2050_low",
              "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
              "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low", "innovation-rhodium18b_low", "innovation-triple_low",
              "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high", "innovation-rhodium18b_high", "innovation-triple_high"]:
    # for i in ["innovation-rhodium18b_high", "innovation-DACHubs_low"]:
        main(i, "2050")
