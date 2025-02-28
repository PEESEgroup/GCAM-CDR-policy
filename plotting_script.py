import plotting
import data_manipulation
import constants as c
import pandas as pd
import numpy as np

def figure2(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 2
    :return: N/A
    """
    # read in biochar application rates, and get the application rates
    biochar_app_rate = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level.csv")

    # add extra data to dataframe to help downstream code
    biochar_app_rate[biochar_year] = biochar_app_rate['kg_bio_ha']
    biochar_app_rate['GCAM'] = biochar_app_rate['region']
    biochar_app_rate['Units'] = 'kg biochar/ha/yr'
    biochar_app_rate["SSP"] = SSP[0]

    # extract information on crops
    biochar_app_rate['technology'] = biochar_app_rate['GCAM_commodity']
    biochar_app_rate['technology'] = biochar_app_rate.apply(
        lambda row: data_manipulation.relabel_food(row, "technology"), axis=1)

    # plot histogram of crop/region price combinations
    plotting.plot_regional_hist_avg(biochar_app_rate, biochar_year, [SSP], "region-basin-crop-irr combination count",
                                    "histogram of biochar app rates in " + biochar_year, "technology", "na", RCP,
                                    nonBaselineScenario)

    # remove outliers for plotting purposes
    outlier_cutoff = 6000  # kg/ha/yr
    biochar_app_rate_no_outlier = biochar_app_rate[biochar_app_rate[biochar_year] < outlier_cutoff]
    plotting.plot_regional_hist_avg(biochar_app_rate_no_outlier, biochar_year, [SSP],
                                    "region-basin-crop-irr combination count",
                                    "histogram of outlier " + str(
                                        outlier_cutoff) + "kg per ha removed biochar app rates", "technology", "na",
                                    RCP, nonBaselineScenario)

    outlier_cutoff = 3000  # kg/ha/yr
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
    released_N = data_manipulation.group(released_N, ["SSP"])  # get global level data
    pyrolysis_N = data_manipulation.group(pyrolysis_N, ["SSP"])  # get global level data

    flat_diff_land = data_manipulation.flat_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    perc_diff_land = data_manipulation.percent_difference(released_N, pyrolysis_N, ["SSP", "LandLeaf", "GCAM"])
    data_manipulation.drop_missing(flat_diff_land).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/change_in_N.csv")
    data_manipulation.drop_missing(perc_diff_land).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/percent_difference_in_N.csv")


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
    land_use = data_manipulation.get_sensitivity_data(nonBaselineScenario, "detailed_land_allocation", SSP, RCP=RCP,
                                                      source="masked")
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
                                                                   regional) * 100) + ",%\n")
    plotting.plot_alluvial(land_for_alluvial, biochar_year, base_year)
    # write out .csv data for different land management types
    with open("data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
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
    flat_diff_land["Units"] = "thousand km$^2$"
    global_land = data_manipulation.group(flat_diff_land, ["LandLeaf", "Version"])
    flat_diff_land = data_manipulation.group(flat_diff_land, ["GCAM", "LandLeaf", "Version"])

    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "land use change by region in " + str(biochar_year), RCP, nonBaselineScenario)
    data_manipulation.drop_missing(global_land).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/global_LUC.csv")

    plotting.plot_stacked_bar_product(global_land, c.GCAMConstants.biochar_x, SSP, "LandLeaf",
                                      "global land use change by year", RCP, nonBaselineScenario)

    flat_diff_land = data_manipulation.percent_of_total(released_land, pyrolysis_land, ["SSP", "LandLeaf", "GCAM"],
                                                        biochar_year)

    flat_diff_land['GCAM'] = flat_diff_land.apply(lambda row: data_manipulation.relabel_region(row), axis=1)
    flat_diff_land["LandLeaf"] = flat_diff_land.apply(lambda row: data_manipulation.relabel_land_use(row), axis=1)
    plotting.plot_stacked_bar_product(flat_diff_land, str(biochar_year), SSP, "LandLeaf",
                                      "land use change by region in " + str(biochar_year), RCP, nonBaselineScenario)


def figure4(nonBaselineScenario, RCP, SSP):
    """
    Returns plots for figure 3
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :return: graph of biochar C sequestration, biochar C emissions avoidance, and biochar prices
    """
    # plotting changes in energy mix
    ref_released = data_manipulation.get_sensitivity_data(["released"],
                                                          "primary_energy_consumption_by_region_direct_equivalent", SSP,
                                                          RCP=RCP, source="original")
    ref_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                           "primary_energy_consumption_by_region_direct_equivalent",
                                                           SSP, RCP=RCP, source="masked")

    # get the right SSP data
    ref_released["SSP"] = "released"
    ref_pyrolysis["SSP"] = "pyrolysis"

    # get the flat difference and plot it
    flat_diff = data_manipulation.flat_difference(ref_released, ref_pyrolysis, ["fuel"])
    data_manipulation.drop_missing(flat_diff).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/change_in_primary_energy_consumption.csv")
    perc_diff = data_manipulation.percent_difference(ref_released, ref_pyrolysis, ["fuel"])
    data_manipulation.drop_missing(perc_diff).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/percent_difference_primary_energy_consumption.csv")

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

    #output non-grouped GHG impacts
    data_manipulation.drop_missing(co2_seq_pyrolysis).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/biochar_c_sequestration.csv")
    data_manipulation.drop_missing(co2_avd_pyrolysis).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/biochar_c_avoidance.csv")

    # group data for plotting
    co2_seq_pyrolysis = data_manipulation.group(co2_seq_pyrolysis, ["SSP", "Version"])
    co2_avd_pyrolysis = data_manipulation.group(co2_avd_pyrolysis, ["SSP", "Version"])

    # avoided agricultural emissions from lands managed with biochar
    ghg_er = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                    "nonCO2_emissions_by_tech_excluding_resource_production",
                                                    SSP, RCP=RCP, source="masked")

    ag_avd_n2o_land = ghg_er[ghg_er['technology'].str.contains("biochar")]  # get only biochar lut
    ag_avd_ch4_land = ghg_er[ghg_er['technology'].str.contains("biochar")]
    ag_avd_n2o_land = ag_avd_n2o_land[ag_avd_n2o_land[['GHG']].isin(["N2O_AGR"]).any(axis=1)]  # select specific ghg
    ag_avd_ch4_land = ag_avd_ch4_land[ag_avd_ch4_land[['GHG']].isin(["CH4_AGR"]).any(axis=1)]
    ag_avd_n2o_land = data_manipulation.group(ag_avd_n2o_land,
                                              ["Version", "GHG"])  # group all biochar land leafs by version
    ag_avd_ch4_land = data_manipulation.group(ag_avd_ch4_land, ["Version", "GHG"])
    for i in c.GCAMConstants.future_x:
        ag_avd_n2o_land[str(i)] = ag_avd_n2o_land.apply(
            lambda row: data_manipulation.avd_soil_emissions(row, "GHG", str(i)), axis=1)
        ag_avd_ch4_land[str(i)] = ag_avd_ch4_land.apply(
            lambda row: data_manipulation.avd_soil_emissions(row, "GHG", str(i)), axis=1)
    ag_avd_n2o_land["Units"] = "Avoided cropland N$_2$O"
    ag_avd_ch4_land["Units"] = "Avoided cropland CH$_4$"

    # avoided CH4 and N2O emissions from avoided biomass decomposition
    biochar_ghg_er = ghg_er[ghg_er['technology'].str.contains("biochar")].copy(deep=True)
    biochar_ghg_er['technology'] = biochar_ghg_er.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                        axis=1)
    biochar_ghg_er = biochar_ghg_er[biochar_ghg_er['technology'].str.contains("|".join(products))]  # removes LUT
    biochar_ghg_er = data_manipulation.group(biochar_ghg_er, ["technology", "SSP", "Version", "GHG"])

    biochar_ghg_er["Units"] = biochar_ghg_er.apply(lambda row: "Avoided biomass decomposition N$_2$O" if row["GHG"] == "N2O" else "Avoided biomass decomposition CH$_4$", axis=1)

    # convert using GWP values
    for i in c.GCAMConstants.future_x:
        biochar_ghg_er[str(i)] = biochar_ghg_er.apply(
            lambda row: data_manipulation.ghg_ER(row, "GHG", str(i)), axis=1)

    # print ungrouped data
    data_manipulation.drop_missing(biochar_ghg_er).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/biochar_ghg_avoided_decomposition.csv")

    # group data for final plotting
    biochar_ghg_er = data_manipulation.group(biochar_ghg_er, ["SSP", "Version", "GHG"])

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

    # combine all direct sources of GHG emissions changes into a single df/graph
    biochar_ghg_emissions = pd.concat([biochar_ghg_er, co2_seq_pyrolysis, co2_avd_pyrolysis, ag_avd_n2o_land, ag_avd_ch4_land, flat_diff_luc])

    # calculate net CO2 impact
    df_sum = biochar_ghg_emissions.sum(axis=0)
    df_sum["Units"] = "Net Emissions Impact" # this unit is used to label the graph
    df_sum["SSP"] = ag_avd_ch4_land["SSP"].unique()[0]
    df_sum = pd.DataFrame(df_sum, columns=['Total']).T
    biochar_ghg_emissions = pd.concat([biochar_ghg_emissions, df_sum])
    biochar_ghg_emissions["GHG_ER_type"] = biochar_ghg_emissions["Units"]
    biochar_ghg_emissions["Units"] = "Mt CO$_2$-eq/yr"

    # plotting ghg emissions avoidance
    plotting.plot_line_by_product(biochar_ghg_emissions, biochar_ghg_emissions["Units"].unique(), "GHG_ER_type", [SSP[0]], "SSP",
                                  "ghg emissions changes in " + SSP[0], RCP, nonBaselineScenario)

    # output values of avoided and sequestered ghg emissions from biochar
    data_manipulation.drop_missing(biochar_ghg_emissions).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/biochar_direct_ghg_emissions.csv")

    # output values of biochar supply
    supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP, RCP=RCP,
                                                            source="masked")
    biochar_supply = supply[supply[['product']].isin(["biochar"]).any(axis=1)].copy(deep=True)
    biochar_supply = data_manipulation.group(biochar_supply, ["product", "Version"])

    manure_supply = supply[supply[['product']].isin(["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]).any(axis=1)].copy(deep=True)
    manure_supply = data_manipulation.group(manure_supply, ["product", "Version"])

    # calculate "LCA" impacts of biochar by mass biochar and global mass feedstock mix
    total_biochar = data_manipulation.group(biochar_supply, ["SSP"])
    total_manure = data_manipulation.group(manure_supply, ["SSP"])
    LCA_biochar = pd.merge(df_sum, total_biochar, on="SSP", suffixes=("", "_kg biochar"))
    LCA_manure = pd.merge(df_sum, total_manure, on="SSP", suffixes=("", "_kg biochar"))
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

    data_manipulation.drop_missing(LCA).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/biochar_manure_supply_GWP_kg_FU.csv")

    # frequency of biochar prices
    biochar_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP, RCP=RCP,
                                                           source="masked")
    biochar_price['product'] = biochar_price.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    biochar_price = biochar_price[biochar_price[['product']].isin(["biochar"]).any(axis=1)]
    biochar_price = biochar_price.melt(["GCAM", "product"], [str(i) for i in c.GCAMConstants.biochar_x])
    biochar_price['2024_value'] = biochar_price['value'] / .17 * 1000  # converting from 1975 to 2024 dollars
    biochar_price["Units"] = "USD$2024/ton"
    plotting.plot_regional_hist_avg(biochar_price, '2024_value', SSP, "count region/year combinations",
                                    "histogram of price of biochar", "variable", "na", RCP, nonBaselineScenario)
    data_manipulation.drop_missing(biochar_price).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(RCP) + "/biochar_price.csv")

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


def figure5(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for figure 5
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: N/A
    """
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

    # Staple expenditure as percentage of average income – food demand prices and GDP per capita PPP by region
    # get data
    released_staple_expenditure = data_manipulation.get_sensitivity_data(["released"], "food_demand_prices", SSP,
                                                                         RCP=RCP, source="original")
    pyrolysis_staple_expenditure = data_manipulation.get_sensitivity_data(nonBaselineScenario, "food_demand_prices",
                                                                          SSP, RCP=RCP, source="masked")
    diff_food_staple_income = data_manipulation.flat_difference(pyrolysis_staple_expenditure,
                                                                released_staple_expenditure,
                                                                ["SSP", "GCAM", "input"])

    diff_food_staple_income['GCAM'] = diff_food_staple_income.apply(lambda row: data_manipulation.relabel_region(row),
                                                                    axis=1)
    diff_food_staple_income['input'] = diff_food_staple_income.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)
    diff_food_staple_income[
        biochar_year] = diff_food_staple_income[
                            biochar_year] * 1.62  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=200501&year2=202401

    diff_food_staple_income = diff_food_staple_income.sort_values(by=biochar_year, ascending=False)
    diff_food_staple_income["Units"] = "2024 USD$/Mcal/day"

    data_manipulation.drop_missing(diff_food_staple_income).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/change_in_food_staple_income.csv")

    # calculate global average percent difference
    perc_diff = data_manipulation.percent_difference(pyrolysis_staple_expenditure,
                                                     released_staple_expenditure,
                                                     ["SSP", "GCAM", "input"])

    perc_diff['GCAM'] = perc_diff.apply(lambda row: data_manipulation.relabel_region(row),
                                        axis=1)
    perc_diff['input'] = perc_diff.apply(
        lambda row: data_manipulation.relabel_food_demand(row), axis=1)
    perc_diff[biochar_year] = perc_diff[
                                  biochar_year] * 1.62  # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=200501&year2=202401

    perc_diff = perc_diff.sort_values(by=biochar_year, ascending=False)
    perc_diff["Units"] = "%"

    data_manipulation.drop_missing(perc_diff).to_csv(
        "data/data_analysis/supplementary_tables/" + str(nonBaselineScenario) + "/" + str(
            RCP) + "/percent_difference_food_staple_income.csv")

    # add an empty row at the top of the dataframe
    new_row1 = pd.DataFrame(diff_food_staple_income.loc[0]).transpose()
    new_row2 = pd.DataFrame(diff_food_staple_income.loc[0]).transpose()
    new_row1[biochar_year] = 0
    new_row1["GCAM"] = " "
    new_row2[biochar_year] = 0
    new_row2["GCAM"] = " "
    new_row2["input"] = "Staples"
    diff_food_staple_income = pd.concat([new_row1, new_row2, diff_food_staple_income, new_row2, new_row1])

    # plot results
    plotting.plot_regional_rose(diff_food_staple_income, biochar_year, SSP,
                                "change in food expenditure (USD$2024/Mcal/day)",
                                "food expenditure in " + biochar_year + " in " + str(SSP[0]),
                                "input", RCP, nonBaselineScenario)


def cue_figure(nonBaselineScenario, RCP, SSP, biochar_year):
    """
    Returns plots for potential figure in the CUE conference paper
    :param nonBaselineScenario: the scenario to be compared to the released scenario
    :param RCP: the RCP pathways being considered
    :param SSP: the SSP pathways being considered
    :param biochar_year: the year for biochar/carbon prices to be evaluated and plotted
    :return: N/A
    """
    #TODO: gather data we want to plot
    # 2 figures: biochar scenarios only/change vs baseline
    # biochar scenarios only
    # Biochar Supply
    supply = data_manipulation.get_sensitivity_data(nonBaselineScenario, "supply_of_all_markets", SSP, RCP=RCP,
                                                            source="masked")
    biochar_supply = supply[supply[['product']].isin(["biochar"]).any(axis=1)].copy(deep=True)
    biochar_supply = data_manipulation.group(biochar_supply, ["SSP", "Version"])
    biochar_supply["Units"] = "Supply of biochar (Mt)"

    # median price of biochar
    biochar_price = data_manipulation.get_sensitivity_data(nonBaselineScenario, "prices_of_all_markets", SSP, RCP=RCP,
                                                           source="masked")
    biochar_price['product'] = biochar_price.apply(lambda row: data_manipulation.remove__(row, "product"), axis=1)
    biochar_price['GCAM'] = "None"
    biochar_price = biochar_price[biochar_price[['product']].isin(["biochar"]).any(axis=1)]
    for i in c.GCAMConstants.x:
        biochar_price[str(i)] = biochar_price[str(i)] / .17 * 1000 # converting from 1975 to 2024 dollars
    biochar_price = biochar_price.groupby([str(i) for i in c.GCAMConstants.column_order if str(i) not in [str(j) for j in c.GCAMConstants.x]]).median().reset_index()
    biochar_price["Units"] = "Price of Biochar (USD$2024/ton)"

    # Net CO2 emissions (except LUC)
    co2_pyrolysis = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                           "CO2_emissions_by_tech_excluding_resource_production",
                                                           SSP, RCP=RCP, source="masked")
    co2_pyrolysis['GCAM'] = 'All'  # avoids an issue later in plotting for global SSP being dropped
    co2_pyrolysis['technology'] = co2_pyrolysis.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                      axis=1)
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
    co2_seq_pyrolysis = data_manipulation.group(co2_seq_pyrolysis, ["SSP", "Version"])
    co2_avd_pyrolysis = data_manipulation.group(co2_avd_pyrolysis, ["SSP", "Version"])

    # avoided agricultural emissions from lands managed with biochar
    ghg_er = data_manipulation.get_sensitivity_data(nonBaselineScenario,
                                                    "nonCO2_emissions_by_tech_excluding_resource_production",
                                                    SSP, RCP=RCP, source="masked")

    ag_avd_n2o_land = ghg_er[ghg_er['technology'].str.contains("biochar")]  # get only biochar lut
    ag_avd_ch4_land = ghg_er[ghg_er['technology'].str.contains("biochar")]
    ag_avd_n2o_land = ag_avd_n2o_land[ag_avd_n2o_land[['GHG']].isin(["N2O_AGR"]).any(axis=1)]  # select specific ghg
    ag_avd_ch4_land = ag_avd_ch4_land[ag_avd_ch4_land[['GHG']].isin(["CH4_AGR"]).any(axis=1)]
    ag_avd_n2o_land = data_manipulation.group(ag_avd_n2o_land,
                                              ["Version", "GHG"])  # group all biochar land leafs by version
    ag_avd_ch4_land = data_manipulation.group(ag_avd_ch4_land, ["Version", "GHG"])
    for i in c.GCAMConstants.future_x:
        ag_avd_n2o_land[str(i)] = ag_avd_n2o_land.apply(
            lambda row: data_manipulation.avd_soil_emissions(row, "GHG", str(i)), axis=1)
        ag_avd_ch4_land[str(i)] = ag_avd_ch4_land.apply(
            lambda row: data_manipulation.avd_soil_emissions(row, "GHG", str(i)), axis=1)
    ag_avd_n2o_land["Units"] = "Avoided cropland N$_2$O"
    ag_avd_ch4_land["Units"] = "Avoided cropland CH$_4$"

    # avoided CH4 and N2O emissions from avoided biomass decomposition
    biochar_ghg_er = ghg_er[ghg_er['technology'].str.contains("biochar")].copy(deep=True)
    biochar_ghg_er['technology'] = ghg_er.apply(lambda row: data_manipulation.remove__(row, "technology"),
                                                        axis=1)
    biochar_ghg_er = biochar_ghg_er[biochar_ghg_er['technology'].str.contains("|".join(products))]  # removes LUT
    biochar_ghg_er = data_manipulation.group(biochar_ghg_er, ["SSP", "Version", "GHG"])

    biochar_ghg_er["Units"] = biochar_ghg_er.apply(lambda row: "Avoided biomass decomposition N$_2$O" if row["GHG"] == "N2O" else "Avoided biomass decomposition CH$_4$", axis=1)

    # convert using GWP values
    for i in c.GCAMConstants.future_x:
        biochar_ghg_er[str(i)] = biochar_ghg_er.apply(
            lambda row: data_manipulation.ghg_ER(row, "GHG", str(i)), axis=1)

    # combine all direct sources of GHG emissions changes into a single df/graph
    biochar_ghg_emissions = pd.concat([biochar_ghg_er, co2_seq_pyrolysis, co2_avd_pyrolysis, ag_avd_n2o_land, ag_avd_ch4_land])

    # calculate net CO2 impact
    biochar_ghg_emissions = biochar_ghg_emissions.groupby('Version').sum().reset_index()
    biochar_ghg_emissions["Units"] = "Net Emissions (Mt CO$_2$-eq/yr)" # this unit is used to label the graph
    biochar_ghg_emissions["SSP"] = ag_avd_ch4_land["SSP"].unique()[0]

    within_biochar = pd.concat([biochar_supply, biochar_price, biochar_ghg_emissions]).reset_index()

    # this method requires baseline data as an entry in the dataset, at the bottom
    base_version_biochar = "default"
    plotting.sensitivity(within_biochar, RCP, base_version_biochar, biochar_year, "Units", "Version", nonBaselineScenario)

    # change vs baseline
    # Change LUC emissions
    released_luc = data_manipulation.get_sensitivity_data(["released"], "LUC_emissions_by_LUT", SSP, RCP=RCP,
                                                          source="original")
    pyrolysis_luc = data_manipulation.get_sensitivity_data(nonBaselineScenario, "LUC_emissions_by_LUT", SSP,
                                                           RCP=RCP, source="masked")

    released_luc = data_manipulation.group(released_luc, ["SSP", "Version"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["SSP", "Version"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["SSP"])
    perc_diff_luc = data_manipulation.percent_difference(released_luc, pyrolysis_luc, ["SSP"])

    for i in c.GCAMConstants.future_x:
        flat_diff_luc[str(i)] = 3.664 * flat_diff_luc[str(i)]  # 3.664 converts C to CO2-eq
    flat_diff_luc["Units"] = "Change in LUC emissions (Mt CO2-eq)"
    perc_diff_luc["Units"] = "% Change in LUC emissions"

    # Change in food Pcals
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
    flat_diff_Pcal = flat_diff_Pcal[~flat_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    perc_diff_Pcal = perc_diff_Pcal[~perc_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    flat_diff_Pcal = data_manipulation.group(flat_diff_Pcal, ["Version"])
    perc_diff_Pcal = data_manipulation.group(perc_diff_Pcal, ["Version"])

    # change in biofuel lands
    # change in croplands
    # change in herd size
    # change in temperature/forcing in 2100



    #TODO: initialize baseline as a separate dataframe.
    #TODO: duplicate for flat_diffs as well
    # ensure perc diff has no na
    base_version_released = "released"
    perc_diff_biofuel = perc_diff_biofuel[perc_diff_biofuel[biochar_year].notna()]  # remove .nan rows from df
    # create baseline scenarios of 0% change
    baseline_data = perc_diff_biofuel.copy(deep=True)
    baseline_data['Version'] = base_version_released
    for j in c.GCAMConstants.x:
        baseline_data[str(j)] = 0
    perc_diff_biofuel = pd.concat([perc_diff_biofuel, baseline_data]).reset_index()

    # plot products
    plotting.sensitivity(perc_diff_biofuel, RCP, base_version_released, biochar_year, "technology", "Version", nonBaselineScenario)
    plotting.sensitivity(perc_diff_biofuel, RCP, base_version_released, biochar_year, "technology", "Version",
                         nonBaselineScenario)


def main():
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    reference_SSP = ["SSP1"]  # the first SSP in the list is assumed to be the baseline
    reference_RCP = "6p0"
    other_scenario = ["default"]  # the first scenario in the list is assumed to be the baseline
    biochar_year = "2050"
    #figure2(other_scenario, reference_RCP, reference_SSP, biochar_year)
    #figure3(other_scenario, reference_RCP, reference_SSP, biochar_year)
    #figure4(other_scenario, reference_RCP, reference_SSP)
    #figure5(other_scenario, reference_RCP, reference_SSP, biochar_year)
    cue_figure(other_scenario, reference_RCP, reference_SSP, biochar_year)


if __name__ == '__main__':
    main()
