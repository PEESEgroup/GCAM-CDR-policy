import constants as c
import pandas as pd
import data_manipulation


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


def get_biooil_yield(row, product_column, year_column, products, scenario):
    """
    produces the yield from the product
    :param row: a pd Series from a dataframe
    :param column: the column of the pd series being searched
    :param products: the list of suffixes to remove
    :return: the relabeled technology
    """
    for z in products:
        if z in row[product_column]:
            return row[year_column] * c.GCAMConstants.manure_biooil_ratio[scenario, z]


if __name__ == '__main__':
    nonBaselineScenario = "pyrolysis"
    RCP = "6p0"
    ifBiochar = True
    ifBiocharToFertilizer = True
    ifBiooilSecout = True

    #TODO: develop mask for year and scenario

    # check IO coefficients
    supply = pd.read_csv("data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/supply_of_all_markets.csv")  # current wd is /xml for some reason

    # get relevant products
    products = ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure", "beef_biochar",
                "dairy_biochar", "goat_biochar", "pork_biochar", "poultry_biochar", "manure fuel feedstock"]
    co2_emissions = pd.read_csv("data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/CO2_emissions_by_tech_excluding_resource_production.csv")
    co2_emissions = co2_emissions[co2_emissions['sector'].str.contains("|".join(products))]

    #get fertilizer figures by tech
    fert_tech = pd.read_csv("data/gcam_out/" + str(
        nonBaselineScenario) + "/" + RCP + "/fertilizer_production_by_tech.csv")
    fert_tech = fert_tech[fert_tech['subsector'].str.contains("|".join(products))]

    for j in ["beef", "dairy", "goat", "pork", "poultry"]:
        # carbon yields from manure
        products = [str(j) + " manure"]
        co2 = co2_emissions[co2_emissions['sector'].str.contains("|".join([str(j) + "_biochar"]))]
        manure = supply[supply['product'].str.contains("|".join(products))]
        # get global manure supply
        manure = manure.groupby(['SSP']).sum()
        manure['GCAM'] = 'Global'
        comb = pd.merge(co2, manure, how="inner", on=['GCAM', 'SSP'])
        IO_check(comb, c.GCAMConstants.manure_C_ratio, "assert C and manure", nonBaselineScenario)

        # N fertilizer yields from biochar
        if ifBiocharToFertilizer:
            products = [str(j) + "_biochar"]
            fert = fert_tech[fert_tech['subsector'].str.contains("|".join(products))]
            biochar = supply[supply['product'].str.contains("|".join(products))]
            comb = pd.merge(fert, biochar, how="inner", on=['GCAM', 'SSP'])
            IO_check(comb, c.GCAMConstants.biochar_fert_ratio, "assert fertilizer and biochar", nonBaselineScenario)

        # manure to biochar coefficient
        # get separate manure and biochar entries
        if ifBiochar:
            products = [str(j) + " manure"]
            manure = supply[supply['product'].str.contains("|".join(products))]
            products = [str(j) + "_biochar"]
            biochar = supply[supply['product'].str.contains("|".join(products))]
            # merge and extract coefficient
            comb = pd.merge(manure, biochar, how="inner", on=['GCAM', 'SSP'])
            IO_check(comb, c.GCAMConstants.manure_biochar_ratio, "assert manure and biochar", nonBaselineScenario)

    # manure to manure fuel coefficient
    products = ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure"]
    manure_fuel = supply[supply['product'].str.contains("|".join(["manure fuel feedstock"]))]
    manure = supply[supply['product'].str.contains("|".join(products))].copy(deep=True)
    # calculation theoretical bio-oil output
    for i in c.GCAMConstants.plotting_x:
        manure["check_"+str(i)] = manure.apply(
            lambda row: get_biooil_yield(row, "product", str(i), products, nonBaselineScenario),
            axis=1)
    manure = data_manipulation.group(manure, ["SSP", "GCAM"])
    comb = pd.merge(manure, manure_fuel, how="inner", on=['GCAM', 'SSP'])
    for k in c.GCAMConstants.SSPs:
        # check coef on an SSP basis
        comb_SSP = comb[comb[['SSP']].isin([k]).any(axis=1)]
        for i in c.GCAMConstants.plotting_x:
            if ifBiooilSecout:
                try:  # if calculated coefficient is less than expected coefficient
                    assert abs(comb_SSP["check_" + str(i)].sum()) > abs(comb_SSP[str(i) + "_y"].sum())  # c.f. DDGS calculated vs. stated ratios
                except AssertionError:  # print out that the scenario is no good
                    print("assert manure to biooil fails in year", str(i), "in", str(k),
                          "with actual sum", str(comb_SSP[str(i) + "_y"].sum()), "and expected sum",
                          str(comb_SSP["check_" + str(i)].sum()))
            else:
                try:  # if mean coefficient isn't within 5% of target
                    assert abs(comb_SSP["check_" + str(i)].sum()) * .95 < abs(
                        comb_SSP[str(i) + "_y"].sum()) < \
                           abs(comb_SSP["check_" + str(i)].sum()) * 1.05
                except AssertionError:  # print out that the scenario is no good
                    print("biooil calculation fails in year", str(i), "in", str(k),
                          "with supply", str(comb_SSP[str(i) + "_y"].sum()))

    # animal products to manure coefficients | other secondary output coefficients
    products_manure = ["beef manure", "dairy manure", "goat manure", "pork manure", "poultry manure", "Soybean", "OilCrop"]
    products_animal = ["Beef", "Dairy", "SheepGoat", "Pork", "Poultry", "DDGS and feedcakes", "DDGS and feedcakes"]
    for m, n in zip(products_manure, products_animal):
        manure = supply[supply['product'].str.contains("|".join([m]))]
        animals = supply[supply['product'].str.contains("|".join([n]))]
        comb = pd.merge(manure, animals, how="inner", on=['GCAM', 'SSP'])
        for k in c.GCAMConstants.SSPs:
            # check coef on an SSP basis
            comb_SSP = comb[comb[['SSP']].isin([k]).any(axis=1)]
            for i in c.GCAMConstants.plotting_x:
                # generally happens that the ratio produced is less than the ratio given in the .csv files
                # TODO: figure out why
                try:  # if calculated coefficient is less than expected coefficient
                    assert comb_SSP[str(i) + "_x"].sum()/comb_SSP[str(i) + "_y"].sum() < c.GCAMConstants.secout[i, m]  # c.f. DDGS calculated vs. stated ratios
                except AssertionError:  # print out that the scenario is no good
                    print("assert secout from", m, "fails in year", str(i), "in", str(k),
                          "with actual ratio", str(comb_SSP[str(i) + "_x"].sum()/comb_SSP[str(i) + "_y"].sum()), "and expected ratio",
                          str(c.GCAMConstants.secout[i, n]))
                pass
