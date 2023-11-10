import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# global variables
SSPs = ["1", "2", "3", "4", "5"]
RCPs = ["baseline"]
version = ["released", "pyrolysis"]
GCAM_region = ["USA", "Africa_Eastern", "Africa_Northern", "Africa_Southern", "Africa_Western", "Australia_NZ",
               "Brazil", "Canada", "Central America and Caribbean", "Central Asia", "China", "EU-12", "EU-15",
               "Europe_Eastern", "Europe_Non_EU", "European Free Trade Association", "India", "Indonesia", "Japan",
               "Mexico", "Middle East", "Pakistan", "Russia", "South Africa", "South America_Northern",
               "South America_Southern", "South Asia", "South Korea", "Southeast Asia", "Taiwan", "Argentina",
               "Colombia"]


def read_data(file, sector):
    """
    reads in a .csv data file, and returns either all the information, or specific categories, depending on the data source
    :param file: the filename
    :param sector: the sector for which data is acquired
    :return: a pandas dataframe containing the necessary data
    """
    # read in the .csv file with a header
    df = pd.read_csv(file, header=0)

    # drop NA values
    df = df.dropna()

    # check to make sure the first row has a substring that matches the SSP part of the file name
    ssp = file[5:9]

    if ssp not in df.iloc[0, 0]:
        print(file)
        raise ValueError("SSP in filename does not match SSP in data")

    # if the sector doesn't exist, we want all the data to be returned
    if sector == "NA":
        return df
    # our new sectors aren't in the released model, so return nothing
    elif ("biochar" not in sector or "manure" not in sector) and "released" in file:
        return pd.DataFrame()

    # get specific data for certain columns
    df2 = df[df['Market'].str.contains(sector)]
    return df2


def get_data(entries, data_type):
    """
    control code for getting data from the .csv files
    :param entries: the sectors for which data is requested
    :param data_type: the type of data (i.e. price, supply)
    :return: a dictionary of dataframes across all SSPs, RCPs, model versions, and sectors
    """
    # reading in the data into a list of dataframes
    frames = {}
    for i in SSPs:
        for j in RCPs:
            for k in version:
                for l in entries:
                    # read in the data
                    df = read_data("data/SSP" + i + "_" + j + "_" + k + "_" + data_type + ".csv", l)

                    # add the data to the dictionary of data
                    key = "SSP" + i + "_" + j + "_" + k + "_" + l + "_" + data_type
                    frames[key] = df
    return frames


def plot_CO2_conc(data):
    """
    Takes in CO2 concentration data and produces output relevant to a "both"-type variable
    :param data: CO2 concentration data
    :return: 3 plots
    """
    pair_color = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6',
                  '#6a3d9a', '#ffff99', '#b15928']

    for z in range(3):
        i = 0
        for item in data.items():
            # get label
            words = item[0].split("_")
            lab = words[0] + " " + words[1] + " " + words[2]

            # get x data
            x = [col for col in item[1].columns]
            x = x[2:len(x) - 1]

            # convert x data to numeric
            x = [int(temp) for temp in x]

            # get y data
            y = item[1].loc[0, :].values.tolist()
            y = y[2:len(y) - 1]

            # convert y data to numeric
            y = [float(temp) for temp in y]

            if z == 2 or z == 1:
                if i % 2 == 0:
                    # this is the first entry
                    y_2 = y
                else:
                    if z == 1:
                        y = [y[i] - y_2[i] for i in range(len(y))]
                        print("SSP", i, "CO2 diff:", y)
                    else:
                        y = [100 * (y[i] - y_2[i]) / y_2[i] for i in range(len(y))]
                    plt.plot(x, y, label=lab, color=pair_color[i])
            else:
                # identify the right color for the plot
                c = -1
                c += 2 * int(words[0][3])  # converts SSP number
                if words[2] == "released":
                    c -= 1  # 5 SSP runs, so offset released versions

                plt.plot(x, y, label=lab, color=pair_color[c])

            i = i + 1

        plt.xlabel("Year")
        if z == 0:
            plt.ylabel("CO2 concentration (ppm)")
        elif z == 1:
            plt.ylabel("Change in CO2 concentration (ppm)")
        elif z == 2:
            plt.ylabel("Percent change in CO2 concentrtaion")
        plt.legend()
        plt.show()


def plot_sequestration(data):
    """
    Takes in CO2 sequestration data and produces output relevant to a "pyro"-type variable
    :param data: CO2 sequestration data
    :return: figures
    """
    for z in range(2):
        i = 0

        fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
        fig.tight_layout()

        for item in data.items():
            # get label
            words = item[0].split("_")
            lab = words[0]

            if words[2] != "released":
                # get x data
                x = [col for col in item[1].columns]
                x = x[8:len(x) - 1]
                x = [int(temp) for temp in x]

                # get y data
                y = item[1][item[1]["subsector"].str.contains("biochar")]

                # get y data
                y1 = y.values.tolist()
                y_labels = []
                for j in range(len(y1)):
                    y_labels.append(y1[j][1])
                    y1[j] = y1[j][8:len(y1[j]) - 1]
                    y1[j] = [-temp for temp in y1[j]]
                    if z == 1:
                        y1[j] = np.cumsum(y1[j])

                # plot data
                axs[int(i / 3), int(i % 3)].stackplot(x, y1[0], y1[1], y1[2], y1[3], labels=y_labels)
                axs[int(i / 3), int(i % 3)].set_title(lab)
                axs[int(i / 3), int(i % 3)].set_xlabel("year")
                if z == 1:
                    axs[int(i / 3), int(i % 3)].set_ylabel("Cumulative Mt C Sequestration")
                else:
                    axs[int(i / 3), int(i % 3)].set_ylabel("Mt C Sequestration")
                axs[int(i / 3), int(i % 3)].margins(x=0.001)
                handles, labels = axs[int(i / 3), int(i % 3)].get_legend_handles_labels()

                # update the figure counter
                i = i + 1

        fig.legend(handles, labels, loc='lower right')
        fig.delaxes(axs[1, 2])
        plt.show()


def plot_meat(data):
    for z in range(4):
        fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
        fig.tight_layout()

        df = pd.DataFrame()
        col = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080,
               2085, 2090, 2095, 2100, "management", "livestock", "SSP", "version"]

        for item in data.items():
            # get label
            words = item[0].split("_")
            lab = words[0]

            # get x data
            x = [col for col in item[1].columns]
            x = x[5:len(x) - 1]

            # convert x data to numeric
            x = [int(temp) for temp in x]

            # get y data
            management = ['Mixed', 'Pastoral']
            livestock = ['Beef', 'Dairy', 'Pork', 'Poultry']
            for i in management:
                for j in livestock:
                    y = item[1]
                    y = y[(y['sector'] == j) & (y['subsector'] == i)]  # pork and poultry do not have pastoral types
                    y = y.sum(numeric_only=True).values.tolist()
                    print(i, j, y)
                    y.append(i)
                    y.append(j)
                    y.append(words[0])
                    y.append(words[2])
                    df = pd.concat([df, pd.DataFrame([y], columns=col)], ignore_index=True)

        # get the difference between the production method for each livestock between versions for each SSP
        SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
        livestock = ['Beef', 'Dairy', 'Pork', 'Poultry']
        l = 0

        for i in SSPs:
            k = 0
            livestock_d_y_m = []
            livestock_d_y_p = []
            for j in livestock:
                # get individual entries
                y_m_released = df[(df['livestock'] == j) & (df['SSP'] == i) & (df['management'] == 'Mixed') & (
                        df['version'] == 'released')].values.tolist()
                y_p_released = df[(df['livestock'] == j) & (df['SSP'] == i) & (df['management'] == 'Pastoral') & (
                        df['version'] == 'released')].values.tolist()
                y_m_pyro = df[(df['livestock'] == j) & (df['SSP'] == i) & (df['management'] == 'Mixed') & (
                        df['version'] == 'pyrolysis')].values.tolist()
                y_p_pyro = df[(df['livestock'] == j) & (df['SSP'] == i) & (df['management'] == 'Pastoral') & (
                        df['version'] == 'pyrolysis')].values.tolist()
                y_m_released = y_m_released[0][0:len(y_m_released) - 5]
                y_p_released = y_p_released[0][0:len(y_p_released) - 5]
                y_m_pyro = y_m_pyro[0][0:len(y_m_pyro) - 5]
                y_p_pyro = y_p_pyro[0][0:len(y_p_pyro) - 5]

                print(i, j, [a + b - c - d for a, b, c, d in zip(y_m_pyro, y_p_pyro, y_m_released, y_p_released)][10])

                if z == 0:  # base production levels
                    y_labels = [
                        ["Mixed Beef Released", "Pastoral Beef Released", "Mixed Beef Pyrolysis",
                         "Pastoral Beef Pyrolysis"],
                        ["Mixed Dairy Released", "Pastoral Dairy Released", "Mixed Dairy Pyrolysis",
                         "Pastoral Dairy Pyrolysis"],
                        ["Mixed Pork Released", "Pastoral Pork Released", "Mixed Pork Pyrolysis",
                         "Pastoral Pork Pyrolysis"],
                        ["Mixed Poultry Released", "Pastoral Poultry Released", "Mixed Poultry Pyrolysis",
                         "Pastoral Poultry Pyrolysis"]]
                    color_map = [['#393b79', '#5254a3', '#6b6ecf', '#9c9ede'],
                                 ['#637939', '#8ca252', '#b5cf6b', '#cedb9c'],
                                 ['#8c6d31', '#bd9e39', '#e7ba52', '#e7cb94'],
                                 ['#843c39', '#ad494a', '#d6616b', '#e7969c'],
                                 ['#7b4173', '#a55194', '#ce6dbd', '#de9ed6']]
                    axs[int(l / 3), int(l % 3)].plot(x, y_m_released, label=y_labels[k][0], color=color_map[k][0])
                    axs[int(l / 3), int(l % 3)].plot(x, y_p_released, label=y_labels[k][1], color=color_map[k][1])
                    axs[int(l / 3), int(l % 3)].plot(x, y_m_pyro, label=y_labels[k][2], color=color_map[k][2])
                    axs[int(l / 3), int(l % 3)].plot(x, y_p_pyro, label=y_labels[k][3], color=color_map[k][3])
                    axs[int(l / 3), int(l % 3)].set_title(i)
                    axs[int(l / 3), int(l % 3)].set_xlabel("year")
                    k = k + 1
                elif z == 1:  # change in production
                    # calculate change
                    d_y_m = [(b - a) for a, b in zip(y_m_released, y_m_pyro)]
                    d_y_p = [(b - a) for a, b in zip(y_p_released, y_p_pyro)]
                    # prepare for stacked chart
                    livestock_d_y_m.append(d_y_m)
                    livestock_d_y_p.append(d_y_p)
                    k = k + 1
                elif z == 2:  # cumulative change in production
                    d_y_m = [(b - a) for a, b in zip(y_m_released, y_m_pyro)]
                    d_y_p = [(b - a) for a, b in zip(y_p_released, y_p_pyro)]
                    d_y_m = np.cumsum(d_y_m).tolist()
                    d_y_p = np.cumsum(d_y_p).tolist()
                    # prepare for stacked chart
                    livestock_d_y_m.append(d_y_m)
                    livestock_d_y_p.append(d_y_p)
                    k = k + 1
                elif z == 3:  # percentage change in production
                    # calculate change
                    d_y_m = [100 * (b - a) / (a + 1e-7) for a, b in zip(y_m_released, y_m_pyro)]
                    d_y_p = [100 * (b - a) / (a + 1e-7) for a, b in zip(y_p_released, y_p_pyro)]
                    # prepare for stacked chart
                    livestock_d_y_m.append(d_y_m)
                    livestock_d_y_p.append(d_y_p)
                    k = k + 1

            # plot data
            if z != 0:
                y_labels = ["Beef-Mixed", "Dairy-Mixed", "Pork-Mixed", "Poultry-Mixed", "Beef-Pastoral",
                            "Dairy-Pastoral",
                            "Pork-Pastoral", "Poultry-Pastoral"]
                color_map = ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#1f78b4', '#33a02c', '#e31a1c', '#ff7f00']
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_m[0], label=y_labels[0], color=color_map[0])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_m[1], label=y_labels[1], color=color_map[1])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_m[2], label=y_labels[2], color=color_map[2])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_m[3], label=y_labels[3], color=color_map[3])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_p[0], label=y_labels[4], color=color_map[4])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_p[1], label=y_labels[5], color=color_map[5])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_p[2], label=y_labels[6], color=color_map[6])
                axs[int(l / 3), int(l % 3)].plot(x, livestock_d_y_p[3], label=y_labels[7], color=color_map[7])
                axs[int(l / 3), int(l % 3)].set_title(i)
                axs[int(l / 3), int(l % 3)].set_xlabel("year")
                mixed_livestock = pd.DataFrame(livestock_d_y_m)
                pastoral_livestock = pd.DataFrame(livestock_d_y_p)
            if z == 0:
                axs[int(l / 3), int(l % 3)].set_ylabel("Yearly meat production (Mt)")
            elif z == 1:
                axs[int(l / 3), int(l % 3)].set_ylabel("Yearly change in meat production (Mt) (Pyrolysis-Released)")
            elif z == 2:
                axs[int(l / 3), int(l % 3)].set_ylabel("Cumulative change in meat production (Mt) (Pyrolysis-Released)")
            elif z == 3:
                axs[int(l / 3), int(l % 3)].set_ylabel("Percentage change in meat production (Mt) (Pyrolysis-Released)")
            axs[int(l / 3), int(l % 3)].margins(x=0.001)
            handles, labels = axs[int(l / 3), int(l % 3)].get_legend_handles_labels()

            # update the figure counter
            l = l + 1

        fig.legend(handles, labels, loc='lower right')
        fig.delaxes(axs[1, 2])
        plt.show()


def plot_random_stuff(supply):
    products = ["Beef", "Dairy", "Pork", "Poultry"]
    data = [supply]

    # extract supply and price data
    for w in range(1):
        s = pd.DataFrame()
        for item in data[w].items():
            words = item[0].split("_")

            # get x data
            x = [col for col in item[1].columns]
            x = x[2:len(x) - 1]

            # convert x data to numeric
            x = [int(temp) for temp in x]

            # get y data
            y = item[1]
            y = y[(y['Market'].str.contains(products[0])) | (y['Market'].str.contains(products[1])) |
                  (y['Market'].str.contains(products[2])) | (y['Market'].str.contains(products[3]))]
            y = y.assign(Version=words[2])

            s = pd.concat([s, y])

    d_perc_table = pd.DataFrame()
    d_flat_table = pd.DataFrame()
    col = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080,
           2085, 2090, 2095, 2100, "products", "GCAM_region", "SSP"]

    for j in GCAM_region:
        for k in ["SSP1"]:
            # get specific rows from the data frame
            d_s_r = s[s['Scenario'].str.contains(k) & s['Market'].str.contains(j)
                      & s['Version'].str.contains("released")]
            d_s_p = s[s['Scenario'].str.contains(k) & s['Market'].str.contains(j)
                      & s['Version'].str.contains("pyrolysis")]

            d_s_r = d_s_r.iloc[:, 2:int(len(d_s_r.columns) - 2)]
            d_s_p = d_s_p.iloc[:, 2:int(len(d_s_p.columns) - 2)]

            d_s_r = d_s_r.sum(axis=0).values.tolist()
            d_s_p = d_s_p.sum(axis=0).values.tolist()

            # calculate flat change
            d_s = [b - a for a, b in zip(d_s_r, d_s_p)]
            d_s.append("sum")
            d_s.append(j)
            d_s.append(k)
            d_flat_table = pd.concat([d_flat_table, pd.DataFrame([d_s], columns=col)])

            # calculate percent change
            d_s = [100 * (a - b) / (b + 1e-7) for a, b in zip(d_s_p, d_s_r)]
            d_s.append("sum")
            d_s.append(j)
            d_s.append(k)
            print(j, k, d_s)
            d_perc_table = pd.concat([d_perc_table, pd.DataFrame([d_s], columns=col)])

    print("change in supply table", d_flat_table)
    print("percent change in supply table", d_perc_table)

    years = [2050, 2100]

    # set up world map
    world = get_world()

    # set up plotting data
    d = 0
    data = d_perc_table
    lab = "Percent Change in Supply"
    fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
    cmap = plt.colormaps.get_cmap('viridis')
    normalizer = Normalize(min(data[2050].min(), data[2100].min()), max(data[2050].max(), data[2100].max()))
    im = cm.ScalarMappable(norm=normalizer, cmap=cmap)
    fig.tight_layout()

    for i in years:
        data = d_perc_table[[i, "products", "GCAM_region", "SSP"]]
        merged = pd.merge(world, data, on="GCAM_region", how='left')
        merged = merged.replace("", np.nan)

        merged.plot(column=i, ax=axs[d], cmap=cmap, norm=normalizer)

        axs[d].set_title("Year: " + str(i) + " | All Livestock Products")

        d = d + 1

    # update the figure with shared colorbar
    fig.delaxes(axs[2])
    axins1 = inset_axes(
        axs[2],
        width="40%",  # width: 50% of parent_bbox width
        height="10%",  # height: 5%
        loc="upper center",
    )
    axins1.xaxis.set_ticks_position("bottom")
    fig.colorbar(im, cax=axins1, orientation="horizontal", label=lab)
    plt.show()


def plot_world_meat(supply, price):
    products = ["Beef", "Dairy", "Pork", "Poultry"]
    ssp = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    data = [supply, price]

    # extract supply and price data
    for w in range(2):
        s = pd.DataFrame()
        for item in data[w].items():
            words = item[0].split("_")

            # get x data
            x = [col for col in item[1].columns]
            x = x[2:len(x) - 1]

            # convert x data to numeric
            x = [int(temp) for temp in x]

            # get y data
            y = item[1]
            y = y[(y['Market'].str.contains(products[0])) | (y['Market'].str.contains(products[1])) |
                  (y['Market'].str.contains(products[2])) | (y['Market'].str.contains(products[3]))]
            y = y.assign(Version=words[2])

            s = pd.concat([s, y])

        if w == 0:
            supply_table = s
            print("supply table", s)
        else:
            price_table = s
            print("price table", s)

        d_flat_table = pd.DataFrame()
        d_perc_table = pd.DataFrame()
        col = [1990, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 2055, 2060, 2065, 2070, 2075, 2080,
               2085, 2090, 2095, 2100, "products", "GCAM_region", "SSP"]

        for i in products:
            for j in GCAM_region:
                for k in ssp:
                    # get specific rows from the data frame
                    d_s_r = s[s['Scenario'].str.contains(k) & s['Market'].str.contains(j)
                              & s['Market'].str.contains(i) & s['Version'].str.contains("released")].values.tolist()[0]
                    d_s_p = s[s['Scenario'].str.contains(k) & s['Market'].str.contains(j) &
                              s['Market'].str.contains(i) & s['Version'].str.contains("pyrolysis")].values.tolist()[0]
                    d_s_p = d_s_p[2:len(d_s_p) - 2]
                    d_s_r = d_s_r[2:len(d_s_r) - 2]

                    # calculate flat change
                    d_s = [a - b for a, b in zip(d_s_p, d_s_r)]
                    d_s.append(i)
                    d_s.append(j)
                    d_s.append(k)
                    d_flat_table = pd.concat([d_flat_table, pd.DataFrame([d_s], columns=col)])

                    # calculate percent change
                    d_s = [100 * (a - b) / (b + 1e-7) for a, b in zip(d_s_p, d_s_r)]
                    d_s.append(i)
                    d_s.append(j)
                    d_s.append(k)
                    d_perc_table = pd.concat([d_perc_table, pd.DataFrame([d_s], columns=col)])

        if w == 0:
            d_flat_supply_table = d_flat_table
            d_perc_supply_table = d_perc_table
            print("change in supply table", d_flat_table)
            print("percent change in supply table", d_perc_table)
        else:
            d_flat_price_table = d_flat_table
            d_perc_price_table = d_perc_table
            print("change in price table", d_flat_table)
            print("percent change in price table", d_perc_table)

    # change in dollars spent table
    d_money_perc_table = pd.DataFrame()
    d_money_flat_table = pd.DataFrame()
    for i in products:
        for j in GCAM_region:
            for k in ssp:
                # get data
                s_released = \
                    supply_table[supply_table['Scenario'].str.contains(k) & supply_table['Market'].str.contains(j)
                                 & supply_table['Market'].str.contains(i) & supply_table['Version'].str.contains(
                        "released")].values.tolist()[0]
                s_pyro = \
                    supply_table[supply_table['Scenario'].str.contains(k) & supply_table['Market'].str.contains(j) &
                                 supply_table['Market'].str.contains(i) & supply_table['Version'].str.contains(
                        "pyrolysis")].values.tolist()[0]
                p_released = price_table[price_table['Scenario'].str.contains(k) & price_table['Market'].str.contains(j)
                                         & price_table['Market'].str.contains(i) & price_table['Version'].str.contains(
                    "released")].values.tolist()[0]
                p_pyro = price_table[price_table['Scenario'].str.contains(k) & price_table['Market'].str.contains(j)
                                     & price_table['Market'].str.contains(i) & price_table['Version'].str.contains(
                    "released")].values.tolist()[0]
                s_released = s_released[2:len(s_released) - 2]
                s_pyro = s_pyro[2:len(s_pyro) - 2]
                p_released = p_released[2:len(p_released) - 2]
                p_pyro = p_pyro[2:len(p_pyro) - 2]

                # calculate money spent
                money_spent_released = [a * b for a, b in zip(s_released, p_released)]
                money_spent_pyro = [a * b for a, b in zip(s_pyro, p_pyro)]

                # calculate change in money spent
                d_money_flat = [a - b for a, b in zip(money_spent_pyro, money_spent_released)]
                d_money_perc = [100 * (a - b) / (b + 1e-7) for a, b in zip(money_spent_pyro, money_spent_released)]

                # put back into df
                d_money_flat.append(i)
                d_money_flat.append(j)
                d_money_flat.append(k)
                d_money_perc.append(i)
                d_money_perc.append(j)
                d_money_perc.append(k)
                d_money_flat_table = pd.concat([d_money_flat_table, pd.DataFrame([d_money_flat], columns=col)])
                d_money_perc_table = pd.concat([d_money_perc_table, pd.DataFrame([d_money_perc], columns=col)])

    print("change in money spent table", d_money_flat_table)
    print("percent change in money spent table", d_money_perc_table)

    years = [2050, 2100]

    # set up world map
    world = get_world()

    # set up plotting data
    for i in years:
        for w in range(2):
            for v in range(2):
                if v == 0:
                    if w == 0:
                        data = d_flat_supply_table
                        lab = "Change in Supply (Mt)"
                    else:
                        data = d_perc_supply_table
                        lab = "Percent Change in Supply"
                else:
                    if w == 0:
                        data = d_flat_price_table
                        lab = "Change in Price (1975$/kg)"
                    else:
                        data = d_perc_price_table
                        lab = "Percent Change in Price (1975$/kg)"

                data = data[[i, "products", "GCAM_region", "SSP"]]

                for l in products:
                    d = 0
                    fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
                    cmap = plt.colormaps.get_cmap('viridis')
                    norm_data = data[(data["products"] == l)]
                    normalizer = Normalize(norm_data[i].min(), norm_data[i].max())
                    im = cm.ScalarMappable(norm=normalizer, cmap=cmap)
                    fig.tight_layout()

                    for k in ssp:
                        # get specific subset of data for product and SSP
                        filter_data = data[(data["SSP"] == k) & (data["products"] == l)]

                        merged = pd.merge(world, filter_data, on="GCAM_region", how='left')
                        merged = merged.replace("", np.nan)

                        merged.plot(column=i, ax=axs[int(d / 3), int(d % 3)], cmap=cmap, norm=normalizer)
                        if v == 0:
                            if w == 0:
                                axs[int(d / 3), int(d % 3)].set_title("Year: " + str(i) +
                                                                      " | Product: " + l + " | " + k)
                            else:
                                axs[int(d / 3), int(d % 3)].set_title("Year: " + str(i) +
                                                                      " | Product: " + l + " | " + k)
                        else:
                            if w == 0:
                                axs[int(d / 3), int(d % 3)].set_title("Year: " + str(i) +
                                                                      " | Product: " + l + " | " + k)
                            else:
                                axs[int(d / 3), int(d % 3)].set_title("Year: " + str(i) +
                                                                      " | Product: " + l + " | " + k)
                        d = d + 1

                    # update the figure with shared colorbar
                    fig.delaxes(axs[1, 2])
                    axins1 = inset_axes(
                        axs[1, 2],
                        width="100%",  # width: 50% of parent_bbox width
                        height="10%",  # height: 5%
                        loc="center",
                    )
                    axins1.xaxis.set_ticks_position("bottom")
                    fig.colorbar(im, cax=axins1, orientation="horizontal", label=lab)
                    plt.show()


def get_world():
    # get basic data
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

    # add GCAM country regions as a column
    world['GCAM_region'] = world.apply(lambda row: label_region(row), axis=1)

    return world


def label_region(row):
    if row['name'] in ["Burundi", "Comoros", "Djibouti", "Eritrea", "Ethiopia", "Kenya", "Madagascar", "Mauritius",
                       "Reunion", "Rwanda", "S. Sudan", "Sudan", "Somalia", "Uganda", "Somaliland"]:
        return "Africa_Eastern"
    if row['name'] in ["Algeria", "Egypt", "W. Sahara", "Libya", "Morocco", "Tunisia"]:
        return "Africa_Northern"
    if row['name'] in ["Angola", "Botswana", "Lesotho", "Mozambique", "Malawi", "Namibia", "Swaziland", "Tanzania",
                       "Zambia", "Zimbabwe", "eSwatini"]:
        return "Africa_Southern"
    if row['name'] in ["Benin", "Burkina Faso", "Central African Rep.", "Côte d'Ivoire", "Cameroon",
                       "Dem. Rep. Congo", "Congo", "Cape Verde", "Gabon", "Ghana", "Guinea", "Gambia",
                       "Guinea-Bissau", "Eq. Guinea", "Liberia", "Mali", "Mauritania", "Niger", "Nigeria",
                       "Senegal", "Sierra Leone", "Sao Tome and Principe", "Chad", "Togo"]:
        return "Africa_Western"
    if row['name'] in ['Argentina']:
        return "Argentina"
    if row['name'] in ["Australia", 'New Zealand']:
        return "Australia_NZ"
    if row['name'] in ["Brazil"]:
        return "Brazil"
    if row['name'] in ["Canada"]:
        return "Canada"
    if row['name'] in ["Aruba", "Anguilla", "Netherlands Antilles", "Antigua & Barbuda", "Bahamas", "Belize", "Bermuda",
                       "Barbados", "Costa Rica", "Cuba", "Cayman Islands", "Dominica", "Dominican Rep.",
                       "Guadeloupe", "Grenada", "Guatemala", "Honduras", "Haiti", "Jamaica", "Saint Kitts and Nevis",
                       "Saint Lucia", "Montserrat", "Martinique", "Nicaragua", "Panama", "El Salvador",
                       "Trinidad and Tobago", "Saint Vincent and the Grenadines"]:
        return "Central America and Caribbean"
    if row['name'] in ["Armenia", "Azerbaijan", "Georgia", "Kazakhstan", "Kyrgyzstan", "Mongolia", "Tajikistan",
                       "Turkmenistan", "Uzbekistan"]:
        return "Central Asia"
    if row['name'] in ["China"]:
        return "China"
    if row['name'] in ["Colombia"]:
        return "Colombia"
    if row['name'] in ["Bulgaria", "Cyprus", "Czechia", "Estonia", "Hungary", "Lithuania", "Latvia", "Malta",
                       "Poland", "Romania", "Slovakia", "Slovenia", "N. Cyprus"]:
        return "EU-12"
    if row['name'] in ["Andorra", "Austria", "Belgium", "Denmark", "Finland", "France", "Germany", "Greece",
                       "Greenland", "Ireland", "Italy", "Luxembourg", "Monaco", "Netherlands", "Portugal", "Sweden",
                       "Spain", "United Kingdom"]:
        return "EU-15"
    if row['name'] in ["Belarus", "Moldova", "Ukraine"]:
        return "Europe_Eastern"
    if row['name'] in ["Iceland", "Norway", "Switzerland"]:
        return "European Free Trade Association"
    if row['name'] in ["Albania", "Bosnia and Herz.", "Croatia", "Macedonia", "Montenegro", "Serbia", "Turkey",
                       "North Macedonia", "Kosovo"]:
        return "Europe_Non_EU"
    if row['name'] in ["India"]:
        return "India"
    if row['name'] in ["Indonesia"]:
        return "Indonesia"
    if row['name'] in ["Japan"]:
        return "Japan"
    if row['name'] in ["Mexico"]:
        return "Mexico"
    if row['name'] in ["United Arab Emirates", "Bahrain", "Iran", "Iraq", "Israel", "Jordan", "Kuwait", "Lebanon",
                       "Oman", "Palestine", "Qatar", "Saudi Arabia", "Syria", "Yemen"]:
        return "Middle East"
    if row['name'] in ["Pakistan"]:
        return "Pakistan"
    if row['name'] in ["Russia"]:
        return "Russia"
    if row['name'] in ["South Africa"]:
        return "South Africa"
    if row['name'] in ["French Guiana", "Guyana", "Suriname", "Venezuela"]:
        return "South America_Northern"
    if row['name'] in ["Bolivia", "Chile", "Ecuador", "Peru", "Paraguay", "Uruguay"]:
        return "South America_Southern"
    if row['name'] in ["Afghanistan", "Bangladesh", "Bhutan", "Sri Lanka", "Maldives", "Nepal"]:
        return "South Asia"
    if row['name'] in ["American Samoa", "Brunei", "Cocos (Keeling) Islands", "Cook Islands",
                       "Christmas Island", "Fiji", "Federated States of Micronesia", "Guam", "Cambodia", "Kiribati",
                       "Laos", "Marshall Islands", "Myanmar", "Northern Mariana Islands",
                       "Malaysia", "Mayotte", "New Caledonia", "Norfolk Island", "Niue", "Nauru",
                       "Pacific Islands Trust Territory", "Pitcairn Islands", "Philippines", "Palau",
                       "Papua New Guinea", "North Korea", "French Polynesia", "Singapore",
                       "Solomon Is.", "Seychelles", "Thailand", "Tokelau", "Timor-Leste", "Tonga", "Tuvalu",
                       "Vietnam", "Vanuatu", "Samoa"]:
        return "Southeast Asia"
    if row['name'] in ["South Korea"]:
        return "South Korea"
    if row['name'] in ["Taiwan"]:
        return "Taiwan"
    if row['name'] in ['United States of America', "Puerto Rico"]:
        return "USA"
    return "mistake"


def plot_fertilizer(data):
    fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
    fig.tight_layout()

    # get the difference between the production method for each livestock between versions for each SSP
    SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    l = 0
    df = pd.DataFrame()

    for item in data.items():
        # get label
        words = item[0].split("_")

        # get x data
        x = [col for col in item[1].columns]
        x = x[5:len(x) - 1]

        # convert x data to numeric
        x = [int(temp) for temp in x]

        # get y data
        y = item[1]
        y['Version'] = words[2]

        df = pd.concat([df, y], ignore_index=True)

    for i in SSPs:
        y_released = df[(df['Scenario'].str.contains(i)) & (df['Version'] == "released")]
        y_pyro = df[(df['Scenario'].str.contains(i)) & (df['Version'] == "pyrolysis")]

        color_map = [['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                     ['#c5b0d5', '#aec7e8', '#c49c94', '#ffbb78', '#98df8a', '#f7b6d2', '#c7c7c7', '#ff9896']]
        for j in range(len(y_released.index)):
            y_r = y_released.iloc[j, :].values.tolist()
            lab = y_r[2] + " - " + y_r[len(y_r) - 1]
            units = y_r[len(y_r) - 2]
            y = y_r[5:len(y_r) - 2]
            axs[int(l / 3), int(l % 3)].plot(x, y, label=lab, color=color_map[0][j])
        for j in range(len(y_pyro.index)):
            y_p = y_pyro.iloc[j, :].values.tolist()
            lab = y_p[2] + " - " + y_p[len(y_p) - 1]
            y = y_p[5:len(y_p) - 2]
            axs[int(l / 3), int(l % 3)].plot(x, y, label=lab, color=color_map[1][j])

        axs[int(l / 3), int(l % 3)].set_ylabel(units)
        axs[int(l / 3), int(l % 3)].set_title(i)
        handles, labels = axs[int(l / 3), int(l % 3)].get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        l = l + 1

    fig.legend(handles, labels, loc='lower right')
    fig.delaxes(axs[1, 2])
    plt.show()


def plot_refining(data):
    df = pd.DataFrame()

    for item in data.items():
        # get label
        words = item[0].split("_")

        # get x data
        x = [col for col in item[1].columns]
        x = x[5:len(x) - 1]

        # convert x data to numeric
        x = [int(temp) for temp in x]

        # get y data
        y = item[1]
        y['Version'] = words[2]

        df = pd.concat([df, y], ignore_index=True)

    color_dict = {}
    more_colors = -2

    for z in range(3):
        fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
        fig.tight_layout()

        # get the difference between the production method for each livestock between versions for each SSP
        SSPs = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
        l = 0

        for i in SSPs:
            y_released = df[(df['Scenario'].str.contains(i)) & (df['Version'] == "released")]
            y_pyro = df[(df['Scenario'].str.contains(i)) & (df['Version'] == "pyrolysis")]

            color_map = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896',
                         '#9467bd', '#c5b0d5',
                         '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d',
                         '#17becf', '#9edae5']

            # plot items appearing in the released version
            for j in range(len(y_released.index)):
                y_r = y_released.iloc[j, :].values.tolist()
                lab = y_r[4] + " - " + y_r[len(y_r) - 1]
                units = y_r[len(y_r) - 2]
                if z == 0:
                    tech = y_r[4]
                    y = y_r[5:len(y_r) - 2]
                elif z == 1:
                    tech = y_r[4]
                    y_r = y_r[5:len(y_r) - 2]
                    y_p = y_pyro[(y_pyro["technology"].str.contains(tech))].values.tolist()
                    y_p = y_p[0][5:len(y_p) - 2]
                    y = [b - a for a, b in zip(y_r, y_p)]
                    lab = tech
                    units = "Change in refining output (EJ)"
                elif z == 2:
                    tech = y_r[4]
                    y_r = y_r[5:len(y_r) - 2]
                    y_p = y_pyro[(y_pyro["technology"] == tech)].values.tolist()
                    y_p = y_p[0][5:len(y_p) - 2]
                    y = [100 * (b - a) / (a + 1e-7) for a, b in zip(y_r, y_p)]
                    lab = tech
                    units = "Percent change in refining output (EJ)"

                # get color information
                num = color_dict.get(tech)

                if num is None:
                    more_colors += 2
                    num = more_colors
                    color_dict[tech] = num

                axs[int(l / 3), int(l % 3)].plot(x, y, label=lab, color=color_map[num])

            if z == 0:
                print(color_dict)
                # plot refined liquids products in the pyrolysis model
                for j in range(len(y_pyro.index)):
                    y_p = y_pyro.iloc[j, :].values.tolist()
                    lab = y_p[4] + " - " + y_p[len(y_p) - 1]
                    y = y_p[5:len(y_p) - 2]
                    num = color_dict.get(y_p[4])

                    # get a new color if this is a liquid from a new technology
                    if num is None:
                        more_colors += 1
                        num = more_colors
                        color_dict[y_p[4]] = num

                    # offsetting by 1
                    num = num + 1
                    axs[int(l / 3), int(l % 3)].plot(x, y, label=lab, color=color_map[num])

            axs[int(l / 3), int(l % 3)].set_ylabel(units)
            axs[int(l / 3), int(l % 3)].set_title(i)
            handles, labels = axs[int(l / 3), int(l % 3)].get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
            l = l + 1

        fig.legend(handles, labels, loc='upper left')
        fig.delaxes(axs[1, 2])
        plt.show()


def label_product(row):
    products = ["beef manure", "dairy manure", "poultry manure", "pork manure", "manure fuel feedstock", "manure fuel",
                "beef_biochar", "dairy_biochar", "poultry_biochar", "pork_biochar"]
    for i in products:
        if i in row['Market']:
            return i
    return ""


def label_SSP(row):
    ssp = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
    for i in ssp:
        if i in row['Scenario']:
            return i
    return ""


def label_Scenario(row):
    for i in GCAM_region:
        if i in row['Market']:
            return i
    return ""


def plot_world_pyrolysis(supply_data, price_data):
    products = ["beef manure", "dairy manure", "poultry manure", "pork manure", "manure fuel feedstock",
                "beef_biochar", "dairy_biochar", "poultry_biochar", "pork_biochar"]
    ssp = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]

    supply_table = pd.DataFrame()
    price_table = pd.DataFrame()

    for item in supply_data.items():
        # find the product
        if not item[1].empty:
            item[1]['products'] = item[1].apply(lambda row: label_product(row), axis=1)
            item[1]['GCAM_region'] = item[1].apply(lambda row: label_Scenario(row), axis=1)
            item[1]['SSP'] = item[1].apply(lambda row: label_SSP(row), axis=1)
            supply_table = pd.concat([supply_table, item[1]], ignore_index=True)
    for item in price_data.items():
        if not item[1].empty:
            item[1]['products'] = item[1].apply(lambda row: label_product(row), axis=1)
            item[1]['GCAM_region'] = item[1].apply(lambda row: label_Scenario(row), axis=1)
            item[1]['SSP'] = item[1].apply(lambda row: label_SSP(row), axis=1)
            price_table = pd.concat([price_table, item[1]], ignore_index=True)

    print("supply table", supply_table)
    print("price table", price_table)

    years = [2050, 2100]

    # set up world map
    world = get_world()

    # set up plotting data
    for i in years:
        for w in range(2):
            if w == 0:
                data = supply_table
            else:
                data = price_table

            data = data[[str(i), "products", "GCAM_region", "SSP"]]

            for l in products:
                d = 0
                fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
                cmap = plt.colormaps.get_cmap('viridis')
                norm_data = data[(data["products"] == l)]
                normalizer = Normalize(norm_data[str(i)].min(), norm_data[str(i)].max())
                im = cm.ScalarMappable(norm=normalizer, cmap=cmap)
                fig.tight_layout()

                for k in ssp:
                    # get specific subset of data for product and SSP
                    filter_data = data[(data["SSP"] == k) & (data["products"] == l)]

                    merged = pd.merge(world, filter_data, on="GCAM_region", how='left')
                    merged = merged.replace("", np.nan)

                    merged.plot(column=str(i), ax=axs[int(d / 3), int(d % 3)], cmap=cmap, norm=normalizer)

                    axs[int(d / 3), int(d % 3)].set_title("Year: " + str(i) + " | Product: " + l + " | " + k)
                    d = d + 1

                # update the figure with shared colorbar
                fig.delaxes(axs[1, 2])
                axins1 = inset_axes(
                    axs[1, 2],
                    width="100%",  # width: 50% of parent_bbox width
                    height="10%",  # height: 5%
                    loc="center",
                )

                if w == 0:
                    lab = "Product Supply (EJ or Mt)"
                else:
                    lab = "Product Price 1975$/(GJ or kg)"

                axins1.xaxis.set_ticks_position("bottom")
                fig.colorbar(im, cax=axins1, orientation="horizontal", label=lab)
                plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get price data
    price = ["beef manure", "dairy manure", "poultry manure", "pork manure", "manure fuel feedstock", "manure fuel",
             "beef_biochar", "dairy_biochar", "poultry_biochar", "pork_biochar"]
    price_data_type = "market_prices"
    price_data = get_data(price, price_data_type)

    # get supply data
    supply = ["beef manure", "dairy manure", "poultry manure", "pork manure", "manure fuel feedstock", "manure fuel",
              "beef_biochar", "dairy_biochar", "poultry_biochar", "pork_biochar"]
    supply_data_type = "market_supply"
    supply_data = get_data(supply, supply_data_type)

    # get all entries for refining, fertilizer, CO2 emissions by tech, CO2 concentrations, feed consumption
    NA = ["NA"]

    # get fertilizer data
    fert_data_type = "N_fertilizer"
    fert_data = get_data(NA, fert_data_type)

    # get bio-oil data
    biooil_data_type = "refining_liquids"
    biooil_data = get_data(NA, biooil_data_type)

    # get meat data
    meat_data_type = "meat_dairy_consumption"
    meat_production_data = get_data(NA, meat_data_type)

    meat_supply_data = get_data(NA, "market_supply")
    meat_price_data = get_data(NA, "market_prices")

    # get CO2 concentration data
    concentration_data_type = "CO2_conc"
    concentration_data = get_data(NA, concentration_data_type)

    # get CO2 sequestration data
    sequestration_data_type = "CO2_seq"
    sequestration_data = get_data(NA, sequestration_data_type)

    print("all input data processed")
    # plots for variables that only appear in the pyrolysis models (pyro):
    # 1. plot of production by SSP
    # 2. plot of cumulative production by SSP

    # plots for variables that appear in both models that are non-geographical (both):
    # 1. plot of production by SSP
    # 2a. plot of change in production by SSP
    # 2b. plot of cumulative change in production by SSP
    # 2c. plot of percentage change in production by SSP

    # plots for variables that only appear in the pyrolysis models and are regional (pyro-regional):
    # 1a. table of production by year, product, region, and SSP
    # 1b. table of cumulative production by year, product, region, and SSP
    # 1c. table of price by year, product, region, and SSP
    # 1d. table of dollars spent (supply * price) by year, product, region, and SSP
    # 2a1. plot of supply by SSP by product in 2050 by region on map
    # 2a2. plot of supply by SSP by product in 2100 by region on map
    # 2b1. plot of price by SSP by product in 2050 by region on map
    # 2b2. plot of price by SSP by product in 2100 by region on map

    # plots for variables that appear in both models that are non-geographical (both-regional):
    # 1a1. table of supply by year, product, region, and SSP
    # 1a2. table of change in supply by year, product, region, and SSP
    # 1a3. table of percentage change in supply by year, product, region, and SSP
    # 1b1. table of price by year, product, region, and SSP
    # 1b2. table of percentage change in price by year, product, region, and SSP
    # 1b3. table of price by year, product, region, and SSP
    # 1c1. table of change in dollars spent (supply * price) by year, product, region, and SSP
    # 1c2. table of percentage change in dollars spent (supply * price) by year, product, region, and SSP
    # 1c3. global flat and percentage change in dollars spent by product
    # 2a1. plot of change in supply by SSP by product in 2050 by region on map
    # 2a2. plot of change in supply by SSP by product in 2100 by region on map
    # 2a3. plot of percent change in supply by SSP by product in 2050 by region on map
    # 2a4. plot of percent change in supply by SSP by product in 2100 by region on map
    # 2b1. plot of change in price by SSP by product in 2050 by region on map
    # 2b2. plot of change in price by SSP by product in 2100 by region on map
    # 2b3. plot of percent change in price by SSP by product in 2050 by region on map
    # 2b4. plot of percent change in price by SSP by product in 2100 by region on map

    # make plots
    # plot_CO2_conc(concentration_data)
    # plot_sequestration(sequestration_data)
    #plot_meat(meat_production_data)
    plot_world_meat(meat_supply_data, meat_price_data)
    # plot_fertilizer(fert_data)
    # plot_refining(biooil_data)
    # plot_world_pyrolysis(supply_data, price_data)
    plot_random_stuff(meat_supply_data)
