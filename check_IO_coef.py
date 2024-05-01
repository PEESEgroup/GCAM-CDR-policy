import constants as c
import pandas as pd
import os

if __name__ == '__main__':
    nonBaselineScenario = "pyrolysis"
    RCP = "4p5"

    # check IO coefficients
    supply = pd.read_csv("../data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")  # current wd is /xml for some reason

    # get relevant products
    products = ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure", "beef_biochar",
                "dairy_biochar", "goat_biochar", "pork_biochar", "poultry_biochar", "manure fuel feedstock",
                "N fertilizer"]
    supply = supply[supply['product'].str.contains("|".join(products))]

    # get carbon capture figures by technology
    co2_emi_released = pd.read_csv("../data/gcam_out/released/" + RCP + "/CO2_emissions_by_region.csv")
    co2_emi_released = co2_emi_released[co2_emi_released['sector'].str.contains("|".join(products))]

    # join dataframes

    for j in ["beef", "dairy", "goat", "pork", "poultry"]:
        # carbon yields from biochar

        # N fertilizer yields from biochar

        # manure to biochar coefficient
        # get separate manure and biochar entries
        products = [str(j) + " manure"]
        manure = supply[supply['product'].str.contains("|".join(products))]
        products = [str(j) + "_biochar"]
        biochar = supply[supply['product'].str.contains("|".join(products))]
        # merge and extract coefficient
        comb = pd.merge(manure, biochar, how="inner", on=['GCAM', 'SSP'])
        for i in c.GCAMConstants.plotting_x:
            comb["check_" + str(i)] = comb[str(i) + "_x"] / comb[str(i) + "_y"]

        for k in c.GCAMConstants.SSPs:
            # check coef on an SSP basis
            comb_SSP = comb[comb[['SSP']].isin([k]).any(axis=1)]
            for i in c.GCAMConstants.plotting_x:
                try:  # if mean coefficient isn't within 5% of target
                    assert c.GCAMConstants.manure_biochar_ratio[str(j)] * .95 < comb_SSP["check_" + str(i)].mean() < \
                           c.GCAMConstants.manure_biochar_ratio[str(j)] * 1.05
                except AssertionError:  # print out that the scenario is no good
                    print("assert manure and biochar fails for product", str(j), "in year", str(i), "in", str(k),
                          "with mean", str(comb_SSP["check_" + str(i)].mean()))

            # biochar to manure fuel coefficient
            pass
