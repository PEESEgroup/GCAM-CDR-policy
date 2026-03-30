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
    tech_neutrality()
    # compare_policy_costs("CDRIA-2035_high", "45Q-2040_high")
    # CAGR(config_fname, "2050")
    # land_allocation(config_fname, "2050")
    # cement(config_fname, "2050")
    # electricity(config_fname, "2050")
    # state_CDR(config_fname, "2050")
    # C_tax(config_fname, reference_year)
    # C_prices(config_fname, reference_year)
    # CDR_subsidies(config_fname, "2035", "2040")


def tech_neutrality():
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high"]

    # get CDR data
    all_data = pd.DataFrame()
    for nonBaselineScenario in scenarios:
        nonBaselineScenario = str(nonBaselineScenario).replace("_", "/")
        fpath = "./data/data_analysis/supplementary_tables/" + nonBaselineScenario + "/policy cost by technology.csv"
        pyrolysis_df = pd.read_csv(fpath)
        if all_data.empty:
            all_data = pyrolysis_df
        else:
            all_data = pd.concat([all_data, pyrolysis_df])
    CDR = all_data[["2025_supply", "2030_supply", "2035_supply", "2040_supply", "2045_supply", "2050_supply",
                    "2025", "2030", "2035", "2040", "2045", "2050",
                    "scenario", "baseline", "product", "Units"]]
    CDR = CDR[CDR["product"].isin(["BECCS", "DAC", "OEW", "TEW"])]
    CDR = CDR.fillna(0)  # fill na with 0

    # subtract the effects of the baseline scenarios to find the impacts of policy
    baselines = CDR[(CDR["scenario"] == "low") | (CDR["scenario"] == "high")].copy(deep=True)
    CDR = CDR[~CDR["scenario"].isin(["low", "high"])]
    CDR = pd.merge(CDR, baselines, "left", ["baseline", "product", "Units"], suffixes=("_original", "_baseline"))
    CDR["scenario"] = CDR["scenario_original"]

    # calculate the changes in supply
    for i in c.GCAMConstants.plotting_x:
        CDR[str(i)+"_supply"] = CDR[str(i)+"_supply_original"] - CDR[str(i)+"_supply_baseline"]
    CDR = CDR[["2025_supply", "2030_supply", "2035_supply", "2040_supply", "2045_supply", "2050_supply",
               "scenario", "baseline", "product", "Units"]]

    # calculate spend and supply and which technology it is applied to
    for i in c.GCAMConstants.plotting_x:
        supply_sums = CDR.groupby(['scenario'])[str(i)+"_supply"].transform(lambda x: x.abs().sum())
        CDR[str(i)] = CDR[str(i)+"_supply"]/supply_sums  # what is the impact of policy on supply of CDR by technology compared to baseline?



def CAGR(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low",
                 "45Q-2040_high", "45Q-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    CDR = data_manipulation.get_sensitivity_data(scenarios, "CDR_by_tech")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]
    CDR = data_manipulation.group(CDR, ["baseline", "scenario", "technology"])
    CDR["GCAM"] = "USA"
    CDR["Units"] = "CAGR (%)"

    # CAGR calculations
    for i in c.GCAMConstants.plotting_x:
        # rename columns
        CDR[str(i) + "_original"] = CDR[str(i)]

    for i in c.GCAMConstants.plotting_x:
        # calculate CAGR
        if i > 2025:
            # (new/old)^(1/t [5 years]) -1     -> *100 to go to %
            CDR[str(i)] = 100*((CDR[str(i)+ "_original"]/CDR[str(i-5)+ "_original"]) ** (1/5) - 1)
        else:
            CDR[str(i)] = np.nan

    CDR_DAC = CDR[CDR["technology"] == "DAC"].copy(deep=True)
    CDR_BECCS = CDR[CDR["technology"] == "BECCS"].copy(deep=True)
    CDR_OEW = CDR[CDR["technology"] == "OEW"].copy(deep=True)
    CDR_TEW = CDR[CDR["technology"] == "TEW"].copy(deep=True)

    plotting.plot_line_product_CI(CDR_DAC, "baseline", "CAGR for DAC by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_BECCS, "baseline", "CAGR for BECCS by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_OEW, "baseline", "CAGR for OEW by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_TEW, "baseline", "CAGR for TEW by baseline scenario", region=["USA"])


def land_allocation(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    allocation = data_manipulation.get_sensitivity_data(scenarios, "aggregated_land_allocation", "masked")
    allocation = allocation[allocation["GCAM"] == "USA"]
    allocation = allocation.drop('Unnamed: 0', axis=1)
    allocation["Units"] = "Land (thousand km$^2$)"

    biomass_allocation = allocation[allocation["LandLeaf"] == "biomass"].copy(deep=True)
    managed_forests = allocation[allocation["LandLeaf"] == "forest (managed)"].copy(deep=True)
    unmanaged_forests = allocation[allocation["LandLeaf"] == "forest (unmanaged)"].copy(deep=True)

    plotting.plot_line_product_CI(biomass_allocation, "baseline", "Land allocated to bioenergy crops by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(managed_forests, "baseline", "Land allocated to managed forests by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(unmanaged_forests, "baseline", "Land allocated to unmanaged forests by baseline scenario", region=["USA"])


def C_tax(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]
    CO2_emissions = data_manipulation.get_sensitivity_data(scenarios, "CO2_emissions_by_sector")
    CO2_emissions = CO2_emissions[CO2_emissions["GCAM"].isin(c.GCAMConstants.USA_region)]
    CO2_emissions = CO2_emissions[CO2_emissions["sector"] != "CDR_regional"]  # excluded from the C tax
    CO2_emissions = CO2_emissions.groupby(["scenario", "baseline", "Units"]).sum(min_count=1).reset_index()
    # get a baseline CO2 emissions
    baseline_emissions = pd.read_csv("data/data_analysis/baseline_co2_emissions.csv")
    # process emissions revenue
    CO2_prices = data_manipulation.get_sensitivity_data(scenarios, "CO2_prices")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_tax_revenue = pd.merge(CO2_emissions, CO2_prices, "left", ["baseline", "scenario"], suffixes=("_supply", "_price"))
    for i in c.GCAMConstants.plotting_x:
        # (Mt C * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        CO2_tax_revenue[str(i)] = (CO2_tax_revenue[str(i) + "_supply"] / c.GCAMConstants.CO2_to_C) * (
                CO2_tax_revenue[str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC) / 1000 # to billion
    # process deadweight loss
    CO2_tax_price = pd.merge(CO2_emissions, CO2_prices, "left", ["baseline", "scenario"], suffixes=("_supply", "_price"))
    CO2_tax_price["Units"] = "MTC"
    deadweight_loss = pd.merge(CO2_tax_price, baseline_emissions, "left", "Units", suffixes=("_actual", "_baseline"))
    for i in c.GCAMConstants.plotting_x:
        # ((Mt C - Mt C) * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        deadweight_loss[str(i)] = (
                0.5 * (deadweight_loss[str(i)] - deadweight_loss[str(i) + "_supply"]) / c.GCAMConstants.CO2_to_C *
                (deadweight_loss[str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC)) / 1000 # to billion

    deadweight_loss = deadweight_loss[["scenario", "baseline", "2025", "2030", "2035", "2040", "2045", "2050"]]
    CO2_tax_revenue = CO2_tax_revenue[["scenario", "baseline", "2025", "2030", "2035", "2040", "2045", "2050"]]
    deadweight_loss["Units"] = "Billion 2025$USD/yr"
    CO2_tax_revenue["Units"] = "Billion 2025$USD/yr"
    deadweight_loss["product"] = "Deadweight Loss"
    CO2_tax_revenue["product"] = "C Tax Revenue"
    deadweight_loss["GCAM"] = "USA"
    CO2_tax_revenue["GCAM"] = "USA"

    plotting.plot_line_product_CI(deadweight_loss, "baseline", "Deadweight loss by baseline scenario", region=["USA"], skip_years=2)
    plotting.plot_line_product_CI(CO2_tax_revenue, "baseline", "C tax revenue by baseline scenario", region=["USA"], skip_years=2)

def C_prices(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    CO2_prices = data_manipulation.get_sensitivity_data(scenarios, "CO2_prices", "masked")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_prices = CO2_prices.drop('Unnamed: 0', axis=1)
    CO2_prices["Units"] = "C Tax (USD/t CO$_{2}$-eq)"

    for i in c.GCAMConstants.plotting_x:
        CO2_prices[str(i)] = CO2_prices[str(i)] / c.GCAMConstants.USD2025_tCO2_to_1990_tC

    plotting.plot_line_product_CI(CO2_prices, "baseline", "C tax prices by baseline scenario", region=["USA"])


def state_CDR(config_fname, reference_year):
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    supply = data_manipulation.get_sensitivity_data(scenarios, "CDR_by_tech", source="masked")
    price = data_manipulation.get_sensitivity_data(scenarios, "prices_of_all_markets", source="masked")

    price = price[price["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price[price["product"].isin(["DAC", "TEW", "OEW", "BECCS"])]
    price["Units"] = "2025$/t CDR"
    supply = supply[supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price.drop('Unnamed: 0', axis=1)
    supply = supply.drop('Unnamed: 0', axis=1)
    supply["product"] = supply["technology"]

    for i in c.GCAMConstants.plotting_x:
        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=197501&year2=202501
        price[str(i)] = price[str(i)] / c.GCAMConstants.USD2025_tCO2_to_1975_kgC
        supply[str(i)] = supply[str(i)] / c.GCAMConstants.CO2_to_C

    # sort by baseline
    CDR_price_low = price[price["baseline"] == "low"].copy(deep=True)
    CDR_price_high = price[price["baseline"] == "high"].copy(deep=True)
    CDR_supply_low = supply[supply["baseline"] == "low"].copy(deep=True)
    CDR_supply_high = supply[supply["baseline"] == "high"].copy(deep=True)

    # market sizes
    CDR_market_low = pd.merge(CDR_price_low, CDR_supply_low, "right", on=["GCAM", "baseline", "scenario", "product"], suffixes=("_price", "_supply"))
    CDR_market_high = pd.merge(CDR_price_high, CDR_supply_high, "right", on=["GCAM", "baseline", "scenario", "product"],
                              suffixes=("_price", "_supply"))
    # calculate size of markets and remove outliers
    for i in c.GCAMConstants.plotting_x:
        CDR_market_low[str(i)] = CDR_market_low[str(i) + "_price"] * CDR_market_low[str(i) + "_supply"]
        CDR_market_low[str(i) + "_price"] = CDR_market_low.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        CDR_market_low[str(i) + "_supply"] = CDR_market_low.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)
        CDR_market_high[str(i)] = CDR_market_high[str(i) + "_price"] * CDR_market_high[str(i) + "_supply"]
        CDR_market_high[str(i) + "_price"] = CDR_market_high.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        CDR_market_high[str(i) + "_supply"] = CDR_market_high.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)

        # still some rare price outliers
        CDR_market_low[str(i) + "_price"] = CDR_market_low.apply(
            lambda row: row[str(i) + "_price"] if row[str(i) + "_price"] < 1000 else np.nan, axis=1)
        CDR_market_high[str(i) + "_price"] = CDR_market_high.apply(
            lambda row: row[str(i) + "_price"] if row[str(i) + "_price"] < 1000 else np.nan, axis=1)

    # add units
    CDR_market_low["Units"] = "Million USD/yr"
    CDR_market_high["Units"] = "Million USD/yr"

    # split back into price and supply markets
    CDR_price_low = CDR_market_low.copy(deep=True)
    CDR_supply_low = CDR_market_low.copy(deep=True)
    CDR_price_high = CDR_market_high.copy(deep=True)
    CDR_supply_high = CDR_market_high.copy(deep=True)

    for i in c.GCAMConstants.plotting_x:
        CDR_price_low[str(i)] = CDR_price_low[str(i) + "_price"]
        CDR_supply_low[str(i)] = CDR_supply_low[str(i) + "_supply"]
        CDR_price_high[str(i)] = CDR_price_high[str(i) + "_price"]
        CDR_supply_high[str(i)] = CDR_supply_high[str(i) + "_supply"]

    # update units
    CDR_price_low["Units"] = "$/t CDR"
    CDR_supply_low["Units"] = "log$_{10}$(Mt CDR)"
    CDR_price_high["Units"] = "$/t CDR"
    CDR_supply_high["Units"] = "log$_{10}$(Mt CDR)"
    CDR_market_low["Units"] = "Million USD/yr"
    CDR_market_high["Units"] = "Million USD/yr"

    # only include necessary information
    plotting_cols = ["2025", "2030", "2035", "2040", "2045", "2050", "GCAM", "product", "baseline", "scenario", "Units"]
    CDR_price_low = CDR_price_low[plotting_cols]
    CDR_price_high = CDR_price_high[plotting_cols]
    CDR_supply_low = CDR_supply_low[plotting_cols]
    CDR_supply_high = CDR_supply_high[plotting_cols]
    CDR_market_low = CDR_market_low[plotting_cols]
    CDR_market_high = CDR_market_high[plotting_cols]

    # take log of supply and market size
    for i in c.GCAMConstants.plotting_x:
        CDR_supply_low[str(i)] = np.log10(CDR_supply_low[str(i)])
        CDR_supply_high[str(i)] = np.log10(CDR_supply_high[str(i)])

    # plotting graphs
    plotting.plot_line_product_CI(CDR_price_low, "product", "CDR prices in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_price_high, "product", "CDR prices in high baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_supply_low, "product", "CDR supply in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_supply_high, "product", "CDR supply in high baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_market_low, "product", "CDR markets in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_market_high, "product", "CDR markets in high baseline", skip_years=0)


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

    if config_fname.split("/")[1] == "nothing":
        # no BECCS in the nothing baseline
        CDR = CDR[CDR["technology"] != "BECCS"]

    # choropleth map
    plotting.plot_regional_hist_avg(CDR, 'plot',
                                    "change in size of CDR markets from 2035 to 2040",
                                    "technology", config_fname)
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
    cost_diff = cost_diff[cost_diff["product"] != "C Tax Revenue"]
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
    for i in ["s1-procureScaling-n_nothing", "s1-procure3B-n_nothing"]:
        main(i, "2050")
