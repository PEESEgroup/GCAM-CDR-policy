import numpy as np
import constants as c
import pandas as pd


def flat_difference(old, new, columns):
    """
    Calculates the flat difference between two dataframes (new - old)
    :param old: the old dataframe
    :param new: the new dataframe
    :param columns: the list of columns that will uniquely identify each product
    :return: a combined dataframe
    """
    # get values from dataframes
    merged = old.merge(new, how="left", on=columns, suffixes=("_left", "_right"))

    for i in c.GCAMConstants.x:
        merged[str(i)] = merged[str(i) + "_right"] - merged[str(i) + "_left"]
        merged = merged.drop([str(i) + "_left"], axis=1)

    # update the version name
    merged['Version'] = "flat diff between " + str(merged['Version_right'][0]) + " and " + str(
        merged['Version_left'][0])
    merged = merged.drop(['Version_right'], axis=1)
    merged = merged.drop(['Version_left'], axis=1)

    # fix the column names
    merged.columns = merged.columns.str.replace("_left", '')
    merged = merged[c.GCAMConstants.column_order]

    return merged


def percent_difference(old, new, columns):
    """
    calculates the percent difference between two dataframes
    :param old: the old dataframe
    :param new: the new dataframe
    :param columns: the columns necessary to uniquely identify a product
    :return: a dataframe containing the percent change between the dataframes
    """
    # get values from dataframes
    merged = old.merge(new, how="left", on=columns, suffixes=("_left", "_right"))

    for i in c.GCAMConstants.x:
        merged[str(i)] = 100 * (merged[str(i) + "_right"] - merged[str(i) + "_left"]) / (
                merged[str(i) + "_left"] + 1e-7)
        merged = merged.drop([str(i) + "_left"], axis=1)

    # update columns
    merged = merged.drop(['Units_left'], axis=1)
    merged = merged.drop(['Units_right'], axis=1)
    merged['Units'] = '%'
    merged['Version'] = "% diff between " + str(merged['Version_right'][0]) + " and " + str(merged['Version_left'][0])

    # replace columns
    merged.columns = merged.columns.str.replace("_left", '')
    merged = merged[c.GCAMConstants.column_order]

    return merged


def percent_of_total(old, new, columns):
    """
    calculates the percent difference between two dataframes
    :param old: the old dataframe
    :param new: the new dataframe
    :param columns: the columns necessary to uniquely identify a product
    :return: a dataframe containing the percent change between the dataframes
    """
    # get values from dataframes
    merged = old.merge(new, how="left", on=columns, suffixes=("_left", "_right"))
    df = pd.DataFrame()

    for j in c.GCAMConstants.SSPs:
        for k in merged["GCAM"].unique().tolist():
            merged_filter = merged[(merged['SSP'].isin([j])) & (merged['GCAM'].isin([k]))]  # filter by region
            for i in c.GCAMConstants.x:
                sum_col = merged_filter[str(i) + "_left"].sum()
                merged_filter = merged_filter.assign(
                    e=100 * (merged_filter[str(i) + "_right"] - merged_filter[str(i) + "_left"]) / sum_col)
                merged_filter[str(i)] = merged_filter["e"]
                merged_filter = merged_filter.drop([str(i) + "_left"], axis=1)
                merged_filter = merged_filter.drop([str(i) + "_right"], axis=1)

                if k == "Global" and str(i) == "2050":
                    print("total is", sum_col, "thousand sq km in", j)
                    merged_filter["GCAM"] = "Global (net)"

            merged_filter.drop(["e"], axis=1)
            df = pd.concat([df, merged_filter])

    # update columns
    df = df.drop(['Units_left'], axis=1)
    df = df.drop(['Units_right'], axis=1)
    df['Units'] = '%'
    df['Version'] = "% diff of the total"

    # replace columns
    df.columns = df.columns.str.replace("_left", '')
    df = df[c.GCAMConstants.column_order]

    return df


def group(df, columns):
    """
    Groups a dataframe with may subproducts into a single line
    :param df: the dataframe being grouped
    :param columns: the list of columns used to form a group
    :return: a dataframe with grouped entries
    """
    unit = df.groupby(columns).first().reset_index()["Units"]
    df = df.groupby(columns).sum()
    df = df.reset_index()
    df['Units'] = unit
    return df


def flat_summation(old, new, columns):
    """
    Calculates the flat element-wise summation between two dataframes
    :param old: the old dataframe
    :param new: the new dataframe
    :param columns: the list of columns that will uniquely identify each product
    :return: a combined dataframe
    """
    # get values from dataframes
    merged = old.merge(new, how="left", on=columns, suffixes=("_left", "_right"))

    for i in c.GCAMConstants.x:
        merged[str(i)] = merged[str(i) + "_right"] + merged[str(i) + "_left"]
        merged = merged.drop([str(i) + "_left"], axis=1)

    # update the version name
    merged['Version'] = "flat diff between " + str(merged['Version_right'][0]) + " and " + str(
        merged['Version_left'][0])
    merged = merged.drop(['Version_right'], axis=1)
    merged = merged.drop(['Version_left'], axis=1)

    # fix the column names
    merged.columns = merged.columns.str.replace("_left", '')
    merged = merged[c.GCAMConstants.column_order]

    return merged


def label_year(row):
    """
    identifies the year of maximum disruption
    :param row: a pd Series from a dataframe
    :return: the index of the maximum disruption value
    """
    row = row.iloc[:len(c.GCAMConstants.x)]
    max_val = row.max()
    min_val = row.min()
    if abs(min_val) > max_val:
        return row.idxmin()
    else:
        return row.idxmin()


def label_disruption(row):
    """
    gets the information for the maximum disruption
    :param row: pd Series containing a row from a dataframe
    :return: the value that is the furthest distances away from zero change
    """
    row = row.iloc[:len(c.GCAMConstants.x)]
    max_val = row.max()
    min_val = row.min()
    if abs(min_val) > max_val:
        return min_val
    else:
        return max_val


def label_supply_in_year(row):
    """
    function to get the amount of supply in the year of maximum disruption
    :param row: pd Series of a row in the dataframe
    :return: the supply in the yeart of maximum disruption
    """
    return row[str(row['year']) + "_right"]


def years_to_maximum_disruption(difference_dataframe, supply_dataframe, SSP, products, product_column):
    """
    calculates the year in which the maximum disruption, or change between released model and pyrolysis model occurs
    :param difference_dataframe: the dataframe with the differences between model versions
    :param supply_dataframe: the supply in the released model
    :param SSP: the SSP being evaluated
    :param products: the products being evaluated
    :param product_column: the column containing the relevant products
    :return: the dataframe containing this additional information
    """
    # at this stage, if this df is empty, then we know that there is no material to plot
    df = difference_dataframe[
        (difference_dataframe['SSP'].isin(SSP)) & (difference_dataframe[product_column].isin(products))]
    df2 = supply_dataframe[(supply_dataframe['SSP'].isin(SSP)) & (supply_dataframe[product_column].isin(products))]
    df = pd.merge(df, df2, on=["SSP", "GCAM", "technology"], how="left", suffixes=("", "_right"))

    df['disruption'] = df.apply(lambda row: label_disruption(row), axis=1)
    df['year'] = df.apply(lambda row: label_year(row), axis=1)
    df['supply_at_year'] = df.apply(lambda row: label_supply_in_year(row), axis=1)

    return df


def change_between_years(dataframe):
    """
    calculates the amount of change between adjacent years for a given dataframe
    :param dataframe: the dataframe containing data
    :return: a dataframe with additional columns for rates of change of product value between years
    """
    for i in c.GCAMConstants.x:
        if i != 1990 and i != 2005:
            dataframe[str(i - 5) + "-" + str(i)] = (dataframe[str(i)] - dataframe[str(i - 5)])
    return dataframe


def percentage_change_between_years(dataframe):
    """
    calculates the percentage change between adjacent years for a given dataframe
    :param dataframe: the dataframe containing data
    :return: a dataframe with additional columns for rates of change of product value between years
    """
    for i in c.GCAMConstants.x:
        if i != 1990 and i != 2005:
            dataframe[str(i - 5) + "-" + str(i)] = 100 * (dataframe[str(i)] - dataframe[str(i - 5)]) / (
                dataframe[str(i - 5)])
    return dataframe


def label_fuel_tech(row, column, products):
    """
    relabels similar technologies to enable grouping
    :param row: a pd Series from a dataframe
    :param column: the column of the pd series being searched
    :param products: the list of suffixes to remove
    :return: the relabeled technology
    """
    for i in products:
        if i in row[column]:
            to_return = row[column].rstrip(i)
            if to_return == "cellulosic ethano":  # dunno why rstrip removes an extra character for cellulosic ethanol
                return "cellulosic ethanol"
            return to_return
    return row[column]


def label_sequestration_sectors(row):
    """
    returns the aggregated sector to better show plots
    :param row: row of a pandas dataframe
    :return: aggregated sector or original one
    """
    if row['sector'] in ["H2 central production", "H2 wholesale dispensing"]:
        return "hydrogen"
    elif row['sector'] in ["backup_electricity", "district heat", "refining"]:
        return "other energy sector"
    elif row['sector'] in ["chemical energy use", "chemical feedstocks", "N fertilizer", "alumina", "cement",
                           "iron and steel", "other industrial energy use", "other industrial feedstocks",
                           "process heat cement"]:
        return "industrial energy use"
    elif row['sector'] in ["comm cooling", "comm heating", "comm others"]:
        return "commercial energy use"
    elif row['sector'] in ["elec_biomass (IGCC CCS)", "elec_biomass (IGCC)", "elec_biomass (conv CCS)",
                           "elec_biomass (conv)"]:
        return "electricity - biomass"
    elif row['sector'] in ["elec_coal (IGCC CCS)", "elec_coal (IGCC)", "elec_coal (conv pul CCS)",
                           "elec_coal (conv pul)"]:
        return "electricity - coal"
    elif row['sector'] in ["elec_gas (CC CCS)", "elec_gas (CC)", "elec_gas (steam/CT)"]:
        return "electricity - gas"
    elif row['sector'] in ["elec_refined liquids (CC CCS)", "elec_refined liquids (CC)",
                           "elec_refined liquids (steam/CT)"]:
        return "electricity - refined liquids"
    elif row['sector'] in ["gas pipeline", "gas processing"]:
        return "gas processing"
    elif row['sector'] in ["resid cooling", "resid heating", "resid others"]:
        return "commercial energy use"
    elif row['sector'] in ["trn_aviation_intl", "trn_freigh", "trn_freight_road", "trn_pass", "trn_pass_road",
                           "trn_pass_road_LDV", "trn_pass_road_LDV_4W", "trn_shipping_intl", "trn_freight"]:
        return "transportation"
    elif row['sector'] in ['regional biomass', 'regional biomassOil', "regional corn for ethanol",
                           "regional sugar for ethanol"]:
        return "other biomass for refining"
    else:
        return row['sector']


def remove__(row, column):
    """
    relabels similar technologies to enable grouping
    :param row: a pd Series from a dataframe
    :param column: the column of the pd series being searched
    :return: the relabeled technology
    """
    to_return = row[column].replace("_", " ")
    return to_return


def relabel_region(row):
    """
    lambda function to relabel GCAM regions for greater accessibility
    :param row: row of data
    :return: updated name of GCAM region
    """
    GCAM_region = row["GCAM"]
    matches = ["Argentina", "Brazil", "Canada", "Central America and Caribbean", "Central Asia", "China",
               "Colombia", "European Free Trade Association", "India", "Indonesia", "Mexico",
               "Japan", "Middle East", "Pakistan", "Russia", "South Africa", "South Asia",
               "Southeast Asia", "South Korea", "Taiwan", "USA", "Global"]
    if any(x in GCAM_region for x in matches):
        return GCAM_region
    elif GCAM_region == "Middle East":
        return "Middle East"
    elif GCAM_region == "Indonesia":
        return "Indonesia"
    elif GCAM_region == "Global":
        return "Global"
    elif "Africa_Eastern" == GCAM_region:
        return "Eastern Africa"
    elif "Africa_Northern" == GCAM_region:
        return "Northern Africa"
    elif "Africa_Southern" == GCAM_region:
        return "Southern Africa"
    elif "Africa_Western" == GCAM_region:
        return "Western Africa"
    elif "Australia_NZ" == GCAM_region:
        return "Australia, New Zealand"
    elif "EU-12" == GCAM_region:
        return "Northeastern EU"
    elif "EU-15" == GCAM_region:
        return "Western EU"
    elif "Europe_Eastern" == GCAM_region:
        return "Eastern Europe"
    elif "Europe_Non_EU" == GCAM_region:
        return "Other Europe"
    elif "South America_Northern" == GCAM_region:
        return "Northern South America"
    elif "South America_Southern" == GCAM_region:
        return "Southern South America"
    elif "Global (net)" == GCAM_region:
        return "Global (net)"
    else:
        return "error"


def relabel_land_use(row):
    """
    lambda function to relabel GCAM LandLeaf for greater accessibility. From: https://jgcri.github.io/gcam-doc/land.html
    :param row: row of data
    :return: updated name of GCAM region
    """
    luc = row["LandLeaf"]
    matches = ["crops"]
    if any(x in luc for x in matches):
        return luc
    elif luc == "biomass":
        return "biomass for energy"
    elif luc == "grass":
        return "grass land"
    elif luc == "shrub":
        return "shrub land"
    elif "forest (managed)" == luc:
        return "commercial forest"
    elif "forest (unmanaged)" == luc:
        return "forest"
    elif "pasture (grazed)" == luc:
        return "intensively-grazed pasture"
    elif "pasture (other)" == luc:
        return "other pasture"
    elif "otherarable" == luc:
        return "other arable land"
    else:
        return luc


def relabel_food(row):
    """
    lambda function to relabel GCAM food categories for greater accessibility. From: A_demand_technology.csv
    :param row: row of data
    :return: updated name of GCAM region
    """
    food = row["technology"]
    matches = ["Corn", "Rice", "Wheat"]
    if any(x in food for x in matches):
        return food
    elif food == "Fruits" or food == "Vegetables":
        return "Fruits and Vegetables"
    elif food == "Legumes" or food == "NutsSeeds":
        return "Plant Protein"
    elif food == "Soybean" or food == "OilCrop" or food == "OilPalm":
        return "Plant Oils"
    elif "FiberCrop" == food:
        return "Fiber Crops"
    elif "MiscCrop" == food:
        return "Other Crops"
    elif "OtherGrain" == food:
        return "Other Grains"
    elif "RootTuber" == food:
        return "Roots and Tubers"
    elif "Beef" == food or "Dairy" == food or "Pork" == food or "Poultry" == food or "SheepGoat" == food or "OtherMeat_Fish" == food:
        return "Animal Protein"
    else:
        return food


def relabel_food_demand(row):
    """
    lambda function to relabel GCAM food demand categories for greater accessibility.
    :param row: row of data
    :return: updated name of GCAM region
    """
    food = row["input"]  # Products in staples vs. non staples in A_demand_subsector.csv
    if food == "FoodDemand_NonStaples":
        return "Non-Staples"
    elif food == "FoodDemand_Staples":
        return "Staples"
    else:
        return "error"


def relabel_fertilizer_product(row):
    """
    lambda function to relabel GCAM food demand categories for greater accessibility.
    :param row: row of data
    :return: updated name of GCAM region
    """
    input = row["subsector"]
    if input == "beef_biochar" or input == "dairy_biochar" or input == "goat_biochar" or input == "pork_biochar" or input == "poultry_biochar":
        return "biochar"
    elif input == "gas" or input == "refined liquids" or input == "coal":
        return "fossil fuels"
    else:
        return input

