import matplotlib.pyplot as plt
import numpy as np
import plotting
import data_manipulation
import constants as c
import pandas as pd
import stats as stats


def standard_plots(nonBaselineScenario, RCP):
    # Plotting animal products
    released_CO2_price = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_prices.csv")
    pyrolysis_CO2_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_prices.csv")
    products = ["CO2"]
    released_CO2_price = released_CO2_price[released_CO2_price[['product']].isin(products).any(axis=1)]
    pyrolysis_CO2_price = pyrolysis_CO2_price[pyrolysis_CO2_price[['product']].isin(products).any(axis=1)]
    perc_diff_CO2_price = data_manipulation.percent_difference(released_CO2_price, pyrolysis_CO2_price, ["SSP", "product", "GCAM"])
    plotting.plot_world(perc_diff_CO2_price, products, ["SSP1", "SSP2"], "year", "product", c.GCAMConstants.future_x)

    released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/supply_of_all_markets.csv")
    pyrolysis_supply = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")
    products = ["Beef", "Pork", "Dairy", "Poultry"]
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    perc_diff = data_manipulation.percent_difference(released_supply, pyrolysis_supply, ["SSP", "product", "GCAM"])
    plotting.plot_world(perc_diff, products, ["SSP2"], "product", "product", [2050])

    # plotting CO2 concentrations
    co2_conc_released = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_concentrations.csv")
    co2_conc_pyrolysis = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_concentrations.csv")
    flat_diff_CO2 = data_manipulation.flat_difference(co2_conc_released, co2_conc_pyrolysis, ["SSP"])
    flat_diff_CO2["GCAM"] = "All"
    plotting.plot_line(flat_diff_CO2, ["PPM"], c.GCAMConstants.SSPs, "SSP", "Units", "Version")

    # livestock systems
    feed_released = pd.read_csv("data/gcam_out/released/" + RCP + "/feed_consumption_by_meat_and_dairy_tech.csv")
    feed_pyrolysis = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/feed_consumption_by_meat_and_dairy_tech.csv")
    columns = ['sector', 'subsector', 'SSP']
    feed_released = data_manipulation.group(feed_released, columns)
    feed_pyrolysis = data_manipulation.group(feed_pyrolysis, columns)
    flat_diff_feed = data_manipulation.flat_difference(feed_released, feed_pyrolysis, ["SSP", "sector", "subsector"])
    plotting.plot_line(flat_diff_feed, ['Beef', 'Dairy', 'Poultry', 'Pork'], c.GCAMConstants.SSPs, "SSP", "sector",
                       "subsector")
    # perc_diff_feed = data_manipulation.percent_difference(feed_released, feed_pyrolysis, ["SSP", "sector", "subsector"])
    # plotting.plot_line(perc_diff_feed, ['Beef', 'Dairy', 'Poultry', 'Pork'], c.GCAMConstants.SSPs, "SSP", "sector",
    #                    "subsector")

    # refined liquids production
    ref_released = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    ref_pyrolysis = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    products = ["sugar cane ethanol", "manure fuel", "corn ethanol",
                "cellulosic ethanol", "biodiesel", "FT biofuels", "BTL with hydrogen"]
    flat_diff_biofuel = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["SSP", "technology", "GCAM"])
    plotting.plot_line(flat_diff_biofuel, products, c.GCAMConstants.SSPs, "product", "technology", "Units")
    per_diff_biofuel = data_manipulation.change_between_years(flat_diff_biofuel)
    # plotting.plot_world(per_diff_biofuel, products, ["SSP2"], "year", "technology",
    #                     ["2020-2025", "2025-2030", "2030-2035", "2035-2040", "2040-2045", "2045-2050", "2050-2055",
    #                      "2055-2060", "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090",
    #                      "2090-2095", "2095-2100"])
    flat_diff_manure_fuel = data_manipulation.change_between_years(ref_pyrolysis)
    # plotting.plot_world(flat_diff_manure_fuel, ["manure fuel"], ["SSP2"], "year", "technology",
    #                     ["2020-2025", "2025-2030", "2030-2035", "2035-2040", "2040-2045", "2045-2050", "2050-2055",
    #                      "2055-2060", "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090",
    #                      "2090-2095", "2095-2100"])
    released_cost = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_costs_by_tech.csv")
    released_prod = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    released_new = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    pyrolysis_cost = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_costs_by_tech.csv")
    pyrolysis_prod = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
    pyrolysis_new = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech_new.csv")
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
    pyrolysis_new = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech_new.csv")
    pyrolysis_prod = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
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

    # Plotting Fertilizer and refined liquids prices
    released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")
    products = ["N fertilizer", "refined liquids enduse"]
    released_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    pyrolysis_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    perc_diff_f_price = data_manipulation.percent_difference(released_price, pyrolysis_price,
                                                             ["SSP", "product", "GCAM"])
    print("price")
    plotting.plot_world(perc_diff_f_price, products, ["SSP2"], "year", "product", c.GCAMConstants.plotting_x)

    released_supply = pd.read_csv("data/gcam_out/released/" + RCP + "/supply_of_all_markets.csv")
    pyrolysis_supply = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")
    products = ["N fertilizer"] #, "refined liquids enduse"
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    pyrolysis_supply = pyrolysis_supply[pyrolysis_supply[['product']].isin(products).any(axis=1)]
    perc_diff_f_supply = data_manipulation.percent_difference(released_supply, pyrolysis_supply,
                                                              ["SSP", "product", "GCAM"])
    print("supply")
    plotting.plot_world(perc_diff_f_supply, products, ["SSP2"], "year", "product", c.GCAMConstants.plotting_x)

    # regional change in N fertilizer production technologies
    technologies = ["biochar_sup", "gas", "hydrogen"]
    released_f = pd.read_csv("data/gcam_out/released/" + RCP + "/fertilizer_production_by_tech.csv")
    pyrolysis_f = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/fertilizer_production_by_tech.csv")
    released_prod = pd.read_csv("data/gcam_out/released/" + RCP + "/refined_liquids_production_by_tech.csv")
    pyrolysis_prod = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/refined_liquids_production_by_tech.csv")
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

    # plotting the years in which the maximum disruptions occur (both flat and percentage) for all N fertilizer and biofuel technologies
    technologies = ["coal", "gas", "hydrogen"]
    products = ["sugar cane ethanol", "corn ethanol", "cellulosic ethanol", "biodiesel", "FT biofuels",
                "BTL with hydrogen"]
    years_flat_f = data_manipulation.years_to_maximum_disruption(flat_diff_f, released_f, ["SSP2"], technologies,
                                                                 "technology")
    years_perc_f = data_manipulation.years_to_maximum_disruption(perc_diff_f, released_f, ["SSP2"], technologies,
                                                                 "technology")
    years_flat_prod = data_manipulation.years_to_maximum_disruption(flat_diff_prod, released_prod, ["SSP2"], products,
                                                                    "technology")
    years_perc_prod = data_manipulation.years_to_maximum_disruption(perc_diff_prod, released_prod, ["SSP2"], products,
                                                                    "technology")
    plotting.plot_disruption_by_years(years_flat_f, technologies, "technology", ["SSP2"], "lower right")
    plotting.plot_disruption_by_years(years_perc_f, technologies, "technology", ["SSP2"], "lower right")
    plotting.plot_disruption_by_years(years_flat_prod, products, "technology", ["SSP2"], "lower left")
    plotting.plot_disruption_by_years(years_perc_prod, products, "technology", ["SSP2"], "upper left")
    # cutting off upper bounds because they are sad
    for i in c.GCAMConstants.plotting_x:
        perc_diff_prod.loc[perc_diff_prod[str(i)] > 100, str(i)] = np.nan
    years_perc_prod = data_manipulation.years_to_maximum_disruption(perc_diff_prod, released_prod, ["SSP2"], products,
                                                                    "technology")
    plotting.plot_disruption_by_years(years_perc_prod, products, "technology", ["SSP2"], "upper left")

    # regional land use change
    landleafs = ["biomass", "crops", "forest (managed)", "forest (unmanaged)", "grass", "otherarable",
                 "pasture (grazed)", "pasture (other)", "shrubs"]
    released_land = pd.read_csv("data/gcam_out/released/" + RCP + "/aggregated_land_allocation.csv")
    pyrolysis_land = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/aggregated_land_allocation.csv")
    perc_diff_land = data_manipulation.percent_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])
    # plotting.plot_world(perc_diff_land, landleafs, ["SSP2"], "year", "LandLeaf", [2020, 2035, 2050, 2075, 2100])
    landleafs = ["biomass", "crops"]
    plotting.plot_world(perc_diff_land, landleafs, ["SSP2"], "year", "LandLeaf", c.GCAMConstants.plotting_x)
    perc_diff_land_2 = data_manipulation.change_between_years(perc_diff_land)
    # plotting.plot_world(perc_diff_land_2, ["biomass"], ["SSP2"], "year", "LandLeaf",
    #                     ["2020-2025", "2025-2030", "2030-2035", "2035-2040", "2040-2045", "2045-2050", "2050-2055",
    #                      "2055-2060", "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090",
    #                      "2090-2095", "2095-2100"])
    # plotting.plot_world(perc_diff_land_2, ["crops"], ["SSP2"], "year", "LandLeaf",
    #                     ["2020-2025", "2025-2030", "2030-2035", "2035-2040", "2040-2045", "2045-2050", "2050-2055",
    #                      "2055-2060", "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090",
    #                      "2090-2095", "2095-2100"])

    # plotting correlation between land use change and fertilizer price change
    perc_diff_crops = perc_diff_land[perc_diff_land["LandLeaf"].isin(["crops"])]
    perc_diff_f_price = perc_diff_f_price[perc_diff_f_price["product"].isin(["N fertilizer"])]
    perc_diff_f_supply = perc_diff_f_supply[perc_diff_f_supply["product"].isin(["N fertilizer"])]
    correlation_f_price = pd.merge(perc_diff_crops, perc_diff_f_price, how="left", on=["GCAM", "SSP"],
                                   suffixes=("_left", "_right"))
    correlation_f_supply = pd.merge(perc_diff_crops, perc_diff_f_supply, how="left", on=["GCAM", "SSP"],
                                    suffixes=("_left", "_right"))
    years = c.GCAMConstants.plotting_x
    plotting.plot_correlation(correlation_f_price, years, ["SSP2"],
                              "% change in crop land use", "% change in fertilizer price", "lower left")
    plotting.plot_correlation(correlation_f_supply, years, ["SSP2"],
                              "% change in crop land use", "% change in fertilizer supply", "upper left")
    correlation_f = pd.merge(perc_diff_f_price, perc_diff_f_supply, how="left", on=["GCAM", "SSP"],
                             suffixes=("_left", "_right"))
    plotting.plot_correlation(correlation_f, years, ["SSP2"],
                              "% change in fertilizer price", "% change in fertilizer supply", "upper left")
    perc_diff_biomass = perc_diff_land[perc_diff_land["LandLeaf"].isin(["biomass"])]
    correlation_biomass_price = pd.merge(perc_diff_biomass, perc_diff_f_price, how="left", on=["GCAM", "SSP"],
                                         suffixes=("_left", "_right"))
    correlation_biomass_supply = pd.merge(perc_diff_biomass, perc_diff_f_supply, how="left", on=["GCAM", "SSP"],
                                          suffixes=("_left", "_right"))
    plotting.plot_correlation(correlation_biomass_price, years, ["SSP2"],
                              "% change in biomass land use", "% change in fertilizer price", "upper left")
    plotting.plot_correlation(correlation_biomass_supply, years, ["SSP2"],
                              "% change in biomass land use", "% change in fertilizer supply", "upper left")
    perc_diff_prod_biofuel = perc_diff_biofuels[perc_diff_biofuels["subsector"].isin(["biomass liquids"])]
    correlation_biomass_biofuel = pd.merge(perc_diff_prod_biofuel, perc_diff_biomass, how="left", on=["GCAM", "SSP"],
                                           suffixes=("_left", "_right"))
    correlation_biofuel_fertilizer = pd.merge(perc_diff_prod_biofuel, perc_diff_f_supply, how="left",
                                              on=["GCAM", "SSP"], suffixes=("_left", "_right"))
    years = [2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]
    plotting.plot_correlation(correlation_biomass_biofuel, years, ["SSP2"],
                              "% change in biofuel supply", "% change in biomass land use", "upper left")
    plotting.plot_correlation(correlation_biofuel_fertilizer, years, ["SSP2"],
                              "% change in biofuel supply", "% change in fertilizer supply", "upper left")

    # agricultural commodity price changes
    crops = ["Corn", "FiberCrop", "FodderGrass", "FodderHerb", "Forest", "Fruits", "Legumes", "MiscCrop", "NutSeeds",
             "OilCrop", "OtherGrain", "Pasture", "Rice", "RootTuber", "Soybean", "SugarCrop",
             "Vegetables", "Wheat", "biomass"]
    released_ag_prices = pd.read_csv("data/gcam_out/released/" + RCP + "/ag_commodity_prices.csv")
    pyrolysis_ag_prices = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/ag_commodity_prices.csv")
    perc_diff_ag_prices = data_manipulation.percent_difference(released_ag_prices, pyrolysis_ag_prices,
                                                               ["SSP", "sector", "GCAM"])
    #plotting.plot_world(perc_diff_ag_prices, crops, ["SSP2"], "year", "sector", [2020, 2035, 2050, 2075, 2100])
    biomass_price = perc_diff_ag_prices[perc_diff_ag_prices["sector"].isin(["biomass"])]
    correlation_biomass_price_supply = pd.merge(biomass_price, perc_diff_biomass, "left", on=["GCAM", "SSP"],
                                                suffixes=("_left", "_right"))
    plotting.plot_correlation(correlation_biomass_price_supply, c.GCAMConstants.plotting_x, ["SSP2"], "% change in biomass price", "% change in biomass supply", "upper left")

    # correlograms
    products = ["manure fuel feedstock", "beef manure", "dairy manure", "pork manure", "poultry manure", "goat manure"]
    price_price = pd.read_csv("data/gcam_out/price/" + RCP + "/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")
    price_price = price_price[price_price[['product']].isin(products).any(axis=1)]
    pyrolysis_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    price_price = data_manipulation.percentage_change_between_years(price_price)
    pyrolysis_price = data_manipulation.percentage_change_between_years(pyrolysis_price)
    cols = ["2020-2025", "2025-2030", "2030-2035", "2035-2040", "2040-2045", "2045-2050", "2050-2055", "2055-2060",
            "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090", "2090-2095", "2095-2100"]
    # cols = ["2040-2045", "2045-2050", "2050-2055", "2055-2060",
    #         "2060-2065", "2065-2070", "2070-2075", "2075-2080", "2080-2085", "2085-2090", "2090-2095", "2095-2100"]
    plotting.plot_correlogram(pyrolysis_price, c.GCAMConstants.SSPs, cols, [2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100])


def prices(nonBaselineScenario, RCP, SSP):
    # # carbon prices
    # released_CO2_price = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_prices.csv")
    # pyrolysis_CO2_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_prices.csv")
    # products = ["CO2"]
    # released_CO2_price = released_CO2_price[released_CO2_price[['product']].isin(products).any(axis=1)]
    # pyrolysis_CO2_price = pyrolysis_CO2_price[pyrolysis_CO2_price[['product']].isin(products).any(axis=1)]
    # perc_diff_CO2_price = data_manipulation.flat_difference(released_CO2_price, pyrolysis_CO2_price, ["SSP", "product", "GCAM"])
    # print("change in world carbon prices")
    # plotting.plot_world(perc_diff_CO2_price, products, SSP, "year", "product", c.GCAMConstants.plotting_x)
    #
    # # refined liquids prices
    # released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")
    # pyrolysis_price = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")
    # products = ["refined liquids enduse"]
    # released_refliquids_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    # pyrolysis_ref_liquids_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    # perc_diff_f_price = data_manipulation.percent_difference(released_refliquids_price, pyrolysis_ref_liquids_price,
    #                                                          ["SSP", "product", "GCAM"])
    # print("change in refined liquids price")
    # plotting.plot_world(perc_diff_f_price, products, SSP, "year", "product", c.GCAMConstants.plotting_x)
    #
    # # food prices
    # released_food_price = pd.read_csv("data/gcam_out/released/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    # pyrolysis_food_price = pd.read_csv(
    #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    # products = ["regional beef", "regional corn", "regional dairy", "regional fibercrop", "regional forest", "regional fruits", "regional iron and steel", "regional legumes", "regional misccrop", "regional nuts_seeds", "regional oilcrop", "regional oilpalm", "regional othergrain", "regional pork", "regional poultry", "regional rice", "regional root_tuber", "regional sheepgoat", "regional soybean", "regional sugarcrop", "regional vegetables", "regional wheat"]
    # for j in products:
    #     r_f = released_food_price[released_food_price[['sector']].isin([j]).any(axis=1)]
    #     p_f = pyrolysis_food_price[pyrolysis_food_price[['sector']].isin([j]).any(axis=1)]
    #     perc_diff_food_price = data_manipulation.percent_difference(r_f, p_f,
    #                                                              ["SSP", "sector", "GCAM"])
    #     print("change in", str(j), "price")
    #     plotting.plot_world(perc_diff_food_price, [j], SSP, "year", "sector", c.GCAMConstants.plotting_x)
    #
    # fertilizer prices
    released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")
    products = ["N fertilizer"]
    released_f_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    pyrolysis_f_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    perc_diff_f_price = data_manipulation.percent_difference(released_f_price, pyrolysis_f_price,
                                                             ["SSP", "product", "GCAM"])
    print("change in fertilizer price")
    # plotting.plot_world(perc_diff_f_price, products, SSP, "year", "product", c.GCAMConstants.plotting_x)

    # refined liquids prices
    "refined liquids enduse"
    products = ["refined liquids enduse"]
    released_refliq_price = released_price[released_price[['product']].isin(products).any(axis=1)]
    pyrolysis_refliq_price = pyrolysis_price[pyrolysis_price[['product']].isin(products).any(axis=1)]
    released_refliq_price = released_refliq_price[released_refliq_price[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_refliq_price = pyrolysis_refliq_price[pyrolysis_refliq_price[['SSP']].isin(SSP).any(axis=1)]
    perc_diff_refliq_price = data_manipulation.percent_difference(released_refliq_price, pyrolysis_refliq_price,
                                                             ["SSP", "product", "GCAM"])
    print("change in refined liquids price")
    # plotting.plot_world(perc_diff_refliq_price, products, SSP, "year", "product", c.GCAMConstants.plotting_x)

    # correlation between food and energy prices
    released_foo_price = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    pyrolysis_foo_price = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")

    for products in ["regional beef" , "regional dairy", "regional wheat"]:
        for energy in ["refined liquids enduse", "crude oil", "electricity", "natural gas"]:
            #get right energy source
            released_refliq_price = released_price[released_price[['product']].isin([energy]).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_price[pyrolysis_price[['product']].isin([energy]).any(axis=1)]
            released_refliq_price = released_refliq_price[released_refliq_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_refliq_price[pyrolysis_refliq_price[['SSP']].isin(SSP).any(axis=1)]
            stats.stationarity_test(released_refliq_price)
            print(len(released_refliq_price), len(pyrolysis_refliq_price))
            perc_diff_refliq_price = data_manipulation.percent_difference(released_refliq_price, pyrolysis_refliq_price, ["SSP", "product", "GCAM"])

            released_food_price = released_foo_price[released_foo_price[['sector']].isin([products]).any(axis=1)]
            pyrolysis_food_price = pyrolysis_foo_price[pyrolysis_foo_price[['sector']].isin([products]).any(axis=1)]
            released_food_price = released_food_price[released_food_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_food_price = pyrolysis_food_price[pyrolysis_food_price[['SSP']].isin(SSP).any(axis=1)]
            perc_diff_food = data_manipulation.percent_difference(released_food_price, pyrolysis_food_price, ["SSP", "sector", "GCAM"])
            correlation_food_energy_released = pd.merge(released_food_price, released_refliq_price, how="left",
                                                        on=["GCAM", "SSP"],
                                                        suffixes=("_left", "_right"))
            correlation_food_energy_pyrolysis = pd.merge(pyrolysis_food_price, pyrolysis_refliq_price, how="left",
                                                         on=["GCAM", "SSP"],
                                                         suffixes=("_left", "_right"))
            correlation_food_energy_diff = pd.merge(perc_diff_food, perc_diff_refliq_price, how="left",
                                                    on=["GCAM", "SSP"],
                                                    suffixes=("_left", "_right"))

            years = c.GCAMConstants.plotting_x
            print("correlation in released", products, "price and energy price")
            stats.plot_correlation(correlation_food_energy_released, years, SSP,
                                      "released " + str(products) + " price", "released " + energy + " price", "lower left")
            print("correlation in pyrolysis", products, "price and energy price")
            stats.plot_correlation(correlation_food_energy_pyrolysis, years, SSP,
                                      "pyrolysis " + str(products) + " price", "pyrolysis " + energy + " price", "upper left")
            print("correlation in change in", products, "price and " + energy + " price")
            stats.plot_correlation(correlation_food_energy_diff, years, SSP,
                                      "% change in " + str(products) + " price", "% change in " + energy + " price", "upper left")

            # correlation between land use and energy prices
            # released_land = pd.read_csv("data/gcam_out/released/" + RCP + "/aggregated_land_allocation.csv")
            # pyrolysis_land = pd.read_csv(
            #     "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/aggregated_land_allocation.csv")
            # land = ["crops"]
            # released_land = released_land[released_land[['LandLeaf']].isin(land).any(axis=1)]
            # pyrolysis_land = pyrolysis_land[pyrolysis_land[['LandLeaf']].isin(land).any(axis=1)]
            # perc_diff_land = data_manipulation.percent_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])
            # perc_diff_crops = perc_diff_land[perc_diff_land["LandLeaf"].isin(["crops"])]
            # correlation_food_energy_diff = pd.merge(perc_diff_crops, perc_diff_refliq_price, how="left",
            #                                         on=["GCAM", "SSP"],
            #                                         suffixes=("_left", "_right"))
            # years = c.GCAMConstants.plotting_x
            # print("correlation in change in land use and energy price")
            # plotting.plot_correlation(correlation_food_energy_diff, years, SSP,
            #                           "% change in " + str(land) + " use", "% change in " + energy + " price", "upper left")
            #
            # # correlation between ag input and output prices
            # correlation_ag_food_diff = pd.merge(perc_diff_food, perc_diff_land, how="left",
            #                                         on=["GCAM", "SSP"],
            #                                         suffixes=("_left", "_right"))
            # print("correlation in difference", products, "price and land use")
            # plotting.plot_correlation(correlation_ag_food_diff, years, SSP,
            #                           "% change in " + str(products) + " price", "% change in " + str(land) + " use", "upper left")


def carbon_prices(nonBaselineScenario, RCP, SSP):
    released_CO2_price = pd.read_csv("data/gcam_out/released/" + RCP + "/CO2_prices.csv")
    pyrolysis_CO2_price = pd.read_csv("data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/CO2_prices.csv")
    products = ["CO2"]
    released_CO2_price = released_CO2_price[released_CO2_price[['product']].isin(products).any(axis=1)]
    pyrolysis_CO2_price = pyrolysis_CO2_price[pyrolysis_CO2_price[['product']].isin(products).any(axis=1)]
    flat_diff_CO2_price = data_manipulation.flat_difference(released_CO2_price, pyrolysis_CO2_price, ["SSP", "product", "GCAM"])

    released_foo_price = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    pyrolysis_foo_price = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")

    for products in ["regional beef", "regional dairy", "regional corn", "regional wheat"]:
        released_food_price = released_foo_price[released_foo_price[['sector']].isin([products]).any(axis=1)]
        pyrolysis_food_price = pyrolysis_foo_price[pyrolysis_foo_price[['sector']].isin([products]).any(axis=1)]
        released_food_price = released_food_price[released_food_price[['SSP']].isin(SSP).any(axis=1)]
        pyrolysis_food_price = pyrolysis_food_price[pyrolysis_food_price[['SSP']].isin(SSP).any(axis=1)]
        perc_diff_food = data_manipulation.percent_difference(released_food_price, pyrolysis_food_price, ["SSP", "sector", "GCAM"])

        #test for stationarity
        print("released food price")
        stats.stationarity_test(released_food_price)
        print("pyrolysis food price")
        stats.stationarity_test(pyrolysis_food_price)
        print("released CO2 price")
        stats.stationarity_test(released_CO2_price)
        print("pyrolysis CO2 price")
        stats.stationarity_test(pyrolysis_CO2_price)

        correlation_food_energy_released = pd.merge(released_food_price, released_CO2_price, how="left",
                                                    on=["GCAM", "SSP"],
                                                    suffixes=("_left", "_right"))
        correlation_food_energy_pyrolysis = pd.merge(pyrolysis_food_price, pyrolysis_CO2_price, how="left",
                                                     on=["GCAM", "SSP"],
                                                     suffixes=("_left", "_right"))
        correlation_food_energy_diff = pd.merge(perc_diff_food, flat_diff_CO2_price, how="left",
                                                on=["GCAM", "SSP"],
                                                suffixes=("_left", "_right"))

        years = c.GCAMConstants.plotting_x
        print("correlation in released", products, "price and energy price")
        stats.plot_correlation(correlation_food_energy_released, years, SSP,
                                  "released " + str(products) + " price", "released CO2 price", "lower left")
        print("correlation in pyrolysis", products, "price and energy price")
        stats.plot_correlation(correlation_food_energy_pyrolysis, years, SSP,
                                  "pyrolysis " + str(products) + " price", "pyrolysis CO2 price", "upper left")
        print("correlation in change in", products, "price and CO2 price")
        stats.plot_correlation(correlation_food_energy_diff, years, SSP,
                                  "% change in " + str(products) + " price", "change in CO2 price", "upper left")

def price_correlation(nonBaselineScenario, RCP, SSP):
    released_price = pd.read_csv("data/gcam_out/released/" + RCP + "/prices_of_all_markets.csv")
    pyrolysis_price = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/prices_of_all_markets.csv")

    # correlation between food and energy prices
    released_foo_price = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")
    pyrolysis_foo_price = pd.read_csv(
        "data/gcam_out/" + str(
            nonBaselineScenario) + "/" + RCP + "/ag_regional_prices_weighted_average_between_domestic_and_imported_prices.csv")

    for products in ["regional beef" , "regional dairy", "regional wheat"]:
        for energy in ["refined liquids enduse", "crude oil", "electricity", "natural gas"]:
            #get right energy source
            released_refliq_price = released_price[released_price[['product']].isin([energy]).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_price[pyrolysis_price[['product']].isin([energy]).any(axis=1)]
            released_refliq_price = released_refliq_price[released_refliq_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_refliq_price = pyrolysis_refliq_price[pyrolysis_refliq_price[['SSP']].isin(SSP).any(axis=1)]

            # get right food sources
            released_food_price = released_foo_price[released_foo_price[['sector']].isin([products]).any(axis=1)]
            pyrolysis_food_price = pyrolysis_foo_price[pyrolysis_foo_price[['sector']].isin([products]).any(axis=1)]
            released_food_price = released_food_price[released_food_price[['SSP']].isin(SSP).any(axis=1)]
            pyrolysis_food_price = pyrolysis_food_price[pyrolysis_food_price[['SSP']].isin(SSP).any(axis=1)]

            # test for stationarity
            print("released", products, "price")
            stats.stationarity_test(released_food_price)
            print("pyrolysis", products, "price")
            stats.stationarity_test(pyrolysis_food_price)
            print("released", energy, "price")
            stats.stationarity_test(released_refliq_price)
            print("pyrolysis", energy, "price")
            stats.stationarity_test(pyrolysis_refliq_price)

            print("released", products, "price as dependent on", energy, "price")
            released_res = stats.plot_eq4_correlation(released_refliq_price, released_food_price, SSP)

            print("pyrolysis", products, "price as dependent on", energy, "price")
            pyrolysis_res = stats.plot_eq4_correlation(pyrolysis_refliq_price, pyrolysis_food_price,SSP)
            stats.plot_price_coefficients(pyrolysis_res, released_res, "price coefficients for " + products + " and " + energy)


if __name__ == '__main__':
    # standard_plots("pyrolysis", "4p5")
    for i in ["SSP1", "SSP2"]:
        #prices("pyrolysis", "4p5", [i])
        print(i)
        price_correlation("pyrolysis", "4p5", [i])
