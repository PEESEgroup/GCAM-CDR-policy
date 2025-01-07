from matplotlib import pyplot as plt

import constants
import plotting
import data_manipulation
import constants as c
import pandas as pd
import stats as stats

def pop_and_calories(nonBaselineScenario, RCP, SSP):
    # get population data
    released_pop = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/population_by_region.csv")
    pyrolysis_pop = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/population_by_region.csv")
    released_pop = released_pop[released_pop[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_pop = pyrolysis_pop[pyrolysis_pop[['SSP']].isin(SSP).any(axis=1)]
    flat_diff_pop = data_manipulation.flat_difference(released_pop, pyrolysis_pop, ["SSP", "GCAM"])
    print(flat_diff_pop["2050"])

    # get calorie data
    released_Pcal = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/food_consumption_by_type_specific.csv")
    pyrolysis_Pcal = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/food_consumption_by_type_specific.csv")
    released_Pcal = released_Pcal[released_Pcal[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_Pcal = pyrolysis_Pcal[pyrolysis_Pcal[['SSP']].isin(SSP).any(axis=1)]
    released_global_pcal = released_Pcal[released_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    print(released_global_pcal[["subsector", "technology", "2050", "Units"]])
    flat_diff_Pcal = data_manipulation.flat_difference(released_Pcal, pyrolysis_Pcal, ["GCAM", "SSP", "subsector", "subsector.1", "technology"]).drop_duplicates()
    perc_diff_Pcal = data_manipulation.percent_difference(released_Pcal, pyrolysis_Pcal, ["GCAM", "SSP", "subsector", "subsector.1",  "technology"]).drop_duplicates()
    # perc_diff_Pcal["Units"] = "%"
    global_flat = flat_diff_Pcal[flat_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    print(global_flat[["subsector", "technology", "2050", "Units"]])
    flat_diff_Pcal = flat_diff_Pcal[~flat_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    perc_diff_Pcal = perc_diff_Pcal[~perc_diff_Pcal[['GCAM']].isin(["Global"]).any(axis=1)]
    plotting.plot_regional_hist_avg(flat_diff_Pcal, "2050", SSP, "count region-foodstuff", "Flat difference in Pcals consumed in pyrolysis and reference scenario", "technology", "na")
    plotting.plot_regional_hist_avg(perc_diff_Pcal, "2050", SSP, "count region-foodstuff",
                                    "Percent difference in Pcals consumed in pyrolysis and reference scenario",
                                    "technology", "na")

    print(flat_diff_Pcal["2050"])


def luc_by_region(nonBaselineScenario, RCP, SSP):
    # get luc data
    released_luc = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/LUC_emissions_by_LUT.csv")
    pyrolysis_luc = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/LUC_emissions_by_LUT.csv")
    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP"])
    released_luc = released_luc[released_luc[['SSP']].isin(SSP).any(axis=1)]
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP"])
    print(flat_diff_luc[["GCAM", "2050", "Units"]])
    # plotting.plot_world_by_years(flat_diff_luc, ["MtC/yr"], "Units", ["2040", "2045", "2050"], SSP,
    #                              "net difference in LUC emissions by region")

    flat_diff_luc = data_manipulation.group(flat_diff_luc, ["SSP"])
    plotting.plot_line_by_product(flat_diff_luc, ["SSP1"], "SSP", ["SSP1"], "SSP", "Net LUC compared to reference scenario")

    released_luc = pd.read_csv(
        "data/gcam_out/released/" + RCP + "/original/LUC_emissions_by_LUT.csv")
    pyrolysis_luc = pd.read_csv(
        "data/gcam_out/" + str(nonBaselineScenario) + "/" + RCP + "/masked" + "/LUC_emissions_by_LUT.csv")
    released_luc = released_luc[released_luc[['SSP']].isin(SSP).any(axis=1)]
    released_luc["LandLeaf"] = released_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    pyrolysis_luc["LandLeaf"] = pyrolysis_luc.apply(lambda row: data_manipulation.relabel_detailed_land_use(row), axis=1)
    released_luc = data_manipulation.group(released_luc, ["GCAM", "SSP", "LandLeaf"])
    pyrolysis_luc = data_manipulation.group(pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    flat_diff_luc = data_manipulation.flat_difference(released_luc, pyrolysis_luc, ["GCAM", "SSP", "LandLeaf"])
    for i in ["2040", "2045", "2050"]:
        plotting.plot_regional_hist_avg(flat_diff_luc, i, SSP, "count region-LandLeaf",
                                    "Flat diffference in LUC emissions between pyrolysis and reference scenario in " + i,
                                    "LandLeaf", "na")


def main():
    reference_SSP = "SSP1"
    reference_RCP = "2p6"
    luc_by_region("biochar", reference_RCP, [reference_SSP])
    pop_and_calories("biochar", reference_RCP, [reference_SSP])

if __name__ == '__main__':
    main()