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


def group(df, columns):
    """
    Groups a dataframe with may subproducts into a single line
    :param df: the dataframe being grouped
    :param columns: the list of columns used to form a group
    :return: a dataframe with grouped entries
    """
    unit = df['Units'].unique()[0]
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
    df = difference_dataframe[(difference_dataframe['SSP'].isin(SSP)) & (difference_dataframe[product_column].isin(products))]
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
            dataframe[str(i-5) +"-" + str(i)] = (dataframe[str(i)] - dataframe[str(i-5)])
    return dataframe


def percentage_change_between_years(dataframe):
    """
    calculates the percentage change between adjacent years for a given dataframe
    :param dataframe: the dataframe containing data
    :return: a dataframe with additional columns for rates of change of product value between years
    """
    for i in c.GCAMConstants.x:
        if i != 1990 and i != 2005:
            dataframe[str(i-5) +"-" + str(i)] = 100*(dataframe[str(i)] - dataframe[str(i-5)])/(dataframe[str(i-5)])
    return dataframe

def label_fuel_tech(row, column, products):
    """
    identifies the year of maximum disruption
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
