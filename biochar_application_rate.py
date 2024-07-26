import math
import constants as c
import pandas as pd
import data_manipulation
import plotting


def nutrient_supply(row, product, nutrient, year, biochar=False):
    """
    calculates the nutrient supply based on the supply of animal products :param row: row in a pandas dataframe
    :param product: product used as the basis for calculation, with the gompertz function being added to calculations
    based on supply of animal products :param nutrient: nutrient applied to the field :param year: year of supply
    :param biochar: if just the supply of biochar is calculated :return: supply of the nutrient in Mt
    :param row: row in pandas dataframe
    :param nutrient: nutrient being analyzed, such as C, P, or K
    :param year: GCAM model year
    """
    biochar_to_nutrient = 0
    biochar_yields = 0
    manure_yields = 1
    feedstock = row[product]
    if feedstock == "beef manure" or feedstock == "Beef":
        biochar_yields = 1/2.1815
        if feedstock == "Beef":
            manure_yields = 2.589 * gompertz(year)
        if nutrient == "C":
            # 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution
            # of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
            biochar_to_nutrient = .396
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "dairy manure" or feedstock == "Dairy":
        biochar_yields = 1/2.1052
        if feedstock == "Dairy":
            manure_yields = 0.018 * gompertz(year)
        if nutrient == "C":
            # 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
            biochar_to_nutrient = .396
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .001754
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .009630
    if feedstock == "goat manure" or feedstock == "SheepGoat":
        if feedstock == "SheepGoat":
            manure_yields = 3.101 * gompertz(year)
        biochar_yields = 1/2.055
        if nutrient == "C":
            # 9: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
            biochar_to_nutrient = .420
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C # same as beef
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "pork manure" or feedstock == "Pork":
        if feedstock == "Pork":
            manure_yields = 0.304 * gompertz(year)
        biochar_yields = 1/2.136
        if nutrient == "C":
            # 9: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
            biochar_to_nutrient = .386
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C # same as beef
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "poultry manure" or feedstock == "Poultry":
        biochar_yields = 1/2.1276
        if feedstock == "Poultry":
            manure_yields = 1.381 * gompertz(year)
        if nutrient == "C":
            # 4: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
            biochar_to_nutrient = .762
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .030555
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .048616

    # Mt manure * Mt biochar/Mt manure * Mt nutrient/Mt biochar * 1 (if already manure)
    # Mt animal product * Mt manure/Mt animal product * Mt biochar/Mt manure * Mt nutrient/Mt biochar (if using released model)
    if biochar:
        return row[year] * biochar_yields * manure_yields
    else:
        # Mt manure * Mt biochar/Mt manure * Mt nutrient/Mt biochar * 1 (if already manure)
        # Mt animal product * Mt manure/Mt animal product * Mt biochar/Mt manure * Mt nutrient/Mt biochar (if using released model)
        return row[year] * biochar_yields * biochar_to_nutrient * manure_yields


def gompertz(year):
    """
    calculates the rate of biochar adoption based on a gompertz curve from literature
    :param year: GCAM model year
    :return: fraction of adoption
    """
    return 1*math.exp(-11*math.exp(-0.25*(int(year)-2028)))


def plot_world(dataframe, year, title):
    """
    Plots dataframe on a world map
    :param dataframe: data to be plotted
    :param year: list of years to be plotted
    :param title: title of plot
    :return: N/A
    """
    try:
        counter = 0
        # get plot information
        axs, cmap, fig, im, ncol, normalizer, nrow = plotting.create_subplots(
            dataframe=dataframe,
            inner_loop_set=year,
            products=[""],
            year=year,
            SSP=["SSP1"],
            product_column="",
            title=title)

        # iterate through all subplots
        for j in year:
            subplot_title = str(j)
            plotting.get_df_to_plot(
                dataframe=dataframe,
                ncol=ncol,
                nrow=nrow,
                fig=fig,
                axs=axs,
                cmap=cmap,
                normalizer=normalizer,
                counter=counter,
                column="",
                products="",
                SSPs="SSP1",
                years=j,
                subplot_title=subplot_title)
            counter = counter + 1

        # update the figure with shared colorbar
        dl = len(year)
        lab = ""
        plotting.add_colorbar_and_plot(axs, dl, fig, im, lab, ncol, nrow)
    except ValueError as e:
        print(e)


def nutrient_spatial_analysis(supply, land, version):
    """
    conducts a spatial andlysis of nutrient needs by crops
    :param supply: supply of biochar
    :param land: land area devoted to crops
    :param version: scenario name
    :return: .csv files containing nutrient supplies and demands by region
    """
    # get nutrient demands in kg/ha
    released_nutrients = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_agRecommendedNutrientRates.csv")
    # remove header rows
    released_nutrients = released_nutrients.loc[9:]
    released_nutrients.columns = released_nutrients.iloc[0]
    released_nutrients = released_nutrients.drop(released_nutrients.index[0])
    # remove extra columns
    released_crop_nutrients = released_nutrients[["GCAM_commodity", "Commodity_Median_P", "Commodity_Median_K"]]
    released_crop_nutrients = released_crop_nutrients.drop_duplicates()
    released_crop_nutrients = released_crop_nutrients.astype(
        {'Commodity_Median_P': 'float', 'Commodity_Median_K': 'float'})
    # merge nutrient requirements to land supply
    land_nutrients = pd.merge(land, released_crop_nutrients, "left", left_on=["LandLeaf"],
                              right_on=["GCAM_commodity"])
    # calculate P and K requirements by year
    for i in c.GCAMConstants.biochar_x:
        conversion_factor = 1e-9 * 100000  # kg/ha to Mt/thousand km^2
        land_nutrients[str(i) + "_P"] = land_nutrients[str(i)] * land_nutrients[
            "Commodity_Median_P"] * conversion_factor
        land_nutrients[str(i) + "_K"] = land_nutrients[str(i)] * land_nutrients[
            "Commodity_Median_K"] * conversion_factor

    # nutrient demands by crop/region
    P_demand_crop_region = land_nutrients.groupby(["GCAM", "LandLeaf"])[[str(i) + "_P" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_demand_crop_region = land_nutrients.groupby(["GCAM", "LandLeaf"])[
        [str(i) + "_K" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_demand_crop_region.to_csv("gcam/input/gcamdata/inst/extdata/aglu/P_demand_crop_region_" + version + ".csv")
    K_demand_crop_region.to_csv("gcam/input/gcamdata/inst/extdata/aglu/K_demand_crop_region_" + version + ".csv")

    land_nutrients = data_manipulation.group(land_nutrients, ["GCAM"])  # group nutrient demands by GCAM region
    # for each year with biochar, calculate supply of nutrients
    for i in c.GCAMConstants.biochar_x:
        supply[str(i) + "_C"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "C", str(i)), axis=1)
        supply[str(i) + "_P"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "P", str(i)), axis=1)
        supply[str(i) + "_K"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "K", str(i)), axis=1)
        supply[str(i) + "_biochar"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "K", str(i), biochar=True), axis=1)
    # group amounts by region and process dataframe
    C_supply = supply.groupby("GCAM")[[str(i) + "_C" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_supply = supply.groupby("GCAM")[[str(i) + "_P" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_supply = supply.groupby("GCAM")[[str(i) + "_K" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    biochar_supply = supply.groupby("GCAM")[[str(i) + "_biochar" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_demand = land_nutrients.groupby("GCAM")[[str(i) + "_P" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_demand = land_nutrients.groupby("GCAM")[[str(i) + "_K" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    C_supply.columns = C_supply.columns.str.rstrip("_C")
    P_supply.columns = P_supply.columns.str.rstrip("_P")
    K_supply.columns = K_supply.columns.str.rstrip("_K")
    biochar_supply.columns = biochar_supply.columns.str.rstrip("_biochar")
    P_demand.columns = P_demand.columns.str.rstrip("_P")
    K_demand.columns = K_demand.columns.str.rstrip("_K")
    C_supply["Units"] = "Mt"
    P_supply["Units"] = "Mt"
    K_supply["Units"] = "Mt"
    P_demand["Units"] = "Mt"
    K_demand["Units"] = "Mt"
    P_merged = pd.merge(P_supply, P_demand, on=["GCAM"], suffixes=("_supply", "_demand"))
    K_merged = pd.merge(K_supply, K_demand, on=["GCAM"], suffixes=("_supply", "_demand"))

    for i in c.GCAMConstants.biochar_x:
        # calculate excess nutrient supply relative to demand
        P_merged[str(i) + "_diff"] = (P_merged[str(i) + "_supply"] - P_merged[str(i) + "_demand"])
        K_merged[str(i) + "_diff"] = (K_merged[str(i) + "_supply"] - K_merged[str(i) + "_demand"])

        # calculate ratio of nutrient supply to demand
        P_merged[str(i) + "_ratio"] = (P_merged[str(i) + "_supply"] - P_merged[str(i) + "_demand"]) / P_merged[
            str(i) + "_demand"]
        K_merged[str(i) + "_ratio"] = (K_merged[str(i) + "_supply"] - K_merged[str(i) + "_demand"]) / K_merged[
            str(i) + "_demand"]
    # plot nutrient differences by year
    P_diff = P_merged.groupby("GCAM")[[str(i) + "_diff" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_diff.columns = P_diff.columns.str.rstrip("_diff")
    P_diff["Units"] = "Mt"
    plot_world(P_diff, c.GCAMConstants.biochar_x, "P supply in biochar - P demand (Mt)")
    P_diff.to_csv("data/data_analysis/P_diff_" + version + ".csv")
    K_diff = K_merged.groupby("GCAM")[[str(i) + "_diff" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_diff.columns = K_diff.columns.str.rstrip("_diff")
    K_diff["Units"] = "Mt"
    plot_world(K_diff, c.GCAMConstants.biochar_x, "K supply in biochar - K demand (Mt)")
    K_diff.to_csv("data/data_analysis/K_diff_" + version + ".csv")

    # process P/K ratios and output to csv
    P_ratio = P_merged.groupby("GCAM")[[str(i) + "_ratio" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_ratio.columns = P_ratio.columns.str.rstrip("_ratio")
    P_ratio["Units"] = "Mt"
    P_ratio.to_csv("data/data_analysis/P_ratio_" + version + ".csv")
    K_ratio = K_merged.groupby("GCAM")[[str(i) + "_ratio" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_ratio.columns = K_ratio.columns.str.rstrip("_ratio")
    K_ratio["Units"] = "Mt"
    K_ratio.to_csv("data/data_analysis/K_ratio_" + version + ".csv")

    # process C supply and output to csv
    C_supply.to_csv("data/data_analysis/C_supply" + version + ".csv")
    P_supply.to_csv("data/data_analysis/P_supply" + version + ".csv")
    K_supply.to_csv("data/data_analysis/K_supply" + version + ".csv")
    biochar_supply.to_csv("data/data_analysis/biochar_supply" + version + ".csv")


def nutrient_supply_scenarios():
    """
    reads in data from stored .csv files to prepare nutrient spatial analysis calculation scenarios
    :return: N/A
    """
    # with hypothetical data
    products = ["Beef", "Pork", "Dairy", "SheepGoat", "Poultry"]
    released_supply = pd.read_csv("data/gcam_out/released/2p6/original/supply_of_all_markets.csv")
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    released_supply = released_supply[released_supply[['SSP']].isin(["SSP1"]).any(axis=1)]
    released_supply = released_supply[~released_supply[['GCAM']].isin(["global"]).any(axis=1)]
    # get land area in thousand km2
    released_land = pd.read_csv("data/gcam_out/released/2p6/original/detailed_land_allocation.csv")
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_land_crops(row), axis=1)
    released_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf"])
    released_land = released_land[~released_land[['GCAM']].isin(["global"]).any(axis=1)]
    nutrient_spatial_analysis(released_supply, released_land, "hypothetical")

    # with existing data
    products = ["beef manure", "pork manure", "dairy manure", "poultry manure", "goat manure"]
    biochar_supply = pd.read_csv("data/gcam_out/test/2p6/masked/supply_of_all_markets.csv")
    biochar_supply = biochar_supply[biochar_supply[['product']].isin(products).any(axis=1)]
    biochar_supply = biochar_supply[biochar_supply[['SSP']].isin(["SSP1"]).any(axis=1)]
    biochar_supply = biochar_supply[~biochar_supply[['GCAM']].isin(["global"]).any(axis=1)]
    # get land area in thousand km2
    biochar_land = pd.read_csv("data/gcam_out/test/2p6/masked/detailed_land_allocation.csv")
    biochar_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_land_crops(row), axis=1)
    biochar_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf"])
    biochar_land = biochar_land[~biochar_land[['GCAM']].isin(["global"]).any(axis=1)]
    nutrient_spatial_analysis(biochar_supply, biochar_land, "3Mg_ha")


def nutrient_limit(row, year):
    """
    identifies the limiting nutrient
    :param row: row in pandas dataframe
    :param year: year in GCAM model
    :return: the nutrient that limits biochar application
    """
    # if demand ratio < supply ratio, limit on P
    # else limit on K
    if row[str(year) + "_demand"] > row[str(year) + "_supply"]:
        return "K"
    return "P"


def biochar_rate(row, year):
    """
    calculates the biochar application rate depending on the limiting nutrient
    :param row: row in pandas dataframe
    :param year: GCAM model year
    :return: supply of biochar necessary to meet land requirements for limited nutrient
    """
    # Mt / unitless = Mt
    return row[str(year) + "_P"] / row[str(year) + "_P_frac"] if row[str(year) + "limit"] == "P" else row[str(year) + "_K"] / row[str(year)]


def biochar_application_rate_calculations():
    """
    calculates biochar application rate based on nutrient demands by crop in different land regions by year
    :return: N/A
    """
    P_supply = pd.read_csv("data/data_analysis/P_supplyhypothetical.csv")  # Mt
    K_supply = pd.read_csv("data/data_analysis/K_supplyhypothetical.csv")
    P_K_supply = pd.merge(P_supply, K_supply, how="left", on="GCAM", suffixes=("_P", "_K"))
    for i in c.GCAMConstants.biochar_x:
        P_K_supply[str(i) + "_PK-ratio"] = P_K_supply[str(i) + "_P"] / P_K_supply[str(i) + "_K"]
    P_K_supply = P_K_supply.groupby("GCAM")[
        [str(i) + "_PK-ratio" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_K_supply.columns = P_K_supply.columns.str.rstrip("_PK-ratio")  # P/K of the supply of biochar
    # demand is crop specific - supply is not
    P_demand = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/P_demand_crop_region_hypothetical.csv")  # Mt
    K_demand = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/K_demand_crop_region_hypothetical.csv")
    P_K_demand = pd.merge(P_demand, K_demand, how="left", on=["GCAM", "LandLeaf"], suffixes=("_P", "_K"))
    for i in c.GCAMConstants.biochar_x:
        P_K_demand[str(i) + "_PK-ratio"] = P_K_demand[str(i) + "_P"] / P_K_demand[str(i) + "_K"]
    P_K_demand = P_K_demand.groupby(["GCAM", "LandLeaf"])[
        [str(i) + "_PK-ratio" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_K_demand.columns = P_K_demand.columns.str.rstrip("_PK-ratio")  # P/K of the demand of biochar
    PK_ratios = pd.merge(P_K_demand, P_K_supply, how="left", on="GCAM", suffixes=("_demand", "_supply"))
    for i in c.GCAMConstants.biochar_x:
        PK_ratios[str(i) + "limit"] = PK_ratios.apply(lambda row: nutrient_limit(row, i), axis=1)

    # get P, K, C, biochar supply by region
    biochar_supply = pd.read_csv("data/data_analysis/biochar_supplyhypothetical.csv")  # Mt
    # get P/K as fraction of biochar
    P_frac = pd.merge(biochar_supply, P_supply, how="left", on="GCAM", suffixes=("_biochar", "_P"))
    K_frac = pd.merge(biochar_supply, K_supply, how="left", on="GCAM", suffixes=("_biochar", "_K"))
    # calculate fraction for each time period
    for i in c.GCAMConstants.biochar_x:
        P_frac[str(i)] = P_frac[str(i) + "_P"] / P_frac[str(i) + "_biochar"]
        K_frac[str(i)] = K_frac[str(i) + "_K"] / K_frac[str(i) + "_biochar"]
    # get mean fraction
    P_frac = P_frac.groupby("GCAM")[[str(i) for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_frac = K_frac.groupby("GCAM")[[str(i) for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    # divide demand by P or K fraction depending by limiting factor to get biochar rates
    nutrient_demand = pd.merge(P_demand, K_demand, how="left", on=["GCAM", "LandLeaf"])
    nutrient_demand = pd.merge(nutrient_demand, PK_ratios, how="left", on=["GCAM", "LandLeaf"])
    nutrient_demand = pd.merge(nutrient_demand, K_frac, how="left", on="GCAM")
    nutrient_demand = pd.merge(nutrient_demand, P_frac, how="left", on="GCAM", suffixes=("", "_P_frac"))
    for i in c.GCAMConstants.biochar_x:
        nutrient_demand[str(i) + "_biochar_demand"] = nutrient_demand.apply(lambda row: biochar_rate(row, i), axis=1)
    biochar_demand = nutrient_demand.groupby(["GCAM", "LandLeaf"])[
        [str(i) + "_biochar_demand" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    biochar_demand["Units"] = "Mt biochar"
    released_land = pd.read_csv("data/gcam_out/released/2p6/original/detailed_land_allocation.csv")
    released_land["LandLeaf"] = released_land.apply(lambda row: data_manipulation.relabel_land_crops(row), axis=1)
    released_land = data_manipulation.group(released_land, ["GCAM", "LandLeaf"])
    released_land = released_land[~released_land[['GCAM']].isin(["global"]).any(axis=1)]
    biochar_app_rate = pd.merge(biochar_demand, released_land, how="left", on=["GCAM", "LandLeaf"])
    for i in c.GCAMConstants.biochar_x:
        # [Mt / 1000 km2] / [ha / 1000 km2] * [kg/Mt]
        biochar_app_rate[str(i) + "_app_rate"] = biochar_demand[str(i) + "_biochar_demand"] / biochar_app_rate[
            str(i)] / 100000 * 1e9
    biochar_app_rate = biochar_app_rate.groupby(["GCAM", "LandLeaf"])[
        [str(i) + "_app_rate" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    biochar_app_rate["Units"] = "kg/ha"
    biochar_app_rate.columns = biochar_app_rate.columns.str.rstrip("_app_rate")
    biochar_app_rate.to_csv("gcam/input/gcamdata/inst/extdata/aglu/A_AgBiocharApplicationRateYrCropLand.csv")


if __name__ == '__main__':
    # get supply of animal products
    # nutrient_supply_scenarios()

    # calculate ratio of P / K in supply and demand
    biochar_application_rate_calculations()
