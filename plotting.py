import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import constants as c
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pylab import *
from sklearn.metrics import r2_score
import matplotlib.patches as mpatches
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss


def world_data(data):
    """
    merges the data to be plotted into a geopandas dataframe and selects relevant columns for plotting
    :param data: the dataframe containing GCAM data to be plotted
    :return: a pandas dataframe containing relevant year and column data
    """
    world = gpd.read_file(c.GCAMConstants.processed_map_loc)
    merged = pd.merge(world, data, on="GCAM", how='left')
    merged = merged.replace(c.GCAMConstants.missing, np.nan)

    return merged


def get_subplot_dimensions(list_products):
    """
    returns the number of subplot dimensions based on the number of items being plotted
    :param list_products: the list of things being plotted on one plot
    :return: the number of rows and the number of columns for the plot
    """
    if len(list_products) == 1:
        return 1, 1
    elif len(list_products) == 2:
        return 2, 1
    elif len(list_products) == 3:
        return 3, 1
    elif len(list_products) == 4:
        return 2, 2
    elif len(list_products) == 5 or len(list_products) == 6:
        return 2, 3
    elif len(list_products) == 7 or len(list_products) == 8:
        return 2, 4
    elif len(list_products) == 9:
        return 3, 3
    elif len(list_products) in [10, 11, 12]:
        return 3, 4
    elif len(list_products) in [13, 14, 15, 16]:
        return 4, 4
    elif len(list_products) in [17, 18, 19, 20]:
        return 4, 5
    else:
        raise ValueError("too many products. Can only plot 20 products at a time")


def plot_world(dataframe, products, SSPS, groupby, column, years):
    """
    control function for plotting any plot that is placed on a world map
    :param years: the years for which the plot is to be evaluated
    :param dataframe: the dataframe containing data to be plotted
    :param products: the list of products that are to be plotted
    :param SSPS: the list of SSPs by which the data is to be plotted
    :param groupby: how the data should be grouped. Accepted values include "SSP", "Products
    :param column: the column on which the data should be filtered by product
    :return: shows the relevant plot
    """
    if groupby == "SSP":
        plot_world_by_SSP(dataframe, products, column, years, SSPS)
    elif groupby == "product":
        plot_world_by_products(dataframe, products, column, years, SSPS)
    elif groupby == "year":
        plot_world_by_years(dataframe, products, column, years, SSPS)
    else:
        raise ValueError("only 'SSP', 'products', and 'years' are considered valid groupings at this time")


def plot_world_by_SSP(dataframe, products, column, year, SSP):
    """
    For a given product, plot its values in all SSPs for a given year
    :param dataframe: the dataframe containing the data to be plotted
    :param products: the product being plotted
    :param column: the column in the dataframe containing the product
    :param year: the year being chosen
    :param SSP: the set of shared socioeconomic pathways being used as evaluation
    """
    for j in year:
        for i in products:
            try:
                counter = 0
                # get plot information
                axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
                    dataframe=dataframe,
                    inner_loop_set=SSP,
                    products=[i],
                    year=[j],
                    SSP=SSP,
                    product_column=column)
                # create label for the graph - assumes all values have the same units
                units = dataframe.iat[0, 31]

                for k in SSP:
                    subplot_title = str(k)
                    units = get_df_to_plot(
                        dataframe=dataframe,
                        ncol=ncol,
                        nrow=nrow,
                        fig=fig,
                        axs=axs,
                        cmap=cmap,
                        normalizer=normalizer,
                        counter=counter,
                        column=column,
                        products=i,
                        SSPs=k,
                        years=j,
                        subplot_title=subplot_title)
                    counter = counter + 1

                # update the figure with shared colorbar
                dl = len(SSP)
                lab = "Product: " + i + " | " + str(j) + " | " + units
                add_colorbar_and_plot(axs, dl, fig, im, lab, ncol, nrow)
            except ValueError as e:
                print(e)


def plot_world_by_products(dataframe, products, column, year, SSP):
    """
    For each SSP, plots all relevant products
    :param SSP: the SSP scenario for the plot
    :param year: The year of data to be plotted
    :param dataframe: dataframe containing the data to be plotted
    :param products: the data to be plotted
    :param column: the column for which the data is to be filtered
    :return: shows the relevant plot
    """
    for j in year:
        for k in SSP:
            try:
                counter = 0
                # get plot information
                axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
                    dataframe=dataframe,
                    inner_loop_set=products,
                    products=products,
                    year=[j],
                    SSP=[k],
                    product_column=column)

                # iterate through all subplots
                for i in products:
                    subplot_title = str(i)
                    units = get_df_to_plot(
                        dataframe=dataframe,
                        ncol=ncol,
                        nrow=nrow,
                        fig=fig,
                        axs=axs,
                        cmap=cmap,
                        normalizer=normalizer,
                        counter=counter,
                        column=column,
                        products=i,
                        SSPs=k,
                        years=j,
                        subplot_title=subplot_title)
                    counter = counter + 1

                # update the figure with shared colorbar
                dl = len(products)
                lab = "Year: " + str(j) + " | " + str(k) + " | " + units
                add_colorbar_and_plot(axs, dl, fig, im, lab, ncol, nrow)
            except ValueError as e:
                print(e)


def axs_params(ax, plot_title):
    """
    Provides uniform formatting for all axes
    :param ax: the axis being formatted
    :param plot_title: the title of the subplot
    :return: N/A
    """
    ax.tick_params(left=False, right=False, labelleft=False, labelbottom=False, bottom=False)
    ax.margins(x=0.005, y=0.005)
    ax.set_title(str(plot_title))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def plot_world_by_years(dataframe, products, column, year, SSP):
    """
    For each SSP, plots all relevant products
    :param SSP: the SSP scenario for the plot
    :param year: The year of data to be plotted
    :param dataframe: dataframe containing the data to be plotted
    :param products: the data to be plotted
    :param column: the column for which the data is to be filtered
    :return: shows the relevant plot
    """
    for k in SSP:
        for i in products:
            try:
                counter = 0
                # get plot information
                axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
                    dataframe=dataframe,
                    inner_loop_set=year,
                    products=[i],
                    year=year,
                    SSP=[k],
                    product_column=column)

                # iterate through all subplots
                for j in year:
                    subplot_title = str(j)
                    units = get_df_to_plot(
                        dataframe=dataframe,
                        ncol=ncol,
                        nrow=nrow,
                        fig=fig,
                        axs=axs,
                        cmap=cmap,
                        normalizer=normalizer,
                        counter=counter,
                        column=column,
                        products=i,
                        SSPs=k,
                        years=j,
                        subplot_title=subplot_title)
                    counter = counter + 1

                # update the figure with shared colorbar
                dl = len(year)
                lab = "Product: " + str(i) + " | " + str(k) + " | " + str(units)
                add_colorbar_and_plot(axs, dl, fig, im, lab, ncol, nrow)
            except ValueError as e:
                print(e)


def get_df_to_plot(dataframe, ncol, nrow, fig, axs, cmap, normalizer, counter, column, products, SSPs, years,
                   subplot_title):
    """
    This method filters data and prepare it for plotting
    :param dataframe: the data being plotted
    :param ncol: the number of columns of subplots
    :param nrow: the number of rows of subplots
    :param fig: matplotlib fig
    :param axs: the matplotlib axs being plotted
    :param cmap: the colormap being used
    :param normalizer: the normalizer bieng used
    :param counter: the plot counter
    :param column: the column on which the products are located
    :param products: the products being plotted
    :param SSPs: the SSPs being plotted
    :param years: the years being plotted
    :param subplot_title: the title for the subplot
    :return: unit label for the subplot
    """
    filter_data = dataframe[(dataframe[column].isin([products])) & (dataframe['SSP'].isin([SSPs]))]
    # if there is no data in the filter data, delete all following axis
    if filter_data.empty:
        if ncol == 1:
            if nrow == 1:
                fig.delaxes(axs)
            else:
                fig.delaxes(axs[counter])
        else:
            fig.delaxes(axs[int(counter / ncol), int(counter % ncol)])
    else:
        map_to_plot = world_data(filter_data)
        plot_world_on_axs(
            map_plot=map_to_plot,
            axs=axs,
            cmap=cmap,
            counter=counter,
            plot_title=subplot_title,
            plotting_column=years,
            ncol=ncol,
            nrow=nrow,
            normalizer=normalizer)
        units = map_to_plot['Units'].unique()
        for i in units:
            if str(i) != "nan":
                return str(i)


def plot_world_on_axs(map_plot, axs, cmap, counter, plot_title, plotting_column, ncol, normalizer, nrow):
    """
    Plot the world map in a subplot
    :param map_plot: the dataframe containing map info and the data being plotted
    :param axs: the subplot axis on which the map is being plotted
    :param cmap: the color map for the choropleth map
    :param counter: the counter for which subplot is being counted
    :param plot_title: the subplot title
    :param plotting_column: the column containing data that is the basis of the choropleth map
    :param ncol: the number of columns of subplots
    :param normalizer: the data normalizer for the colorbar
    :param nrow: the number of rows of subplots
    :return: N/A
    """
    if ncol == 1:
        if nrow == 1:
            map_plot.plot(
                column=str(plotting_column),
                missing_kwds=dict(color='grey', label='No Data'),
                ax=axs,
                cmap=cmap,
                norm=normalizer)
            axs_params(axs, plot_title)
        else:
            map_plot.plot(
                column=str(plotting_column),
                missing_kwds=dict(color='grey', label='No Data'),
                ax=axs[int(counter / ncol)],
                cmap=cmap,
                norm=normalizer)
            axs_params(axs[int(counter / ncol)], plot_title)
    else:
        map_plot.plot(
            column=str(plotting_column),
            missing_kwds=dict(color='grey', label='No Data'),
            ax=axs[int(counter / ncol), int(counter % ncol)],
            cmap=cmap,
            norm=normalizer)
        axs_params(axs[int(counter / ncol), int(counter % ncol)], plot_title)


def create_subplots(dataframe, inner_loop_set, products, year, SSP, product_column):
    """
    Creates the boilerplate subplots and colorbars
    :param inner_loop_set: the list of products being iterated over for the different subplots
    :param SSP: The SSP of the scenario
    :param product_column: The column on which the different products being graphed vary
    :param dataframe: the dataframe being evaluated
    :param products: the list of products being evaluated
    :param year: the year in which the data is plotted
    :return: a set of figure objects
    """
    # at this stage, if this df is empty, then we know that there is no material to plot
    df = dataframe[(dataframe['SSP'].isin(SSP)) & (dataframe[product_column].isin(products))]

    # remove the global entry for regional plotting
    df = df.drop(df[df['GCAM'] == "Global"].index)

    if df.empty:
        raise ValueError("These products" + str(products) + "do not exist in this dataframe")

    nrow, ncol = get_subplot_dimensions(inner_loop_set)
    fig, axs = plt.subplots(nrow, ncol, sharex='all', sharey='all', gridspec_kw={'wspace': 0.2, 'hspace': 0.2})
    cmap = plt.colormaps.get_cmap('viridis')
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    normalizer = Normalize(min(df[str(i)].min() for i in year), max(df[str(i)].max() for i in year))
    im = cm.ScalarMappable(norm=normalizer, cmap=cmap)
    return axs, cmap, fig, im, ncol, normalizer, nrow


def add_colorbar_and_plot(axs, datalength, fig, im, lab, ncol, nrow):
    """
    Adds the colorbar to the graph and produces output
    :param axs: matplotlib axes
    :param datalength: the length of the data being plotted
    :param fig: matplotlib fig
    :param im: matplotlib im
    :param lab: label for the colorbar
    :param ncol: number of rows of axes
    :param nrow: number of columns of axes
    :return: plotted figure
    """
    for i in range(nrow * ncol - datalength):
        fig.delaxes(axs[int((datalength + i) / ncol), int((datalength + i) % ncol)])
    if nrow * ncol > datalength:
        axins1 = inset_axes(
            axs[int((datalength) / ncol), int((datalength) % ncol)],
            width="100%",  # width: 50% of parent_bbox width
            height="10%",  # height: 5%
            loc="center",
        )
        axins1.xaxis.set_ticks_position("bottom")
        fig.colorbar(im, cax=axins1, orientation="horizontal", label=lab)
    elif ncol == 1:
        if nrow == 1:
            fig.colorbar(im, shrink=0.6, orientation="vertical", label=lab)
        else:
            fig.colorbar(im, ax=axs[:], shrink=0.6, orientation="vertical", label=lab)
    else:
        fig.colorbar(im, ax=axs[nrow - 1, :], shrink=0.6, orientation="horizontal", label=lab)

    # change figure size and dpi
    fig.set_dpi(100)
    if nrow * ncol == 6:
        fig.set_size_inches(12, 4)
    elif nrow * ncol == 8:
        fig.set_size_inches(16, 5.1)
    elif nrow * ncol == 20:
        fig.set_size_inches(16, 9)
    plt.show()


def plot_line(dataframe, products, SSPS, groupby, column, differentiator):
    """
    Control function for plotting line graphs
    :param dataframe: the line graph being plotted
    :param products: the products to be plotted
    :param SSPS: the SSPs to be plotted
    :param groupby: how the subplots should be grouped
    :param column: the column on which the products differentiate
    :param differentiator: a secondary column by which the products may further be differentiated
    :return: N/A
    """
    if groupby == "SSP":
        plot_line_by_SSP(dataframe, products, column, SSPS, differentiator)
    elif groupby == "product":
        plot_line_by_product(dataframe, products, column, SSPS, differentiator)
    else:
        raise ValueError("only 'SSP', 'product', and 'year' are considered valid groupings at this time")


def plot_line_by_SSP(dataframe, products, column, SSP, differentiator):
    try:
        # get plot information
        axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
            dataframe=dataframe,
            inner_loop_set=products,
            products=products,
            year=c.GCAMConstants.plotting_x,
            SSP=SSP,
            product_column=column)

        # find the number of model versions
        # get color scheme based on number of model versions
        versions = dataframe[differentiator].unique()
        colors, num_colors = get_colors(len(versions))
        counter = 0
        for i in products:
            color_counter = 0
            for k in SSP:
                sub_color = 0
                y = dataframe[(dataframe[column] == i) & (dataframe['SSP'] == k)]

                if not y.empty:
                    # plot all versions in y
                    for j in y[differentiator].unique():
                        # get y label
                        if len(versions) > 1:
                            lab = str(k) + str(j)
                        else:
                            lab = str(k)

                        # get color
                        color = colors[color_counter * num_colors + sub_color]
                        sub_color = sub_color + 1

                        # get line of data to plot and plot it
                        df = y[y[differentiator] == j]
                        y_to_plot = df.values.tolist()[0][c.GCAMConstants.skip_years:c.GCAMConstants.skip_years + len(c.GCAMConstants.plotting_x)]  # only take the x values
                        plot_line_on_axs(
                            x=c.GCAMConstants.plotting_x,
                            y=y_to_plot,
                            lab=lab,
                            color=color,
                            axs=axs,
                            nrow=nrow,
                            ncol=ncol,
                            counter=counter)

                    # get units
                    units = y['Units'].unique()[0]
                    color_counter = color_counter + 1
            l, h = finalize_line_subplot(axs, units, str(i), ncol, nrow, counter)

            counter = counter + 1
        finalize_line_plot(fig, h, l, axs, nrow, ncol, counter)

    except ValueError as e:
        print(e)


def finalize_line_plot(fig, handles, labels, axs, nrow, ncol, counter):
    """
    adds a legend to the plot and removes unnecessary axes
    :param fig: matplotlib figure
    :param handles: matplotlib handles
    :param labels: matplotlib labels
    :param axs: maxplotlib axs
    :param nrow: the number of rows of subplots
    :param ncol: the number of columns of subplots
    :param counter: the number of used subplots
    :return: N/A
    """
    if nrow * ncol == 1:
        fig.legend(handles, labels, bbox_to_anchor=(0.3, 0.7), facecolor='white', framealpha=1)
    elif nrow * ncol == 4:
        fig.legend(handles, labels, bbox_to_anchor=(0.6, 0.6), facecolor='white', framealpha=1)
    elif nrow * ncol == 6 and counter == 5:
        fig.legend(handles, labels, bbox_to_anchor=(0.9, 0.4), facecolor='white', framealpha=1)
    elif nrow * ncol == 6:
        fig.legend(handles, labels, bbox_to_anchor=(0.15, 0.54), facecolor='white', framealpha=1)
    else:
        fig.legend(handles, labels, bbox_to_anchor=(0.6, 0.6), facecolor='white', framealpha=1)

    # remove unnecessary axes
    for i in range(nrow * ncol - counter):
        fig.delaxes(axs[int((counter + i) / ncol), int((counter + i) % ncol)])

    plt.tight_layout()
    plt.show()


def plot_line_on_axs(x, y, lab, color, axs, nrow, ncol, counter):
    """
    Plots a line on the axis
    :param x: x values for the plot
    :param y: y values for the plot
    :param lab: label for the line
    :param color: the line color
    :param axs: the axis being plotted on
    :param nrow: the number of rows of axes
    :param ncol: the number of columns of axes
    :param counter: the number of the current subplot
    :return: N/A
    """
    if ncol == 1:
        if nrow == 1:
            axs.plot(x, y, label=lab, color=color)
        else:
            axs[int(counter / ncol)].plot(x, y, label=lab, color=color)
    else:
        axs[int(counter / ncol), int(counter % ncol)].plot(x, y, label=lab, color=color)


def finalize_line_subplot(axs, ylabel, title, ncol, nrow, counter):
    """
    Applies formatting to a subplot
    :param axs: the axis of the subplot
    :param ylabel: the label for the y-axis
    :param title: the title of the graph
    :param ncol: the number of rows of subplots
    :param nrow: the number of columns of subplots
    :param counter: the current subplot
    :return: labels and handles of the subplot
    """
    if ncol == 1:
        if nrow == 1:
            axs.set_ylabel(ylabel)
            axs.set_xlabel("Years")
            axs.set_title(title)
            handles, labels = axs.get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        else:
            axs[int(counter / ncol)].set_ylabel(ylabel)
            axs[int(counter / ncol)].set_xlabel("Years")
            axs[int(counter / ncol)].set_title(title)
            handles, labels = axs[0].get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    else:
        axs[int(counter / ncol), int(counter % ncol)].set_ylabel(ylabel)
        axs[int(counter / ncol), int(counter % ncol)].set_title(title)
        axs[int(counter / ncol), int(counter % ncol)].set_xlabel("Years")
        handles, labels = axs[0, 0].get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))

    return labels, handles


def plot_line_by_product(dataframe, products, column, SSP, differentiator):
    """
    Plots a line grouped by product
    :param dataframe: the data being plotted
    :param products: the list of products in the data being plotted
    :param column: the column by which the products can be differentiated
    :param SSP: the SSPs being plotted
    :param differentiator: a secondary column to differentiate the products
    :return: N/A
    """
    # get plot information
    axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
        dataframe=dataframe,
        inner_loop_set=SSP,
        products=SSP,
        year=c.GCAMConstants.plotting_x,
        SSP=SSP,
        product_column='SSP')

    # find the number of model versions
    # get color scheme based on number of model versions
    versions = dataframe[differentiator].unique()
    colors, num_colors = get_colors(len(versions))
    counter = 0
    try:
        for k in SSP:
            color_counter = 0
            for i in products:
                sub_color = 0
                y = dataframe[(dataframe[column] == i) & (dataframe['SSP'] == k)]

                if not y.empty:
                    # plot all versions in y
                    for j in y[differentiator].unique():
                        # get y label
                        if len(versions) > 1:
                            lab = str(i) + str(j)
                        else:
                            lab = str(i)

                        # get color
                        color = colors[color_counter * num_colors + sub_color]
                        sub_color = sub_color + 1

                        # get line of data to plot and plot it
                        df = y[y[differentiator] == j]
                        y_to_plot = df.values.tolist()[0][c.GCAMConstants.skip_years:c.GCAMConstants.skip_years+len(c.GCAMConstants.plotting_x)]  # only take the x values
                        plot_line_on_axs(c.GCAMConstants.plotting_x, y_to_plot, lab, color, axs, nrow, ncol, counter)

                    # get units
                    units = y['Units'].unique()[0]
                    l, h = finalize_line_subplot(axs, units, str(k), ncol, nrow, counter)
                    color_counter = color_counter + 1

            counter = counter + 1
        finalize_line_plot(fig, h, l, axs, nrow, ncol, counter)

    except ValueError as e:
        print(e)


def get_colors(num_versions):
    """
    gets a color mapping based on the number of versions of the product
    :param num_versions: the number of unique entries for each product
    :return: a list containing the requisite colors, the number of colors for each product
    """
    if num_versions == 1:
        cmap = matplotlib.colormaps.get_cmap('tab10')
        num_sub_colors = 1
    elif num_versions == 2:
        cmap = matplotlib.colormaps.get_cmap('tab20')
        num_sub_colors = 2
    else:
        cmap = matplotlib.colormaps.get_cmap('tab20b')
        num_sub_colors = 4
    return [matplotlib.colors.rgb2hex(c) for c in cmap.colors], num_sub_colors


def plot_disruption_by_years(dataframe, products, product_column, SSP, legend_location):
    """
    plots the year of maximum disruption by the magnitude of the disruption
    :param dataframe: dataframe containing data to plot
    :param products: the products being plotted
    :param product_column: the column containing the products
    :param SSP: the SSP over which the product is being plotted
    :param legend_location: the location of the legend
    :return: N/A
    """
    colors, divisions = get_colors(2)

    dataframe = dataframe[(dataframe['SSP'].isin(SSP))]
    df_global = dataframe[dataframe['GCAM'] == "Global"]
    df_regional = dataframe.drop(dataframe[dataframe['GCAM'] == "Global"].index)
    df_regional["supply_at_year"] = df_regional["supply_at_year"] + abs(df_regional["supply_at_year"].min())
    df_regional["supply_at_year"] = 80 * (df_regional["supply_at_year"] / df_regional["supply_at_year"].max())

    for i in range(len(products)):
        df_regional["year"] = df_regional["year"].astype(int)
        df_one_product = df_regional[(df_regional[product_column].isin([products[i]]))]
        units = df_regional['Units'].unique().tolist()

        if df_one_product.empty:
            pass
        else:
            plt.scatter(x=df_one_product["year"], y=df_one_product["disruption"], s=df_one_product["supply_at_year"],
                        alpha=.5,
                        color=colors[i * 2], label=products[i])
            if not df_global.empty:
                pass
                # plt.scatter(x=df_global["year"], y=df_global['disruption'], color=colors[i*2+1], label=products[i] + " | global")
    plt.ylabel("Disruption in " + units[0])
    plt.xlabel("Year")
    plt.legend(loc=legend_location)
    plt.show()




