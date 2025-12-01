import os
import plotting
import data_manipulation
import constants as c
import pandas as pd


def main(config_fname, reference_year):
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    config_fname = config_fname.replace("_", "/")
    os.makedirs("./data/data_analysis/images/" + config_fname + "/", exist_ok=True)
    compare_policy_costs("45Q-2040_low", "45Q-2050_low")
    # CDR_subsidies(config_fname, "2035", "2040")


def CDR_subsidies(config_fname, year1, year2):
    # data processing
    CDR = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech", "masked")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]

    CDR["plot"] = CDR[year2] - CDR[year1]

    # choropleth map
    plotting.plot_world_by_products(CDR, "technology", ["plot"],
                                    "Change in CDR (Mt) from " + year1 + " to year " + year2, config_fname)



def pop_and_calories(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    plots changes to population and calories consumed
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year the biochar pathways are being evaluated
    :return: N/A
    """
    # get population data
    released_pop = data_manipulation.get_sensitivity_data(["released"], "population_by_region", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_pop = data_manipulation.get_sensitivity_data(nonBaselineScenario, "population_by_region", SSP, RCP=RCP,
                                                           source="masked")
    flat_diff_pop = data_manipulation.flat_difference(released_pop, pyrolysis_pop, ["SSP", "GCAM"])
    data_manipulation.drop_missing(flat_diff_pop).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/flat_change_in_population.csv")

# calculate food accessibility and undernourishment
    released_caloric_consumption = data_manipulation.get_sensitivity_data(["released"], "food_demand_per_capita", SSP,
                                                                          RCP=RCP, source="original")
    pyrolysis_caloric_consumption = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                                           "food_demand_per_capita", SSP, RCP=RCP,
                                                                           source="masked")
    released_caloric_consumption = data_manipulation.group(released_caloric_consumption, ["SSP", "GCAM", "Version"])
    pyrolysis_caloric_consumption = data_manipulation.group(pyrolysis_caloric_consumption, ["SSP", "GCAM", "Version"])

    # regional averaged food consumption by food type
    # convert Pcal to kcal/capita/day
    # get population data
    released_pop = data_manipulation.get_sensitivity_data(["released"], "population_by_region", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_pop = data_manipulation.get_sensitivity_data(nonBaselineScenario, "population_by_region", SSP, RCP=RCP,
                                                           source="masked")
    released_Pcal = data_manipulation.get_sensitivity_data(["released"], "food_consumption_by_type_specific", SSP,
                                                           RCP=RCP, source="original")
    pyrolysis_Pcal = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_consumption_by_type_specific",
                                                            SSP, RCP=RCP, source="masked")

    # relabel data to make it more human-readable
    released_Pcal['GCAM'] = released_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    released_pop['GCAM'] = released_pop.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_Pcal['GCAM'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_pop['GCAM'] = pyrolysis_pop.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    released_Pcal['technology'] = released_Pcal.apply(lambda row: data_manipulation.relabel_food(row, "technology"),
                                                      axis=1)
    pyrolysis_Pcal['technology'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_food(row, "technology"),
                                                        axis=1)

    # drop MiscCrop and FiberCrop because those products don't have meaningful calories and clutter the graph
    released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Fiber Crops"].index)
    released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Other Crops"].index)
    pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Fiber Crops"].index)
    pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Other Crops"].index)

    released_Pcal = data_manipulation.group(released_Pcal, ["GCAM", "SSP", "technology", "Version"])
    pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["GCAM", "SSP", "technology", "Version"])

    # calculate food accessibility
    # get food prices
    released_staple_expenditure = data_manipulation.get_sensitivity_data(["released"], "food_demand_prices", SSP,
                                                                         RCP=RCP, source="original")
    pyrolysis_staple_expenditure = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_prices",
                                                                          SSP, RCP=RCP, source="masked")
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]

    # get food consumption
    released_staple_consumption = data_manipulation.get_sensitivity_data(["released"], "food_demand_per_capita", SSP,
                                                                         RCP=RCP, source="original")
    pyrolysis_staple_consumption = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_per_capita",
                                                                          SSP, RCP=RCP, source="masked")
    released_staple_consumption = released_staple_consumption[
        released_staple_consumption[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]
    pyrolysis_staple_consumption = pyrolysis_staple_consumption[
        pyrolysis_staple_consumption[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]

    # get GDP per capita
    released_GDP_capita = data_manipulation.get_sensitivity_data(nonBaselineScenario, "GDP_per_capita_PPP_by_region",
                                                                 SSP, RCP=RCP, source="original")
    pyrolysis_GDP_capita = data_manipulation.get_sensitivity_data(nonBaselineScenario, "GDP_per_capita_PPP_by_region",
                                                                  SSP, RCP=RCP, source="masked")

    # calculate consumption times price divided by GDP per capita
    released_consumption = pd.merge(released_staple_consumption, released_staple_expenditure, how="inner",
                                    on=["SSP", "GCAM", "technology"],
                                    suffixes=("_pcal", "_$"))
    pyrolysis_consumption = pd.merge(pyrolysis_staple_consumption, pyrolysis_staple_expenditure, how="inner",
                                     on=["SSP", "GCAM", "technology"],
                                     suffixes=("_pcal", "_$"))

    # other scaling factors
    released_FA = pd.merge(released_consumption, released_GDP_capita, how="left", on=["SSP", "GCAM"],
                           suffixes=("", "_capita"))
    pyrolysis_FA = pd.merge(pyrolysis_consumption, pyrolysis_GDP_capita, how="left", on=["SSP", "GCAM"],
                            suffixes=("", "_capita"))
    released_FA = pd.merge(released_FA, released_caloric_consumption, how="left", on=["SSP", "GCAM"],
                           suffixes=("", "_caloric"))
    pyrolysis_FA = pd.merge(pyrolysis_FA, pyrolysis_caloric_consumption, how="left", on=["SSP", "GCAM"],
                            suffixes=("", "_caloric"))
    for i in c.GCAMConstants.biochar_x:
        # released_FA[str(i)] corresponds to the capita column
        released_FA[str(i)] = released_consumption[str(i) + "_pcal"] * released_consumption[str(i) + "_$"] / \
                              released_FA[str(i)] * 3.542 / released_FA[str(i) + "_caloric"]
        pyrolysis_FA[str(i)] = pyrolysis_consumption[str(i) + "_pcal"] * pyrolysis_consumption[str(i) + "_$"] / \
                               pyrolysis_FA[str(i)] * 3.542 / pyrolysis_FA[str(i) + "_caloric"]

    perc_diff_FA = data_manipulation.percent_difference(released_FA, pyrolysis_FA, ["GCAM", "SSP"])
    plotting.plot_world(perc_diff_FA, ["%"], SSP, "year", "Units", c.GCAMConstants.biochar_x,
                        "Food Accessibility near midcentury ", RCP, nonBaselineScenario)

    # calculate pcal per capita
    released_pcal_pop = pd.merge(released_Pcal, released_pop, how="inner", on=["SSP", "GCAM"],
                                 suffixes=("_pcal", "_pop"))
    pyrolysis_pcal_pop = pd.merge(pyrolysis_Pcal, pyrolysis_pop, how="inner", on=["SSP", "GCAM"],
                                  suffixes=("_pcal", "_pop"))

    # calculate pcal per capita in the biochar year
    released_pcal_pop["pcal_capita_" + biochar_year] = released_pcal_pop[biochar_year + "_pcal"] / (
                1000 * released_pcal_pop[
            biochar_year + "_pop"]) * 1000000000000 / 365 / 2  # * peta to kilo/365/conversion factor of 2 randomly
    pyrolysis_pcal_pop["pcal_capita_" + biochar_year] = pyrolysis_pcal_pop[biochar_year + "_pcal"] / (
            1000 * pyrolysis_pcal_pop[biochar_year + "_pop"]) * 1000000000000 / 365 / 2
    released_pcal_pop["Units"] = "kcal/capita/day"
    pyrolysis_pcal_pop["Units"] = "kcal/capita/day"

    merged_pcal = released_pcal_pop.merge(pyrolysis_pcal_pop, how="inner", on=["SSP", "GCAM", "technology_pcal"],
                                          suffixes=("_left", "_right"))
    merged_pcal["pcal_capita_" + biochar_year] = merged_pcal["pcal_capita_" + biochar_year + "_right"] - merged_pcal[
        "pcal_capita_" + biochar_year + "_left"]
    data_manipulation.drop_missing(merged_pcal).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/change_in_consumption_kcal_capita_day.csv")

    # extract population and identifying information in biochar_year for weighted average calculations
    merged_pop = pd.DataFrame()
    merged_pop["pcal_capita_" + biochar_year] = merged_pcal[biochar_year + "_pop_right"]
    merged_pop["GCAM"] = merged_pcal["GCAM"]
    merged_pop["SSP"] = merged_pcal["SSP"]
    merged_pop["technology_pcal"] = merged_pcal["technology_pcal"]

    plotting.plot_regional_vertical_avg(merged_pcal, "pcal_capita_" + biochar_year, SSP,
                                        "change in food demand (kcal/person/day)",
                                        "change in food demand in " + biochar_year + " in " + str(SSP[0]),
                                        "technology_pcal", merged_pop, RCP, nonBaselineScenario)




def luc_by_region(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    plots information related to land use changes between pyrolysis and reference scenario
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year the biochar pathways are being evaluated
    :return: N/A
    """
    # get luc data
    released_luc = data_manipulation.get_sensitivity_data(["released"], "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_luc = data_manipulation.get_sensitivity_data(nonBaselineScenario, "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                           source="masked")

    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP"])
    perc_diff_luc = data_manipulation.percent_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP"])
    data_manipulation.drop_missing(flat_diff_luc.drop("LandLeaf", axis=1)).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/change_in_LUC_emissions.csv")
    data_manipulation.drop_missing(perc_diff_luc.drop("LandLeaf", axis=1)).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/percent_change_in_LUC_emissions.csv")

    plotting.plot_world_by_years(flat_diff_luc, ["MtC/yr"], "Units", c.GCAMConstants.biochar_x, SSP,
                                 "net difference in LUC emissions by region", RCP, nonBaselineScenario)

    flat_diff_luc = data_manipulation.group(flat_diff_luc, ["SSP"])
    plotting.plot_line_by_product(flat_diff_luc, ["SSP1"], "SSP", ["SSP1"], "SSP",
                                  "Net LUC compared to reference scenario", RCP, nonBaselineScenario)

    released_luc = data_manipulation.get_sensitivity_data(["released"], "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_luc = data_manipulation.get_sensitivity_data(nonBaselineScenario, "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                           source="masked")
    released_luc["LandLeaf"] = released_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    pyrolysis_luc["LandLeaf"] = pyrolysis_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                    axis=1)
    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP", "LandLeaf"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    for i in c.GCAMConstants.biochar_x:
        plotting.plot_regional_hist_avg(flat_diff_luc, str(i), SSP, "count region-LandLeaf",
                                        "Flat diffference in LUC emissions between pyrolysis and reference scenario in " + str(i),
                                        "LandLeaf", "na", RCP, nonBaselineScenario)



def pyrolysis_costing(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    returns information related to the cost of the pyrolysis scenario
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year being evaluated
    :return: N/A
    """
    # get total costs
    total_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "costs_by_tech", SSP, RCP=RCP,
                                                        source="masked")
    unit_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "costs_by_tech_and_input", SSP, RCP=RCP,
                                                       source="masked")
    feedstock_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP, RCP=RCP,
                                                            source="masked")

    total_cost = total_cost[total_cost[['sector']].isin(['biochar']).any(axis=1)]
    unit_cost = unit_cost[unit_cost[['sector']].isin(['biochar']).any(axis=1)]
    feedstock_cost = feedstock_cost[feedstock_cost[['product']].isin(
        ['beef manure', 'dairy manure', 'goat manure', 'pork manure', 'poultry manure', "biochar"]).any(axis=1)]
    data_manipulation.drop_missing(total_cost[["GCAM", biochar_year, "technology", "Units"]]).to_csv("data/data_analysis/total_cost_pyrolysis.csv")
    data_manipulation.drop_missing(unit_cost[["GCAM", biochar_year, "technology", "Units"]]).to_csv("data/data_analysis/unit_cost_pyrolysis.csv")
    data_manipulation.drop_missing(feedstock_cost[["GCAM", biochar_year, "product", "Units"]]).to_csv("data/data_analysis/feedstock_cost_pyrolysis.csv")

    feedstock_cost = feedstock_cost[feedstock_cost[['product']].isin(
        ['beef manure', 'dairy manure', 'goat manure', 'pork manure', 'poultry manure']).any(axis=1)]
    # drop outliers
    feedstock_cost = feedstock_cost[feedstock_cost[biochar_year] < 3]
    feedstock_cost[biochar_year] = feedstock_cost[biochar_year] / 0.17 * 1000
    feedstock_cost["Units"] = "USD$/ton"
    plotting.plot_regional_hist_avg(feedstock_cost, biochar_year, SSP, "count", "price distribution of manures in " + biochar_year, "product",
                                    "na", RCP, nonBaselineScenario)


def biochar_rate_by_land_size(nonBaselineScenario, RCP, SSP):
    """
    scatter plot of biochar application rate to the size of the biochar land area in the biochar year
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # read in biochar application rates, and get the application rates
    biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level.csv")
    region_names = pd.read_csv("gcam/input/gcamdata/inst/extdata/water/basin_to_country_mapping.csv", skiprows=7)

    # add extra data to dataframe to help downstream code
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['Units'] = 'kg biochar/ha/yr'
    biochar_app_rate["SSP"] = SSP[0]

    # rename GLU for mapping
    biochar_app_rate = biochar_app_rate.merge(region_names, "left", left_on="GLU", right_on="GLU_code")
    biochar_app_rate = biochar_app_rate[
        ["kg_bio_ha", "Units", "SSP", "region", "GCAM_commodity", "GCAM_subsector", "GLU_name", "Irr_Rfd"]]
    biochar_app_rate["Irr_Rfd"] = biochar_app_rate["Irr_Rfd"].str.upper()

    # extract information on crops
    biochar_app_rate['technology'] = biochar_app_rate['GCAM_commodity']
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['technology'] = biochar_app_rate.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)

    # read in detailed land allocation
    # biochar cropland application changes
    land_use = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP,
                                                      source="masked")
    # get biochar land use type information
    land_use[["GCAM_subsector", "GLU_name", "Irr_Rfd", "MGMT"]] = land_use['LandLeaf'].str.split("_", expand=True)
    land_use = land_use[
        ["GCAM", "GCAM_subsector", "GLU_name", "Irr_Rfd", "MGMT"] + [str(i) for i in c.GCAMConstants.future_x]]
    land_use["Irr_Rfd"] = land_use["Irr_Rfd"].str.upper()

    # merge datasets
    scatter_data = pd.merge(biochar_app_rate, land_use, "left", on=["GCAM", "GCAM_subsector", "GLU_name", "Irr_Rfd"])

    # remove high outlier
    outlier_cutoff = 3000  # kg/ha/yr
    scatter_data = scatter_data[scatter_data['kg_bio_ha'] < outlier_cutoff]

    # keep only biochar land management and relabel crops
    scatter_data = scatter_data[scatter_data[['MGMT']].isin(["biochar"]).any(axis=1)]
    scatter_data["GCAM_subsector"] = scatter_data.apply(
        lambda row: data_manipulation.relabel_land_crops(row, "GCAM_subsector"), axis=1)

    # plot datasets
    for i in c.GCAMConstants.biochar_x:
        # check to ensure that biochar land doesn't exist until biochar is adopted in 2035
        plotting.plot_regional_vertical(scatter_data, str(i), SSP, y_label="land area (thousand km2)",
                                        title="distribution of usage of biochar lands in " + str(i),
                                        x_column="kg_bio_ha",
                                        x_label="kg biochar/ha/yr", y_column="GCAM_subsector", RCP=RCP,
                                        nonBaselineScenario=nonBaselineScenario)


def farmer_economics(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    plots information related to the changes in farming due to biochar production
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year the biochar pathways are being evaluated
    :return: N/A
    """
    # get data
    pyrolysis_yields = data_manipulation.get_sensitivity_data(nonBaselineScenario, "ag_tech_yield", SSP, RCP=RCP,
                                                              source="masked")
    pyrolysis_land = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP,
                                                            RCP=RCP, source="masked")
    pyrolysis_profit_rate = data_manipulation.get_sensitivity_data(nonBaselineScenario, "profit_rate", SSP, RCP=RCP,
                                                                   source="masked")
    released_yields = data_manipulation.get_sensitivity_data(["released"], "ag_tech_yield", SSP, RCP=RCP,
                                                             source="original")
    released_land = data_manipulation.get_sensitivity_data(["released"], "detailed_land_allocation", SSP, RCP=RCP,
                                                           source="original")
    released_profit_rate = data_manipulation.get_sensitivity_data(["released"], "profit_rate", SSP, RCP=RCP,
                                                                  source="original")
    pyrolysis_yields["Units"] = "NA"
    released_yields["Units"] = "NA"

    # profit rates
    # change in profit to the farmer compared to baseline (hi mgmt type)
    units = pyrolysis_profit_rate["Units"].unique()[0]
    pyrolysis_profit_rate[["Crop", "basin", "rainfed", "mgmt"]] = pyrolysis_profit_rate['LandLeaf'].str.split('_',
                                                                                                              expand=True)
    released_profit_rate[["Crop", "basin", "rainfed", "mgmt"]] = released_profit_rate['LandLeaf'].str.split('_',
                                                                                                            expand=True)
    released_hi_profit = released_profit_rate[released_profit_rate[['mgmt']].isin(["hi"]).any(axis=1)].copy(
        deep=True)
    pyrolysis_biochar_profit = pyrolysis_profit_rate[
        pyrolysis_profit_rate[['mgmt']].isin(["biochar"]).any(axis=1)].copy(
        deep=True)
    pyrolysis_diff_profit = pd.merge(released_hi_profit, pyrolysis_biochar_profit, how="left",
                                     on=["GCAM", "SSP", "Crop", "basin", "rainfed"], suffixes=("_left", "_right"))
    pyrolysis_diff_profit["Units"] = units
    pyrolysis_diff_profit['Crop'] = pyrolysis_diff_profit.apply(
        lambda row: data_manipulation.relabel_land_crops(row, "Crop"), axis=1)
    for i in c.GCAMConstants.x:
        pyrolysis_diff_profit[str(i)] = pyrolysis_diff_profit[str(i) + "_right"] - pyrolysis_diff_profit[
            str(i) + "_left"]

    pyrolysis_diff_profit = pyrolysis_diff_profit.sort_values(by=biochar_year)
    flat_diff_small = pyrolysis_diff_profit[
        (-6e7 < pyrolysis_diff_profit[biochar_year]) & (pyrolysis_diff_profit[biochar_year] < 6e7)]
    flat_diff_large = pyrolysis_diff_profit[
        (-6e7 >= pyrolysis_diff_profit[biochar_year]) | (pyrolysis_diff_profit[biochar_year] >= 6e7)]
    plotting.plot_regional_hist_avg(flat_diff_small, biochar_year, ["SSP1"], "count crop-basin-irrigation-year",
                                    "histogram of small farmer profit rate changes at the crop level in " + biochar_year, "Crop", "na",
                                    RCP, nonBaselineScenario)
    plotting.plot_regional_hist_avg(flat_diff_large, biochar_year, ["SSP1"], "count crop-basin-irrigation-year",
                                    "histogram of large farmer profit rate changes at the crop level in " + biochar_year, "Crop", "na",
                                    RCP, nonBaselineScenario)

    # change in per crop supply
    pyrolysis_yields_lands = pd.merge(pyrolysis_yields, pyrolysis_land, "left", left_on=["GCAM", "SSP", "technology"],
                                      right_on=["GCAM", "SSP", "LandLeaf"], suffixes=("_left", "_right"))
    released_yields_lands = pd.merge(released_yields, released_land, "left",
                                     left_on=["GCAM", "SSP", "technology"], right_on=["GCAM", "SSP", "LandLeaf"],
                                     suffixes=("_left", "_right"))
    pyrolysis_lands_grouping = pyrolysis_yields_lands.copy(deep=True)
    released_lands_grouping = released_yields_lands.copy(deep=True)

    for i in c.GCAMConstants.x:
        pyrolysis_yields_lands[str(i)] = pyrolysis_yields_lands[str(i) + "_left"] * pyrolysis_yields_lands[
            str(i) + "_right"]
        released_yields_lands[str(i)] = released_yields_lands[str(i) + "_left"] * released_yields_lands[
            str(i) + "_right"]
        pyrolysis_lands_grouping[str(i)] = pyrolysis_yields_lands[str(i) + "_right"]
        released_lands_grouping[str(i)] = released_yields_lands[str(i) + "_right"]

    # group by crop
    pyrolysis_yields_lands[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"
    released_yields_lands[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"
    pyrolysis_lands_grouping[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"
    released_lands_grouping[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"
    pyrolysis_yields_lands["sector"] = pyrolysis_yields_lands["sector_left"]
    released_yields_lands["sector"] = released_yields_lands["sector_left"]
    pyrolysis_lands_grouping["sector"] = pyrolysis_lands_grouping["sector_left"]
    released_lands_grouping["sector"] = released_lands_grouping["sector_left"]
    pyrolysis_effective_yield = data_manipulation.group(pyrolysis_yields_lands, ["GCAM", "SSP", "sector"])
    released_effective_yield = data_manipulation.group(released_yields_lands, ["GCAM", "SSP", "sector"])
    pyrolysis_lands_grouping = data_manipulation.group(pyrolysis_lands_grouping, ["GCAM", "SSP", "sector"])
    released_lands_grouping = data_manipulation.group(released_lands_grouping, ["GCAM", "SSP", "sector"])

    # divide by available crop land
    pyrolysis_effective_yield = pd.merge(pyrolysis_effective_yield, pyrolysis_lands_grouping, "left",
                                         on=["GCAM", "SSP", "sector"],
                                         suffixes=("_left", "_right"))
    released_effective_yield = pd.merge(released_effective_yield, released_lands_grouping, "left",
                                        on=["GCAM", "SSP", "sector"],
                                        suffixes=("_left", "_right"))
    for i in c.GCAMConstants.x:
        pyrolysis_effective_yield[str(i)] = pyrolysis_effective_yield[str(i) + "_left"] / pyrolysis_effective_yield[
            str(i) + "_right"]
        released_effective_yield[str(i)] = released_effective_yield[str(i) + "_left"] / released_effective_yield[
            str(i) + "_right"]

    pyrolysis_effective_yield[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"
    released_effective_yield[
        ['Version', 'output', 'concentration', 'input', 'product', 'fuel', 'LandLeaf', 'GHG', "Units", "subsector",
         "technology"]] = "NA"

    pyrolysis_effective_yield = pyrolysis_effective_yield[c.GCAMConstants.column_order]
    released_effective_yield = released_effective_yield[c.GCAMConstants.column_order]

    # yield differences between crops
    flat_diff_effective_yields = data_manipulation.flat_difference(released_effective_yield, pyrolysis_effective_yield,
                                                                   ["GCAM", "SSP", "sector"])
    plotting.plot_regional_hist_avg(flat_diff_effective_yields, biochar_year, ["SSP1"], "count region-year",
                                    "histogram of yield changes at the crop level in " + biochar_year, "sector", "na", RCP,
                                    nonBaselineScenario)

    empty_pyro = pyrolysis_land[pyrolysis_land["LandLeaf"].str.contains("biochar")].copy(deep=True)
    for i in c.GCAMConstants.x:
        empty_pyro[str(i)] = 0
    released_land = pd.concat([released_land, empty_pyro])
    # subtract from pyrolysis land
    flat_diff_mgmt = data_manipulation.flat_difference(released_land, pyrolysis_land, ["GCAM", "SSP", "LandLeaf"])
    flat_diff_mgmt[["Crop", "basin", "rainfed", "mgmt"]] = flat_diff_mgmt['LandLeaf'].str.split('_', expand=True)
    flat_diff_mgmt = flat_diff_mgmt[flat_diff_mgmt['mgmt'].notna()]
    flat_diff_mgmt = flat_diff_mgmt.sort_values(by=biochar_year)
    flat_diff_small = flat_diff_mgmt[(-1 < flat_diff_mgmt[biochar_year]) & (flat_diff_mgmt[biochar_year] < 1)]
    flat_diff_large = flat_diff_mgmt[(-1 >= flat_diff_mgmt[biochar_year]) | (flat_diff_mgmt[biochar_year] >= 1)]
    plotting.plot_regional_hist_avg(flat_diff_small, biochar_year, ["SSP1"], "count basin-crop-irrigation",
                                    "histogram of small land mgmt changes in terms of area compared to reference scenario in " + biochar_year,
                                    "mgmt", "na", RCP, nonBaselineScenario)
    plotting.plot_regional_hist_avg(flat_diff_large, biochar_year, ["SSP1"], "count basin-crop-irrigation",
                                    "histogram of large land mgmt changes in terms of area compared to reference scenario in " + biochar_year,
                                    "mgmt", "na", RCP, nonBaselineScenario)

    # land leaf shares histogram
    pyrolysis_landleafs = data_manipulation.get_sensitivity_data(nonBaselineScenario, "land_leaf_shares", SSP, RCP=RCP,
                                                                 source="masked")
    pyrolysis_landleafs[["Crop", "basin", "rainfed", "MGMT"]] = pyrolysis_landleafs['LandLeaf'].str.split('_',
                                                                                                          expand=True)
    pyrolysis_landleafs = pyrolysis_landleafs[pyrolysis_landleafs[['MGMT']].isin(["biochar"]).any(axis=1)]
    pyrolysis_landleafs["Units"] = "land share"
    for i in c.GCAMConstants.biochar_x:
        plotting.plot_regional_hist_avg(pyrolysis_landleafs, str(i), SSP, "count land leafs",
                                        "histogram of land leaf shares for biochar lands in " + str(i), "Crop", "na",
                                        RCP, nonBaselineScenario)

    # output differences in carbon prices
    c_pyro_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "CO2_prices", SSP, RCP=RCP,
                                                          source="masked")
    c_rel_price = data_manipulation.get_sensitivity_data(["released"], "CO2_prices", SSP, RCP=RCP,
                                                         source="original")
    product = ["CO2"]
    c_rel_price = c_rel_price[c_rel_price[['product']].isin(product).any(axis=1)]
    c_pyro_price = c_pyro_price[c_pyro_price[['product']].isin(product).any(axis=1)]
    for i in c.GCAMConstants.x:
        c_rel_price[str(i)] = c_rel_price[
                                  str(i)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
        c_pyro_price[str(i)] = c_pyro_price[
                                   str(i)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
    flat_diff_c_price = data_manipulation.flat_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
    flat_diff_c_price["Units"] = "USD$2024/t C"
    perc_diff_c_price = data_manipulation.percent_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
    data_manipulation.drop_missing(flat_diff_c_price).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/change_in_carbon_price.csv")
    data_manipulation.drop_missing(perc_diff_c_price).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/percent_change_in_carbon_price.csv")


def figure1(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 1
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathway being considered
    :param SSP: the SSP pathway being considered
    :param biochar_year: the year being analyzed in detail
    :return: N/A
    """
    # plotting CO2 sequestering
    co2_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                           "CO2_emissions_by_tech_excluding_resource_production",
                                                           SSP, RCP=RCP, source="masked")
    co2_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    co2_pyrolysis['technology'] = co2_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                      axis=1)
    co2_pyrolysis['Units'] = "Net change in Mt C/yr"
    products = ["beef biochar", "dairy biochar", "pork biochar", "poultry biochar", "goat biochar"]
    co2_pyrolysis = co2_pyrolysis[co2_pyrolysis['technology'].str.contains("|".join(products))]
    # make two copies so as to split the C coefficient between avoided and sequestered
    co2_seq_pyrolysis = co2_pyrolysis.copy(deep=True)
    co2_avd_pyrolysis = co2_pyrolysis

    # carbon sequestration is portrayed as a negative emission in GCAM, but measured as a positive in this study
    for i in c.GCAMConstants.future_x:
        co2_seq_pyrolysis[str(i)] = 3.664 * co2_seq_pyrolysis.apply(
            lambda row: data_manipulation.seq_C(row, "technology", str(i)),
            axis=1)  # 3.664 converts C to CO2-eq
        co2_avd_pyrolysis[str(i)] = 3.664 * co2_avd_pyrolysis.apply(
            lambda row: data_manipulation.avd_C(row, "technology", str(i)),
            axis=1)
    co2_seq_pyrolysis["Units"] = "Sequestered C in biochar"
    co2_avd_pyrolysis["Units"] = "Net pyrolysis CO$_2$"

    out_co2_seq_pyrolysis = data_manipulation.get_CI(co2_seq_pyrolysis, "technology")
    out_co2_avd_pyrolysis = data_manipulation.get_CI(co2_avd_pyrolysis, "technology")

    # output non-grouped GHG impacts
    data_manipulation.drop_missing(out_co2_seq_pyrolysis).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_c_sequestration.csv")
    data_manipulation.drop_missing(out_co2_avd_pyrolysis).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_c_avoidance.csv")

    # group data for plotting
    co2_seq_pyrolysis = data_manipulation.group(co2_seq_pyrolysis, ["SSP", "Version", "Units"])
    co2_avd_pyrolysis = data_manipulation.group(co2_avd_pyrolysis, ["SSP", "Version", "Units"])

    # avoided agricultural emissions from lands managed with biochar
    ghg_er = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                    "nonCO2_emissions_by_tech_excluding_resource_production",
                                                    SSP, RCP=RCP, source="masked")

    ag_avd_n2o_land = ghg_er[ghg_er['technology'].str.contains("biochar")]  # get only biochar lut
    ag_avd_n2o_land = ag_avd_n2o_land[ag_avd_n2o_land[['GHG']].isin(["N2O_AGR"]).any(axis=1)]  # select specific ghg
    ag_avd_n2o_land = data_manipulation.group(ag_avd_n2o_land,
                                              ["Version", "GHG"])  # group all biochar land leafs by version
    for i in c.GCAMConstants.future_x:
        ag_avd_n2o_land[str(i)] = ag_avd_n2o_land.apply(
            lambda row: data_manipulation.avd_soil_emissions(row, "GHG", str(i)), axis=1)
    ag_avd_n2o_land["Units"] = "Avoided cropland N$_2$O"

    out_ag_avd_n2o_land = data_manipulation.get_CI(ag_avd_n2o_land, "GHG")

    # output non-grouped GHG impacts
    data_manipulation.drop_missing(out_ag_avd_n2o_land).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_soil_N2O_flux.csv")

    # avoided CH4 and N2O emissions from avoided biomass decomposition
    biochar_ghg_er = ghg_er[ghg_er['technology'].str.contains("biochar")].copy(deep=True)
    biochar_ghg_er['technology'] = biochar_ghg_er.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                        axis=1)
    biochar_ghg_er = biochar_ghg_er[biochar_ghg_er['technology'].str.contains("|".join(products))]  # removes LUT
    biochar_ghg_er = data_manipulation.group(biochar_ghg_er, ["SSP", "Version", "GHG"])

    biochar_ghg_er["Units"] = biochar_ghg_er.apply(lambda row: "Avoided biomass decomposition N$_2$O" if row[
                                                                                                             "GHG"] == "N2O" else "Avoided biomass decomposition CH$_4$",
                                                   axis=1)

    # convert using GWP values
    for i in c.GCAMConstants.future_x:
        biochar_ghg_er[str(i)] = biochar_ghg_er.apply(
            lambda row: data_manipulation.ghg_ER(row, "GHG", str(i)), axis=1)

    # print grouped data
    out_biochar_ghg_er = data_manipulation.get_CI(biochar_ghg_er, "GHG")
    data_manipulation.drop_missing(out_biochar_ghg_er).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_ghg_avoided_decomposition.csv")

    # get luc emissions data
    released_luc = data_manipulation.get_sensitivity_data(["released"], "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_luc = data_manipulation.get_sensitivity_data(nonBaselineScenario, "LUC_emissions_by_LUT", SSP,
                                                           RCP=RCP, source="masked")

    released_luc = data_manipulation.group(released_luc, ["SSP", "Version"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["SSP", "Version"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["SSP"])
    for i in c.GCAMConstants.future_x:
        flat_diff_luc[str(i)] = 3.664 * flat_diff_luc[str(i)]  # 3.664 converts C to CO2-eq
    flat_diff_luc["Units"] = "Change in LUC emissions"

    out_flat_diff_luc = data_manipulation.get_CI(flat_diff_luc, "Units")
    data_manipulation.drop_missing(out_flat_diff_luc).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_LUC_emissions.csv")

    # combine all direct sources of GHG emissions changes into a single df/graph
    biochar_ghg_emissions = pd.concat([biochar_ghg_er, co2_avd_pyrolysis, ag_avd_n2o_land])

    # calculate sum of all non-indirect, non-CDR emissions impact
    df_GHG_ER = biochar_ghg_emissions.groupby(
        "Version").sum().reset_index().copy(deep=True)  # sum in new dataframe. It's fine that all other information is overwritten, as units are all Mt CO2-eq
    df_GHG_ER["Units"] = "Net GHG ER"  # this unit is used to label the graph
    df_GHG_ER["SSP"] = ag_avd_n2o_land["SSP"].unique()[0]

    biochar_ghg_emissions = pd.concat([biochar_ghg_emissions, co2_seq_pyrolysis, flat_diff_luc])

    # calculate net CO2 impact
    df_sum = biochar_ghg_emissions.groupby(
        "Version").sum().reset_index()  # sum in new dataframe. It's fine that all other information is overwritten, as units are all Mt CO2-eq
    df_sum["Units"] = "Net Emissions Impact"  # this unit is used to label the graph
    df_sum["SSP"] = ag_avd_n2o_land["SSP"].unique()[0]
    biochar_ghg_emissions = pd.concat([biochar_ghg_emissions, df_GHG_ER, df_sum])
    biochar_ghg_emissions["GHG_ER_type"] = biochar_ghg_emissions["Units"]
    biochar_ghg_emissions["Units"] = "GHG Emissions (Mt CO$_2$-eq/yr)"

    # output values of avoided and sequestered ghg emissions from biochar
    out_biochar_ghg_emissions = data_manipulation.get_CI(biochar_ghg_emissions, "GHG_ER_type")
    data_manipulation.drop_missing(out_biochar_ghg_emissions).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/all_biochar_ghg_cdr_sources.csv")

    # plotting ghg emissions avoidance
    plotting.plot_line_by_product(out_biochar_ghg_emissions, out_biochar_ghg_emissions["GHG_ER_type"].unique(),
                                  "GHG_ER_type",
                                  [SSP[0]], "SSP",
                                  "ghg emissions changes in " + SSP[0], RCP, nonBaselineScenario)

    # output values of biochar supply
    supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP, RCP=RCP,
                                                    source="masked")
    biochar_supply = supply[supply[['product']].isin(["biochar"]).any(axis=1)].copy(deep=True)
    biochar_supply = data_manipulation.group(biochar_supply, ["Version", "Units"])
    biochar_supply["Units"] = "Mt Biochar"

    manure_supply = supply[
        supply[['product']].isin(["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(
            axis=1)].copy(deep=True)
    manure_supply = data_manipulation.group(manure_supply, ["Version", "Units"])
    manure_supply["Units"] = "Mt Manure Mix"

    # calculate "LCA" impacts of biochar by mass biochar and global mass feedstock mix
    LCA_biochar = pd.merge(df_sum, biochar_supply, on="Version", suffixes=("", "_kg biochar"))
    LCA_manure = pd.merge(df_sum, manure_supply, on="Version", suffixes=("", "_kg biochar"))
    for i in c.GCAMConstants.future_x:
        if np.isnan(LCA_biochar[str(i) + "_kg biochar"][0]):
            LCA_biochar[str(i)] = 0
            LCA_manure[str(i)] = 0
        else:
            LCA_biochar[str(i)] = LCA_biochar[str(i) + ""] / LCA_biochar[str(i) + "_kg biochar"]
            LCA_manure[str(i)] = LCA_manure[str(i) + ""] / LCA_manure[str(i) + "_kg biochar"]
    LCA_biochar["Units"] = "kg CO2-eq/kg biochar"
    LCA_manure["Units"] = "kg CO2-eq/kg manure mix"
    LCA_biochar = LCA_biochar[c.GCAMConstants.column_order]
    LCA_manure = LCA_manure[c.GCAMConstants.column_order]

    LCA = pd.concat([biochar_supply, LCA_biochar, manure_supply, LCA_manure])

    out_LCA = data_manipulation.get_CI(LCA, "Units")
    data_manipulation.drop_missing(out_LCA).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/biochar_manure_supply_GWP_kg_FU.csv")


def figure2(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 2
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathway being considered
    :param SSP: the SSP pathway being considered
    :param biochar_year: the year being analyzed in detail
    :return: N/A
    """
    # get CI for area of crop land with biochar application
    CI_land_use = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP,
                                                      source="masked",
                                                      only_first_scenario=False)  # only take the first/baseline scenario

    # get land use type information
    CI_land_use[["Crop", "Basin", "IRR_RFD", "MGMT"]] = CI_land_use['LandLeaf'].str.split("_", expand=True)
    CI_land_use["Crop"] = CI_land_use.apply(lambda row: data_manipulation.relabel_land_crops(row, "Crop"), axis=1)
    # group land use by crop and management type
    unit = CI_land_use.groupby(["Crop", "MGMT"]).first().reset_index()["Units"]
    CI_land_use = CI_land_use.groupby(["Crop", "MGMT", "Version"]).sum(min_count=1)
    CI_land_use = CI_land_use.reset_index()
    CI_land_use['Units'] = unit
    CI_land_use['MGMT'] = CI_land_use.apply(lambda row: data_manipulation.relabel_MGMT(row), axis=1)
    CI_land_use["cat"] = CI_land_use["Crop"] + CI_land_use["MGMT"]

    CI_land_use_global = CI_land_use.groupby(["MGMT", "Version"]).sum(min_count=1).reset_index() # group by management for global numbers
    CI_land_use_crop = data_manipulation.get_CI(CI_land_use, "cat") # group by mgmt and crop for crop-specific numbers
    CI_land_use_global = data_manipulation.get_CI(CI_land_use_global, "MGMT")
    data_manipulation.drop_missing(CI_land_use_global).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/land_use_by_mgmt.csv")
    data_manipulation.drop_missing(CI_land_use_crop).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/land_use_by_mgmt_and_crop.csv")


    # biochar cropland application changes
    land_use = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP,
                                                      source="masked",
                                                      only_first_scenario=True)  # only take the first/baseline scenario
    # get land use type information
    land_use[["Crop", "Basin", "IRR_RFD", "MGMT"]] = land_use['LandLeaf'].str.split("_", expand=True)
    land_use["Crop"] = land_use.apply(lambda row: data_manipulation.relabel_land_crops(row, "Crop"), axis=1)
    # group land use by crop and management type
    unit = land_use.groupby(["Crop", "MGMT"]).first().reset_index()["Units"]
    land_use = land_use.groupby(["Crop", "MGMT", "Basin", "GCAM"]).sum(min_count=1)
    land_use = land_use.reset_index()
    land_use['Units'] = unit
    land_use['SSP'] = land_use.apply(lambda row: data_manipulation.relabel_SSP(row), axis=1)
    land_use['MGMT'] = land_use.apply(lambda row: data_manipulation.relabel_MGMT(row), axis=1)
    land_use['GCAM'] = land_use.apply(lambda row: data_manipulation.relabel_region(row), axis=1)

    # process alluvial data
    scale_factor = 10
    base_year = "2020"
    land_for_alluvial = data_manipulation.process_luc(land_use, scale_factor, base_year, biochar_year)

    # build a alluvial plot
    land_for_alluvial[[biochar_year, "Management_" + biochar_year, "Region_" + biochar_year]] = land_for_alluvial[
        biochar_year].str.split("_",
                                expand=True)
    land_for_alluvial[[base_year, "Management_" + base_year, "Region_" + base_year]] = land_for_alluvial[
        base_year].str.split("_",
                             expand=True)
    counts = land_for_alluvial["Management_" + biochar_year].value_counts() / scale_factor * 1000

    # Region_ biochar_year data is stored in Region
    land_for_alluvial["Region"] = land_for_alluvial.apply(
        lambda row: data_manipulation.relabel_region_alluvial(row, biochar_year, base_year), axis=1)
    land_for_alluvial["Management"] = land_for_alluvial.apply(
        lambda row: data_manipulation.relabel_management_alluvial(row, counts, "Management_" + biochar_year), axis=1)
    land_for_alluvial = land_for_alluvial.sort_values(by=['Management', "Region"], ascending=[True, True])

    # get percentage of land with different management types on a regional basis
    region_management_type = ""
    for usage in land_for_alluvial["Management"].unique():
        for gcam in land_for_alluvial["Region"].unique():
            regional = land_for_alluvial[land_for_alluvial[['Region']].isin([gcam]).any(axis=1)]
            region_management_type = region_management_type + (str(usage) + ", " + str(gcam) + ", " +
                                                               str(len(regional[regional["Management"] == usage]) / len(
                                                                   regional) * 100) + ",%," +
                                                               str(len(regional[regional["Management"] == usage])*scale_factor) + ",km2\n") # scale factor used to adjust units
    plotting.plot_alluvial(land_for_alluvial, biochar_year, base_year)

    # write out .csv data for different land management types
    with open("data/data_analysis/supplementary_tables/" + str(
            RCP) + "/regional_land_mgmt.csv", 'w') as csvFile:
        csvFile.write(region_management_type)

    # regional land use change
    released_land = data_manipulation.get_sensitivity_data(["released"], "detailed_land_allocation", SSP, RCP=RCP,
                                                           source="original")
    pyrolysis_land = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP,
                                                            RCP=RCP, source="masked")
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                    axis=1)
    pyrolysis_land["LandLeaf"] = pyrolysis_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                      axis=1)
    pyrolysis_land = data_manipulation.group(pyrolysis_land, ["GCAM", "LandLeaf", "Version"])
    released_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf", "Version"])
    flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    flat_diff_land["Units"] = "Land Use Change (thousand km$^2$)"
    global_land = data_manipulation.group(flat_diff_land, ["LandLeaf", "Version"])
    flat_diff_land = data_manipulation.group(flat_diff_land, ["GCAM", "LandLeaf", "Version"])
    flat_diff_land["categorization"] = flat_diff_land["GCAM"] + flat_diff_land["LandLeaf"]

    CI_flat_diff_land = data_manipulation.get_CI(flat_diff_land, "categorization")
    CI_global_land = data_manipulation.get_CI(global_land, "LandLeaf")

    # get median data for each for plotting
    CI_flat_diff_land_median = CI_flat_diff_land[CI_flat_diff_land["Version"] == "Median"]
    CI_global_land_median = CI_global_land[CI_global_land["Version"] == "Median"]

    plotting.plot_stacked_bar_product(CI_flat_diff_land_median, str(biochar_year), SSP, "LandLeaf",
                                      "median land use change by region in " + str(biochar_year), RCP,
                                      nonBaselineScenario)
    data_manipulation.drop_missing(CI_global_land).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/global_LUC.csv")

    plotting.plot_stacked_bar_product(CI_global_land_median, c.GCAMConstants.biochar_x, SSP, "LandLeaf",
                                      "median global land use change by year", RCP, nonBaselineScenario)

    perc_diff_land = data_manipulation.percent_of_total(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"],
                                                        biochar_year)
    perc_diff_land["Units"] = "Land Use Change (%)"
    perc_diff_land['GCAM'] = perc_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    perc_diff_land["LandLeaf"] = perc_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    perc_diff_land["categorization"] = perc_diff_land["GCAM"] + perc_diff_land["LandLeaf"]
    CI_perc_diff_land = data_manipulation.get_CI(perc_diff_land, "categorization")
    CI_perc_diff_land = CI_perc_diff_land[CI_perc_diff_land["Version"] == "Median"]
    plotting.plot_stacked_bar_product(CI_perc_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "median % land use change by region in " + str(biochar_year), RCP,
                                      nonBaselineScenario)


def figure3(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 3
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathway being considered
    :param SSP: the SSP pathway being considered
    :param biochar_year: the year being analyzed in detail
    :return: N/A
    """
    # Biochar Supply
    supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP, RCP=RCP,
                                                    source="masked", only_first_scenario=False)
    biochar_supply = supply[supply[['product']].isin(["biochar"]).any(axis=1)].copy(deep=True)
    biochar_supply = data_manipulation.group(biochar_supply, ["SSP", "Version"])
    biochar_supply["Units"] = "Supply of biochar (Mt)"

    plotting.sensitivity(biochar_supply, RCP, nonBaselineScenario[0], biochar_year, "Units", "Version", nonBaselineScenario,
                         title="biochar supply (Mt)")

    # frequency of biochar prices
    biochar_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP, RCP=RCP,
                                                           source="masked")
    biochar_price['product'] = biochar_price.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    biochar_price = biochar_price[biochar_price[['product']].isin(["biochar"]).any(axis=1)]
    biochar_price["Units"] = "$/ton biochar"
    for i in c.GCAMConstants.x:
        biochar_price[str(i)] = biochar_price[str(i)] / .17 * 1000

    biochar_price_plotting = biochar_price.melt(["GCAM", "product", "Version", "Units"],
                                                [str(i) for i in c.GCAMConstants.biochar_x])
    plotting.plot_regional_hist_avg(biochar_price_plotting, 'value', SSP, "count region+year+scenario combinations",
                                    "histogram of price of biochar", "variable", "na", RCP, nonBaselineScenario)

    # CI outputs
    CI_biochar_price = data_manipulation.get_CI(biochar_price, "GCAM")
    data_manipulation.drop_missing(CI_biochar_price).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/biochar_price.csv")

    # manure prices and cost breakdown for plant operators
    total_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "costs_by_tech", SSP, RCP=RCP,
                                                        source="masked")
    unit_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "costs_by_tech_and_input", SSP, RCP=RCP,
                                                       source="masked")
    feedstock_cost = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP, RCP=RCP,
                                                            source="masked")

    total_cost = total_cost[total_cost[['sector']].isin(['biochar']).any(axis=1)]
    unit_cost = unit_cost[unit_cost[['sector']].isin(['biochar']).any(
        axis=1)]  # don't need CI for unit costs - constants defined in input .csv - even sensitivity unit costs are fixed
    feedstock_cost = feedstock_cost[feedstock_cost[['product']].isin(
        ['beef manure', 'dairy manure', 'goat manure', 'pork manure', 'poultry manure']).any(axis=1)]

    # update prices to 2024 USD
    for i in c.GCAMConstants.x:
        total_cost[str(i)] = total_cost[str(i)] / .17 * 1000
        unit_cost[str(i)] = unit_cost[str(i)] / .17 * 1000
        feedstock_cost.loc[feedstock_cost[str(i)] > 0.034, str(i)] = np.nan  # remove outlier prices > $200/ton manure in current prices
        feedstock_cost[str(i)] = feedstock_cost[str(i)] / .17 * 1000

    # update units
    total_cost["Units"] = "$/ton biochar"
    unit_cost["Units"] = "$/ton biochar"
    feedstock_cost["Units"] = "$/ton manure"
    total_cost["categorization"] = total_cost["GCAM"] + total_cost["technology"]
    feedstock_cost["categorization"] = feedstock_cost["GCAM"] + feedstock_cost["product"]

    CI_total_cost = data_manipulation.get_CI(total_cost, "categorization")
    CI_feedstock_cost = data_manipulation.get_CI(feedstock_cost, "categorization")
    data_manipulation.drop_missing(CI_total_cost).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/total_cost_pyrolysis.csv")
    data_manipulation.drop_missing(unit_cost).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/unit_cost_pyrolysis.csv")
    data_manipulation.drop_missing(CI_feedstock_cost).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/feedstock_cost_pyrolysis.csv")

    feedstock_cost_plotting = feedstock_cost.melt(["GCAM", "product", "Version", "Units"], [biochar_year])
    feedstock_cost_plotting = feedstock_cost_plotting.dropna()
    plotting.plot_regional_hist_avg(feedstock_cost_plotting, 'value', SSP, "count region+scenario combinations",
                                    "histogram of price of manures in 2050", "product", "na", RCP, nonBaselineScenario)

    # profit rates
    # get data
    pyrolysis_profit_rate = data_manipulation.get_sensitivity_data(nonBaselineScenario, "profit_rate", SSP, RCP=RCP,
                                                                   source="masked")
    released_profit_rate = data_manipulation.get_sensitivity_data(["released"], "profit_rate", SSP, RCP=RCP,
                                                                  source="original")
    # change in profit to the farmer compared to baseline (hi mgmt type)
    pyrolysis_profit_rate[["Crop", "basin", "rainfed", "mgmt"]] = pyrolysis_profit_rate['LandLeaf'].str.split('_',
                                                                                                              expand=True)
    released_profit_rate[["Crop", "basin", "rainfed", "mgmt"]] = released_profit_rate['LandLeaf'].str.split('_',
                                                                                                            expand=True)
    released_hi_profit = released_profit_rate[released_profit_rate[['mgmt']].isin(["hi"]).any(axis=1)].copy(
        deep=True)
    pyrolysis_biochar_profit = pyrolysis_profit_rate[
        pyrolysis_profit_rate[['mgmt']].isin(["biochar"]).any(axis=1)].copy(
        deep=True)
    pyrolysis_diff_profit = pd.merge(released_hi_profit, pyrolysis_biochar_profit, how="left",
                                     on=["GCAM", "SSP", "Crop", "basin", "rainfed"], suffixes=("_left", "_right"))
    pyrolysis_diff_profit["Units"] = "Change in Profit Rate (%)"
    pyrolysis_diff_profit['Crop'] = pyrolysis_diff_profit.apply(
        lambda row: data_manipulation.relabel_land_crops(row, "Crop"), axis=1)
    for i in c.GCAMConstants.x:
        pyrolysis_diff_profit[str(i)] = 100 * (pyrolysis_diff_profit[str(i) + "_right"] - pyrolysis_diff_profit[
            str(i) + "_left"]) / pyrolysis_diff_profit[str(i) + "_left"]

    pyrolysis_diff_profit = pyrolysis_diff_profit.sort_values(by=biochar_year)
    # drop rows where there is .nan in 2050
    pyrolysis_diff_profit.dropna(subset=[biochar_year], inplace=True)
    # drop rows where the profit rate is 0 for biochar - i.e. no crops are grown
    pyrolysis_diff_profit = pyrolysis_diff_profit[pyrolysis_diff_profit[biochar_year + "_right"] != 0]
    # drop outlier rows
    pyrolysis_diff_profit = pyrolysis_diff_profit[
        (-3e2 < pyrolysis_diff_profit[biochar_year]) & (pyrolysis_diff_profit[biochar_year] < 1e2)]

    plotting.plot_regional_hist_avg(pyrolysis_diff_profit, biochar_year, ["SSP1"], "count crop-basin-irrigation-scenario",
                                    "histogram of percentage profit rate changes at the crop level in " + biochar_year,
                                    "Crop", "na", RCP, nonBaselineScenario)

    # read in biochar application rates, and get the application rates
    baseline_biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level_baseline_yield_baseline.csv")
    low_biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level_baseline_yield_low.csv")
    high_biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level_baseline_yield_high.csv")

    outlier_cutoff = 15000  # kg/ha/yr
    biochar_app_rate_baseline_no_outlier = baseline_biochar_app_rate[baseline_biochar_app_rate["kg_bio_ha"] < outlier_cutoff]
    biochar_app_rate_low_no_outlier = low_biochar_app_rate[low_biochar_app_rate["kg_bio_ha"] < outlier_cutoff]
    biochar_app_rate_high_no_outlier = high_biochar_app_rate[high_biochar_app_rate["kg_bio_ha"] < outlier_cutoff]
    P_app_rate_no_outlier = baseline_biochar_app_rate[baseline_biochar_app_rate["kg_P_ha"] < 200]

    # plotting maps/tables for each crop by GLU, etc
    # uncomment to recreate the maps
    plotting.basin_data(biochar_app_rate_baseline_no_outlier, "kg_bio_ha", "baseline/biochar application rate by")
    plotting.basin_data(biochar_app_rate_low_no_outlier, "kg_bio_ha", "low/biochar application rate by")
    plotting.basin_data(biochar_app_rate_high_no_outlier, "kg_bio_ha", "high/biochar application rate by")
    plotting.basin_data(P_app_rate_no_outlier, "kg_P_ha", "P/application rate by")

    # combine all 3 scenarios, calculate and output CI
    biochar_app_rate_CI = pd.concat([biochar_app_rate_low_no_outlier, biochar_app_rate_baseline_no_outlier, biochar_app_rate_high_no_outlier])
    biochar_app_rate_CI["cat"] = biochar_app_rate_CI["GLU"] + "_" + biochar_app_rate_CI["GCAM_subsector"] + "_" + biochar_app_rate_CI["region"]
    lmu = pd.DataFrame(columns=biochar_app_rate_CI.columns)
    for i in biochar_app_rate_CI["cat"].unique():
        # get a dataframe just for this product
        data = biochar_app_rate_CI[biochar_app_rate_CI["cat"] == i].copy(deep=True)

        # copy 3 rows over to lmu
        output_vals = data.head(3).copy(deep=True)
        if len(output_vals) == 3:
            output_vals["Version"] = ["Lower CI", "Median", "Upper CI"]

            np_data = data["kg_bio_ha"].dropna().values  # get data for a particular year
            sMu = np.mean(np_data)
            median = np.median(np_data)
            sem = stats.sem(np_data)
            n = len(np_data)
            df = n - 1
            lower, upper = stats.t.interval(0.95, df=df, loc=sMu,
                                            scale=sem)  # confidence interval with equal areas around the mean

            # add lower, mean, upper to output dataframe
            output_vals["kg_bio_ha"] = [lower, median, upper]

            # add lower level low mean upper dataframe to higher level one
            lmu = pd.concat([lmu, output_vals])

    data_manipulation.drop_missing(lmu).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/crop-basin-region-biochar-application-rate_CI.csv")

    # add extra data to dataframe to help downstream code
    biochar_app_rate = baseline_biochar_app_rate.copy(deep=True)
    biochar_app_rate[biochar_year] = biochar_app_rate['kg_bio_ha']
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['Units'] = 'kg biochar/ha/yr'
    biochar_app_rate["SSP"] = SSP[0]

    # extract information on crops
    biochar_app_rate['technology'] = biochar_app_rate['GCAM_commodity']
    biochar_app_rate['technology'] = biochar_app_rate.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)

    # plot histogram of biochar application rates
    # adjusted to remove outliers for plotting purposes
    outlier_cutoff = 30000  # kg/ha/yr
    biochar_app_rate_no_outlier = biochar_app_rate[biochar_app_rate[biochar_year] < outlier_cutoff]
    plotting.plot_regional_hist_avg(biochar_app_rate_no_outlier, biochar_year, [SSP],
                                    "region-basin-crop-irr combination count",
                                    "histogram of outlier " + str(
                                        outlier_cutoff) + "kg per ha removed biochar app rates", "technology", "na",
                                    RCP, nonBaselineScenario)

    outlier_cutoff = 5000  # kg/ha/yr
    lower_cutoff = 250
    biochar_app_rate_no_outlier = biochar_app_rate[biochar_app_rate[biochar_year] < outlier_cutoff]
    biochar_app_rate_no_outlier = biochar_app_rate_no_outlier[biochar_app_rate_no_outlier[biochar_year] > lower_cutoff]
    plotting.plot_regional_hist_avg(biochar_app_rate_no_outlier, biochar_year, [SSP],
                                    "region-basin-crop-irr combination count",
                                    "histogram of outlier " + str(lower_cutoff) + "-" + str(outlier_cutoff)
                                    + " kg per ha removed biochar app rates", "technology", "na", RCP,
                                    nonBaselineScenario)

    # global fertilizer reduction
    released_N = data_manipulation.get_sensitivity_data(["released"], "ammonia_production_by_tech", SSP, RCP=RCP,
                                                        source="original")
    pyrolysis_N = data_manipulation.get_sensitivity_data(nonBaselineScenario, "ammonia_production_by_tech", SSP,
                                                         RCP=RCP, source="masked")
    released_N = data_manipulation.group(released_N, ["Version"])  # get global level data
    pyrolysis_N = data_manipulation.group(pyrolysis_N, ["Version"])  # get global level data

    flat_diff_N = data_manipulation.flat_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    perc_diff_N = data_manipulation.percent_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    perc_diff_N_CI = data_manipulation.get_CI(perc_diff_N, "LandLeaf")
    flat_diff_N_CI = data_manipulation.get_CI(flat_diff_N, "LandLeaf")

    data_manipulation.drop_missing(flat_diff_N_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/change_in_N.csv")
    data_manipulation.drop_missing(perc_diff_N_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/percent_difference_in_N.csv")


def figure4(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    returns information related to increased herd sizes and feed demands due to the introduction of pyrolysis
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year the biochar pathways are being evaluated
    :return: N/A
    """
    # gather data and slice by product types
    released_supply = data_manipulation.get_sensitivity_data(["released"], "supply_of_all_markets", SSP, RCP=RCP,
                                                             source="original")
    pyrolysis_supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP,
                                                              RCP=RCP, source="masked")
    feed = ["FodderHerb_Residue", "FeedCrops", "Pasture_FodderGrass", "Scavenging_Other"]  # the different feed types
    released_feed = released_supply[released_supply[['product']].isin(feed).any(axis=1)].copy(deep=True)
    released_feed['product'] = released_feed.apply(lambda row: data_manipulation.relabel_feeds(row), axis=1)
    pyrolysis_feed = pyrolysis_supply[pyrolysis_supply[['product']].isin(feed).any(axis=1)].copy(deep=True)
    pyrolysis_feed['product'] = pyrolysis_feed.apply(lambda row: data_manipulation.relabel_feeds(row), axis=1)
    products = ["Beef", "Dairy", "SheepGoat", "Pork", "Poultry"]  # the different product types
    released_products = released_supply[released_supply[['product']].isin(products).any(axis=1)].copy(deep=True)
    pyrolysis_products = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)].copy(deep=True)
    released_products['product'] = released_products.apply(lambda row: data_manipulation.relabel_animals(row), axis=1)
    pyrolysis_products['product'] = pyrolysis_products.apply(lambda row: data_manipulation.relabel_animals(row), axis=1)

    # calculate changes compared to released scenario
    perc_diff_feed = data_manipulation.percent_difference(released_feed, pyrolysis_feed, ["GCAM", "SSP", "product"])
    perc_diff_animal = data_manipulation.percent_difference(released_products, pyrolysis_products,
                                                            ["GCAM", "SSP", "product"])
    perc_diff_feed["categorization"] = perc_diff_feed["product"] + perc_diff_feed["GCAM"]
    perc_diff_animal["categorization"] = perc_diff_animal["product"] + perc_diff_animal["GCAM"]

    perc_diff_feed_CI = data_manipulation.get_CI(perc_diff_feed, "categorization")
    perc_diff_animal_CI = data_manipulation.get_CI(perc_diff_animal, "categorization")

    perc_diff_feed_CI["Units"] = "median change in feed supply compared to reference scenario (%)"
    perc_diff_animal_CI["Units"] = "median change in\n herd size compared\n to reference scenario (%)"

    # plot figures on CI
    plotting.plot_world(perc_diff_feed_CI[perc_diff_feed_CI["Version"] == "Median"], perc_diff_feed_CI['product'].unique(), SSP, "product", "product", [biochar_year],
                        "CI for percentage change in animal feed by region in " + biochar_year, RCP, nonBaselineScenario)
    plotting.plot_world(perc_diff_animal_CI[perc_diff_animal_CI["Version"] == "Median"], perc_diff_animal_CI['product'].unique(), SSP, "product", "product",
                        [biochar_year],
                        "CI for percentage change in animal products by region in " + biochar_year, RCP, nonBaselineScenario)

    # get net differences at global level
    released_feed = data_manipulation.group(released_feed, ["SSP", "Version"])
    pyrolysis_feed = data_manipulation.group(pyrolysis_feed, ["SSP", "Version"])
    total_perc_diff_feed = data_manipulation.percent_difference(released_feed, pyrolysis_feed, ["SSP"])
    released_products = data_manipulation.group(released_products, ["SSP", "Version"])
    pyrolysis_products = data_manipulation.group(pyrolysis_products, ["SSP", "Version"])
    total_perc_diff_animal = data_manipulation.percent_difference(released_products, pyrolysis_products, ["SSP"])

    # recombine data to be exported
    total_perc_diff_feed_CI = data_manipulation.get_CI(total_perc_diff_feed, "SSP")
    total_perc_diff_animal_CI = data_manipulation.get_CI(total_perc_diff_animal, "SSP")

    # print out data to .csv
    data_manipulation.drop_missing(total_perc_diff_feed_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/CI_total_change_in_animal_feed.csv")
    data_manipulation.drop_missing(perc_diff_feed_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/CI_percent_change_in_animal_feed.csv")
    data_manipulation.drop_missing(total_perc_diff_animal_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/CI_total_change_in_animal_herd.csv")
    data_manipulation.drop_missing(perc_diff_animal_CI).to_csv(
        "data/data_analysis/supplementary_tables/" + str(RCP) + "/CI_percent_change_in_animal_herd.csv")


def figure5(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 5
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: N/A
    """
    # get calorie data
    released_Pcal = data_manipulation.get_sensitivity_data(["released"], "food_consumption_by_type_specific", SSP,
                                                           RCP=RCP, source="original")
    pyrolysis_Pcal = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_consumption_by_type_specific",
                                                            SSP, RCP=RCP, source="masked")

    flat_diff_Pcal = data_manipulation.flat_difference(released_Pcal, pyrolysis_Pcal,
                                                       ["GCAM", "SSP", "subsector", "subsector.1",
                                                        "technology"]).drop_duplicates()
    perc_diff_Pcal = data_manipulation.percent_difference(released_Pcal, pyrolysis_Pcal,
                                                          ["GCAM", "SSP", "subsector", "subsector.1",
                                                           "technology"]).drop_duplicates()

    # calculate difference
    # at a higher level of aggregation
    flat_diff_Pcal_plotting = data_manipulation.group(flat_diff_Pcal, ["GCAM", "subsector", "Version"])
    flat_diff_Pcal_plotting['subsector'] = flat_diff_Pcal_plotting.apply(
        lambda row: data_manipulation.relabel_food(row, "subsector"), axis=1)
    flat_diff_Pcal_plotting['GCAM'] = flat_diff_Pcal_plotting.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    perc_diff_Pcal['technology'] = perc_diff_Pcal.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)
    perc_diff_Pcal['GCAM'] = perc_diff_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_Pcal_plotting["categorization"] = flat_diff_Pcal_plotting["GCAM"] + flat_diff_Pcal_plotting["subsector"]
    perc_diff_Pcal["categorization"] = perc_diff_Pcal["GCAM"] + perc_diff_Pcal["technology"]

    # turn into CI data
    flat_diff_Pcal_plotting = data_manipulation.get_CI(flat_diff_Pcal_plotting, "categorization")
    CI_perc_diff_Pcal_plotting = data_manipulation.get_CI(perc_diff_Pcal, "categorization")


    released_Pcal_global = data_manipulation.group(released_Pcal, ["Version", "SSP"])
    pyrolysis_Pcal_global = data_manipulation.group(pyrolysis_Pcal, ["Version", "SSP"])
    flat_diff_Pcal_global = data_manipulation.flat_difference(released_Pcal_global, pyrolysis_Pcal_global, ["SSP"])
    flat_diff_Pcal_global = data_manipulation.get_CI(flat_diff_Pcal_global, "SSP")
    perc_diff_Pcal_global = data_manipulation.percent_difference(released_Pcal_global, pyrolysis_Pcal_global, ["SSP"])
    perc_diff_Pcal_global = data_manipulation.get_CI(perc_diff_Pcal_global, "SSP")

    data_manipulation.drop_missing(perc_diff_Pcal_global).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/global_CI_perc_change_in_pcals.csv")

    data_manipulation.drop_missing(flat_diff_Pcal_global).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/global_CI_change_in_pcals.csv")

    data_manipulation.drop_missing(flat_diff_Pcal_plotting).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/CI_change_in_pcals.csv")

    data_manipulation.drop_missing(CI_perc_diff_Pcal_plotting).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/CI_perc_change_in_pcals.csv")

    perc_diff_Pcal = perc_diff_Pcal[perc_diff_Pcal[biochar_year] < 4]
    perc_diff_Pcal = perc_diff_Pcal[perc_diff_Pcal[biochar_year] > -4]

    # plotting graphs
    perc_diff_Pcal["Units"] = "Change in Pcals consumed compared to reference scenario (%)"
    plotting.plot_regional_hist_avg(perc_diff_Pcal, biochar_year, SSP, "count region-scenario combinations",
                                    "outlier removed Percent difference in Pcals consumed in pyrolysis and reference scenario in " + biochar_year,
                                    "technology", "na", RCP, nonBaselineScenario)

    plotting.plot_regional_vertical_avg(flat_diff_Pcal_plotting, biochar_year, SSP,
                                        "change in food demand (Pcal)",
                                        "change in food demand in " + biochar_year + " in subsector " + str(SSP[0]),
                                        "subsector", "", RCP, nonBaselineScenario)

    # change in food prices
    # get data
    released_staple_expenditure = data_manipulation.get_sensitivity_data(["released"], "food_demand_prices", SSP,
                                                                         RCP=RCP, source="original")
    pyrolysis_staple_expenditure = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_prices",
                                                                          SSP, RCP=RCP, source="masked")
    pyrolysis_staple_expenditure['GCAM'] = pyrolysis_staple_expenditure.apply(
        lambda row: data_manipulation.relabel_region(row), axis=1)
    released_staple_expenditure['GCAM'] = released_staple_expenditure.apply(
        lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_staple_expenditure['input'] = pyrolysis_staple_expenditure.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)
    released_staple_expenditure['input'] = released_staple_expenditure.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)

    # sort by staple/non-staple
    released_Pcal['input'] = released_Pcal.apply(lambda row: data_manipulation.relabel_staple(row, "technology"),
                                                 axis=1)
    released_Pcal = data_manipulation.group(released_Pcal, ["Version", "GCAM", "input"])
    released_Pcal['GCAM'] = released_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_Pcal['input'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_staple(row, "technology"),
                                                   axis=1)
    pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["Version", "GCAM", "input"])
    pyrolysis_Pcal['GCAM'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)

    # merge together
    released_Pcal_cost = pd.merge(released_staple_expenditure, released_Pcal, on=["GCAM", "input", "Version"],
                                  suffixes=("_cost", "_pcal"))
    pyrolsis_Pcal_cost = pd.merge(pyrolysis_staple_expenditure, pyrolysis_Pcal, on=["GCAM", "input", "Version"],
                                  suffixes=("_cost", "_pcal"))

    for i in c.GCAMConstants.x:
        released_Pcal_cost[str(i)] = released_Pcal_cost[str(i) + "_cost"] * released_Pcal_cost[str(i) + "_pcal"]
        pyrolsis_Pcal_cost[str(i)] = pyrolsis_Pcal_cost[str(i) + "_cost"] * pyrolsis_Pcal_cost[str(i) + "_pcal"]
        released_Pcal_cost = released_Pcal_cost.drop([str(i) + "_pcal"], axis=1)
        pyrolsis_Pcal_cost = pyrolsis_Pcal_cost.drop([str(i) + "_pcal"], axis=1)

    # add global rows
    released_Pcal_cost.columns = released_Pcal_cost.columns.str.replace("_pcal", '')  # only label columns
    pyrolsis_Pcal_cost.columns = pyrolsis_Pcal_cost.columns.str.replace("_pcal", '')  # only label columns
    released_Pcal_cost_global = released_Pcal_cost.groupby(["Version", 'input', "SSP"]).sum().reset_index().copy(deep=True)
    pyrolsis_Pcal_cost_global = pyrolsis_Pcal_cost.groupby(["Version", 'input', "SSP"]).sum().reset_index().copy(deep=True)
    released_Pcal_cost_global["GCAM"] = "Global"
    pyrolsis_Pcal_cost_global["GCAM"] = "Global"
    released_Pcal_cost = pd.concat([released_Pcal_cost, released_Pcal_cost_global]).reset_index()
    pyrolsis_Pcal_cost = pd.concat([pyrolsis_Pcal_cost, pyrolsis_Pcal_cost_global]).reset_index()

    flat_diff_food_staple_income = data_manipulation.flat_difference(released_Pcal_cost,
                                                                     pyrolsis_Pcal_cost,
                                                                     ["GCAM", "input"])
    perc_diff_food_staple_income = data_manipulation.percent_difference(released_Pcal_cost,
                                                                        pyrolsis_Pcal_cost,
                                                                        ["GCAM", "input"])
    flat_diff_food_staple_income["cat"] = flat_diff_food_staple_income["GCAM"] + flat_diff_food_staple_income["input"]
    perc_diff_food_staple_income["cat"] = perc_diff_food_staple_income["GCAM"] + perc_diff_food_staple_income["input"]


    CI_flat_diff_cost = data_manipulation.get_CI(flat_diff_food_staple_income, "cat")
    CI_perc_diff_cost = data_manipulation.get_CI(perc_diff_food_staple_income, "cat")

    data_manipulation.drop_missing(CI_flat_diff_cost).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/change_in_food_prices.csv")
    data_manipulation.drop_missing(CI_perc_diff_cost).to_csv(
        "data/data_analysis/supplementary_tables/" + str(
            RCP) + "/percent_change_in_food_prices.csv")

    # plot results
    plotting.plot_regional_vertical_avg(CI_perc_diff_cost, biochar_year, SSP, "change in food prices (%)",
                                        "change in food prices in " + biochar_year + " in " + str(SSP[0]),
                                        "input", "", RCP, nonBaselineScenario)


def figure6(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for potential figure in the CUE conference paper
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: N/A
    """
    # 2 figures: percent/change vs baseline
    # change vs baseline
    # change in biofuel lands
    released_land = data_manipulation.get_sensitivity_data(["released"], "detailed_land_allocation", SSP, RCP=RCP,
                                                           source="original", only_first_scenario=False)
    pyrolysis_land = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP,
                                                            RCP=RCP, source="masked", only_first_scenario=False)
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                    axis=1)
    pyrolysis_land["LandLeaf"] = pyrolysis_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                      axis=1)
    pyrolysis_land = data_manipulation.group(pyrolysis_land, ["LandLeaf", "Version", "SSP"])
    released_land = data_manipulation.group(released_land, ["SSP", "LandLeaf", "Version"])
    pyrolysis_land_bioenergy = pyrolysis_land[pyrolysis_land[['LandLeaf']].isin(["Biomass for Energy"]).any(axis=1)]
    released_land_bioenergy = released_land[released_land[['LandLeaf']].isin(["Biomass for Energy"]).any(axis=1)]
    flat_diff_bioenergy = data_manipulation.flat_difference(released_land_bioenergy, pyrolysis_land_bioenergy,
                                                            ["LandLeaf"])
    perc_diff_bioenergy = data_manipulation.percent_difference(released_land_bioenergy, pyrolysis_land_bioenergy,
                                                               ["LandLeaf"])
    flat_diff_bioenergy["Units"] = "Change in bioenergy land supply (thousand km$^2$)"
    perc_diff_bioenergy["Units"] = "% change in bioenergy land supply"

    # change in croplands
    pyrolysis_land_crops = pyrolysis_land[pyrolysis_land[['LandLeaf']].isin(["Crops"]).any(axis=1)]
    released_land_crops = released_land[released_land[['LandLeaf']].isin(["Crops"]).any(axis=1)]
    flat_diff_crops = data_manipulation.flat_difference(released_land_crops, pyrolysis_land_crops, ["LandLeaf"])
    perc_diff_crops = data_manipulation.percent_difference(released_land_crops, pyrolysis_land_crops,
                                                           ["LandLeaf"])
    flat_diff_crops["Units"] = "Change in crop land supply (thousand km$^2$)"
    perc_diff_crops["Units"] = "% change in crop land supply"

    # change in herd size
    released_supply = data_manipulation.get_sensitivity_data(["released"], "supply_of_all_markets", SSP, RCP=RCP,
                                                             source="original", only_first_scenario=False)
    pyrolysis_supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP,
                                                              RCP=RCP, source="masked", only_first_scenario=False)
    feed = ["FodderHerb_Residue", "FeedCrops", "Pasture_FodderGrass", "Scavenging_Other"]  # the different feed types
    released_feed = released_supply[released_supply[['product']].isin(feed).any(axis=1)]
    pyrolysis_feed = pyrolysis_supply[pyrolysis_supply[['product']].isin(feed).any(axis=1)]
    products = ["Beef", "Dairy", "SheepGoat", "Pork", "Poultry"]  # the different product types
    released_products = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_products = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]

    released_feed = data_manipulation.group(released_feed, ["SSP", "Version"])
    pyrolysis_feed = data_manipulation.group(pyrolysis_feed, ["SSP", "Version"])
    released_products = data_manipulation.group(released_products, ["SSP", "Version"])
    pyrolysis_products = data_manipulation.group(pyrolysis_products, ["SSP", "Version"])

    flat_diff_feed = data_manipulation.flat_difference(released_feed, pyrolysis_feed, ["SSP"])
    perc_diff_feed = data_manipulation.percent_difference(released_feed, pyrolysis_feed, ["SSP"])
    flat_diff_feed["Units"] = "Change in feed supply (Mt)"
    perc_diff_feed["Units"] = "% change in feed supply"
    flat_diff_animal = data_manipulation.flat_difference(released_products, pyrolysis_products,
                                                         ["SSP"])
    perc_diff_animal = data_manipulation.percent_difference(released_products, pyrolysis_products,
                                                            ["SSP"])
    flat_diff_animal["Units"] = "Change in herd size (Mt)"
    perc_diff_animal["Units"] = "% change in herd size"

    # change in temperature/forcing in 2100
    released_temp = data_manipulation.get_sensitivity_data(["released"], "global_mean_temperature", SSP, RCP=RCP,
                                                           source="original", only_first_scenario=False)
    pyrolysis_temp = data_manipulation.get_sensitivity_data(nonBaselineScenario, "global_mean_temperature", SSP,
                                                            RCP=RCP, source="masked", only_first_scenario=False)
    flat_diff_temp = data_manipulation.flat_difference(released_temp, pyrolysis_temp, ["SSP"])
    perc_diff_temp = data_manipulation.percent_difference(released_temp, pyrolysis_temp, ["SSP"])
    flat_diff_temp["Units"] = "Change in global temperature (degree C)"
    perc_diff_temp["Units"] = "% change in global temperature"

    # concat data frames
    flat_diffs = pd.concat(
        [flat_diff_bioenergy, flat_diff_crops, flat_diff_feed, flat_diff_animal,
         flat_diff_temp]).reset_index()
    perc_diffs = pd.concat(
        [perc_diff_bioenergy, perc_diff_crops, perc_diff_feed, perc_diff_animal,
         perc_diff_temp]).reset_index()

    # ensure perc diff has no na
    perc_diffs = perc_diffs[perc_diffs[biochar_year].notna()]  # remove .nan rows from df
    flat_diffs = flat_diffs[flat_diffs[biochar_year].notna()]  # remove .nan rows from df

    # plot products
    plotting.sensitivity(flat_diffs, RCP, nonBaselineScenario[0], biochar_year, "Units", "Version", nonBaselineScenario,
                         title="sensitivty analysis change compared to reference scenario")
    plotting.sensitivity(perc_diffs, RCP, nonBaselineScenario[0], biochar_year, "Units", "Version",
                         nonBaselineScenario,
                         title="sensitivty analysis percentage change compared to reference scenario")


def compare_policy_costs(scenario1, scenario2):
    """
    compares the total annual policy costs between two scenarios
    :param scenario1: old scenario
    :param scenario2: new scenario
    :return: graph new-old scenario
    """
    scenario1 = scenario1.replace("_", "/")
    scenario2 = scenario2.replace("_", "/")
    scenario = scenario1.split("_")[0]
    dataframe = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario2 +
                            "/policy cost by technology.csv")
    cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario1 +
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
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product", "change in policy cost by year " + scenario2.replace("/", "_") + " - " + scenario1.replace("/", "_"),
                                      scenario2)

    # no C tax
    cost_diff = cost_diff[cost_diff["product_price_old"] != "CO2"]
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product", "change in policy cost by year (no C tax) " + scenario2.replace("/", "_") + " - " + scenario1.replace("/", "_"),
                                      scenario2)


if __name__ == '__main__':
    for i in ["s1-itc-l_low"]:
        main(i, "2050")
