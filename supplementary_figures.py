import os
import plotting
import data_manipulation
import constants as c
import pandas as pd
import numpy as np


def main(config_fname, reference_year):
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    config_fname = config_fname.replace("_", "/")
    os.makedirs("./data/data_analysis/images/" + config_fname + "/", exist_ok=True)
    # compare_policy_costs("CDRIA-rhodium18b_low", "CDRIA-2035_low")
    cement(config_fname, "2050")
    electricity(config_fname, "2050")
    # CDR_subsidies(config_fname, "2035", "2040")


def cement(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    supply = data_manipulation.get_sensitivity_data(scenarios, "cement_production_by_tech_conv_and_ccs", source="masked")
    price = data_manipulation.get_sensitivity_data(scenarios, "cement_prices", source="masked")
    for i in c.GCAMConstants.plotting_x:
        price[str(i)] = price.apply(lambda row: row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 if row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 < 1000 else np.nan, axis=1)

    price = price[price["GCAM"].isin(c.GCAMConstants.USA_region)]
    price["Units"] = "2025$/kg"
    supply = supply[supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price.drop('Unnamed: 0', axis=1)
    supply = supply.drop('Unnamed: 0', axis=1)

    # sort by baseline
    cement_price_low = price[price["baseline"] == "low"].copy(deep=True)
    cement_price_high = price[price["baseline"] == "high"].copy(deep=True)
    cement_supply_low = supply[supply["baseline"] == "low"].copy(deep=True)
    cement_supply_high = supply[supply["baseline"] == "high"].copy(deep=True)

    plotting.plot_line_product_CI(cement_price_low, "sector", "cement prices in low baseline")
    plotting.plot_line_product_CI(cement_price_high, "sector", "cement prices in high baseline")
    plotting.plot_line_product_CI(cement_supply_low, "technology", "cement supply in low baseline")
    plotting.plot_line_product_CI(cement_supply_high, "technology", "cement supply in high baseline")


def electricity(config_fname, reference_year):
    # get scenario data
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    elec_supply = data_manipulation.get_sensitivity_data(scenarios, "elec_gen_by_subsector", source="masked")
    elec_price = data_manipulation.get_sensitivity_data(scenarios, "elec_prices_by_sector", source="masked")
    # convert to modern moneys and eliminate outliers
    for i in c.GCAMConstants.plotting_x:
        elec_price[str(i)] = elec_price.apply(lambda row: row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 / 0.277778 if row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 / 0.277778 < 1000 else np.nan, axis=1)

    # focus on US regions
    elec_price["Units"] = "2025$/MWh"
    elec_price = elec_price[elec_price["GCAM"].isin(c.GCAMConstants.USA_region)]
    elec_supply = elec_supply[elec_supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    elec_price = elec_price.drop('Unnamed: 0', axis=1)
    elec_supply = elec_supply.drop('Unnamed: 0', axis=1)

    # rename and group elec techs
    elec_supply["subsector"] = elec_supply.apply(lambda row: data_manipulation.elec_supply_sectors(row), axis=1)
    elec_supply = data_manipulation.group(elec_supply, ["subsector", "scenario", "baseline", "Units"])
    elec_supply["GCAM"] = elec_supply["baseline"]

    # sort by baseline
    elec_price_low = elec_price[elec_price["baseline"] == "low"].copy(deep=True)
    elec_price_high = elec_price[elec_price["baseline"] == "high"].copy(deep=True)

    plotting.plot_line_product_CI(elec_price_low, "fuel", "electricity prices in low baseline")
    plotting.plot_line_product_CI(elec_price_high, "fuel", "electricity prices in high baseline")
    plotting.plot_line_product_CI(elec_supply, "subsector", "national electricity supply", region=elec_supply["baseline"].unique())


def CDR_subsidies(config_fname, year1, year2):
    # data processing
    CDR = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech", "masked")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]

    CDR["plot"] = CDR[year2] - CDR[year1]

    # choropleth map
    plotting.plot_world_by_products(CDR, "technology", ["plot"],
                                    "Change in CDR (Mt) from " + year1 + " to year " + year2, config_fname)


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
            cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
        else:
            cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                      "change in policy cost by year " + scenario2.replace("/",
                                                                                           "_") + " - " + scenario1.replace(
                                          "/", "_"),
                                      scenario2)

    # no C tax
    cost_diff = cost_diff[cost_diff["product_price_old"] != "CO2"]
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                      "change in policy cost by year (no C tax) " + scenario2.replace("/",
                                                                                                      "_") + " - " + scenario1.replace(
                                          "/", "_"),
                                      scenario2)


if __name__ == '__main__':
    for i in ["low_low"]:
        main(i, "2050")
