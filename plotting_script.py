import numpy as np
import plotting
import data_manipulation
import constants as c
import pandas as pd
import stats as stats


def food(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to food insecurity
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # #changes to animal livestock production
    # released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/supply_of_all_markets.csv")
    # pyrolysis_supply = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")
    # products = ["Beef", "Pork", "Dairy", "Poultry"]
    # released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    # pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    # perc_diff = data_manipulation.percent_difference(released_supply, pyrolysis_supply, ["SSP", "product", "GCAM"])
    # plotting.plot_world(perc_diff, products, ["SSP2"], "product", "product", [2050])
    # # livestock systems
    # feed_released = pd.read_csv("data/gcam_out/released/" + RCP + "/feed_consumption_by_meat_and_dairy_tech.csv")
    # feed_pyrolysis = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/feed_consumption_by_meat_and_dairy_tech.csv")
    # columns = ['sector', 'subsector', 'SSP']
    # feed_released = data_manipulation.group(feed_released, columns)
    # feed_pyrolysis = data_manipulation.group(feed_pyrolysis, columns)
    # flat_diff_feed = data_manipulation.flat_difference(feed_released, feed_pyrolysis, ["SSP", "sector", "subsector"])
    # plotting.plot_line(flat_diff_feed, ['Beef', 'Dairy', 'Poultry', 'Pork'], c.GCAMConstants.SSPs, "SSP", "sector",
    #                    "subsector")
    #
    # # Changes to crop production
    # # Changes to agricultural commodity prices
    # crops = ["Corn", "FiberCrop", "FodderGrass", "FodderHerb", "Forest", "Fruits", "Legumes", "MiscCrop", "NutSeeds",
    #          "OilCrop", "OtherGrain", "Pasture", "Rice", "RootTuber", "Soybean", "SugarCrop",
    #          "Vegetables", "Wheat", "biomass"]
    # released_ag_prices = pd.read_csv("data/gcam_out/released/" + RCP + "/ag_commodity_prices.csv")
    # pyrolysis_ag_prices = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/ag_commodity_prices.csv")
    # perc_diff_ag_prices = data_manipulation.percent_difference(released_ag_prices, pyrolysis_ag_prices,
    #                                                            ["SSP", "sector", "GCAM"])
    # plotting.plot_world(perc_diff_ag_prices, crops, ["SSP2"], "year", "sector", [2020, 2035, 2050, 2075, 2100])
    #
    # # Changes to food prices
    # released_price = pd.read_csv(
    #     "data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")  # prices_of_all_markets
    # pyrolysis_price = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")  # prices_of_all_markets
    # released_foo_price = pd.read_csv(
    #     "data/gcam_out/released/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    # pyrolysis_foo_price = pd.read_csv(
    #     "data/gcam_out/" + str(
    #         nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    # perc_diff_food_prices = data_manipulation.percent_difference(released_foo_price, pyrolysis_foo_price,
    #                                                            ["SSP", "sector", "GCAM"])
    # plotting.plot_world(perc_diff_food_prices, crops, ["SSP2"], "year", "sector", [2020, 2035, 2050, 2075, 2100])
    #
    # # correlation between food and energy prices
    # for products in ["regional beef", "regional dairy", "regional wheat"]:
    #     for energy in ["refined liquids enduse", "crude oil", "electricity", "natural gas"]:
    #         # get right energy source
    #         released_refliq_price = released_price[released_price[['product']].isin([energy]).any(axis=1)]
    #         pyrolysis_refliq_price = pyrolysis_price[pyrolysis_price[['product']].isin([energy]).any(axis=1)]
    #         released_refliq_price = released_refliq_price[released_refliq_price[['SSP']].isin(SSP).any(axis=1)]
    #         pyrolysis_refliq_price = pyrolysis_refliq_price[pyrolysis_refliq_price[['SSP']].isin(SSP).any(axis=1)]
    #
    #         # get right food sources
    #         released_food_price = released_foo_price[released_foo_price[['sector']].isin([products]).any(axis=1)]
    #         pyrolysis_food_price = pyrolysis_foo_price[pyrolysis_foo_price[['sector']].isin([products]).any(axis=1)]
    #         released_food_price = released_food_price[released_food_price[['SSP']].isin(SSP).any(axis=1)]
    #         pyrolysis_food_price = pyrolysis_food_price[pyrolysis_food_price[['SSP']].isin(SSP).any(axis=1)]
    #
    #         # test for stationarity
    #         print("released", products, "price")
    #         stats.stationarity_test(released_food_price, 2050)
    #         print("pyrolysis", products, "price")
    #         stats.stationarity_test(pyrolysis_food_price, 2050)
    #         print("released", energy, "price")
    #         stats.stationarity_test(released_refliq_price, 2050)
    #         print("pyrolysis", energy, "price")
    #         stats.stationarity_test(pyrolysis_refliq_price, 2050)
    #
    #         # tests for correlation
    #         released_res = stats.calc_price_linkage(released_refliq_price, released_food_price, SSP, 2050)
    #         pyrolysis_res = stats.calc_price_linkage(pyrolysis_refliq_price, pyrolysis_food_price, SSP, 2050)
    #         plotting.plot_price_coefficients(pyrolysis_res, released_res,
    #                                          "price coefficients for " + products + " and " + energy + " in " + SSP[0])

    # Global averaged per capita food available for consumption – food demand per capita
    #get data
    released_per_capita_kcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/food_demand_per_capita.csv")
    pyrolysis_per_capita_kcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/food_demand_per_capita.csv")

    # remove distinction between staples and non staples
    released_per_capita_kcal = data_manipulation.group(released_per_capita_kcal, ['GCAM', "SSP"])
    pyrolysis_per_capita_kcal = data_manipulation.group(pyrolysis_per_capita_kcal, ['GCAM', "SSP"])

    # apply analysis to few select regions
    regions = ["Africa_Southern", "Brazil", "China", "EU-15", "Russia", "USA"]
    released_per_capita_kcal = released_per_capita_kcal[released_per_capita_kcal[['GCAM']].isin(regions).any(axis=1)]
    pyrolysis_per_capita_kcal = pyrolysis_per_capita_kcal[pyrolysis_per_capita_kcal[['GCAM']].isin(regions).any(axis=1)]

    # plot data
    plotting.plot_regional_vertical(released_per_capita_kcal, 2050, SSP, "1000 kcal/person/day", "Released " + str(RCP))
    plotting.plot_regional_vertical(pyrolysis_per_capita_kcal, 2050, SSP, "1000 kcal/person/day",
                                    "Pyrolysis " + str(RCP))

    # Staple expenditure as percentage of average income5 – food demand prices and GDP per capita PPP by region
    #get data
    released_staple_expenditure = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/food_demand_prices.csv")
    pyrolysis_staple_expenditure = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/food_demand_prices.csv")
    released_income = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/GDP_per_capita_PPP_by_region.csv")
    pyrolysis_income = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/GDP_per_capita_PPP_by_region.csv")

    # only select staples
    staples = ["FoodDemand_Staples"]
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['input']].isin(staples).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['input']].isin(staples).any(axis=1)]

    # calculate portion of income spent on food staples
    released_food_portion_income = pd.merge(released_income, released_staple_expenditure, on=["GCAM", "SSP"], how="left", suffixes=("_income", "_expenditure"))
    pyrolysis_food_portion_income = pd.merge(pyrolysis_income, pyrolysis_staple_expenditure, on=["GCAM", "SSP"],
                                            how="left", suffixes=("_income", "_expenditure"))

    released_food_portion_income["2050a"] = 100 * (
                released_food_portion_income["2050_expenditure"] / released_food_portion_income["2050_income"])
    pyrolysis_food_portion_income["2050a"] = 100 * (
            pyrolysis_food_portion_income["2050_expenditure"] / pyrolysis_food_portion_income["2050_income"])
    released_food_portion_income["2010"] = 100 * (
                released_food_portion_income["2010_expenditure"] / released_food_portion_income["2010_income"])
    pyrolysis_food_portion_income["2010"] = 100 * (
                pyrolysis_food_portion_income["2010_expenditure"] / pyrolysis_food_portion_income["2010_income"])

    # plot results
    plotting.plot_regional_vertical(released_food_portion_income, "2050a", SSP, "staple expenditure as percentage of income",
                                    "Released " + str(RCP))
    plotting.plot_regional_vertical(pyrolysis_food_portion_income, "2050a", SSP, "staple expenditure as percentage of income",
                                    "Pyrolysis " + str(RCP))

    # food prices - percentage change over 2010
    # get data
    released_staple_expenditure = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/food_demand_prices.csv")
    pyrolysis_staple_expenditure = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/food_demand_prices.csv")

    # select on data for food staples
    staples = ["FoodDemand_Staples"]
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['input']].isin(staples).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['input']].isin(staples).any(axis=1)]

    # calculate percentage changes in food prices
    released_staple_expenditure["2050a"] = 100 * (
                released_staple_expenditure["2050"] - released_staple_expenditure["2010"]) / \
                                           released_staple_expenditure["2010"]
    pyrolysis_staple_expenditure["2050a"] = 100 * (
            pyrolysis_staple_expenditure["2050"] - pyrolysis_staple_expenditure["2010"]) / \
                                            pyrolysis_staple_expenditure["2010"]
    released_staple_expenditure["2010"] = 0
    pyrolysis_staple_expenditure["2010"] = 0

    #plot results
    plotting.plot_regional_vertical(released_staple_expenditure, "2050a", SSP, "percent change in food prices compared to 2010",
                                    "Released " + str(RCP))
    plotting.plot_regional_vertical(pyrolysis_staple_expenditure, "2050a", SSP, "percent change in food prices compared to 2010",
                                    "Pyrolysis " + str(RCP))


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
    ref_released = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    ref_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    products = ["sugar cane ethanol", "manure fuel", "corn ethanol",
                "cellulosic ethanol", "biodiesel", "FT biofuels", "BTL with hydrogen"]
    flat_diff_biofuel = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["SSP", "technology", "GCAM"])
    plotting.plot_line(flat_diff_biofuel, products, c.GCAMConstants.SSPs, "product", "technology", "Units")
    released_cost = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_costs_by_tech.csv")
    released_prod = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    released_new = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    pyrolysis_cost = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_costs_by_tech.csv")
    pyrolysis_prod = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    pyrolysis_new = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    flat_diff_cost = data_manipulation.flat_difference(released_cost, pyrolysis_cost, ["SSP", "technology", "GCAM"])
    flat_diff_prod = data_manipulation.flat_difference(released_prod, pyrolysis_prod, ["SSP", "technology", "GCAM"])
    flat_diff_new = data_manipulation.flat_difference(released_new, pyrolysis_new, ["SSP", "technology", "GCAM"])
    products = ["cellulosic ethanol", "biodiesel", "FT biofuels", "BTL with hydrogen", "sugar cane ethanol",
                "corn ethanol"]
    print("flat diff cost")
    plotting.plot_world(flat_diff_cost, products, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)
    print("flat diff production")
    plotting.plot_world(flat_diff_prod, products, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)
    print("flat diff new capacity")
    plotting.plot_world(flat_diff_new, products, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)

    # comparison of decrease in newly installed production of biofuels compared to the supply of manure fuel
    released_new = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    released_prod = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    pyrolysis_new = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    pyrolysis_prod = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    flat_diff_new = data_manipulation.flat_difference(released_new, pyrolysis_new, ["SSP", "technology", "GCAM"])
    flat_diff_prod = data_manipulation.flat_difference(released_prod, pyrolysis_prod, ["SSP", "technology", "GCAM"])
    flat_diff_new = data_manipulation.group(flat_diff_new, ["SSP", "GCAM", "subsector"])
    flat_diff_prod = data_manipulation.group(flat_diff_prod, ["SSP", "GCAM", "subsector"])
    released_biofuels = data_manipulation.group(released_prod, ["SSP", "GCAM", "subsector"])
    pyrolysis_biofuels = data_manipulation.group(pyrolysis_prod, ["SSP", "GCAM", "subsector"])
    perc_diff_biofuels = data_manipulation.percent_difference(released_biofuels, pyrolysis_biofuels,
                                                              ["SSP", "subsector", "GCAM"])
    products = ["biomass liquids"]
    plotting.plot_world(flat_diff_new, products, ["SSP2"], "year", "subsector", c.GCAMConstants.plotting_x)
    products = ["manure fuel"]
    print("newly installed capacity")
    plotting.plot_world(pyrolysis_new, products, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)

    def label_ssp(row):
        if row['subsector'] == "biomass liquids":
            return "biofuels"
        elif row['technology'] == "manure fuel":
            return "biofuels"
        return row['technology']

    # Changes in supplies of renewable biofuels
    products = ["biofuels"]
    flat_diff_new['technology'] = flat_diff_new.apply(lambda row: label_ssp(row), axis=1)
    flat_diff_prod['technology'] = flat_diff_prod.apply(lambda row: label_ssp(row), axis=1)
    flat_diff_installed = data_manipulation.flat_summation(pyrolysis_new, flat_diff_new, ["SSP", "technology", "GCAM"])
    flat_diff_supply = data_manipulation.flat_summation(pyrolysis_prod, flat_diff_prod, ["SSP", "technology", "GCAM"])
    print("difference in newly installed biofuel capacity")
    plotting.plot_world(flat_diff_installed, products, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)
    print("difference in biofuel supply")
    plotting.plot_world(flat_diff_supply, products, ["SSP2"], "year", "technology",
                        c.GCAMConstants.plotting_x)


def climate(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to climate
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # # Changes in CO2 concentrations
    # co2_conc_released = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_concentrations.csv")
    # co2_conc_pyrolysis = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_concentrations.csv")
    # flat_diff_CO2 = data_manipulation.flat_difference(co2_conc_released, co2_conc_pyrolysis, ["SSP"])
    # flat_diff_CO2["GCAM"] = "All"
    # plotting.plot_line(flat_diff_CO2, ["PPM"], c.GCAMConstants.SSPs, "SSP", "Units", "Version")
    #
    # # Changes in carbon prices
    # released_CO2_price = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_prices.csv")
    # pyrolysis_CO2_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_prices.csv")
    # products = ["CO2"]
    # released_CO2_price = released_CO2_price[released_CO2_price[['product']].isin(products).any(axis=1)]
    # pyrolysis_CO2_price = pyrolysis_CO2_price[pyrolysis_CO2_price[['product']].isin(products).any(axis=1)]
    # perc_diff_CO2_price = data_manipulation.percent_difference(released_CO2_price, pyrolysis_CO2_price,
    #                                                            ["SSP", "product", "GCAM"])
    # plotting.plot_world(perc_diff_CO2_price, products, ["SSP1", "SSP2"], "year", "product", c.GCAMConstants.future_x)
    #
    # # plotting CO2 sequestering
    # co2_seq_released = pd.read_csv(
    #     "data/gcam_out/released/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    # co2_seq_pyrolysis = pd.read_csv(
    #     "data/gcam_out/" + str(
    #         nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    # co2_seq_released['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    # co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    # products = ["beef_biochar", "dairy_biochar", "pork_biochar", "poultry_biochar", "goat_biochar"]
    # biochar_pyrolysis = co2_seq_pyrolysis[co2_seq_pyrolysis['sector'].str.contains("|".join(products))]
    # plotting.plot_line(biochar_pyrolysis, products, SSP, "SSP", "sector", "Version")
    #
    # # combine similar sectors
    # co2_seq_released['sector'] = co2_seq_released.apply(lambda row: label_sequestration_sectors(row), axis=1)
    # co2_seq_released['sector'] = co2_seq_pyrolysis.apply(lambda row: label_sequestration_sectors(row), axis=1)
    #
    # # merge sectors in the CO2 sequestered data
    # co2_seq_released_comb = data_manipulation.group(co2_seq_released, ["sector", "SSP"])
    # co2_seq_pyrolysis_comb = data_manipulation.group(co2_seq_released, ["sector", "SSP"])
    #
    # # plot difference
    # flat_diff_CO2 = data_manipulation.flat_difference(co2_seq_released_comb, co2_seq_pyrolysis_comb,
    #                                                   ["sector", "SSP"])
    # plotting.plot_line(flat_diff_CO2, flat_diff_CO2["sector"].unique(), SSP, "SSP", "sector", "Version")
    #
    # # Contribution to cumulative emissions reduction
    # co2_seq_released = pd.read_csv(
    #     "data/gcam_out/released/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    # co2_seq_pyrolysis = pd.read_csv(
    #     "data/gcam_out/" + str(
    #         nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    # co2_seq_released['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    # co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    #
    # for i in ["sector", "subsector", "technology"]:
    #     co2_seq_released_stacked = data_manipulation.group(co2_seq_released, [i, "SSP"])
    #     co2_seq_pyrolysis_stacked = data_manipulation.group(co2_seq_pyrolysis, [i, "SSP"])
    #     flat_diff_CO2_stacked = data_manipulation.flat_difference(co2_seq_released_stacked,
    #                                                               co2_seq_pyrolysis_stacked, [i, "SSP"])
    #     plotting.plot_stacked_bar(flat_diff_CO2_stacked, c.GCAMConstants.plotting_x, c.GCAMConstants.SSPs, i, 5)

    # Annual carbon emissions – CO2 emissions by region, sector, resource production
    co2_emi_released = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_emissions_by_region.csv")
    co2_emi_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_region.csv")
    flat_diff_CO2 = data_manipulation.flat_difference(co2_emi_released, co2_emi_pyrolysis, ["SSP", "GCAM"])
    flat_diff_CO2["GCAM"] = "All"
    plotting.plot_line(flat_diff_CO2, ["MTC"], c.GCAMConstants.SSPs, "SSP", "Units", "Version")

    # Changes to CH4 and N2O emissions – nonCO2 emissions by region
    nonco2_emi_released = pd.read_csv("data/gcam_out/released/" + RCP + "/nonCO2_emissions_by_region.csv")
    nonco2_emi_pyrolysis = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/nonCO2_emissions_by_region.csv")
    flat_diff_nonCO2 = data_manipulation.flat_difference(nonco2_emi_released, nonco2_emi_pyrolysis, ["SSP", "GCAM", "GHG"])
    flat_diff_nonCO2["GCAM"] = "All"
    plotting.plot_line(flat_diff_nonCO2, ["N2O_AGR", "CH4_AGR", "NMVOC_AGR", "NOx_AGR", "NH3_AGR"], c.GCAMConstants.SSPs, "SSP", "GHG", "Version")


def land(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to land use
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # regional land use change
    landleafs = ["biomass", "crops", "forest (managed)", "forest (unmanaged)", "grass", "otherarable",
                 "pasture (grazed)", "pasture (other)", "shrubs"]
    released_land = pd.read_csv("data/gcam_out/released/" + RCP + "/aggregated_land_allocation.csv")
    pyrolysis_land = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/aggregated_land_allocation.csv")
    perc_diff_land = data_manipulation.percent_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])
    # plotting.plot_world(perc_diff_land, landleafs, ["SSP2"], "year", "LandLeaf", c.GCAMConstants.plotting_x)

    flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])
    plotting.plot_stacked_bar_SSP(flat_diff_land, 2050, SSP, "LandLeaf", 1, RCP)


def fertilizer(nonBaselineScenario, RCP, SSP):
    """
    Returns plots related to fertilizer
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # Plotting Fertilizer prices
    released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")
    products = ["N fertilizer"]
    released_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    pyrolysis_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    perc_diff_f_price = data_manipulation.percent_difference(released_price, pyrolysis_price,
                                                             ["SSP", "product", "GCAM"])
    print("price")
    plotting.plot_world(perc_diff_f_price, products, ["SSP2"], "year", "product", c.GCAMConstants.plotting_x)

    # supply of fertilizer
    released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/supply_of_all_markets.csv")
    pyrolysis_supply = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")
    products = ["N fertilizer"]
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    perc_diff_f_supply = data_manipulation.percent_difference(released_supply, pyrolysis_supply,
                                                              ["SSP", "product", "GCAM"])
    print("supply")
    plotting.plot_world(perc_diff_f_supply, products, ["SSP2"], "year", "product", c.GCAMConstants.plotting_x)

    # regional change in N fertilizer production technologies
    technologies = ["biochar_sup", "gas", "hydrogen"]
    released_f = pd.read_csv("data/gcam_out/released/" + RCP + "/fertilizer_production_by_tech.csv")
    pyrolysis_f = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/fertilizer_production_by_tech.csv")
    released_prod = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    pyrolysis_prod = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    released_prod = data_manipulation.group(released_prod, ["SSP", "GCAM", "technology"])
    pyrolysis_prod = data_manipulation.group(pyrolysis_prod, ["SSP", "GCAM", "technology"])
    flat_diff_prod = data_manipulation.flat_difference(released_prod, pyrolysis_prod, ["SSP", "technology", "GCAM"])
    perc_diff_prod = data_manipulation.percent_difference(released_prod, pyrolysis_prod, ["SSP", "technology", "GCAM"])
    released_f = data_manipulation.group(released_f, ["SSP", "GCAM", "technology"])
    pyrolysis_f = data_manipulation.group(pyrolysis_f, ["SSP", "GCAM", "technology"])
    flat_diff_f = data_manipulation.flat_difference(released_f, pyrolysis_f, ["SSP", "GCAM", "technology"])
    perc_diff_f = data_manipulation.percent_difference(released_f, pyrolysis_f, ["SSP", "GCAM", "technology"])
    plotting.plot_world(flat_diff_f, technologies, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)
    plotting.plot_world(perc_diff_f, technologies, ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)
    plotting.plot_world(pyrolysis_f, ["biochar_sup"], ["SSP2"], "year", "technology", c.GCAMConstants.plotting_x)


def label_sequestration_sectors(row):
    """
    returns the aggregated sector to better show plots
    :param row: row of a pandas dataframe
    :return: aggregated sector or original one
    """
    if row['sector'] in ["H2 central production", "H2 wholesale dispensing"]:
        return "hydrogen"
    elif row['sector'] in ["backup_electricity", "district heat", "refining"]:
        return "other energy sector"
    elif row['sector'] in ["chemical energy use", "chemical feedstocks", "N fertilizer", "alumina", "cement",
                           "iron and steel", "other industrial energy use", "other industrial feedstocks",
                           "process heat cement"]:
        return "industrial energy use"
    elif row['sector'] in ["comm cooling", "comm heating", "comm others"]:
        return "commercial energy use"
    elif row['sector'] in ["elec_biomass (IGCC CCS)", "elec_biomass (IGCC)", "elec_biomass (conv CCS)",
                           "elec_biomass (conv)"]:
        return "electricity - biomass"
    elif row['sector'] in ["elec_coal (IGCC CCS)", "elec_coal (IGCC)", "elec_coal (conv pul CCS)",
                           "elec_coal (conv pul)"]:
        return "electricity - coal"
    elif row['sector'] in ["elec_gas (CC CCS)", "elec_gas (CC)", "elec_gas (steam/CT)"]:
        return "electricity - gas"
    elif row['sector'] in ["elec_refined liquids (CC CCS)", "elec_refined liquids (CC)",
                           "elec_refined liquids (steam/CT)"]:
        return "electricity - refined liquids"
    elif row['sector'] in ["gas pipeline", "gas processing"]:
        return "gas processing"
    elif row['sector'] in ["resid cooling", "resid heating", "resid others"]:
        return "commercial energy use"
    elif row['sector'] in ["trn_aviation_intl", "trn_freigh", "trn_freight_road", "trn_pass", "trn_pass_road",
                           "trn_pass_road_LDV", "trn_pass_road_LDV_4W", "trn_shipping_intl", "trn_freight"]:
        return "transportation"
    elif row['sector'] in ['regional biomass', 'regional biomassOil', "regional corn for ethanol",
                           "regional sugar for ethanol"]:
        return "other biomass for refining"
    else:
        return row['sector']


if __name__ == '__main__':
    for j in ["4p5", "6p0"]:
        #food("pyrolysis", j, c.GCAMConstants.SSPs)
        #energy("pyrolysis", j, c.GCAMConstants.SSPs)
        climate("pyrolysis", j, c.GCAMConstants.SSPs)
        # land("pyrolysis", j, c.GCAMConstants.SSPs)
        #fertilizer("pyrolysis", j, c.GCAMConstants.SSPs)
