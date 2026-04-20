import geopandas as gpd
import pandas as pd
import constants as c
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pylab import *
import data_manipulation


def world_data(data):
    """
    merges the data to be plotted into a geopandas dataframe and selects relevant columns for plotting
    :param data: the dataframe containing GCAM data to be plotted
    :return: a pandas dataframe containing relevant year and column data
    """
    world = gpd.read_file(c.GCAMConstants.processed_map_loc)
    merged = pd.merge(world, data, left_on="STUSPS", right_on="GCAM", how='left')
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
        return 2, 2
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
    elif len(list_products) == 51:
        return 9, 6
    else:
        raise ValueError("too many products. Can only plot 20 products at a time")


def plot_world_by_products(dataframe, column, year, title, nonBaselineScenario):
    """
    For each SSP, plots all relevant products
    :param year: The year of data to be plotted
    :param dataframe: dataframe containing the data to be plotted
    :param column: the column for which the data is to be filtered
    :param title: the title for the plot
    :param nonBaselineScenario: the set of scenarios in the sensitivity analysis being evaluated
    :return: shows the relevant plot
    """
    for j in year:
        try:
            counter = 0
            units = "N/A"
            # get plot information
            products = dataframe[column].unique()
            axs, cmap, fig, im, ncol, normalizer, nrow = create_subplots(
                dataframe=dataframe,
                inner_loop_set=products,
                products=products,
                year=[j],
                title=title)

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
                    years=j,
                    subplot_title=subplot_title)
                counter = counter + 1

            # update the figure with shared colorbar
            dl = len(products)
            lab = units
            add_colorbar_and_plot(axs, dl, fig, im, lab, ncol, nrow, title, nonBaselineScenario)
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
    ax.set_title(str(plot_title), fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


def get_df_to_plot(dataframe, ncol, nrow, fig, axs, cmap, normalizer, counter, column, products, years, subplot_title):
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
    :param years: the years being plotted
    :param subplot_title: the title for the subplot
    :return: unit label for the subplot
    """
    if column != "":
        filter_data = dataframe[dataframe[[column]].isin([products]).any(axis=1)]
    else:
        filter_data = dataframe

    # if there is no data in the filter data, delete all following axis
    if filter_data.empty:
        if ncol == 1:
            if nrow == 1:
                fig.delaxes(axs)
            else:
                fig.delaxes(axs[counter])
        else:
            fig.delaxes(axs[int(counter % nrow), int(counter / nrow)])
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
                ax=axs[int(counter % nrow)],
                cmap=cmap,
                norm=normalizer)
            axs_params(axs[int(counter % nrow)], plot_title)
    else:
        map_plot.plot(
            column=str(plotting_column),
            missing_kwds=dict(color='grey', label='No Data'),
            ax=axs[int(counter % nrow), int(counter / nrow)],
            cmap=cmap,
            norm=normalizer)
        axs_params(axs[int(counter % nrow), int(counter / nrow)], plot_title)


def create_subplots(dataframe, inner_loop_set, products, year, title):
    """
    Creates the boilerplate subplots and colorbars
    :param inner_loop_set: the list of products being iterated over for the different subplots
    :param dataframe: the dataframe being evaluated
    :param products: the list of products being evaluated
    :param year: the year in which the data is plotted
    :param title: the title of the plot
    :return: a set of figure objects
    """
    # at this stage, if this df is empty, then we know that there is no material to plot
    if dataframe.empty:
        raise ValueError("These products" + str(products) + "do not exist in this dataframe")
    df = dataframe.replace([np.inf, -np.inf], np.nan)

    # get subplot size
    nrow, ncol = get_subplot_dimensions(inner_loop_set)

    # make plots and color scheme
    fig, axs = plt.subplots(nrow, ncol, sharex='all', sharey='all', gridspec_kw={'wspace': 0.2, 'hspace': 0.2})
    cmap = plt.colormaps.get_cmap('viridis')
    fig.suptitle(title)
    normalizer = Normalize(min(df[str(i)].min() for i in year), max(df[str(i)].max() for i in year))
    im = cm.ScalarMappable(norm=normalizer, cmap=cmap)
    if year != ["plot"]:
        plt.xticks(range(min([int(y) for y in year]), max([int(y) for y in year]) + 1, 5))
    return axs, cmap, fig, im, ncol, normalizer, nrow


def add_colorbar_and_plot(axs, datalength, fig, im, lab, ncol, nrow, fname, nonBaselineScenario):
    """
    Adds the colorbar to the graph and produces output
    :param axs: matplotlib axes
    :param datalength: the length of the data being plotted
    :param fig: matplotlib fig
    :param im: matplotlib im
    :param lab: label for the colorbar
    :param ncol: number of rows of axes
    :param nrow: number of columns of axes
    :param fname: filename for output image
    :param nonBaselineScenario: the set of scenarios in the sensitivity analysis being evaluated
    :return: plotted figure
    """
    del_axes_counter = 0
    for i in range(nrow * ncol - datalength):
        fig.delaxes(axs[int((datalength + i) % nrow), int((datalength + i) / nrow)])
        del_axes_counter = del_axes_counter + 1
    if nrow * ncol > datalength:
        if del_axes_counter == 3:
            axins1 = inset_axes(
                axs[int((datalength + 1) % nrow), int((datalength + 1) / nrow)],
                width=str(100 * del_axes_counter) + "%",  # width: 50% of parent_bbox width
                height="10%",  # height: 5%
                loc="center",
            )
        else:
            axins1 = inset_axes(
                axs[int(datalength % nrow), int(datalength / nrow)],
                width=str(100 * del_axes_counter) + "%",  # width: 50% of parent_bbox width
                height="10%",  # height: 5%
                loc="center",
            )
        axins1.xaxis.set_ticks_position("bottom")
        axins1.set_title(lab)
        fig.colorbar(im, cax=axins1, orientation="horizontal")
    elif ncol == 1:
        if nrow == 1:
            cax = fig.add_axes([0.9, 0.25, 0.02, 0.5])
            fig.colorbar(im, cax=cax, shrink=0.6, orientation="vertical", label=lab)
        else:
            fig.colorbar(im, ax=axs[:], shrink=0.6, orientation="vertical", label=lab)
    else:
        fig.colorbar(im, ax=axs[nrow - 1, :], shrink=0.6, orientation="horizontal", label=lab)

    # change figure size and dpi
    fig.set_dpi(300)
    if nrow * ncol == 6:
        plt.gcf().set_size_inches(6, 6)
    elif nrow * ncol == 8:
        plt.gcf().set_size_inches(16, 5.1)
    elif nrow * ncol == 20:
        plt.gcf().set_size_inches(16, 9)
    else:
        plt.gcf().set_size_inches(6, 6)
    plt.savefig("data/data_analysis/images/" + nonBaselineScenario.replace("_", "/") + "/" + fname + ".png", dpi=300)
    plt.show()


def finalize_line_plot(fig, handles, labels, axs, nrow, ncol, counter, title, RCP, nonBaselineScenario):
    """
    adds a legend to the plot and removes unnecessary axes
    :param fig: matplotlib figure
    :param handles: matplotlib handles
    :param labels: matplotlib labels
    :param axs: maxplotlib axs
    :param nrow: the number of rows of subplots
    :param ncol: the number of columns of subplots
    :param counter: the number of used subplots
    :param title: the title of the plot
    :param RCP: the RCP pathway on which the scenarios are evaluated
    :param nonBaselineScenario: the set of scenarios in the sensitivity analysis being evaluated
    :return: N/A
    """
    if nrow * ncol == 1:
        fig.legend(handles, labels, bbox_to_anchor=(1, .895), facecolor='white', framealpha=1)
        plt.subplots_adjust(bottom=0.4, right=.7)
    elif nrow * ncol == 2:
        fig.legend(handles, labels, bbox_to_anchor=(1, .895), facecolor='white', framealpha=1)
        plt.subplots_adjust(bottom=0.4, right=.7)
    elif nrow * ncol == 4:
        fig.legend(handles, labels, bbox_to_anchor=(0.6, 0.6), facecolor='white', framealpha=1)
        plt.tight_layout()
    elif nrow * ncol == 6 and counter == 5:
        fig.legend(handles, labels, bbox_to_anchor=(0.9, 0.4), facecolor='white', framealpha=1)
        plt.tight_layout()
    elif nrow * ncol == 6:
        fig.legend(handles, labels, bbox_to_anchor=(0.15, 0.54), facecolor='white', framealpha=1)
        plt.tight_layout()
    else:
        fig.legend(handles, labels, bbox_to_anchor=(0.94, 0.3), facecolor='white', framealpha=1)
        # plt.tight_layout()

    # remove unnecessary axes
    for i in range(nrow * ncol - counter):
        fig.delaxes(axs[int((counter + i) % nrow), int((counter + i) / nrow)])

    plt.savefig("data/data_analysis/images/" + str(RCP) + "/" + title + ".png", dpi=300)
    plt.show()


def plot_line_on_axs(x, y, lab, color, axs, nrow, ncol, counter):
    """
    Plots a line on the axis
    :param x: x values for the plot
    :param y: y values for the plot
    :param lab: label for the line
    :param color: the color of the line
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
            axs[int(counter % nrow)].plot(x, y, label=lab, color=color)
    elif nrow == 1:
        axs[int(counter % ncol)].plot(x, y, label=lab, color=color)
    else:
        axs[int(counter % nrow), int(counter / nrow)].plot(x, y, label=lab, color=color)


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
            axs.set_xlabel("Year")
            axs.set_title(title)
            handles, labels = axs.get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
        else:
            axs[int(counter % nrow)].set_ylabel(ylabel)
            axs[int(counter % nrow)].set_xlabel("Year")
            axs[int(counter % nrow)].set_title(title)
            handles, labels = axs[0].get_legend_handles_labels()
            labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    elif nrow == 1:
        axs[int(counter % ncol)].set_ylabel(ylabel)
        axs[int(counter % ncol)].set_xlabel("Year")
        axs[int(counter % ncol)].set_title(title)
        handles, labels = axs[0].get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    else:
        axs[int(counter % nrow), int(counter / nrow)].set_ylabel(ylabel)
        axs[int(counter % nrow), int(counter / nrow)].set_title(title)
        # axs[int(counter % ncol), int(counter / ncol)].set_xlabel("Year")
        handles, labels = axs[0, 0].get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))

    return labels, handles


def get_colors(num_versions):
    """
    gets a color mapping based on the number of versions of the product
    :param num_versions: the number of unique entries for each product
    :return: a list containing the requisite colors, the number of colors for each product
    """
    if num_versions == 1:
        num_sub_colors = 1
        return ["#BFBE43", "#74A751", "#698FC6", "#DD9452", "#C16861", "#A577A8", "#72B1B4", "#DCC060", "#AD9077",
                "#9299A9"], num_sub_colors
    elif num_versions == 2:
        cmap = matplotlib.colormaps.get_cmap('tab20')
        num_sub_colors = 2
    elif num_versions == 4:
        cmap = matplotlib.colormaps.get_cmap('tab20b')
        num_sub_colors = 4
    else:
        return ["#1F78C8", "#ff0000", "#33a02c", "#6A33C2", "#ff7f00", "#565656",
                "#FFD700", "#a6cee3", "#FB6496", "#b2df8a", "#CAB2D6", "#FDBF6F",
                "#999999", "#EEE685", "#C8308C", "#FF83FA", "#C814FA", "#0000FF",
                "#36648B", "#00E2E5", "#00FF00", "#778B00", "#BEBE00", "#8B3B00",
                "#A52A3C"], 25
    return [matplotlib.colors.rgb2hex(c) for c in cmap.colors], num_sub_colors


def plot_stacked_bar_product(df, year, column, title, nonBaselineScenario):
    """
    Plots a stacked bar graph
    :param df: dataframe
    :param year: list of years to be plotted
    :param column: column in the df to be plotted
    :param title: title for the plot
    :param nonBaselineScenario: the set of scenarios in the sensitivity analysis being evaluated
    :return: N/A
    """
    try:
        # get subplot information
        nrow, ncol = get_subplot_dimensions([year])
        fig, axs = plt.subplots(nrow, ncol, sharex='all', sharey='all', gridspec_kw={'wspace': 0.2, 'hspace': 0.2})
        colors, num_colors = get_colors(1)

        # format table
        if not isinstance(year, list):
            plot_df = df.loc[:, [year, 'GCAM', column]]
            plot_df = plot_df.pivot(index='GCAM', columns=column, values=year)
            plot_df = plot_df.loc[:, (plot_df != 0).any(axis=0)]
            # add a column to df for sorting, then remove it
            plot_df["sum"] = plot_df.abs().sum(axis=1)
            plot_df = plot_df.sort_values(by="sum", ascending=False)
            plot_df = plot_df.drop(['sum'], axis=1)
            # plot stacked bar chart
            plot_df.plot(kind="bar", stacked=True, color=colors, ax=axs)
        else:
            plot_df = pd.melt(df, id_vars=[column], value_vars=[str(j) for j in year])
            plot_df = plot_df.pivot(index="variable", columns=column, values="value")
            # plot stacked bar chart
            plot_df.plot(kind="bar", stacked=True, color=colors, ax=axs)

            # add the sum of changes
            row_sums = plot_df.sum(axis=1)
            plt.scatter(row_sums.index, row_sums.values, color="black", marker="x", label="Net Change", zorder=3)

            # add the number of the net impact
            for i in row_sums.index:
                plt.text(i, row_sums[i], str(int(row_sums[i])), fontsize=10, ha='center', va='bottom')

            # add a horizontal line at y = 0
            plt.axhline(y=0, color='darkgrey', linestyle='--')

        # format plot
        axs.set_title(title)
        axs.set_ylabel(df["Units"].unique()[0])
        plt.legend(bbox_to_anchor=(1, 1))
        plt.subplots_adjust(bottom=0.15, right=.8, left=.15)
        plt.xticks(rotation=60, ha='right')
        if title == "global land use change by year":
            plt.gcf().set_size_inches(7, 8)
        else:
            plt.gcf().set_size_inches(12, 6)
        plt.savefig("data/data_analysis/images/" + nonBaselineScenario.replace("_", "/") + "/" + title + ".png",
                    dpi=300)
        plt.show()

    except ValueError as e:
        print(e)


def plot_line_product_CI(dataframe, column, title, region=c.GCAMConstants.USA_region, skip_years=3):
    """
    Plots a line grouped by product
    :param dataframe: the data being plotted
    :param column: the column by which the products can be differentiated
    :param title: the title of the plot
    :param region: default region of interest are the US states
    :param skip_years: number of columns to skip in df before relevant plot information
    :return: N/A
    """
    if dataframe.empty:  # if the datafame is empty, nothing can be plotted
        print("empty dataframe")
        return
    # get plot information
    # get subplot size
    ncol, nrow = get_subplot_dimensions(region)

    # make plots and color scheme
    fig, axs = plt.subplots(nrow, ncol, sharey='all', sharex='all')

    # find the number of model versions
    # get color scheme based on number of model versions
    colors, num_colors = get_colors(1)
    # get colors and baseline
    color_map = {item: index for index, item in enumerate(dataframe[column].unique())}
    counter = 0

    # each region gets its own subplot
    for j in region:
        y_region = dataframe[dataframe["GCAM"] == j]
        baseline = ""
        if not y_region.empty:
            baseline = y_region["baseline"].unique()[0]

        # each product gets its own line and color
        for i in dataframe[column].unique():
            y = y_region[y_region[column] == i]
            # baseline is a special line to be plotted
            # if this plot is sorted by baseline, then there is no real need to filter on the baseline
            if column == "baseline":
                baseline = i
            baseline_plot = y[y["scenario"] == baseline]

            if not y.empty:
                # plot all versions in y
                color = colors[color_map[i]]

                y_to_plot = baseline_plot.values.tolist()[0][
                            skip_years:skip_years + len(c.GCAMConstants.plotting_x)]  # only take the x values
                plot_line_on_axs(c.GCAMConstants.plotting_x, y_to_plot, str(i), color, axs, nrow, ncol, counter)

                # plot min and max data across SSPs
                min_seq = [y[str(i)].min() for i in c.GCAMConstants.plotting_x]
                max_seq = [y[str(i)].max() for i in c.GCAMConstants.plotting_x]

                # plot the min and max data
                if nrow == 1 and ncol == 1:
                    axs.fill_between(c.GCAMConstants.plotting_x, y1=min_seq, y2=max_seq, alpha=0.15, color=color)
                elif nrow == 1 or ncol == 1:
                    axs[int(counter % ncol)].fill_between(c.GCAMConstants.plotting_x, y1=min_seq, y2=max_seq,
                                                          alpha=0.15, color=color)
                else:
                    axs[int(counter % nrow), int(counter / nrow)].fill_between(c.GCAMConstants.plotting_x, y1=min_seq,
                                                                               y2=max_seq, alpha=0.15, color=color)

        # finalize each subplot
        units = dataframe['Units'].unique()[0]
        l, h = finalize_line_subplot(axs, units, j, ncol, nrow, counter)
        counter = counter + 1

    finalize_line_plot(fig, h, l, axs, nrow, ncol, counter, title, baseline, "nonBaselineScenario")


def plot_regional_hist_avg(prices, year, title, column, config_fname):
    """
    Plots regional data in a stacked bar histogram
    :param prices: price data being plotted
    :param year: evaluation column
    :param title: title of graph
    :param column: column used to identify unique categories
    :param config_fname: scenario name information
    :return: N/A
    """
    df = prices.loc[:, [str(year), column]]
    products = df[column].unique().tolist()
    units = prices["Units"].unique()[0]
    df = df.pivot(columns=column, values=str(year))
    df = df.sort_values([column for column in df.columns])

    # get colors
    n = len(products)
    if n == 5:
        n = 1
    colors, divisions = get_colors(n / 2)

    if (np.isnan(prices[year].max())) or (np.isnan(prices[year].min())):
        return

    # plot histogram
    if config_fname.split("/")[1] == "nothing":
        bind_width = (prices[year].max() + .1 - prices[year].min() - .1) / 10
    else:
        bind_width = (int(prices[year].max() + .1) - int(prices[year].min() - .1)) / 40
    bins = [bind_width * i for i in
            range(int(prices[year].min() / bind_width) - 1, int(prices[year].max() / bind_width) + 2)]

    data_series = [df[column] for column in df.columns]

    plt.hist(data_series, bins, stacked=True, label=df.columns, histtype='bar',
             color=[colors[i] for i in range(len(products))])

    # finalize plot
    plt.ylabel("count")
    plt.xlabel(units)
    plt.xticks(rotation=60, ha='right')
    plt.xlim(np.floor(prices[year].min() - bind_width), np.ceil(prices[year].max() + bind_width))
    plt.title(title)
    plt.legend(bbox_to_anchor=(1, 1))
    plt.subplots_adjust(bottom=0.4, right=.7)
    plt.savefig("data/data_analysis/images/" + str(config_fname).replace("_", "/") + "/" + title + ".png", dpi=300)
    plt.show()


def plot_marimekko(df, year, x, y, color, title, config_fname, subsidy_df):
    """
    makes a marimekko plot
    :param df: df to be plotted
    :param year: year to be plotted
    :param x: x values
    :param y: y values
    :param color: color
    :param title: subplot title
    :param config_fname: information for storing results
    :param subsidy_df: information about any included subsidies
    :return: N/A
    """
    # update the columns of the dataframe and make it much smaller
    cols = [str(i) + x for i in year]
    cols.extend([str(i) + y for i in year])
    cols.extend([color, "GCAM", "Units" + x, "Units" + y])
    df = df[cols]

    # drop columns that only have nan
    df = df.dropna(how='all', axis=1)

    # get subplot size
    nrow, ncol = get_subplot_dimensions(year)
    # make plots
    fig, axs = plt.subplots(ncol, nrow, sharex=False, sharey=False, constrained_layout=True)
    colors, num = get_colors(1)
    mapping = {df[color].unique()[i]: colors[i] for i in range(len(df[color].unique()))}
    df['colors'] = df[color].map(mapping)
    subsidy_color = "#000000"
    df.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_",
                                                                                     "/") + "/" + title + "_no_subsidy.csv")

    counter = 0
    for i in year:
        try:
            df[str(i) + "_subsidized"] = df.apply(lambda row: data_manipulation.subsidy_lookup(row, str(i), subsidy_df),
                                                  axis=1)
            df = df.sort_values(by=str(i) + "_subsidized")
            add_subsidy_label = True
            unique_labels = {}
            current_x = 0
            for index, col_width in df[str(i) + x].items():
                if df.loc[index, color] in unique_labels:
                    addLabel = False
                else:
                    unique_labels[df.loc[index, color]] = "done"
                    addLabel = True
                axs[int(counter / nrow), int(counter % nrow)].bar(
                    x=current_x + col_width / 2,  # Center the bar within its width
                    height=df.loc[index, str(i) + y],
                    width=col_width,
                    bottom=0,
                    color=df.loc[index, "colors"],
                    linewidth=0.5,
                    label=df.loc[index, color] if addLabel else "_"
                )
                # if there is a subsidy attached to the product, add that in
                product = df.loc[index, "product_price"]
                subsidy_prod = subsidy_df[subsidy_df["stub-technology"].isin([product])]
                if not subsidy_prod.empty:
                    axs[int(counter / nrow), int(counter % nrow)].bar(
                        x=current_x + col_width / 2,  # Center the bar within its width
                        height=subsidy_prod[str(i)],
                        width=col_width,
                        bottom=df.loc[index, str(i) + y] - subsidy_prod[str(i)],  # bottom to top is height of subsidy
                        color=subsidy_color,
                        linewidth=0.5,
                        alpha=0.5,
                        label="Subsidy" if add_subsidy_label else "_"
                    )
                    add_subsidy_label = False
                current_x += col_width

            # update subplot characteristics
            # axs[int(counter / nrow), int(counter % nrow)].set_ylim(0, 1.05 * (
            #             df[str(i) + y].max() + subsidy_df[str(i)].max()))
            axs[int(counter / nrow), int(counter % nrow)].set_title(str(i))
            axs[int(counter / nrow), int(counter % nrow)].set_xlabel(df["Units" + x].unique()[0])
            axs[int(counter / nrow), int(counter % nrow)].set_ylabel(df["Units" + y].unique()[0])
            axs[int(counter / nrow), int(counter % nrow)].set_title(str(i))
            axs[int(counter / nrow), int(counter % nrow)].legend()
            counter += 1
        except KeyError as e:
            print(e)

    # finalize plot
    if counter < ncol * nrow:
        fig.delaxes(axs[int(counter / nrow), int(counter % nrow)])
    plt.suptitle(title)
    plt.gcf().set_size_inches(8, 10)
    plt.savefig("data/data_analysis/images/" + str(config_fname).replace("_", "/") + "/" + title + ".png", dpi=300)
    df.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" + title + ".csv")
    plt.show()
    return df


def compare_marimekko(scenario_df, baseline_df, config_fname):
    """
    compare two marimekko plots
    :param scenario_df: dataframe containing price and supply data for the scenario
    :param baseline_df: dataframe containing price and supply data for the baseline
    :param config_fname: configuration filename to keep track of model outputs
    :return: N/A
    """
    nrow, ncol = get_subplot_dimensions(c.GCAMConstants.plotting_x)
    # make plots
    fig, axs = plt.subplots(ncol, nrow, sharex=False, sharey=False, constrained_layout=True)
    colors, num = get_colors(1)
    counter = 0
    for i in c.GCAMConstants.plotting_x:
        try:
            # get cumulative values, and lower and upper bounds
            scenario_df = scenario_df.sort_values(by=str(i) + "_subsidized")
            scenario_df[str(i) + "_upper"] = scenario_df[str(i) + "_supply"].cumsum()
            scenario_df[str(i) + "_lower"] = scenario_df[str(i) + "_upper"] - scenario_df[str(i) + "_supply"]
            baseline_df = baseline_df.sort_values(by=str(i) + "_subsidized")
            baseline_df[str(i) + "_upper"] = baseline_df[str(i) + "_supply"].cumsum()
            baseline_df[str(i) + "_lower"] = baseline_df[str(i) + "_upper"] - baseline_df[str(i) + "_supply"]

            if max(baseline_df[str(i) + "_upper"]) > max(scenario_df[str(i) + "_upper"]):
                x = np.linspace(baseline_df[str(i) + "_lower"].min(),
                                baseline_df[str(i) + "_upper"].max(), 3000)
            else:
                x = np.linspace(scenario_df[str(i) + "_lower"].min(),
                                scenario_df[str(i) + "_upper"].max(), 3000)

            # create the piecewise functions
            scenario_conditions = []
            for index, row in scenario_df.iterrows():
                scenario_conditions.append(
                    (row[str(i) + "_lower"] <= x) & (x < row[str(i) + "_upper"]))

            scenario_values = scenario_df[str(i) + "_price"].values
            scenario_y = np.piecewise(x, scenario_conditions, scenario_values)

            baseline_conditions = []
            for index, row in baseline_df.iterrows():
                baseline_conditions.append(
                    (row[str(i) + "_lower"] <= x) & (x < row[str(i) + "_upper"]))

            baseline_values = baseline_df[str(i) + "_price"].values
            baseline_y = np.piecewise(x, baseline_conditions, baseline_values)

            marimekko_diff(x, scenario_y, baseline_y, axs, counter, nrow, colors, i)
            counter += 1
        except KeyError as e:
            print(e)

    if counter < ncol * nrow:
        fig.delaxes(axs[int(counter / nrow), int(counter % nrow)])
    title = "change in price and quantity of CDR in comparison to the baseline"
    plt.suptitle(title)
    plt.gcf().set_size_inches(12, 10)
    plt.savefig("data/data_analysis/images/" + str(config_fname).replace("_", "/") + "/" + title + ".png", dpi=300)
    plt.show()


def marimekko_diff(x, scenario_y, baseline_y, axs, counter, nrow, colors, year):
    """
    calculates the difference between two marimekko plots
    :param x: x axis
    :param scenario_y: prices of cdr in the scenario
    :param baseline_y: prices of cdr in the baseline
    :param axs: axis to be plotted on
    :param counter: counter to keep track of current axis
    :param nrow: parameter to keep track of current axis
    :param colors: keep consistent colors
    :param year: year being plotted
    :return: N/A
    """
    df = pd.DataFrame(x)
    df.columns = ["x"]
    df["scenario_y"] = scenario_y
    df["baseline_y"] = baseline_y
    df["diff"] = df.apply(lambda row: marimekko_diff_line(row), axis=1)
    df["width"] = df["x"].max() / len(df["x"])
    df["condition"] = df.apply(lambda row: marimekko_condition(row), axis=1)

    # add in the colors
    rect = Rectangle((0, 0), 0, 0, color=colors[0], label="reduced supply")
    axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
    rect = Rectangle((0, 0), 0, 0, color=colors[1], label="increased supply")
    axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
    rect = Rectangle((0, 0), 0, 0, color=colors[2], label="increased cost")
    axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
    rect = Rectangle((0, 0), 0, 0, color=colors[3], label="decreased cost")
    axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)

    # Iterate and add patches based on a condition in the 'condition' column
    for index, row in df.iterrows():
        if row['condition'] == "reduced supply":
            if row["scenario_y"] == row["baseline_y"] and row["diff"] == 0:
                pass
            else:
                # (x,y) coordinates of the bottom-left corner, width, height
                rect = Rectangle((row['x'], 0), row["width"], row["diff"], color=colors[0])
                axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
        if row['condition'] == "increased supply":
            rect = Rectangle((row['x'], 0), row["width"], row["diff"], color=colors[1])
            axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
        if row['condition'] == "increased cost":
            rect = Rectangle((row['x'], 0), row["width"], row["diff"], color=colors[2])
            axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)
        if row['condition'] == "decreased cost":
            rect = Rectangle((row['x'], 0), row["width"], row["diff"], color=colors[3])
            axs[int(counter / nrow), int(counter % nrow)].add_patch(rect)

    # add a legend for patches
    axs[int(counter / nrow), int(counter % nrow)].set_title(str(year))
    axs[int(counter / nrow), int(counter % nrow)].set_xlim((df["x"].min() * 1.01, df["x"].max() * 1.01))
    axs[int(counter / nrow), int(counter % nrow)].set_ylim(min([0, (df["diff"].min() * 1.01)]),
                                                           max([0, df["diff"].max() * 1.01]))
    axs[int(counter / nrow), int(counter % nrow)].set_xlabel("Mt CO$_2$-eq")
    axs[int(counter / nrow), int(counter % nrow)].set_ylabel("difference in 2025USD/t CO$_2$-eq")
    axs[int(counter / nrow), int(counter % nrow)].legend()


def marimekko_condition(row):
    """
    identifies how supply and price differ compared to other plots
    :param row: row of a pandas dataframe
    :return: one of four categories
    """
    if row["scenario_y"] == 0:
        # this means that there is baseline y
        return "reduced supply"
    if row["baseline_y"] == 0:
        # this means that there is scenario y
        return "increased supply"
    if row["diff"] > 0:
        # this means that the scenario is more expensive
        return "increased cost"
    else:
        return "decreased cost"


def marimekko_diff_line(row):
    """
    calculate the difference between the two marimekko plots
    :param row: row of a pandas dataframe
    :return: difference between the two, or np.nan if the cost of CDR is 0 (no cdr available)
    """
    return row["scenario_y"] - row["baseline_y"]
