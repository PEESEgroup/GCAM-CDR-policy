from matplotlib import pyplot as plt
import plotting
import data_manipulation
import constants as c
import pandas as pd
import stats as stats
import numpy as np


def food(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to food insecurity
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # changes to animal livestock production
    released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/original/supply_of_all_markets.csv")
    pyrolysis_supply = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/supply_of_all_markets.csv")
    products = ["Beef", "Pork", "Dairy", "Poultry", "SheepGoat"]
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    perc_diff = data_manipulation.percent_difference(released_supply, pyrolysis_supply, ["SSP", "product", "GCAM"])
    for i in SSP:
        plotting.plot_world(perc_diff, products, [i], "product", "product", [2050],
                            "Percent difference in size of livestock markets in 2050")

    """unused figure for analysis::
    changes in livestock systems as indicated by feed supplies - not used in analysis
    feed_released = pd.read_csv("data/gcam_out/released/" + RCP + "/feed_consumption_by_meat_and_dairy_tech.csv")
    feed_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" +  "/feed_consumption_by_meat_and_dairy_tech.csv")
    columns = ['sector', 'subsector', 'SSP']
    feed_released = data_manipulation.group(feed_released, columns)
    feed_pyrolysis = data_manipulation.group(feed_pyrolysis, columns)
    flat_diff_feed = data_manipulation.flat_difference(feed_released, feed_pyrolysis, ["SSP", "sector", "subsector"])
    plotting.plot_line(flat_diff_feed, ['Beef', 'Dairy', 'Poultry', 'Pork', 'SheepGoat'], c.GCAMConstants.SSPs, "SSP", "sector",
                       "subsector", title="Change in livestock feed supply")
    """

    # Changes to crop production
    # Changes to agricultural commodity prices
    crops = ["Corn", "FiberCrop", "FodderGrass", "FodderHerb", "Forest", "Fruits", "Legumes", "MiscCrop", "NutsSeeds",
             "OilCrop", "OtherGrain", "Pasture", "Rice", "RootTuber", "Soybean", "SugarCrop",
             "Vegetables", "Wheat", "biomass"]
    released_ag_prices = pd.read_csv("data/gcam_out/released/" + RCP + "/original/ag_commodity_prices.csv")
    pyrolysis_ag_prices = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/ag_commodity_prices.csv")
    perc_diff_ag_prices = data_manipulation.percent_difference(released_ag_prices, pyrolysis_ag_prices,
                                                               ["SSP", "sector", "GCAM"])
    plotting.plot_world(perc_diff_ag_prices, crops, ["SSP2"], "product", "sector", [2050],
                        "percentage change to agricultural commodity prices in 2050")

    # Changes to food prices
    released_foo_price = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    pyrolysis_foo_price = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    perc_diff_food_prices = data_manipulation.percent_difference(released_foo_price, pyrolysis_foo_price,
                                                                 ["SSP", "sector", "GCAM"])
    crops = ["regional beef", "regional corn", "regional dairy", "regional fruits", "regional legumes",
             "regional nuts_seeds", "regional oilcrop", "regional oilpalm", "regional othergrain", "regional pork",
             "regional poultry", "regional rice", "regional root_tuber", "regional sheepgoat", "regional soybean",
             "regional sugarcrop", "regional vegetables", "regional wheat"]
    plotting.plot_world(perc_diff_food_prices, crops, SSP, "product", "sector", [2050],
                        title="change in regional food prices")

    # correlation between food and energy prices
    for products in ["regional beef", "regional dairy", "regional pork", "regional poultry", "regional sheepgoat",
                     "regional wheat", "regional corn"]:
        for energy in ["crude oil"]:
            # get right energy source
            released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/original/prices_of_all_markets.csv")
            pyrolysis_price = pd.read_csv(
                "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/prices_of_all_markets.csv")
            released_refliq_price = released_price[released_price[['product']].isin([energy]).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_price[pyrolysis_price[['product']].isin([energy]).any(axis=1)]
            released_refliq_price = released_refliq_price[released_refliq_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_refliq_price[pyrolysis_refliq_price[['SSP']].isin(SSP).any(axis=1)]

            # get right food sources
            released_foo_price = pd.read_csv(
                "data/gcam_out/released/" + RCP + "/original/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
            pyrolysis_foo_price = pd.read_csv(
                "data/gcam_out/" + str(
                    nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
            released_food_price = released_foo_price[released_foo_price[['sector']].isin([products]).any(axis=1)]
            pyrolysis_food_price = pyrolysis_foo_price[pyrolysis_foo_price[['sector']].isin([products]).any(axis=1)]
            released_food_price = released_food_price[released_food_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_food_price = pyrolysis_food_price[pyrolysis_food_price[['SSP']].isin(SSP).any(axis=1)]

            # test for stationarity
            print("released", products, "price")
            stats.stationarity_test(released_food_price, 2050)
            print("pyrolysis", products, "price")
            stats.stationarity_test(pyrolysis_food_price, 2050)
            print("released", energy, "price")
            stats.stationarity_test(released_refliq_price, 2050)
            print("pyrolysis", energy, "price")
            stats.stationarity_test(pyrolysis_refliq_price, 2050)

            # tests for correlation
            released_res = stats.calc_price_linkage(released_refliq_price, released_food_price, SSP, 2050)
            pyrolysis_res = stats.calc_price_linkage(pyrolysis_refliq_price, pyrolysis_food_price, SSP, 2050)
            plotting.plot_price_coefficients(pyrolysis_res, released_res,
                                             "price coefficients for " + products + " and " + energy + " in " + SSP[0])

    # regional averaged per capita food available for consumption – food demand per capita
    # get data
    released_per_capita_kcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_demand_per_capita.csv")
    pyrolysis_per_capita_kcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/food_demand_per_capita.csv")
    released_per_capita_kcal = released_per_capita_kcal[released_per_capita_kcal[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_per_capita_kcal = pyrolysis_per_capita_kcal[pyrolysis_per_capita_kcal[['SSP']].isin(SSP).any(axis=1)]
    released_per_capita_kcal.reset_index(drop=True)
    pyrolysis_per_capita_kcal.reset_index(drop=True)

    # cumulative diet change analysis
    regions = c.GCAMConstants.GCAM_region
    flat_diff_cap_kcal = data_manipulation.flat_difference(released_per_capita_kcal, pyrolysis_per_capita_kcal,
                                                           ["SSP", "GCAM", "input"])
    flat_diff_cap_kcal = flat_diff_cap_kcal.dropna(axis=0)
    flat_diff_cap_kcal = flat_diff_cap_kcal[flat_diff_cap_kcal[['GCAM']].isin(regions).any(axis=1)]
    plotting.plot_regional_vertical(flat_diff_cap_kcal, 2050, SSP, "change in food demand (thousand kcal/person/day)",
                                    "change in food demand in " + str(SSP[0]) + " and RCP: " + str(RCP), column="input")

    # regional averaged food consumption by food type
    # convert Pcal to kcal/capita/day
    # get population data
    released_pop = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/population_by_region.csv")
    pyrolysis_pop = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/population_by_region.csv")
    released_pop = released_pop[released_pop[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_pop = pyrolysis_pop[pyrolysis_pop[['SSP']].isin(SSP).any(axis=1)]

    # get Pcal data
    released_Pcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_consumption_by_type_specific.csv")
    pyrolysis_Pcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/food_consumption_by_type_specific.csv")
    released_Pcal = released_Pcal[released_Pcal[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_Pcal = pyrolysis_Pcal[pyrolysis_Pcal[['SSP']].isin(SSP).any(axis=1)]
    released_Pcal = data_manipulation.group(released_Pcal, ["GCAM", "SSP", "technology"])
    pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["GCAM", "SSP", "technology"])

    released_pcal_pop = pd.merge(released_Pcal, released_pop, how="inner", on=["SSP", "GCAM"],
                                 suffixes=("_pcal", "_pop"))
    pyrolysis_pcal_pop = pd.merge(pyrolysis_Pcal, pyrolysis_pop, how="inner", on=["SSP", "GCAM"],
                                  suffixes=("_pcal", "_pop"))

    # calculate pcal per capita in 2050
    released_pcal_pop["pcal_capita_2050"] = released_pcal_pop["2050_pcal"] / (1000 * released_pcal_pop[
        "2050_pop"]) * 1000000000000 / 365 / 2  # * peta to kilo/365/conversion factor of 2 randomly
    pyrolysis_pcal_pop["pcal_capita_2050"] = pyrolysis_pcal_pop["2050_pcal"] / (
            1000 * pyrolysis_pcal_pop["2050_pop"]) * 1000000000000 / 365 / 2
    released_pcal_pop["Units"] = "kcal/capita/day"
    pyrolysis_pcal_pop["Units"] = "kcal/capita/day"

    merged_pcal = released_pcal_pop.merge(pyrolysis_pcal_pop, how="inner", on=["SSP", "GCAM", "technology_pcal"],
                                          suffixes=("_left", "_right"))
    merged_pcal["pcal_capita_2050"] = merged_pcal["pcal_capita_2050" + "_right"] - merged_pcal[
        "pcal_capita_2050" + "_left"]

    # take the userful columns
    foodstuffs = []

    plotting.plot_regional_vertical(merged_pcal, "pcal_capita_2050", SSP, "change in food demand (kcal/person/day)",
                                    "change in food demand in " + str(SSP[0]) + " and RCP " + str(RCP),
                                    column="technology_pcal")

    """
    # verify food consumption values through comparison to food demand figures - yields a factor of 2 for kcal calcs
    released_pcal_pop = data_manipulation.group(released_pcal_pop, "GCAM")
    pyrolysis_pcal_pop = data_manipulation.group(pyrolysis_pcal_pop, "GCAM")
    released_pcal_pop["SSP"] = SSP[0]
    pyrolysis_pcal_pop["SSP"] = SSP[0]
    check_calc_released = pd.merge(released_pcal_pop, released_per_capita_kcal, how="inner", on=["SSP", "GCAM"], suffixes=("_calc", "_truth"))
    check_calc_pyrolysis = pd.merge(pyrolysis_pcal_pop, pyrolysis_per_capita_kcal, how="inner", on=["SSP", "GCAM"], suffixes=("_calc", "_truth"))
    check_calc_released = check_calc_released.loc[:, ["GCAM", "pcal_capita_2050", "2050"]]
    check_calc_released["diff"] = check_calc_released["pcal_capita_2050"] / check_calc_released["2050"]
    check_calc_pyrolysis = check_calc_pyrolysis.loc[:, ["GCAM", "pcal_capita_2050", "2050"]]
    check_calc_pyrolysis["diff"] = check_calc_pyrolysis["pcal_capita_2050"] / check_calc_pyrolysis["2050"]
    """

    # Staple expenditure as percentage of average income – food demand prices and GDP per capita PPP by region
    # get data
    released_staple_expenditure = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_demand_prices.csv")
    pyrolysis_staple_expenditure = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/food_demand_prices.csv")
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['SSP']].isin(SSP).any(axis=1)]
    diff_food_staple_income = data_manipulation.flat_difference(released_staple_expenditure,
                                                                pyrolysis_staple_expenditure, ["SSP", "GCAM", "input"])

    # plot results
    plotting.plot_regional_vertical(diff_food_staple_income, "2050", SSP, "change in food expenditure ($/Mcal/day)",
                                    "food expenditure in 2050 in " + str(SSP[0]) + " and RCP " + str(RCP),
                                    column="input")


def energy(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to energy
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # Changes in energy mix
    # refined liquids production
    ref_released = pd.read_csv("data/gcam_out/released/" + RCP + "/original/refined_liquids_production_by_tech.csv")
    ref_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/refined_liquids_production_by_tech.csv")
    # relabel CCS technologies
    ref_released['technology'] = ref_released.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)
    ref_pyrolysis['technology'] = ref_pyrolysis.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)

    # group technologies
    ref_released = data_manipulation.group(ref_released, ["SSP", "GCAM", "technology"])
    ref_pyrolysis = data_manipulation.group(ref_pyrolysis, ["SSP", "GCAM", "technology"])

    # add manure fuel row to the released version so that the flat diff can be analyzed
    man_fuel = ref_pyrolysis.loc[ref_pyrolysis["technology"] == "manure fuel"]
    for i in c.GCAMConstants.biochar_x:
        man_fuel.loc[:, str(i)] = 0
    ref_released = pd.concat([ref_released, man_fuel])

    # select global region
    ref_released_global = ref_released[ref_released[['GCAM']].isin(["Global"]).any(axis=1)]
    ref_pyrolysis_global = ref_pyrolysis[ref_pyrolysis[['GCAM']].isin(["Global"]).any(axis=1)]
    ref_released = ref_released[~ref_released[['GCAM']].isin(["Global"]).any(axis=1)]
    ref_pyrolysis = ref_pyrolysis[~ref_pyrolysis[['GCAM']].isin(["Global"]).any(axis=1)]

    # plot products
    products = ref_pyrolysis["technology"].unique().tolist()
    products = [products[i] for i in
                [0, 1, 9, 3, 5, 4, 6, 8, 2, 7]]  # put manure fuel at the end so colors stay the same, reorder by type
    flat_diff_biofuel_global = data_manipulation.flat_difference(ref_released_global, ref_pyrolysis_global,
                                                                 ["SSP", "technology", "GCAM"])
    flat_diff_biofuel = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["SSP", "technology", "GCAM"])
    perc_diff_biofuel_global = data_manipulation.percent_difference(ref_released_global, ref_pyrolysis_global,
                                                                    ["SSP", "technology", "GCAM"])
    perc_diff_biofuel = data_manipulation.percent_difference(ref_released, ref_pyrolysis, ["SSP", "technology", "GCAM"])
    plotting.plot_line(flat_diff_biofuel_global, products, SSP, "product", "technology", "Units",
                       "change in supply of refined liquids")
    plotting.plot_world(flat_diff_biofuel, products, ["SSP2"], "product", "technology", ["2050"],
                        "spatial distribution of change in supply of refined liquids")
    products.remove("manure fuel")  # can't have a percent difference with baseline of 0 EJ
    plotting.plot_line(perc_diff_biofuel_global, products, SSP, "product", "technology", "Units",
                       "change in supply of refined liquids")
    plotting.plot_world(perc_diff_biofuel, products, ["SSP2"], "product", "technology", ["2050"],
                        "spatial distribution of change in supply of refined liquids")

    # change in cost of production of regined liquids
    released_cost = pd.read_csv("data/gcam_out/released/" + RCP + "/original/refined_liquids_costs_by_tech.csv")
    pyrolysis_cost = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/refined_liquids_costs_by_tech.csv")
    released_cost['technology'] = released_cost.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)
    pyrolysis_cost['technology'] = pyrolysis_cost.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)

    # group technologies
    released_cost = data_manipulation.group(released_cost, ["SSP", "GCAM", "technology"])
    pyrolysis_cost = data_manipulation.group(pyrolysis_cost, ["SSP", "GCAM", "technology"])

    # plotting
    flat_diff_cost = data_manipulation.flat_difference(released_cost, pyrolysis_cost, ["SSP", "technology", "GCAM"])
    flat_diff_cost = flat_diff_cost[~flat_diff_cost[['GCAM']].isin(["Global"]).any(axis=1)]  # remove global region
    products = flat_diff_cost["technology"].unique().tolist()
    plotting.plot_world(flat_diff_cost, products, SSP, "product", "technology", ["2050"],
                        "change in cost of production of refined liquids")
    perc_diff_cost = data_manipulation.percent_difference(released_cost, pyrolysis_cost, ["SSP", "technology", "GCAM"])
    perc_diff_cost = perc_diff_cost[~perc_diff_cost[['GCAM']].isin(["Global"]).any(axis=1)]  # remove global region
    products = perc_diff_cost["technology"].unique().tolist()
    plotting.plot_world(perc_diff_cost, products, SSP, "product", "technology", ["2050"],
                        "change in cost of production of refined liquids")

    # changes in newly installed refining capacity
    released_new = pd.read_csv("data/gcam_out/released/" + RCP + "/original/refined_liquids_production_by_tech_new.csv")
    pyrolysis_new = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/masked" + "/refined_liquids_production_by_tech_new.csv")
    # relabel CCS technologies
    released_new['technology'] = released_new.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)
    pyrolysis_new['technology'] = pyrolysis_new.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)

    # group technologies
    released_new = data_manipulation.group(released_new, ["SSP", "GCAM", "technology"])
    pyrolysis_new = data_manipulation.group(pyrolysis_new, ["SSP", "GCAM", "technology"])

    # remove global entry
    released_new = released_new[~released_new[['GCAM']].isin(["Global"]).any(axis=1)]
    pyrolysis_new = pyrolysis_new[~pyrolysis_new[['GCAM']].isin(["Global"]).any(axis=1)]

    # add baseline for manure fuel production to released model
    man_fuel = pyrolysis_new.loc[pyrolysis_new["technology"] == "manure fuel"]
    for i in c.GCAMConstants.biochar_x:
        man_fuel.loc[:, str(i)] = 0
    released_new = pd.concat([released_new, man_fuel])

    flat_diff_new = data_manipulation.flat_difference(released_new, pyrolysis_new, ["SSP", "technology", "GCAM"])
    products = flat_diff_new["technology"].unique().tolist()

    plotting.plot_world(flat_diff_new, products, ["SSP2"], "product", "technology", ["2050"],
                        "spatial distribution in changes to newly installed capacity")

    # Changes in price of biofuels
    released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/original/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/prices_of_all_markets.csv")
    products = ["refined liquids enduse"]
    released_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    pyrolysis_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    flat_diff_price = data_manipulation.flat_difference(pyrolysis_price, released_price, ["SSP", "GCAM", "product"])
    perc_diff_price = data_manipulation.percent_difference(pyrolysis_price, released_price, ["SSP", "GCAM", "product"])

    plotting.plot_world(flat_diff_price, products, ["SSP2"], "product", "product", ["2050"],
                        "spatial distribution in change in price of refined liquids")
    plotting.plot_world(perc_diff_price, products, ["SSP2"], "product", "product", ["2050"],
                        "spatial distribution in percentage change in price of refined liquids")


def get_app_rate(row, product, year):
    yields = 0
    feedstock = row[product]
    if feedstock == "beef manure":
        yields = 0.11
    if feedstock == "dairy manure":
        yields = 0.11
    if feedstock == "goat manure":
        yields = 0.11
    if feedstock == "pork manure":
        yields = 0.14
    if feedstock == "poultry manure":
        yields = 0.13

    # Mt manure * Mt C sequestration in biochar/Mt manure
    return row[year] * yields

def climate(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to climate
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # land use change emissions from biochar
    # get luc change data
    luc = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/LUC_emissions_by_LUT.csv")
    luc = luc[luc['LandLeaf'].str.contains("biochar")]
    luc = luc[luc[['SSP']].isin(SSP).any(axis=1)]
    luc = data_manipulation.group(luc, "GCAM")
    luc["Units"] = "Modeled Mt C sequestered"
    luc["product"] = "seq_C"
    luc["SSP"] = "SSP1"
    #plotting.plot_world(luc, ["seq_C"], ["SSP1"], "year", "product", c.GCAMConstants.biochar_x, "Modeled C sequestration (Mt)")

    # calculate biochar sequestration rate
    released_supply = pd.read_csv("data/gcam_out/test/2p6/masked/supply_of_all_markets.csv")
    products = ["beef manure", "pork manure", "dairy manure", "poultry manure", "goat manure"]
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    released_supply = released_supply[released_supply[['SSP']].isin(["SSP1"]).any(axis=1)]
    released_supply = released_supply[~released_supply[['GCAM']].isin(["global"]).any(axis=1)]

    # for each future year
    for i in c.GCAMConstants.biochar_x:
        # calculate application rates
        released_supply[str(i) + "_C"] = released_supply.apply(lambda row: get_app_rate(row, 'product', str(i)), axis=1)

    C_rates = released_supply.groupby("GCAM")[[str(i) + "_C" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    C_rates.columns = C_rates.columns.str.rstrip("_C")
    C_rates["Units"] = "Calculated Sequestered C (Mt)"
    C_rates["SSP"] = "SSP1"

    # map actual C sequestration
    #plotting.plot_world(C_rates, ["SSP1"], ["SSP1"],"year", "SSP", c.GCAMConstants.biochar_x, "Actual C application rates (Mt)")

    colors, num = plotting.get_colors(20)
    for year, j in zip(c.GCAMConstants.biochar_x, range(len(c.GCAMConstants.biochar_x))):
        plt.scatter(C_rates[str(year)], luc[str(year)], color=colors[j])
    plt.xlabel("actual biochar C sequestration by country (Mt)")
    plt.ylabel("modeled biochar C sequestration by country (Mt)")
    plt.title("biochar C sequestration validation")
    plt.show()

    # plotting CO2 avoidance
    co2_seq_released = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/CO2_emissions_by_tech_excluding_resource_production.csv")
    co2_seq_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    co2_seq_released['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    products = ["beef_biochar", "dairy_biochar", "pork_biochar", "poultry_biochar", "goat_biochar"]
    biochar_pyrolysis = co2_seq_pyrolysis[co2_seq_pyrolysis['sector'].str.contains("|".join(products))]
    plotting.plot_line(biochar_pyrolysis, products, SSP, "product", "sector", "Version",
                       title="CO2 emission avoidance from biochar")

    # combine similar sectors
    co2_seq_released['sector'] = co2_seq_released.apply(lambda row: data_manipulation.label_sequestration_sectors(row),
                                                        axis=1)
    co2_seq_pyrolysis['sector'] = co2_seq_pyrolysis.apply(
        lambda row: data_manipulation.label_sequestration_sectors(row), axis=1)

    # merge sectors in the CO2 sequestered data
    co2_seq_released_comb = data_manipulation.group(co2_seq_released, ["sector", "SSP"])
    co2_seq_pyrolysis_comb = data_manipulation.group(co2_seq_pyrolysis, ["sector", "SSP"])

    # plot difference
    flat_diff_CO2 = data_manipulation.flat_difference(co2_seq_released_comb, co2_seq_pyrolysis_comb,
                                                      ["sector", "SSP"])
    plotting.plot_line(flat_diff_CO2, flat_diff_CO2["sector"].unique(), SSP, "product", "sector", "product",
                       title="change in CO2 sequestration by sector")

    # Annual carbon emissions – CO2 emissions by region, sector, resource production
    co2_emi_released = pd.read_csv("data/gcam_out/released/" + RCP + "/original/CO2_emissions_by_region.csv")
    co2_emi_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/CO2_emissions_by_region.csv")
    flat_diff_CO2 = data_manipulation.flat_difference(co2_emi_released, co2_emi_pyrolysis, ["SSP", "GCAM"])
    plotting.plot_world(flat_diff_CO2, ["MTC"], SSP, "product", "Units", ["2050"],
                        "Spatial change in carbon emissions in 2050")

    # Changes to CH4 and N2O emissions – nonCO2 emissions by region
    nonco2_emi_released = pd.read_csv("data/gcam_out/released/" + RCP + "/original/nonCO2_emissions_by_region.csv")
    nonco2_emi_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/nonCO2_emissions_by_region.csv")
    flat_diff_nonCO2 = data_manipulation.flat_difference(nonco2_emi_released, nonco2_emi_pyrolysis,
                                                         ["SSP", "GCAM", "GHG"])
    plotting.plot_world(flat_diff_nonCO2, ["N2O_AGR", "CH4_AGR", "NMVOC_AGR", "NOx_AGR", "NH3_AGR"],
                        SSP, "product", "GHG", ["2050"], "Spatial change in agricultural emissions in 2050")



def land(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to land use
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # regional land use change
    released_land = pd.read_csv("data/gcam_out/released/" + RCP + "/original/aggregated_land_allocation.csv")
    pyrolysis_land = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/aggregated_land_allocation.csv")
    released_land = released_land[released_land[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_land = pyrolysis_land[pyrolysis_land[['SSP']].isin(SSP).any(axis=1)]
    flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])
    perc_diff_land = data_manipulation.percent_of_total(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    plotting.plot_stacked_bar_product(flat_diff_land, "2050", SSP, "LandLeaf", "land use change by region")
    plotting.plot_stacked_bar_product(perc_diff_land, "2050", SSP, "LandLeaf", "land use change by region")


def fertilizer(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to fertilizer
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # # Plotting Fertilizer prices
    # released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/original/prices_of_all_markets.csv")
    # pyrolysis_price = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/prices_of_all_markets.csv")
    # products = ["N fertilizer"]
    # released_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    # pyrolysis_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    # perc_diff_f_price = data_manipulation.percent_difference(released_price, pyrolysis_price,
    #                                                          ["SSP", "product", "GCAM"])
    # plotting.plot_world(perc_diff_f_price, products, ["SSP2"], "product", "product", ["2050"],
    #                     "percent difference in price of fertilizer")
    #
    # # supply of fertilizer
    # released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/original/supply_of_all_markets.csv")
    # pyrolysis_supply = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/supply_of_all_markets.csv")
    # products = ["N fertilizer"]
    # released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    # pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    # perc_diff_f_supply = data_manipulation.percent_difference(released_supply, pyrolysis_supply,
    #                                                           ["SSP", "product", "GCAM"])
    # plotting.plot_world(perc_diff_f_supply, products, ["SSP2"], "product", "product", ["2050"],
    #                     "percent difference in supply of fertilizer")
    #
    # # regional change in N fertilizer production technologies
    # released_f = pd.read_csv("data/gcam_out/released/" + RCP + "/original/fertilizer_production_by_tech.csv")
    # pyrolysis_f = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/fertilizer_production_by_tech.csv")
    #
    # # process data - percent change
    # released_f = data_manipulation.group(released_f, ["SSP", "GCAM", "subsector"])
    # pyrolysis_f = data_manipulation.group(pyrolysis_f, ["SSP", "GCAM", "subsector"])
    # perc_diff_f = data_manipulation.percent_difference(released_f, pyrolysis_f, ["SSP", "GCAM", "subsector"])
    # plotting.plot_world(perc_diff_f, released_f["subsector"].unique().tolist(), ["SSP2"], "product", "subsector",
    #                     ["2050"], "spatial change in N fertilizer production techniques")
    #
    # # absolute change
    # # add biochar row to the released version so that the flat diff can be analyzed
    # biochar = pyrolysis_f.loc[pyrolysis_f["technology"] == "biochar_sup"]
    # for i in c.GCAMConstants.biochar_x:
    #     biochar.loc[:, str(i)] = 0
    # ref_released = pd.concat([released_f, biochar])
    # flat_diff_f = data_manipulation.flat_difference(ref_released, pyrolysis_f, ["SSP", "GCAM", "subsector"])
    # flat_diff_f = flat_diff_f[~flat_diff_f[['GCAM']].isin(["Global"]).any(axis=1)]
    # flat_diff_f = flat_diff_f[flat_diff_f[['SSP']].isin(SSP).any(axis=1)]
    # plotting.plot_world(flat_diff_f, pyrolysis_f["subsector"].unique().tolist(), ["SSP2"], "product", "subsector",
    #                     ["2050"], "spatial change in N fertilizer production techniques")
    #
    # # spatial distribution of biochar/manure supply and prices
    # biochar_supply = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/supply_of_all_markets.csv")
    # products = ["beef_biochar", "dairy_biochar", "pork_biochar", "poultry_biochar", "goat_biochar"]
    # plotting.plot_world(biochar_supply, products, SSP, "product", "product", ["2050"],
    #                     "spatial distribution of biochar supply")
    # products = ["beef manure", "dairy manure", "pork manure", "poultry manure", "goat manure"]
    # plotting.plot_world(biochar_supply, products, SSP, "product", "product", ["2050"],
    #                     "spatial distribution of manure supply")



def figure2(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 2
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the baseline SSP pathway being considered. only the first element in the list is used
    :return: N/A
    """
    # plotting CO2 sequestering
    for r in RCP:
        co2_seq_pyrolysis = pd.read_csv(
            "data/gcam_out/" + str(
                nonBaselineScenario) + "/" + r + "/masked" + "/CO2_emissions_by_tech_excluding_resource_production.csv")
        co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
        co2_seq_pyrolysis['sector'] = co2_seq_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "sector"), axis=1)
        co2_seq_pyrolysis['Units'] = "Mt C"
        products = ["beef_biochar", "dairy_biochar", "pork_biochar", "poultry_biochar", "goat_biochar", "manure fuel", "biochar"]
        biochar_pyrolysis = co2_seq_pyrolysis[co2_seq_pyrolysis['sector'].str.contains("|".join(products))]

        if biochar_pyrolysis["sector"].unique()[0] == "manure fuel":
            technologies = ["slow pyrolysis_beef", "slow pyrolysis_dairy", "slow pyrolysis_goat", "slow pyrolysis_pork", "slow pyrolysis_poultry"]
            plotting.plot_line_product_CI(biochar_pyrolysis, technologies, "technology", SSP[0], "Version",
                                          title="CO2 sequestration from biooil")
        else:
            plotting.plot_line_product_CI(biochar_pyrolysis, products, "technology", "SSP2", "Version",
                                          title="C sequestration from biochar in SSP2 baseline in RCP" + str(r))
        # print values of Mt C sequestered
        biochar_group = data_manipulation.group(biochar_pyrolysis, "SSP")
        print(biochar_group.loc[:, ["2050", "SSP"]])

    # plotting ghg emissions avoidance
    for r in RCP:
        co2_seq_pyrolysis = pd.read_csv(
            "data/gcam_out/" + str(
                nonBaselineScenario) + "/" + r + "/masked" + "/non_CO2_emissions_by_tech_excluding_resource_production.csv")
        co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
        co2_seq_pyrolysis['sector'] = co2_seq_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "sector"),
                                                              axis=1)
        co2_seq_pyrolysis['Units'] = "Mt CH4"
        technologies = ["slow pyrolysis_beef", "slow pyrolysis_dairy", "slow pyrolysis_goat",
                        "slow pyrolysis_pork", "slow pyrolysis_poultry"]
        biochar_pyrolysis = co2_seq_pyrolysis[co2_seq_pyrolysis['technology'].str.contains("|".join(technologies))]

        plotting.plot_line_product_CI(biochar_pyrolysis, technologies, "technology", "SSP2", "Version",
                                          title="CH4 emissions avoidance from biochar in SSP2 baseline in RCP" + str(r))
        # print values of Mt C sequestered
        biochar_group = data_manipulation.group(biochar_pyrolysis, "SSP")
        print(biochar_group.loc[:, ["2050", "SSP"]])


def figure3(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 3
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: N/A
    """
    # spatial distribution of biochar/manure prices
    biochar_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/prices_of_all_markets.csv")
    biochar_price['product'] = biochar_price.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    biochar_supply = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/supply_of_all_markets.csv")
    biochar_supply['product'] = biochar_supply.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    products = ["beef biochar", "dairy biochar", "pork biochar", "poultry biochar", "goat biochar", "manure-fuel", "biochar"]
    biochar_price[str(biochar_year) + "_conv"] = biochar_price[
                                     str(biochar_year)] * 5.92 * 1000  # Jan 1975 to Jan 2024 https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=197501&year2=202401 * kg to ton
    biochar_price.loc[biochar_price[str(biochar_year)] > 2000, str(biochar_year) + "_conv"] = np.nan  # manually removing outliers
    biochar_supply[str(biochar_year) + "_conv"] = biochar_supply[str(biochar_year)]
    biochar_price = biochar_price[biochar_price[['product']].isin(products).any(axis=1)]
    biochar_supply = biochar_supply[biochar_supply[['product']].isin(products).any(axis=1)]

    if not biochar_supply.empty:
        biochar_supply['GCAM'] = biochar_supply.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
        biochar_price['GCAM'] = biochar_price.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
        plotting.plot_regional_hist_avg(biochar_price, str(biochar_year) + "_conv", SSP, "2024 US$/ton", "price of products", "SSP",
                                        biochar_supply)
    else:
        print("no biochar supply for the given year")

    # print out differences in carbon prices
    c_pyro_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/CO2_prices.csv")
    c_rel_price = pd.read_csv("data/gcam_out/released/" + RCP + "/original/CO2_prices.csv")
    c_pyro_price = c_pyro_price.drop_duplicates()
    c_rel_price = c_rel_price.drop_duplicates()
    product = ["CO2"]
    c_rel_price = c_rel_price[c_rel_price[['product']].isin(product).any(axis=1)]
    c_pyro_price = c_pyro_price[c_pyro_price[['product']].isin(product).any(axis=1)]
    flat_diff_c_price = data_manipulation.flat_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
    flat_diff_c_price[str(biochar_year) + "_conv"] = flat_diff_c_price[
                                         str(biochar_year)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
    unique_c_price = flat_diff_c_price[[str(biochar_year) + "_conv", "SSP"]].drop_duplicates()
    print(unique_c_price)
    perc_diff_c_price = data_manipulation.percent_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
    perc_diff_c_price[str(biochar_year) + "_conv"] = perc_diff_c_price[
                                         str(biochar_year)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
    unique_c_price = perc_diff_c_price[[str(biochar_year) + "_conv", "SSP"]].drop_duplicates()
    print(unique_c_price)


def figure4(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 4
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathway being considered
    :param SSP: the SSP pathway being considered
    :param biochar_year: the year being analyzed in detail
    :return: N/A
    """
    # regional land use change
    released_land = pd.read_csv("data/gcam_out/released/" + RCP + "/original/detailed_land_allocation.csv")
    pyrolysis_land = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/detailed_land_allocation.csv")
    released_land = released_land[released_land[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_land = pyrolysis_land[pyrolysis_land[['SSP']].isin(SSP).any(axis=1)]
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    pyrolysis_land["LandLeaf"] = pyrolysis_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    pyrolysis_land = data_manipulation.group(pyrolysis_land, ["GCAM", "LandLeaf"])
    released_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf"])
    flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)

    global_land = data_manipulation.group(flat_diff_land, ["LandLeaf"])
    flat_diff_land = data_manipulation.group(flat_diff_land, ["GCAM", "LandLeaf"])
    print("plot regional land use change in " + str(biochar_year))
    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "land use change by region in " + str(biochar_year))
    print("plotting global land use change across all years")
    plotting.plot_stacked_bar_product(global_land, c.GCAMConstants.biochar_x, SSP, "LandLeaf", "global land use change by year")

    flat_diff_land = data_manipulation.percent_of_total(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf", "land use change by region in " + str(biochar_year))


def figure5(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 5
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # regional averaged food consumption by food type
    # convert Pcal to kcal/capita/day
    # get population data
    released_pop = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/population_by_region.csv")
    pyrolysis_pop = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/population_by_region.csv")
    released_pop = released_pop[released_pop[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_pop = pyrolysis_pop[pyrolysis_pop[['SSP']].isin(SSP).any(axis=1)]
    released_Pcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_consumption_by_type_specific.csv")
    pyrolysis_Pcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/food_consumption_by_type_specific.csv")
    released_Pcal = released_Pcal[released_Pcal[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_Pcal = pyrolysis_Pcal[pyrolysis_Pcal[['SSP']].isin(SSP).any(axis=1)]

    released_Pcal['GCAM'] = released_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    released_pop['GCAM'] = released_pop.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_Pcal['GCAM'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    pyrolysis_pop['GCAM'] = pyrolysis_pop.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    released_Pcal['technology'] = released_Pcal.apply(lambda row: data_manipulation.relabel_food(row), axis=1)
    pyrolysis_Pcal['technology'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_food(row), axis=1)

    # drop MiscCrop and FiberCrop because those products don't have meaningful calories and clutter the graph
    released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Fiber Crops"].index)
    released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Other Crops"].index)
    pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Fiber Crops"].index)
    pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Other Crops"].index)

    released_Pcal = data_manipulation.group(released_Pcal, ["GCAM", "SSP", "technology"])
    pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["GCAM", "SSP", "technology"])

    released_pcal_pop = pd.merge(released_Pcal, released_pop, how="inner", on=["SSP", "GCAM"],
                                 suffixes=("_pcal", "_pop"))
    pyrolysis_pcal_pop = pd.merge(pyrolysis_Pcal, pyrolysis_pop, how="inner", on=["SSP", "GCAM"],
                                  suffixes=("_pcal", "_pop"))

    # calculate pcal per capita in 2050
    released_pcal_pop["pcal_capita_2050"] = released_pcal_pop["2050_pcal"] / (1000 * released_pcal_pop[
        "2050_pop"]) * 1000000000000 / 365 / 2  # * peta to kilo/365/conversion factor of 2 randomly
    pyrolysis_pcal_pop["pcal_capita_2050"] = pyrolysis_pcal_pop["2050_pcal"] / (
            1000 * pyrolysis_pcal_pop["2050_pop"]) * 1000000000000 / 365 / 2
    released_pcal_pop["Units"] = "kcal/capita/day"
    pyrolysis_pcal_pop["Units"] = "kcal/capita/day"

    merged_pcal = released_pcal_pop.merge(pyrolysis_pcal_pop, how="inner", on=["SSP", "GCAM", "technology_pcal"],
                                          suffixes=("_left", "_right"))
    merged_pcal["pcal_capita_2050"] = merged_pcal["pcal_capita_2050" + "_right"] - merged_pcal[
        "pcal_capita_2050" + "_left"]

    # extract population and identifying information in 2050 for weighted average calculations
    merged_pop = pd.DataFrame()
    merged_pop["pcal_capita_2050"] = merged_pcal["2050_pop_right"]
    merged_pop["GCAM"] = merged_pcal["GCAM"]
    merged_pop["SSP"] = merged_pcal["SSP"]
    merged_pop["technology_pcal"] = merged_pcal["technology_pcal"]

    plotting.plot_regional_vertical_avg(merged_pcal, "pcal_capita_2050", SSP, "change in food demand (kcal/person/day)",
                                        title="change in food demand in " + str(SSP[0]) + " and RCP " + str(RCP),
                                        column="technology_pcal", supply=merged_pop)

    # Staple expenditure as percentage of average income – food demand prices and GDP per capita PPP by region
    # get data
    released_staple_expenditure = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_demand_prices.csv")
    pyrolysis_staple_expenditure = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/masked/food_demand_prices.csv")
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['SSP']].isin(SSP).any(axis=1)]
    diff_food_staple_income = data_manipulation.percent_difference(pyrolysis_staple_expenditure,
                                                                   released_staple_expenditure,
                                                                   ["SSP", "GCAM", "input"])

    diff_food_staple_income['GCAM'] = diff_food_staple_income.apply(lambda row: data_manipulation.relabel_region(row),
                                                                    axis=1)
    diff_food_staple_income['input'] = diff_food_staple_income.apply(
        lambda row: data_manipulation.relabel_food_demand(row),
        axis=1)
    diff_food_staple_income[
        "2050_conv"] = diff_food_staple_income[
                           "2050"] * 1.62  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=200501&year2=202401

    diff_food_staple_income = diff_food_staple_income.sort_values(by="2050_conv", ascending=False)

    # add an empty row at the top of the dataframe
    new_row1 = pd.DataFrame(diff_food_staple_income.loc[0]).transpose()
    new_row2 = pd.DataFrame(diff_food_staple_income.loc[0]).transpose()
    new_row1["2050_conv"] = 0
    new_row1["GCAM"] = " "
    new_row2["2050_conv"] = 0
    new_row2["GCAM"] = " "
    new_row2["input"] = "Staples"
    diff_food_staple_income = pd.concat([new_row1, new_row2, diff_food_staple_income, new_row2, new_row1])

    # plot results
    plotting.plot_regional_rose(diff_food_staple_income, "2050_conv", SSP, "decrease in food expenditure (%)",
                                "food expenditure in 2050 in " + str(SSP[0]) + " and RCP " + str(RCP),
                                column="input")


def figure6(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 6
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # regional change in N fertilizer production technologies
    released_f = pd.read_csv("data/gcam_out/released/" + RCP + "/original/fertilizer_production_by_tech.csv")
    pyrolysis_f = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/fertilizer_production_by_tech.csv")

    # process data - percent change
    released_f = data_manipulation.group(released_f, ["SSP", "GCAM", "subsector"])
    pyrolysis_f = data_manipulation.group(pyrolysis_f, ["SSP", "GCAM", "subsector"])

    # relabel and regroup rows
    released_f['subsector'] = released_f.apply(lambda row: data_manipulation.relabel_fertilizer_product(row), axis=1)
    pyrolysis_f['subsector'] = pyrolysis_f.apply(lambda row: data_manipulation.relabel_fertilizer_product(row), axis=1)
    released_f = data_manipulation.group(released_f, ["GCAM", "SSP", "subsector"])
    pyrolysis_f = data_manipulation.group(pyrolysis_f, ["GCAM", "SSP", "subsector"])

    # add biochar row to the released version so that the flat diff can be analyzed
    biochar = pyrolysis_f.loc[pyrolysis_f["subsector"] == "biochar"]
    for i in c.GCAMConstants.biochar_x:
        biochar.loc[:, str(i)] = 0
    ref_released = pd.concat([released_f, biochar])
    flat_diff_f = data_manipulation.flat_difference(ref_released, pyrolysis_f, ["SSP", "GCAM", "subsector"])
    flat_diff_f = flat_diff_f[~flat_diff_f[['GCAM']].isin(["Global"]).any(axis=1)]
    flat_diff_f = flat_diff_f[flat_diff_f[['SSP']].isin(SSP).any(axis=1)]
    plotting.plot_world(flat_diff_f, pyrolysis_f["subsector"].unique().tolist(), ["SSP2"], "product", "subsector",
                        ["2050"], "spatial change in N fertilizer production techniques")

    # Changes in energy mix
    # refined liquids production
    ref_released = pd.read_csv("data/gcam_out/released/" + RCP + "/original/refined_liquids_production_by_tech.csv")
    ref_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/refined_liquids_production_by_tech.csv")
    # relabel CCS technologies
    ref_released['technology'] = ref_released.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)
    ref_pyrolysis['technology'] = ref_pyrolysis.apply(
        lambda row: data_manipulation.label_fuel_tech(row, "technology", [" CCS level 1", " CCS level 2"]), axis=1)

    # group technologies
    ref_released = data_manipulation.group(ref_released, ["SSP", "GCAM", "technology"])
    ref_pyrolysis = data_manipulation.group(ref_pyrolysis, ["SSP", "GCAM", "technology"])

    # add manure fuel row to the released version so that the flat diff can be analyzed
    man_fuel = ref_pyrolysis[ref_pyrolysis[["technology"]].isin(["manure fuel", "manure_fuel"]).any(axis=1)]
    for i in c.GCAMConstants.biochar_x:
        man_fuel.loc[:, str(i)] = 0
    ref_released = pd.concat([ref_released, man_fuel])

    # select global region
    ref_released = ref_released[~ref_released[['GCAM']].isin(["Global"]).any(axis=1)]
    ref_pyrolysis = ref_pyrolysis[~ref_pyrolysis[['GCAM']].isin(["Global"]).any(axis=1)]

    # plot products
    flat_diff_biofuel = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["SSP", "technology", "GCAM"])
    plotting.plot_stacked_bar_year(flat_diff_biofuel, ["2050"], SSP, "technology", .01)


def figure7(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 7
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    for i in RCP:
        # global supply of biochar and manure fuel feedstock
        for k in [["beef biochar", "dairy biochar", "pork biochar", "poultry biochar", "goat biochar"],
                  ["manure fuel feedstock", "manure_fuel"]]:
            biochar_supply = pd.read_csv(
                "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(i) + "/masked" + "/supply_of_all_markets.csv")
            biochar_supply['product'] = biochar_supply.apply(lambda row: data_manipulation.remove__(row, "product"),
                                                             axis=1)
            biochar_supply = biochar_supply[biochar_supply[['product']].isin(k).any(axis=1)]
            biochar_supply = data_manipulation.group(biochar_supply, ["SSP", "product"])
            if not biochar_supply.empty:
                baseline_data = biochar_supply.copy(deep=True)
                baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
                baseline_data["LandLeaf"] = baseline_data.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
                baseline_data["SSP"] = "released"
                for j in c.GCAMConstants.x:
                    baseline_data[str(j)] = 0
                biochar_supply = pd.concat([biochar_supply, baseline_data])
                plotting.sensitivity(biochar_supply, i, "released", "2050", "product")

        # global net land use
        released_land = pd.read_csv("data/gcam_out/released/" + str(i) + "/original/aggregated_land_allocation.csv")
        pyrolysis_land = pd.read_csv(
            "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(i) + "/masked" + "/aggregated_land_allocation.csv")
        released_land = released_land[released_land[['SSP']].isin(SSP).any(axis=1)]
        pyrolysis_land = pyrolysis_land[pyrolysis_land[['SSP']].isin(SSP).any(axis=1)]
        released_land = released_land[released_land[['GCAM']].isin(["Global"]).any(axis=1)]
        pyrolysis_land = pyrolysis_land[pyrolysis_land[['GCAM']].isin(["Global"]).any(axis=1)]

        flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land,
                                                           ["SSP", "LandLeaf", "GCAM"])
        flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row),
                                                          axis=1)

        # add data for a baseline scenario with no land use change
        baseline_data = released_land.copy(deep=True)
        baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
        baseline_data["LandLeaf"] = baseline_data.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0

        # drop tundra, urban, rock and desert because there is no variation
        flat_diff_land = pd.concat([flat_diff_land, baseline_data])
        flat_diff_land = flat_diff_land.drop(flat_diff_land[flat_diff_land["LandLeaf"] == "tundra"].index)
        flat_diff_land = flat_diff_land.drop(flat_diff_land[flat_diff_land["LandLeaf"] == "urban"].index)
        flat_diff_land = flat_diff_land.drop(flat_diff_land[flat_diff_land["LandLeaf"] == "rock and desert"].index)
        plotting.sensitivity(flat_diff_land, i, "released", "2050", "LandLeaf")

        # global food demand
        released_Pcal = pd.read_csv(
            "data/gcam_out/released/" + str(i) + "/original/food_consumption_by_type_specific.csv")
        pyrolysis_Pcal = pd.read_csv(
            "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
                i) + "/masked" + "/food_consumption_by_type_specific.csv")
        released_Pcal = released_Pcal[released_Pcal[['SSP']].isin(SSP).any(axis=1)]
        pyrolysis_Pcal = pyrolysis_Pcal[pyrolysis_Pcal[['SSP']].isin(SSP).any(axis=1)]

        released_Pcal['GCAM'] = released_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
        pyrolysis_Pcal['GCAM'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
        released_Pcal['technology'] = released_Pcal.apply(lambda row: data_manipulation.relabel_food(row), axis=1)
        pyrolysis_Pcal['technology'] = pyrolysis_Pcal.apply(lambda row: data_manipulation.relabel_food(row), axis=1)

        # drop MiscCrop and FiberCrop because those products don't have meaningful calories and clutter the graph
        released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Fiber Crops"].index)
        released_Pcal = released_Pcal.drop(released_Pcal[released_Pcal["technology"] == "Other Crops"].index)
        pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Fiber Crops"].index)
        pyrolysis_Pcal = pyrolysis_Pcal.drop(pyrolysis_Pcal[pyrolysis_Pcal["technology"] == "Other Crops"].index)
        released_Pcal = data_manipulation.group(released_Pcal, ["SSP", "technology"])
        pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["SSP", "technology"])
        diff_Pcal = data_manipulation.flat_difference(released_Pcal, pyrolysis_Pcal, ["SSP", "technology", "GCAM"])

        # add data for a baseline scenario with no land use change
        baseline_data = diff_Pcal.copy(deep=True)
        baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
        baseline_data["technology"] = baseline_data.apply(lambda row: data_manipulation.relabel_food(row), axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0
        diff_Pcal = pd.concat([diff_Pcal, baseline_data])
        plotting.sensitivity(diff_Pcal, i, "released", "2050", "technology")


def carbon_price_biochar_supply(nonBaselineScenario, RCP, SSP):
    carbon_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/original" + "/CO2_prices.csv")
    biochar_supply = pd.read_csv(
            "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
                RCP) + "/original" + "/supply_of_all_markets.csv")
    carbon_price = carbon_price[carbon_price[['SSP']].isin(SSP).any(axis=1)]
    carbon_price = carbon_price[carbon_price[['product']].isin(["CO2"]).any(axis=1)].drop_duplicates()
    biochar_supply = biochar_supply[biochar_supply[['SSP']].isin(SSP).any(axis=1)]
    biochar_supply = biochar_supply[biochar_supply[['product']].isin(["biochar"]).any(axis=1)]

    for i in c.GCAMConstants.biochar_x:
        plt.scatter(biochar_supply[str(i)], carbon_price[str(i)])
        plt.xlabel("biochar supply by country (Mt)")
        plt.ylabel("carbon price (1990$USD/tC)")
        plt.title("carbon price by biochar supply")
    plt.show()



    # spatial distribution of biochar/manure supply and prices
    biochar_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/original" + "/prices_of_all_markets.csv")
    products = ["biochar"]
    plotting.plot_world(biochar_price, products, SSP, "year", "product", c.GCAMConstants.biochar_x,
                        "spatial distribution of biochar prices")
    biochar_price = biochar_price[biochar_price[['product']].isin(products).any(axis=1)]
    biochar_price = biochar_price.melt(["GCAM", "product"], [str(i) for i in c.GCAMConstants.biochar_x])
    biochar_price['2024_value'] = biochar_price['value'] / .17 * 1000
    plt.hist(biochar_price['2024_value'])
    plt.title("biochar price histogram")
    plt.xlabel("biochar price 2024$/ton")
    plt.ylabel("count region-years")
    plt.show()

    prices = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/original" + "/prices_of_all_markets.csv")
    prices = prices[prices[['SSP']].isin(SSP).any(axis=1)]
    biochar_price = prices[prices[['product']].isin(["biochar", "beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(axis=1)]
    manure_price = prices[prices[['product']].isin(
        ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(axis=1)]
    manure_price = manure_price.melt(["GCAM", "product"], [str(i) for i in c.GCAMConstants.biochar_x])
    manure_price['2024_value'] = manure_price['value'] / .17 * 1000
    plt.hist(manure_price['2024_value'])
    plt.title("manure price histogram")
    plt.xlabel("manure price 1975$/kg")
    plt.ylabel("count region-years")
    plt.show()
    print(biochar_price)
    print(manure_price)

    prices = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/original" + "/prices_of_all_markets.csv")
    prices = prices[prices[['SSP']].isin(SSP).any(axis=1)]
    biochar_price = prices[prices[['product']].isin(
        ["biochar", "beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(axis=1)]
    manure_price = prices[prices[['product']].isin(
        ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(axis=1)]
    c_adj_bio_price = pd.merge(biochar_price, carbon_price, on=["GCAM", "SSP"], suffixes=("", "_C"))
    c_adj_bio_price = pd.merge(c_adj_bio_price, manure_price, on=["GCAM", "SSP"], suffixes=("", "_cost"))
    for i in c.GCAMConstants.biochar_x:
        c_adj_bio_price[str(i)+"_adj"] = (c_adj_bio_price[str(i)] - .11*c_adj_bio_price[str(i) + "_C"])*.17/1000
        c_adj_bio_price[str(i) + "_prod_cost"] = (c_adj_bio_price[str(i)] + .11*c_adj_bio_price[str(i) + "_C"]*0.41 - 2.4*c_adj_bio_price[str(i) + "_cost"])*.17/1000
    adj_bio_price = c_adj_bio_price.groupby("GCAM")[[str(i) + "_adj" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    adj_bio_price.columns = adj_bio_price.columns.str.rstrip("_adj")
    adj_bio_price["Units"] = "2024$/ton"
    adj_bio_price["SSP"] = "SSP1"
    adj_bio_price["product"] = "biochar"
    c_adj_bio_prod = c_adj_bio_price.groupby("GCAM")[
        [str(i) + "_adj" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    c_adj_bio_prod.columns = c_adj_bio_prod.columns.str.rstrip("_adj")
    c_adj_bio_prod["Units"] = "2024$/ton"
    c_adj_bio_prod["SSP"] = "SSP1"
    c_adj_bio_prod["product"] = "biochar"

    plotting.plot_world(adj_bio_price, ["biochar"], ["SSP1"], "year", "product", c.GCAMConstants.biochar_x, "2024$ C adj biochar price")
    plotting.plot_world(c_adj_bio_prod, ["biochar"], ["SSP1"], "year", "product", c.GCAMConstants.biochar_x,
                        "2024$ C adj biochar production cost as a biochar price")

def cue_figure(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for potential figure in the CUE conference paper
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    for i in RCP:
        # Changes in energy mix
        # refined liquids production
        ref_released = pd.read_csv("data/gcam_out/released/" + str(i) + "/original/refined_liquids_production_by_tech.csv")
        ref_pyrolysis = pd.read_csv(
            "data/gcam_out/" + str(nonBaselineScenario) + "/" + str(
                i) + "/masked" + "/refined_liquids_production_by_tech.csv")

        # add manure fuel row to the released version so that the flat diff can be analyzed
        man_fuel = ref_pyrolysis[ref_pyrolysis[["technology"]].isin(["manure fuel", "manure_fuel"]).any(axis=1)]
        for j in c.GCAMConstants.biochar_x:
            man_fuel.loc[:, str(j)] = 0
        ref_released = pd.concat([ref_released, man_fuel])

        # select global region
        ref_released = ref_released[ref_released[['GCAM']].isin(["Global"]).any(axis=1)]
        ref_pyrolysis = ref_pyrolysis[ref_pyrolysis[['GCAM']].isin(["Global"]).any(axis=1)]

        # add baseline data
        flat_diff_biofuel = data_manipulation.flat_difference(ref_released, ref_pyrolysis,
                                                              ["SSP", "technology", "GCAM"])
        perc_diff_biofuel = data_manipulation.percent_difference(ref_released, ref_pyrolysis,
                                                                 ["SSP", "technology", "GCAM"])

        baseline_data = flat_diff_biofuel.copy(deep=True)
        baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
        baseline_data["technology"] = baseline_data.apply(lambda row: data_manipulation.relabel_food(row), axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0
        flat_diff_biofuel = pd.concat([flat_diff_biofuel, baseline_data])

        baseline_data = perc_diff_biofuel.copy(deep=True)
        baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
        baseline_data["technology"] = baseline_data.apply(lambda row: data_manipulation.relabel_food(row), axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0
        perc_diff_biofuel = pd.concat([perc_diff_biofuel, baseline_data])

        # plot products
        plotting.sensitivity(flat_diff_biofuel, str(i), "released", "2050", "technology")
        plotting.sensitivity(perc_diff_biofuel, str(i), "released", "2050", "technology")


def main():
    # fertilizer("biochar", "2p6", ["SSP4"])
    # carbon_price_biochar_supply("test", "6p0", ["SSP1"])
    #figure2("biochar", c.GCAMConstants.RCPs, c.GCAMConstants.SSPs)
    # figure3("biochar", "6p0", c.GCAMConstants.SSPs, 2060)
    figure4("biochar", "2p6", ["SSP4"], 2050)
    figure5("biochar", "2p6", ["SSP4"])
    figure6("biochar", "2p6", ["SSP4"])
    figure7("biochar", ["2p6"], ["SSP4"])


if __name__ == '__main__':
    main()
