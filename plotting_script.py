import plotting
import data_manipulation
import constants as c
import pandas as pd


def figure2(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 2
    :return: N/A
    """
    # read in biochar application rates, and get the 2050 application rates
    biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level.csv")

    # add extra data to dataframe to help downstream code
    biochar_app_rate['2050'] = biochar_app_rate['kg_bio_ha']
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['Units'] = 'kg biochar/ha/yr'
    biochar_app_rate["SSP"] = SSP[0]

    # extract information on crops
    biochar_app_rate['technology'] = biochar_app_rate['GCAM_commodity']
    biochar_app_rate['technology'] = biochar_app_rate.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)
    crops = biochar_app_rate["technology"].unique()

    # plot the data
    plotting.plot_world(biochar_app_rate, crops, SSP, "product", "technology", ["2050"],
                        "nutrient-limited biochar application rate")

    # plot histogram of crop/region price combinations
    plotting.plot_regional_hist_avg(biochar_app_rate, "2050", [SSP], "region-basin-crop-irr combination count",
                                    "histogram of biochar app rates", "technology", "na")

    # remove outliers for plotting purposes
    outlier_cutoff = 6000 # kg/ha/yr
    biochar_app_rate_no_outlier = biochar_app_rate[biochar_app_rate['2050'] < outlier_cutoff]
    plotting.plot_regional_hist_avg(biochar_app_rate_no_outlier, "2050", [SSP], "region-basin-crop-irr combination count",
                                    "histogram of outlier " + str(outlier_cutoff) + "kg per ha removed biochar app rates", "technology", "na")

    outlier_cutoff = 2000 # kg/ha/yr
    biochar_app_rate_no_outlier = biochar_app_rate[biochar_app_rate['2050'] < outlier_cutoff]
    plotting.plot_regional_hist_avg(biochar_app_rate_no_outlier, "2050", [SSP], "region-basin-crop-irr combination count",
                                    "histogram of outlier " + str(outlier_cutoff) + "kg per ha removed biochar app rates", "technology", "na")

    # global fertilizer reduction
    released_N = data_manipulation.get_sensitivity_data([["released"]], "ammonia_production_by_tech", SSP, RCP=RCP, source="original")
    pyrolysis_N = data_manipulation.get_sensitivity_data(nonBaselineScenario, "ammonia_production_by_tech", SSP, RCP=RCP, source="masked")
    released_N = data_manipulation.group(released_N, ["SSP"])  # get global level data
    pyrolysis_N = data_manipulation.group(pyrolysis_N, ["SSP"])  # get global level data

    flat_diff_land = data_manipulation.flat_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    perc_diff_land = data_manipulation.percent_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    print(flat_diff_land[["2050", "SSP", "Units"]])
    print(perc_diff_land[["2050", "SSP", "Units"]])


def figure3(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 4
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathway being considered
    :param SSP: the SSP pathway being considered
    :param biochar_year: the year being analyzed in detail
    :return: N/A
    """
    # biochar cropland application changes
    land_use = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP, source="masked")
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
    land_for_alluvial = data_manipulation.process_luc(land_use, scale_factor)

    # build a alluvial plot
    land_for_alluvial[["2050", "Management_2050", "Region_2050"]] = land_for_alluvial['2050'].str.split("_",
                                                                                                        expand=True)
    land_for_alluvial[["2020", "Management_2020", "Region_2020"]] = land_for_alluvial['2020'].str.split("_",
                                                                                                        expand=True)
    counts = land_for_alluvial["Management_2050"].value_counts() / scale_factor * 1000
    print(counts)
    # Region_2050 data is stored in Region
    land_for_alluvial["Region"] = land_for_alluvial.apply(lambda row: data_manipulation.relabel_region_alluvial(row),
                                                          axis=1)
    land_for_alluvial["Management"] = land_for_alluvial.apply(
        lambda row: data_manipulation.relabel_management_alluvial(row, counts), axis=1)
    land_for_alluvial = land_for_alluvial.sort_values(by=['Management', "Region"], ascending=[True, True])

    # get percentage of land with different management types on a regional basis
    print("land management type, region, value, unit")
    for usage in land_for_alluvial["Management"].unique():
        for gcam in land_for_alluvial["Region"].unique():
            regional = land_for_alluvial[land_for_alluvial[['Region']].isin([gcam]).any(axis=1)]
            print(str(usage) + ", " + str(gcam) + " ," +
                  str(len(regional[regional["Management"] == usage]) / len(regional) * 100) + ",%")
    plotting.plot_alluvial(land_for_alluvial)

    # regional land use change
    released_land = data_manipulation.get_sensitivity_data(["released"], "detailed_land_allocation", SSP, RCP=RCP, source="original")
    pyrolysis_land = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP, source="masked")
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),axis=1)
    pyrolysis_land["LandLeaf"] = pyrolysis_land.apply(lambda row: data_manipulation.relabel_detailed_land_use(row),
                                                      axis=1)
    pyrolysis_land = data_manipulation.group(pyrolysis_land, ["GCAM", "LandLeaf"])
    released_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf"])
    flat_diff_land = data_manipulation.flat_difference(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    flat_diff_land["Units"] = "thousand km$^2$"

    global_land = data_manipulation.group(flat_diff_land, ["LandLeaf"])
    flat_diff_land = data_manipulation.group(flat_diff_land, ["GCAM", "LandLeaf"])
    print("plot regional land use change in " + str(biochar_year))

    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "land use change by region in " + str(biochar_year))
    print("plotting global land use change across all years")
    print(global_land.loc[:, ["2050", "LandLeaf", "Units"]])

    plotting.plot_stacked_bar_product(global_land, c.GCAMConstants.biochar_x, SSP, "LandLeaf",
                                      "global land use change by year")

    flat_diff_land = data_manipulation.percent_of_total(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"])

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "land use change by region in " + str(biochar_year))


def figure4(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 3
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: graph of biochar C sequestration, biochar C emissions avoidance, and biochar prices
    """
    # plotting changes in energy mix
    ref_released = data_manipulation.get_sensitivity_data(["released"], "primary_energy_consumption_by_region_direct_equivalent", SSP, RCP=RCP, source="original")
    ref_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario, "primary_energy_consumption_by_region_direct_equivalent", SSP, RCP=RCP, source="masked")

    # get the right SSP data
    ref_released["SSP"] = "released"
    ref_pyrolysis["SSP"] = "pyrolysis"

    # get the flat difference and plot it
    flat_diff = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["fuel"])
    print(flat_diff[[biochar_year, "fuel", "Units"]])
    perc_diff = data_manipulation.percent_difference(ref_released, ref_pyrolysis, ["fuel"])
    print(perc_diff[[biochar_year, "fuel", "Units"]])

    # plotting CO2 sequestering
    co2_seq_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario, "CO2_emissions_by_tech_excluding_resource_production", SSP, RCP=RCP, source="masked")
    co2_seq_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    co2_seq_pyrolysis['technology'] = co2_seq_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                              axis=1)
    co2_seq_pyrolysis['Units'] = "Mt C Sequestered/yr"
    products = ["beef biochar", "dairy biochar", "pork biochar", "poultry biochar", "goat biochar"]
    co2_seq_pyrolysis = co2_seq_pyrolysis[co2_seq_pyrolysis['technology'].str.contains("|".join(products))]

    # carbon sequestration is portrayed as a negative in GCAM, but measured as a positive in this study
    for i in c.GCAMConstants.biochar_x:
        co2_seq_pyrolysis[str(i)] = co2_seq_pyrolysis[str(i)] * -1

    plotting.plot_line_product_CI(co2_seq_pyrolysis, products, "technology", SSP[0], "Version",
                                  title="C sequestration from biochar in " + SSP[0] + " baseline in RCP" + str(RCP))

    # print values of Mt C sequestered
    print("sequestered C\n", co2_seq_pyrolysis.loc[:, [biochar_year, "SSP", "technology", "Units"]])

    # plotting ghg emissions avoidance
    # TODO: update to include avoided N2O emissions
    # TODO: update to report values in Mt CO2-eq
    co2_avd_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario, "nonCO2_emissions_by_tech_excluding_resource_production", SSP, RCP=RCP, source="masked")
    co2_avd_pyrolysis = data_manipulation.group(co2_avd_pyrolysis, ["technology", "SSP"])
    co2_avd_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    co2_avd_pyrolysis['technology'] = co2_avd_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                              axis=1)
    co2_avd_pyrolysis = co2_avd_pyrolysis[co2_avd_pyrolysis['technology'].str.contains("|".join(products))]
    co2_avd_pyrolysis[
        'Units'] = "Mt CH4 Avoided/yr"  # assuming a GWP of 27.2 (IPCC AR6), same GWP used in biochar CH4 avoidance spreadsheet calcs
    # carbon avoidance is portrayed as a negative in GCAM, but measured as a positive in this study
    for i in c.GCAMConstants.biochar_x:
        co2_avd_pyrolysis[str(i)] = co2_avd_pyrolysis[str(i)] * -1
    plotting.plot_line_product_CI(co2_avd_pyrolysis, products, "technology", SSP[0], "Version",
                                  title="carbon emissions avoidance across RCP pathways in " + SSP[0] + " baseline in RCP" + str(
                                      RCP))
    # print values of Mt C avoided
    print("avoided C\n", co2_avd_pyrolysis.loc[:, [biochar_year, "SSP", "technology", "Units"]])

    # print values of biochar supply
    biochar_supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP,RCP=RCP, source="masked")
    biochar_supply = biochar_supply[biochar_supply[['product']].isin(["biochar"]).any(axis=1)]
    biochar_supply = data_manipulation.group(biochar_supply, ["product"])
    print(biochar_supply.loc[:, [biochar_year, "Units"]])

    # frequency of biochar prices
    biochar_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP,RCP=RCP, source="masked")
    biochar_price['product'] = biochar_price.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    biochar_price = biochar_price[biochar_price[['product']].isin(["biochar"]).any(axis=1)]
    biochar_price = biochar_price.melt(["GCAM", "product"], [str(i) for i in c.GCAMConstants.biochar_x])
    biochar_price['2024_value'] = biochar_price['value'] / .17 * 1000  # converting from 1975 to 2024 dollars
    biochar_price["Units"] = "USD$2024/ton"
    plotting.plot_regional_hist_avg(biochar_price, '2024_value', SSP, "count region/year combinations",
                                    "histogram of price of biochar", "variable", supply="na")

    # further analysis on regions with biochar prices <$0
    subzero_biochar_price = biochar_price[biochar_price['2024_value'] < 0]

    # further analysis on regions with biochar prices >$400
    huge_biochar_price = biochar_price[biochar_price['2024_value'] > 400]
    print(subzero_biochar_price)
    print(huge_biochar_price[["GCAM", "variable", "2024_value", "Units"]])

    # print out differences in carbon prices
    for year in c.GCAMConstants.biochar_x:
        c_pyro_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "CO2_prices", SSP,RCP=RCP, source="masked")
        c_rel_price = data_manipulation.get_sensitivity_data(["released"], "CO2_prices", SSP,RCP=RCP, source="original")
        c_pyro_price = c_pyro_price.drop_duplicates()
        c_rel_price = c_rel_price.drop_duplicates()
        product = ["CO2"]
        c_rel_price = c_rel_price[c_rel_price[['product']].isin(product).any(axis=1)]
        c_pyro_price = c_pyro_price[c_pyro_price[['product']].isin(product).any(axis=1)]
        flat_diff_c_price = data_manipulation.flat_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
        flat_diff_c_price[str(year) + "_conv"] = flat_diff_c_price[
                                                     str(year)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
        flat_diff_c_price["Units"] = "USD$2024/t C"
        unique_c_price = flat_diff_c_price[[str(year) + "_conv", "SSP", "Units"]].drop_duplicates()
        print("flat difference between C prices in year " + str(year))
        print(unique_c_price)
        perc_diff_c_price = data_manipulation.percent_difference(c_pyro_price, c_rel_price, ["SSP", "GCAM"])
        perc_diff_c_price[str(year) + "_conv"] = perc_diff_c_price[
                                                     str(year)] * 2.42  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=199001&year2=202401
        flat_diff_c_price["Units"] = "%"
        unique_c_price = perc_diff_c_price[[str(year) + "_conv", "SSP", "Units"]].drop_duplicates()
        print("percent difference between C prices in year " + str(year))
        print(unique_c_price)


def figure5(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 5
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    # calculate food accessibility and undernourishment
    released_caloric_consumption = data_manipulation.get_sensitivity_data(["released"], "food_demand_per_capita", SSP,RCP=RCP, source="original")
    pyrolysis_caloric_consumption = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_per_capita", SSP,RCP=RCP, source="masked")
    released_caloric_consumption = data_manipulation.group(released_caloric_consumption, ["SSP", "GCAM"])
    pyrolysis_caloric_consumption = data_manipulation.group(pyrolysis_caloric_consumption, ["SSP", "GCAM"])

    # regional averaged food consumption by food type
    # convert Pcal to kcal/capita/day
    # get population data
    released_pop = data_manipulation.get_sensitivity_data(["released"], "population_by_region", SSP,RCP=RCP, source="original")
    pyrolysis_pop = data_manipulation.get_sensitivity_data(nonBaselineScenario, "population_by_region", SSP,RCP=RCP, source="masked")
    released_Pcal = data_manipulation.get_sensitivity_data(["released"], "food_consumption_by_type_specific", SSP,RCP=RCP, source="original")
    pyrolysis_Pcal = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_consumption_by_type_specific", SSP,RCP=RCP, source="masked")

    # relabel data to make it more human readable
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

    released_Pcal = data_manipulation.group(released_Pcal, ["GCAM", "SSP", "technology"])
    pyrolysis_Pcal = data_manipulation.group(pyrolysis_Pcal, ["GCAM", "SSP", "technology"])

    # calculate food accessibility
    # get food prices
    released_staple_expenditure = data_manipulation.get_sensitivity_data(["released"], "food_demand_prices", SSP,RCP=RCP, source="original")
    pyrolysis_staple_expenditure = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_prices", SSP,RCP=RCP, source="masked")
    released_staple_expenditure = released_staple_expenditure[
        released_staple_expenditure[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]
    pyrolysis_staple_expenditure = pyrolysis_staple_expenditure[
        pyrolysis_staple_expenditure[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]

    # get food consumption
    released_staple_consumption = data_manipulation.get_sensitivity_data(["released"], "food_demand_per_capita", SSP,RCP=RCP, source="original")
    pyrolysis_staple_consumption = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_per_capita", SSP,RCP=RCP, source="masked")
    released_staple_consumption = released_staple_consumption[
        released_staple_consumption[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]
    pyrolysis_staple_consumption = pyrolysis_staple_consumption[
        pyrolysis_staple_consumption[['input']].isin(["FoodDemand_Staples"]).any(axis=1)]

    # get GDP per capita
    released_GDP_capita = data_manipulation.get_sensitivity_data(nonBaselineScenario, "GDP_per_capita_PPP_by_region", SSP, RCP=RCP, source="original")
    pyrolysis_GDP_capita = data_manipulation.get_sensitivity_data(nonBaselineScenario, "GDP_per_capita_PPP_by_region", SSP, RCP=RCP, source="masked")

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
    plotting.plot_world(perc_diff_FA, ["%"], SSP, "year", "Units", ["2050"], "Food Accessibility")

    # calculate pcal per capita
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
    released_staple_expenditure = data_manipulation.get_sensitivity_data(["released"], "food_demand_prices", SSP, RCP=RCP, source="original")
    pyrolysis_staple_expenditure = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_prices", SSP, RCP=RCP, source="masked")
    diff_food_staple_income = data_manipulation.flat_difference(pyrolysis_staple_expenditure,
                                                                released_staple_expenditure,
                                                                ["SSP", "GCAM", "input"])

    diff_food_staple_income['GCAM'] = diff_food_staple_income.apply(lambda row: data_manipulation.relabel_region(row),
                                                                    axis=1)
    diff_food_staple_income['input'] = diff_food_staple_income.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)
    diff_food_staple_income[
        "2050_conv"] = diff_food_staple_income[
                           "2050"] * 1.62  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=200501&year2=202401

    diff_food_staple_income = diff_food_staple_income.sort_values(by="2050_conv", ascending=False)
    diff_food_staple_income["Units"] = "2024 USD$/Mcal/day"

    print(diff_food_staple_income.groupby("input")["2050_conv"].mean(), SSP[0],
          diff_food_staple_income["Units"].unique()[0])

    # calculate global average percent difference
    perc_diff = data_manipulation.percent_difference(pyrolysis_staple_expenditure,
                                                     released_staple_expenditure,
                                                     ["SSP", "GCAM", "input"])

    perc_diff['GCAM'] = perc_diff.apply(lambda row: data_manipulation.relabel_region(row),
                                        axis=1)
    perc_diff['input'] = perc_diff.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)
    perc_diff["2050_conv"] = perc_diff[
                                 "2050"] * 1.62  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=200501&year2=202401

    perc_diff = perc_diff.sort_values(by="2050_conv", ascending=False)
    perc_diff["Units"] = "%"

    print(perc_diff.groupby("input")["2050_conv"].mean(), SSP[0], perc_diff["Units"].unique()[0])

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
    plotting.plot_regional_rose(diff_food_staple_income, "2050_conv", SSP,
                                "change in food expenditure (USD$2024/Mcal/day)",
                                "food expenditure in 2050 in " + str(SSP[0]) + " and RCP " + str(RCP),
                                column="input")


def cue_figure(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for potential figure in the CUE conference paper
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: N/A
    """
    #TODO: get working
    for i in RCP:
        # Changes in energy mix
        # refined liquids production
        ref_released = data_manipulation.get_sensitivity_data(["released"], "refined_liquids_production_by_tech", SSP, RCP=RCP, source="original")
        ref_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario, "refined_liquids_production_by_tech", SSP, RCP=RCP, source="masked")

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
        baseline_data["technology"] = baseline_data.apply(lambda row: data_manipulation.relabel_food(row, "technology"),
                                                          axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0
        flat_diff_biofuel = pd.concat([flat_diff_biofuel, baseline_data])

        baseline_data = perc_diff_biofuel.copy(deep=True)
        baseline_data = baseline_data[baseline_data[['SSP']].isin(["SSP1"]).any(axis=1)]
        baseline_data["technology"] = baseline_data.apply(lambda row: data_manipulation.relabel_food(row, "technology"),
                                                          axis=1)
        baseline_data["SSP"] = "released"
        for j in c.GCAMConstants.x:
            baseline_data[str(j)] = 0
        perc_diff_biofuel = pd.concat([perc_diff_biofuel, baseline_data])

        # plot products
        plotting.sensitivity(flat_diff_biofuel, str(i), ["released"], "2050", "technology")
        plotting.sensitivity(perc_diff_biofuel, str(i), ["released"], "2050", "technology")


def main():
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    reference_SSP = ["SSP1"] # the first SSP in the list is assumed to be the baseline
    reference_RCP = "6p0"
    other_scenario = ["test"]  # biochar
    biochar_year = "2050"
    #figure2(other_scenario, reference_RCP, reference_SSP)
    #figure3(other_scenario, reference_RCP, reference_SSP, biochar_year)
    figure4(other_scenario, reference_RCP, reference_SSP, biochar_year)
    figure5(other_scenario, reference_RCP, reference_SSP)
    cue_figure(other_scenario, reference_RCP, reference_SSP)


if __name__ == '__main__':
    main()
