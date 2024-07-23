import matplotlib.pyplot as plt
import constants as c
import pandas as pd
import numpy as np
import data_manipulation
import plotting


def get_app_rate(row, product, biochar, nutrient, year, land):
    biochar_to_nutrient = 0
    feedstock = row[product]
    if feedstock == "Beef":
        if nutrient == "C":
            # 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
            biochar_to_nutrient = .396
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "Dairy":
        if nutrient == "C":
            # 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
            biochar_to_nutrient = .396
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .001754
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .009630
    if feedstock == "SheepGoat":
        if nutrient == "C":
            # 9: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
            biochar_to_nutrient = .420
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C # same as beef
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "Pork":
        if nutrient == "C":
            # 9: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
            biochar_to_nutrient = .386
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C # same as beef
            biochar_to_nutrient = .003115
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = 0.033477
    if feedstock == "Poultry":
        if nutrient == "C":
            # 4: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
            biochar_to_nutrient = .762
        elif nutrient == "P":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .030555
        elif nutrient == "K":
            # element info taken from Enders et al. 2012 at 500 C
            biochar_to_nutrient = .048616

    # Mt animal product * Mt biochar/Mt animal product * Mt nutrient/Mt biochar * 1e6 Mg / Mt) / (thousand km2 * hectares/thousand km2)
    return row[year] * row[biochar] * biochar_to_nutrient * 1e6 / (row[land] * 100000) if row[land] != 0 else np.nan


def plot_world(dataframe, year, title):
    try:
        counter = 0
        units = "N/A"
        # get plot information
        axs, cmap, fig, im, ncol, normalizer, nrow = plotting.create_subplots(
            dataframe=dataframe,
            inner_loop_set=year,
            products=[i],
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
                products=i,
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

if __name__ == '__main__':
    # get supply of animal products
    released_supply = pd.read_csv("data/gcam_out/test/2p6/masked/supply_of_all_markets.csv")
    products = ["Beef", "Pork", "Dairy", "Poultry", "SheepGoat"]
    released_supply = released_supply[released_supply[['product']].isin(products).any(axis=1)]
    released_supply = released_supply[released_supply[['SSP']].isin(["SSP1"]).any(axis=1)]
    released_supply = released_supply[~released_supply[['GCAM']].isin(["global"]).any(axis=1)]

    # get hypothetical biochar conversion ratios
    biochar_coef = pd.read_csv("gcam/input/gcamdata/inst/extdata/aglu/A_an_secout - Copy.csv")
    # group by supply sector
    biochar_coef = biochar_coef.groupby("supplysector")[[str(i) for i in c.GCAMConstants.future_x]].mean().reset_index()

    # merge the datasets together
    merged = pd.merge(released_supply, biochar_coef, "left", left_on="product", right_on="supplysector",
                      suffixes=("", "_biochar"))

    # get land area
    released_land = pd.read_csv("data/gcam_out/test/2p6/masked/detailed_land_allocation.csv")
    released_land = released_land[released_land['LandLeaf'].str.contains("biochar")]
    released_land = released_land[released_land[['SSP']].isin(["SSP1"]).any(axis=1)]
    released_land = released_land[released_land['2055'] > 0]
    released_land = data_manipulation.group(released_land, "GCAM") # group by GCAM data
    merged = pd.merge(merged, released_land, "left", left_on="GCAM", right_on="GCAM",
                      suffixes=("", "_land"))

    # for each future year
    for i in c.GCAMConstants.future_x:
        # calculate application rates
        merged[str(i) + "_C"] = merged.apply(
            lambda row: get_app_rate(row, 'product', str(i) + "_biochar", "C", str(i), str(i) + "_land"),
            axis=1)
        merged[str(i) + "_P"] = merged.apply(
            lambda row: get_app_rate(row, 'product', str(i) + "_biochar", "P", str(i), str(i) + "_land"),
            axis=1)
        merged[str(i) + "_K"] = merged.apply(
            lambda row: get_app_rate(row, 'product', str(i) + "_biochar", "K", str(i), str(i) + "_land"),
            axis=1)

    C_rates = merged.groupby("GCAM")[[str(i)+"_C" for i in c.GCAMConstants.future_x]].sum().reset_index()
    P_rates = merged.groupby("GCAM")[[str(i)+"_P" for i in c.GCAMConstants.future_x]].sum().reset_index()
    K_rates = merged.groupby("GCAM")[[str(i)+"_K" for i in c.GCAMConstants.future_x]].sum().reset_index()
    C_rates.columns = C_rates.columns.str.rstrip("_C")
    P_rates.columns = P_rates.columns.str.rstrip("_P")
    K_rates.columns = K_rates.columns.str.rstrip("_K")
    C_rates["Units"] = "Mg/ha"
    P_rates["Units"] = "Mg/ha"
    K_rates["Units"] = "Mg/ha"

    print("P rates Mg/ha")
    print(P_rates[["GCAM", "2055"]])
    print("K rates Mg/ha")
    print(K_rates[["GCAM", "2055"]])

    # map C application rates on cropland, bio-energy land, and both
    plot_world(C_rates, c.GCAMConstants.future_x, "C application rates (Mg/ha)")

    # map P application rates on cropland, bio-energy land, and both
    plot_world(P_rates, c.GCAMConstants.future_x, "P application rates (Mg/ha)")

    # map K application rates on cropland, bio-energy land, and both
    plot_world(K_rates, c.GCAMConstants.future_x, "K application rates (Mg/ha)")

    # graph histogram of C application rates across all years and regions
    C_rates = C_rates[[str(i) for i in c.GCAMConstants.future_x]]
    C_rates = C_rates.melt()
    plt.hist(C_rates["value"])
    plt.title("Histogram of C application rates in all regions in all time periods (Mg/ha)")
    plt.show()

    # graph histogram of P application rates across all years and regions
    P_rates = P_rates[[str(i) for i in c.GCAMConstants.future_x]]
    P_rates = P_rates.melt()
    P_rates['value'] = P_rates['value'] * 1000  # convert from Mg to kg
    plt.hist(P_rates["value"])
    plt.title("Histogram of P application rates in all regions in all time periods (kg/ha)")
    plt.show()

    # graph histogram of K application rates across all years and regions
    K_rates = K_rates[[str(i) for i in c.GCAMConstants.future_x]]
    K_rates = K_rates.melt()
    K_rates['value'] = K_rates['value'] * 1000  # convert from Mg to kg
    plt.hist(K_rates["value"])
    plt.title("Histogram of K application rates in all regions in all time periods (kg/ha)")
    plt.show()
