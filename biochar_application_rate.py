import math

import matplotlib.pyplot as plt
import constants as c
import pandas as pd
import numpy as np
import data_manipulation
import plotting


def nutrient_supply(row, product, nutrient, year):
    """
    calculates the nutrient supply based on the supply of animal products
    :param row: row in a pandas dataframe
    :param product: product used as the basis for calculation, with the gompertz function being added to calculations based on supply of animal products
    :param nutrient: nutrient applied to the field
    :param year: year of supply
    :return: supply of the nutrient in Mt
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
            # 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
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
    return row[year] * biochar_yields * biochar_to_nutrient * manure_yields


def gompertz(year):
    return 1*math.exp(-11*math.exp(-0.25*(int(year)-2028)))


def plot_world(dataframe, year, title):
    try:
        counter = 0
        units = "N/A"
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
            units = plotting.get_df_to_plot(
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
    land_nutrients = data_manipulation.group(land_nutrients, ["GCAM"])  # group nutrient demands by GCAM region
    # for each year with biochar, calculate supply of nutrients
    for i in c.GCAMConstants.biochar_x:
        supply[str(i) + "_C"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "C", str(i)), axis=1)
        supply[str(i) + "_P"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "C", str(i)), axis=1)
        supply[str(i) + "_K"] = supply.apply(
            lambda row: nutrient_supply(row, 'product', "C", str(i)), axis=1)
    # group amounts by region and process dataframe
    C_supply = supply.groupby("GCAM")[[str(i) + "_C" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_supply = supply.groupby("GCAM")[[str(i) + "_P" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_supply = supply.groupby("GCAM")[[str(i) + "_K" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    P_demand = land_nutrients.groupby("GCAM")[[str(i) + "_P" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    K_demand = land_nutrients.groupby("GCAM")[[str(i) + "_K" for i in c.GCAMConstants.biochar_x]].sum().reset_index()
    C_supply.columns = C_supply.columns.str.rstrip("_C")
    P_supply.columns = P_supply.columns.str.rstrip("_P")
    K_supply.columns = K_supply.columns.str.rstrip("_K")
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

    #TODO: process P/K ratios and output to csv
    #TODO: process C supply and output to csv


if __name__ == '__main__':
    # get supply of animal products
    #TODO extract method
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

    # TODO load in P/K ratios
    # TODO combine dataframes, take 1 - minimum ratio, multiply by biochar C to get excess biochar
    # TODO get crop-specific biochar application rates in kg/ha

