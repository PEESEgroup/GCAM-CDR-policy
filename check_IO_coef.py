import constants as c
import pandas as pd


def IO_check(comb, coefficients, assert_str, nonBaselineScenario):
    for i in c.GCAMConstants.plotting_x:
        comb["check_" + str(i)] = comb[str(i) + "_x"] / comb[str(i) + "_y"]
    for k in c.GCAMConstants.SSPs:
        # check coef on an SSP basis
        comb_SSP = comb[comb[['SSP']].isin([k]).any(axis=1)]
        for i in c.GCAMConstants.plotting_x:
            try:  # if mean coefficient isn't within 5% of target
                assert abs(coefficients[nonBaselineScenario, str(j)]) * .95 < abs(comb_SSP["check_" + str(i)].mean()) < \
                       abs(coefficients[nonBaselineScenario, str(j)]) * 1.05
            except AssertionError:  # print out that the scenario is no good
                print(assert_str, "fails for product", str(j), "in year", str(i), "in", str(k),
                      "with mean", str(comb_SSP["check_" + str(i)].mean()))


if __name__ == '__main__':
    nonBaselineScenario = "pyrolysis"
    RCP = "4p5"

    #TODO: develop mask for year and scenario

    # check IO coefficients
    supply = pd.read_csv("../data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")  # current wd is /xml for some reason

    # get relevant products
    products = ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure", "beef_biochar",
                "dairy_biochar", "goat_biochar", "pork_biochar", "poultry_biochar", "manure fuel feedstock"]
    supply = supply[supply['product'].str.contains("|".join(products))]

    # get carbon capture figures by technology
    co2_emissions = pd.read_csv("../data/gcam_out/"+ str(
        nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    co2_emissions = co2_emissions[co2_emissions['sector'].str.contains("|".join(products))]

    #get fertilizer figures by tech
    fert_tech = pd.read_csv("../data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/fertilizer_production_by_tech.csv")
    fert_tech = fert_tech[fert_tech['subsector'].str.contains("|".join(products))]

    for j in ["beef", "dairy", "goat", "pork", "poultry"]:
        # carbon yields from biochar
        products = [str(j) + " manure"]
        co2 = co2_emissions[co2_emissions['sector'].str.contains("|".join([str(j) + "_biochar"]))]
        manure = supply[supply['product'].str.contains("|".join(products))]
        # get global manure supply
        manure = manure.groupby(['SSP']).sum()
        manure['GCAM'] = 'Global'
        comb = pd.merge(co2, manure, how="inner", on=['GCAM', 'SSP'])
        IO_check(comb, c.GCAMConstants.manure_C_ratio, "assert C and manure", nonBaselineScenario)

        # N fertilizer yields from biochar
        products = [str(j) + "_biochar"]
        fert = fert_tech[fert_tech['subsector'].str.contains("|".join(products))]
        biochar = supply[supply['product'].str.contains("|".join(products))]
        comb = pd.merge(fert, biochar, how="inner", on=['GCAM', 'SSP'])
        IO_check(comb, c.GCAMConstants.biochar_fert_ratio, "assert fertilizer and biochar", nonBaselineScenario)

        # manure to biochar coefficient
        # get separate manure and biochar entries
        products = [str(j) + " manure"]
        manure = supply[supply['product'].str.contains("|".join(products))]
        products = [str(j) + "_biochar"]
        biochar = supply[supply['product'].str.contains("|".join(products))]
        # merge and extract coefficient
        comb = pd.merge(manure, biochar, how="inner", on=['GCAM', 'SSP'])
        IO_check(comb, c.GCAMConstants.manure_biochar_ratio, "assert manure and biochar", nonBaselineScenario)

        # biochar to manure fuel coefficient


        # manure to manure fuel coefficient

