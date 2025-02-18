import plotting
import data_manipulation
import constants as c
import pandas as pd


def pop_and_calories(nonBaselineScenario, RCP, SSP):
    """
    plots changes to population and calories consumed
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # get population data
    released_pop = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/population_by_region.csv")
    pyrolysis_pop = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/population_by_region.csv")
    released_pop = released_pop[released_pop[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_pop = pyrolysis_pop[pyrolysis_pop[['SSP']].isin(SSP).any(axis=1)]
    flat_diff_pop = data_manipulation.flat_difference(released_pop, pyrolysis_pop, ["SSP", "GCAM"])
    print(flat_diff_pop["2050"])

    # get calorie data
    released_Pcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_consumption_by_type_specific.csv")
    pyrolysis_Pcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/food_consumption_by_type_specific.csv")
    released_Pcal = released_Pcal[released_Pcal[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_Pcal = pyrolysis_Pcal[pyrolysis_Pcal[['SSP']].isin(SSP).any(axis=1)]
    released_global_pcal = released_Pcal[released_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    print(released_global_pcal[["subsector", "technology", "2050", "Units"]])
    flat_diff_Pcal = data_manipulation.flat_difference(released_Pcal, pyrolysis_Pcal,
                                                       ["GCAM", "SSP", "subsector", "subsector.1",
                                                        "technology"]).drop_duplicates()
    perc_diff_Pcal = data_manipulation.percent_difference(released_Pcal, pyrolysis_Pcal,
                                                          ["GCAM", "SSP", "subsector", "subsector.1",
                                                           "technology"]).drop_duplicates()
    # perc_diff_Pcal["Units"] = "%"
    global_flat = flat_diff_Pcal[flat_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    print(global_flat[["subsector", "technology", "2050", "Units"]])
    flat_diff_Pcal = flat_diff_Pcal[~flat_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    perc_diff_Pcal = perc_diff_Pcal[~perc_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    plotting.plot_regional_hist_avg(flat_diff_Pcal, "2050", SSP, "count region-foodstuff",
                                    "Flat difference in Pcals consumed in pyrolysis and reference scenario",
                                    "technology", "na")
    plotting.plot_regional_hist_avg(perc_diff_Pcal, "2050", SSP, "count region-foodstuff",
                                    "Percent difference in Pcals consumed in pyrolysis and reference scenario",
                                    "technology", "na")

    print(flat_diff_Pcal["2050"])


def luc_by_region(nonBaselineScenario, RCP, SSP):
    """
    plots information related to land use changes between pyrolysis and reference scenario
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # get luc data
    released_luc = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/LUC_emissions_by_LUT.csv")
    pyrolysis_luc = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/LUC_emissions_by_LUT.csv")
    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP"])
    released_luc = released_luc[released_luc[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP"])
    print(flat_diff_luc[["GCAM", "2050", "Units"]])
    # plotting.plot_world_by_years(flat_diff_luc, ["MtC/yr"], "Units", ["2040", "2045", "2050"], SSP,
    #                              "net difference in LUC emissions by region")

    flat_diff_luc = data_manipulation.group(flat_diff_luc, ["SSP"])
    released_luc_total = data_manipulation.group(released_luc, ["SSP"])
    print(released_luc_total[["2040", "2050", "Units"]])
    plotting.plot_line_by_product(flat_diff_luc, ["SSP1"], "SSP", ["SSP1"], "SSP",
                                  "Net LUC compared to reference scenario")

    released_luc = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/LUC_emissions_by_LUT.csv")
    pyrolysis_luc = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/LUC_emissions_by_LUT.csv")
    released_luc = released_luc[released_luc[['SSP']].isin(SSP).any(axis=1)]
    released_luc["LandLeaf"] = released_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    pyrolysis_luc["LandLeaf"] = pyrolysis_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                    axis=1)
    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP", "LandLeaf"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    for i in ["2040", "2045", "2050"]:
        plotting.plot_regional_hist_avg(flat_diff_luc, i, SSP, "count region-LandLeaf",
                                        "Flat diffference in LUC emissions between pyrolysis and reference scenario in " + i,
                                        "LandLeaf", "na")


def animal_feed_and_products(nonBaselineScenario, RCP, SSP):
    """
    returns information related to increased herd sizes and feed demands due to the introduction of pyrolysis
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    released_supply = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/supply_of_all_markets.csv")
    pyrolysis_supply = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/supply_of_all_markets.csv")
    released_supply = released_supply[released_supply[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['SSP']].isin(SSP).any(axis=1)]
    feed = ["FodderHerb_Residue", "FeedCrops", "Pasture_FodderGrass", "Scavenging_Other"]  # the different feed types
    released_feed = released_supply[released_supply[['product']].isin(feed).any(axis=1)]
    pyrolysis_feed = pyrolysis_supply[pyrolysis_supply[['product']].isin(feed).any(axis=1)]
    products = ["Beef", "Dairy", "SheepGoat", "Pork", "Poultry"]  # the different product types
    released_products = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_products = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]

    flat_diff_feed = data_manipulation.flat_difference(released_feed, pyrolysis_feed, ["GCAM", "SSP", "product"])
    perc_diff_feed = data_manipulation.percent_difference(released_feed, pyrolysis_feed, ["GCAM", "SSP", "product"])
    flat_diff_animal = data_manipulation.flat_difference(released_products, pyrolysis_products,
                                                         ["GCAM", "SSP", "product"])
    perc_diff_animal = data_manipulation.percent_difference(released_products, pyrolysis_products,
                                                            ["GCAM", "SSP", "product"])

    plotting.plot_world(flat_diff_feed, feed, SSP, "product", "product", ["2050"],
                        "change in animal feed by region (Mt) in 2050")
    plotting.plot_world(perc_diff_feed, feed, SSP, "product", "product", ["2050"],
                        "percentage change in animal feed by region in 2050")
    plotting.plot_world(flat_diff_animal, products, SSP, "product", "product", ["2050"],
                        "change in animal products by region in 2050")
    plotting.plot_world(perc_diff_animal, products, SSP, "product", "product", ["2050"],
                        "percentage change in animal products by region in 2050")

    flat_diff_feed = data_manipulation.group(flat_diff_feed, ["GCAM"])
    print(data_manipulation.group(released_feed, ["SSP"])[["2050", "Units"]])
    print(flat_diff_feed[["2050", "GCAM", "Units"]])
    flat_diff_animal = data_manipulation.group(flat_diff_animal, ["GCAM"])
    print(data_manipulation.group(released_products, ["SSP"])[["2050", "Units"]])
    print(flat_diff_animal[["2050", "GCAM", "Units"]])


def pyrolysis_costing(nonBaselineScenario, RCP, SSP):
    """
    returns information related to the cost of the pyrolysis scenario
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    #get total costs
    total_cost = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/costs_by_tech.csv")
    # get unit costs (no capex)
    unit_cost = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/costs_by_tech_and_input.csv")
    # get feedstock costs
    feedstock_cost = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/prices_of_all_markets.csv")

    total_cost = total_cost[total_cost[['SSP']].isin(SSP).any(axis=1)]
    unit_cost = unit_cost[unit_cost[['SSP']].isin(SSP).any(axis=1)]
    feedstock_cost = feedstock_cost[feedstock_cost[['SSP']].isin(SSP).any(axis=1)]
    total_cost = total_cost[total_cost[['sector']].isin(['biochar']).any(axis=1)]
    unit_cost = unit_cost[unit_cost[['sector']].isin(['biochar']).any(axis=1)]
    feedstock_cost = feedstock_cost[feedstock_cost[['product']].isin(
        ['beef manure', 'dairy manure', 'goat manure', 'pork manure', 'poultry manure', "biochar"]).any(axis=1)]
    total_cost[["GCAM", "2050", "technology", "Units"]].to_csv("data/data_analysis/total_cost_pyrolysis.csv")
    unit_cost[["GCAM", "2050", "technology", "Units"]].to_csv("data/data_analysis/unit_cost_pyrolysis.csv")
    feedstock_cost[["GCAM", "2050", "product", "Units"]].to_csv("data/data_analysis/feedstock_cost_pyrolysis.csv")

    feedstock_cost = feedstock_cost[feedstock_cost[['product']].isin(
        ['beef manure', 'dairy manure', 'goat manure', 'pork manure', 'poultry manure']).any(axis=1)]
    # drop outliers
    feedstock_cost = feedstock_cost[feedstock_cost["2050"] < 3]
    feedstock_cost["2050"] = feedstock_cost["2050"] / 0.17 * 1000
    feedstock_cost["Units"] = "USD$/ton"
    plotting.plot_regional_hist_avg(feedstock_cost, "2050", SSP, "count", "price distribution of manures", "product",
                                    "na")


def biochar_rate_by_land_size(nonBaselineScenario, RCP, SSP):
    """
    scatter plot of biochar application rate to the size of the biochar land area in 2050
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    #

    # read in biochar application rates, and get the 2050 application rates
    biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level.csv")
    region_names = pd.read_csv("gcam/input/gcamdata/inst/extdata/water/basin_to_country_mapping.csv", skiprows=7)

    # add extra data to dataframe to help downstream code
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['Units'] = 'kg biochar/ha/yr'
    biochar_app_rate["SSP"] = SSP[0]

    # rename GLU for mapping
    biochar_app_rate = biochar_app_rate.merge(region_names, "left", left_on="GLU", right_on="GLU_code")
    biochar_app_rate = biochar_app_rate[["kg_bio_ha", "Units", "SSP", "region", "GCAM_commodity", "GCAM_subsector", "GLU_name", "Irr_Rfd"]]
    biochar_app_rate["Irr_Rfd"] = biochar_app_rate["Irr_Rfd"].str.upper()

    # extract information on crops
    biochar_app_rate['technology'] = biochar_app_rate['GCAM_commodity']
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['technology'] = biochar_app_rate.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)

    # read in detailed land allocation
    # biochar cropland application changes
    land_use = pd.read_csv(
        "data/gcam_out/" + nonBaselineScenario + "/" + RCP + "/original/detailed_land_allocation.csv")
    land_use = land_use[land_use[['SSP']].isin(SSP).any(axis=1)]
    # get biochar land use type information
    land_use[["GCAM_subsector", "GLU_name", "Irr_Rfd", "MGMT"]] = land_use['LandLeaf'].str.split("_", expand=True)
    land_use = land_use[land_use[['MGMT']].isin(["biochar"]).any(axis=1)]
    print(["GCAM", "GCAM_subsector", "GLU_name", "Irr_Rfd", "MGMT"] + [str(i) for i in c.GCAMConstants.future_x])
    land_use = land_use[["GCAM", "GCAM_subsector", "GLU_name", "Irr_Rfd", "MGMT"] + [str(i) for i in c.GCAMConstants.future_x]]
    land_use["Irr_Rfd"] = land_use["Irr_Rfd"].str.upper()

    # merge datasets
    scatter_data = pd.merge(biochar_app_rate, land_use, "left", on=["GCAM", "GCAM_subsector", "GLU_name", "Irr_Rfd"])

    # remove high outlier
    outlier_cutoff = 2000 # kg/ha/yr
    scatter_data = scatter_data[scatter_data['kg_bio_ha'] < outlier_cutoff]

    # plot datasets
    for i in c.GCAMConstants.future_x:
        plotting.plot_regional_vertical(scatter_data, str(i), ["SSP1"], y_label="land area (thousand km2)",
                                    title="distribution of usage of biochar lands in " + str(i), x_column="kg_bio_ha",
                                    x_label="kg biochar/ha/yr", y_column="GCAM_subsector")


def farmer_economics(nonBaselineScenario, RCP, SSP):
    """
    plots information related to the changes in farming due to biochar production
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # get data
    pyrolysis_yields = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/ag_tech_yield.csv")
    pyrolysis_land = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/detailed_land_allocation.csv")
    pyrolysis_profit_rate = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/profit_rate.csv")
    released_yields = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/ag_tech_yield.csv")
    released_land = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/detailed_land_allocation.csv")
    released_profit_rate = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/profit_rate.csv")
    pyrolysis_yields["Units"] = "NA"
    released_yields["Units"] = "NA"
    released_yields = released_yields[released_yields[['SSP']].isin(SSP).any(axis=1)]
    released_land = released_land[released_land[['SSP']].isin(SSP).any(axis=1)]
    released_profit_rate = released_profit_rate[released_profit_rate[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_land = pyrolysis_land[pyrolysis_land[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_profit_rate = pyrolysis_profit_rate[pyrolysis_profit_rate[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_yields = pyrolysis_yields[pyrolysis_yields[['SSP']].isin(SSP).any(axis=1)]

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

    pyrolysis_diff_profit = pyrolysis_diff_profit.sort_values(by='2050')
    flat_diff_small = pyrolysis_diff_profit[
        (-6e7 < pyrolysis_diff_profit['2050']) & (pyrolysis_diff_profit['2050'] < 6e7)]
    flat_diff_large = pyrolysis_diff_profit[
        (-6e7 >= pyrolysis_diff_profit['2050']) | (pyrolysis_diff_profit['2050'] >= 6e7)]
    plotting.plot_regional_hist_avg(flat_diff_small, "2050", ["SSP1"], "count crop-basin-irrigation-year",
                                    "histogram of small farmer profit rate changes at the crop level", "Crop", "na")
    plotting.plot_regional_hist_avg(flat_diff_large, "2050", ["SSP1"], "count crop-basin-irrigation-year",
                                    "histogram of large farmer profit rate changes at the crop level", "Crop", "na")

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
    plotting.plot_regional_hist_avg(flat_diff_effective_yields, "2050", ["SSP1"], "count region-year",
                                    "histogram of yield changes at the crop level", "sector", "na")

    empty_pyro = pyrolysis_land[pyrolysis_land["LandLeaf"].str.contains("biochar")].copy(deep=True)
    for i in c.GCAMConstants.x:
        empty_pyro[str(i)] = 0
    released_land = pd.concat([released_land, empty_pyro])
    # subtract from pyrolysis land
    flat_diff_mgmt = data_manipulation.flat_difference(released_land, pyrolysis_land, ["GCAM", "SSP", "LandLeaf"])
    flat_diff_mgmt[["Crop", "basin", "rainfed", "mgmt"]] = flat_diff_mgmt['LandLeaf'].str.split('_', expand=True)
    flat_diff_mgmt = flat_diff_mgmt[flat_diff_mgmt['mgmt'].notna()]
    flat_diff_mgmt = flat_diff_mgmt.sort_values(by='2050')
    flat_diff_small = flat_diff_mgmt[(-1 < flat_diff_mgmt['2050']) & (flat_diff_mgmt['2050'] < 1)]
    flat_diff_large = flat_diff_mgmt[(-1 >= flat_diff_mgmt['2050']) | (flat_diff_mgmt['2050'] >= 1)]
    plotting.plot_regional_hist_avg(flat_diff_small, "2050", ["SSP1"], "count basin-crop-irrigation",
                                    "histogram of small land mgmt changes in terms of area compared to reference scenario",
                                    "mgmt", "na")
    plotting.plot_regional_hist_avg(flat_diff_large, "2050", ["SSP1"], "count basin-crop-irrigation",
                                    "histogram of large land mgmt changes in terms of area compared to reference scenario",
                                    "mgmt", "na")

    # land leaf shares histogram
    pyrolysis_landleafs = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/land_leaf_shares.csv")
    pyrolysis_landleafs[["Crop", "basin", "rainfed", "MGMT"]] = pyrolysis_landleafs['LandLeaf'].str.split('_', expand=True)
    pyrolysis_landleafs = pyrolysis_landleafs[pyrolysis_landleafs[['MGMT']].isin(["biochar"]).any(axis=1)]
    for i in c.GCAMConstants.biochar_x:
        plotting.plot_regional_hist_avg(pyrolysis_landleafs, str(i), SSP, "count land leafs", "histogram of land leaf shares for biochar lands in "+ str(i), "MGMT", "na")


def main():
    """
    Main method for running all scripts
    :return: N/A
    """
    reference_SSP = "SSP1"
    reference_RCP = "6p0"
    other_scenario = "test"  # biochar
    biochar_rate_by_land_size(other_scenario, reference_RCP, [reference_SSP])
    farmer_economics(other_scenario, reference_RCP, [reference_SSP])
    pyrolysis_costing(other_scenario, reference_RCP, [reference_SSP])
    animal_feed_and_products(other_scenario, reference_RCP, [reference_SSP])
    luc_by_region(other_scenario, reference_RCP, [reference_SSP])
    pop_and_calories(other_scenario, reference_RCP, [reference_SSP])


if __name__ == '__main__':
    main()
