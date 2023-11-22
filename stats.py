import pandas as pd
from pylab import *
import statsmodels.formula.api as smf
import constants
import plotting as plotting
from statsmodels.tsa.stattools import adfuller, kpss
import warnings


def calc_price_linkage(x_dataframe, y_dataframe, SSP, year):
    """
    Calculates the price linkage between the x and y data
    :param x_dataframe: the independent variable
    :param y_dataframe: the dependent variable
    :param SSP: the SSP pathway
    :param year: the termination year of the sample
    :return: results object parameters and p-values on a regional basis
    """
    # process data
    x = x_dataframe[(x_dataframe['SSP'].isin(SSP))]
    y = y_dataframe[(y_dataframe['SSP'].isin(SSP))]
    x = x.transpose()  # transpose dataframe
    y = y.transpose()  # transpose dataframe
    x.columns = x.loc['GCAM']  # rename columns
    y.columns = y.loc['GCAM']  # rename columns

    if year == 2050:
        x = x[4:11] #trim other label information from dataframe
        y = y[4:11]  # trim other label information from dataframe
    else:
        x = x[4:21]  # trim other label information from dataframe
        y = y[4:21]  # trim other label information from dataframe

    data=pd.DataFrame()
    region_data = pd.DataFrame()
    results = pd.DataFrame()

    for region in constants.GCAMConstants.GCAM_region:
        #get regional price information
        y_price = y.loc[:, region]
        x_price = x.loc[:, region]

        # compute input variables
        y_lagged = y_price.shift(1)
        x_lagged = x_price.shift(1)
        p1_p1 = y_price - y_lagged
        p2_p2 = x_price - x_lagged
        p2_p1 = x_lagged-y_lagged

        # build dataframe out of data
        region_data["p1p1"] = pd.to_numeric(p1_p1)
        region_data["p2p2"] = pd.to_numeric(p2_p2)
        region_data["p2p1"] = pd.to_numeric(p2_p1)
        region_data["year"] = pd.to_numeric(x_price.index)
        region_data["GCAM"] = region

        data = data.dropna()
        # build model as a type of linear mixed effects model
        # eq4 as from Baffes, J. and Ajwad, M.I., 2001. Identifying price linkages: a review of the literature and an application to the world market of cotton. Applied Economics, 33(15), pp.1927-1941.
        # (p1_t-p1_t-1) = u + (1-B3)(p2_t-1-p1_t-1) + B1(p2_t-p2_t-1) + ut
        md = smf.ols("p1p1 ~ p2p2 + p2p1", region_data)
        mdf = md.fit()
        # print(mdf.summary())

        #test whether 1-B3 (coefficient of p2p1) is meaningfully different than 0 using p-values
        res = pd.Series([mdf.params["p2p1"], mdf.pvalues["p2p1"], region], index=["coef", "pvalue", "GCAM"])
        results = pd.concat([results, pd.DataFrame(res).transpose()])

    return results


def plot_correlation(dataframe, years, SSP, xlabel, ylabel, label_location):
    """
    Plots the correlation between two varaibles
    :param dataframe: merged dataframe containing data from two GCAM products
    :param years: the years of which the correlation is analyzes
    :param SSP: the SSPs for which this correlation is analyzed
    :param label_location: the location of hte legend for the plot
    :param xlabel: the x label for the plot
    :param ylabel: the y label for the plot
    :return: N/A
    """
    colors, num_colors = plotting.get_colors(len(years))
    dataframe = dataframe[(dataframe['SSP'].isin(SSP))]
    df_global = dataframe[dataframe['GCAM'] == "Global"]
    if not df_global.empty:
        df_regional = dataframe.drop(dataframe[dataframe['GCAM'] == "Global"].index)
    else:
        df_regional = dataframe

    x = []
    y = []

    # get set of x and y data
    counter = 0
    for i in years:
        #add x and y values to the overall line
        x.extend(df_regional[str(i) + "_left"].tolist())
        y.extend(df_regional[str(i) + "_right"].tolist())

        #build the ols model
        df = pd.DataFrame(columns=['y', 'x'])
        df['x'] = df_regional[str(i) + "_left"].tolist()
        df['y'] = df_regional[str(i) + "_right"].tolist()
        weights = np.polyfit(df_regional[str(i) + "_left"].tolist(), df_regional[str(i) + "_right"].tolist(), 1) # degree 1
        model = np.poly1d(weights)
        epsilon = model[0]
        beta = model[1]
        results = smf.ols(formula='y ~ model(x)', data=df).fit() # borrow some R syntax here lol
        # print(results.summary())

        #scatter points on the graph
        plt.scatter(df_regional[str(i) + "_left"].tolist(), df_regional[str(i) + "_right"].tolist(),
                    color=colors[counter])

        x_min = min(df_regional[str(i) + "_left"].tolist())
        x_max = max(df_regional[str(i) + "_left"].tolist())
        x_vals = np.linspace(x_min, x_max, 500)
        y_vals = x_vals*beta + epsilon

        plt.plot(x_vals, y_vals, label=str(i) + " | R2 {:.4f}".format(results.rsquared) + " | p-value {:.4f}".format(results.pvalues["model(x)"]), color=colors[counter])
        counter = counter + 1

    # plot all data and best fit line for the overall fit
    # build the ols model
    df = pd.DataFrame(columns=['y', 'x'])
    df['x'] = x
    df['y'] = y
    weights = np.polyfit(x, y, 1)  # degree 1
    model = np.poly1d(weights)
    epsilon = model[0]
    beta = model[1]
    results = smf.ols(formula='y ~ model(x)', data=df).fit()  # borrow some R syntax here lol
    # print(results.summary())

    x_vals = np.linspace(min(x), max(x), 500)
    y_vals = x_vals * beta + epsilon

    plt.plot(x_vals, y_vals, label="overall" + " | R2 {:.4f}".format(results.rsquared) + " | p-value {:.4f}".format(
        results.pvalues["model(x)"]), color="red")

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(loc=label_location)
    plt.show()


def label_autocorr(row, lag, col):
    """
    Used to calculate autocorrelation
    :param row: the row of data
    :param lag: the lag of the data
    :param col: the column of values to be extracted
    :return:
    """
    row = row[col]
    return row.autocorr(lag=lag)


def plot_correlogram(dataframe, SSP, columns, years):
    """
    Plots a correlogram for every SSP in the dataframe
    :param dataframe: dataframe containing yearly difference data
    :param SSP: the list of SSPs to be evaluated
    :return: N/A
    """
    cmap = matplotlib.colormaps.get_cmap('Pastel1')
    colors = [matplotlib.colors.rgb2hex(colo) for colo in cmap.colors]
    # Get data for 1 SSP
    lag = int(len(years) / 2)
    y_col = []
    for k in range(lag):
        if k != 0:
            lag_num = k
            dataframe['lag_' + str(lag_num)] = dataframe.apply(lambda row: label_autocorr(row, lag_num, columns), axis=1)
            y_col.append('lag_' + str(lag_num))

    nrow, ncol = plotting.get_subplot_dimensions(SSP)
    fig, axs = plt.subplots(nrow, ncol, sharex='all', sharey='all', gridspec_kw={'wspace': 0.2, 'hspace': 0.2})

    axs_counter = 0
    for i in SSP:
        df = dataframe[dataframe["SSP"].isin([i])]
        x = [5 + 5 * j for j in range(lag-1)]

        color_counter = 0
        labels = []
        df = df.dropna()
        for j in df["product"].unique():
            x_plotting = []
            y_plotting = []
            color_counter = color_counter + 1
            for k in df["GCAM"].unique():
                df_to_plot = df[df["product"].isin([j]) & df["GCAM"].isin([k])]
                x_plotting.append(x)
                if not df_to_plot.empty:
                    y_plotting.append(df_to_plot[y_col].values.tolist()[0])
            #transpose data to get different y plots
            data = np.array(y_plotting).T.tolist()
            parts = axs[int(axs_counter / ncol), int(axs_counter % ncol)].violinplot(data,
                                                                                     showmeans=False, showmedians=False,
                                                                                     showextrema=False)

            # set colors and transparency of violin plot
            for pc in parts['bodies']:
                pc.set_facecolor(colors[color_counter])
                pc.set_edgecolor('black')
                pc.set_alpha(0.4)

            # set colors and transparency of medians
            quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)

            inds = np.arange(1, len(medians) + 1)
            axs[int(axs_counter / ncol), int(axs_counter % ncol)].scatter(inds, medians, marker='o', edgecolor="black", color=colors[color_counter], s=30, zorder=3, label=str(j))


        axs[int(axs_counter / ncol), int(axs_counter % ncol)].set_xlabel("lag in years")
        axs[int(axs_counter / ncol), int(axs_counter % ncol)].set_title(str(i))
        axs[int(axs_counter / ncol), int(axs_counter % ncol)].set_ylabel("correlation")
        axs[int(axs_counter / ncol), int(axs_counter % ncol)].set_xticks(np.arange(1, len(x) + 1), labels=x)
        axs[int(axs_counter / ncol), int(axs_counter % ncol)].set_xlim(0.25, len(x) + 0.75)
        axs_counter = axs_counter + 1

    #put labels on graph
    handles, labels = axs[1,1].get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    fig.legend(handles, labels, bbox_to_anchor=(0.9, 0.3), facecolor='white', framealpha=1)
    fig.delaxes(axs[1, 2])
    plt.show()


def adf_test(timeseries):
    """
    calculates the ADF test on a timeseries
    :param timeseries: data used for the adf test
    :return: results of the adf test
    """
    #print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag="AIC")
    dfoutput = pd.Series(
        dftest[0:4],
        index=[
            "Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ],
    )
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    #print(dfoutput)
    return dftest


def kpss_test(timeseries):
    """
    KPSS test for stationarity
    :param timeseries: the time series being tested
    :return: the results of the kpss test
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        #print("Results of KPSS Test:")
        kpsstest = kpss(timeseries, regression="c", nlags="auto")
        kpss_output = pd.Series(
            kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
        )
        for key, value in kpsstest[3].items():
            kpss_output["Critical Value (%s)" % key] = value
        #print(kpss_output)
    return kpsstest


def stationarity_test(dataframe, year):
    """
    Tests for stationarity in a dataset constrained by various years
    :param dataframe: the data being processed
    :param year: the final year of the time series
    :return: N/A
    """
    #convert the dataframe to have time as an index and region as the columns
    df = dataframe.transpose() # transpose dataframe
    df.columns=df.loc['GCAM'] # rename columns
    if year == 2050:
        df = df[4:11] #trim other label information from dataframe
    else:
        df = df[4:21]  # trim other label information from dataframe
    df.index = pd.to_datetime(df.index)

    #convert row indices to datetime
    series_index = ["ADF Test Statistic", "ADF p-value", "KDSS Test Statistic", "KDSS p-value", "Case"]
    stationarity = pd.DataFrame()
    #run stationarity tests on time series for all regions
    for series_name, series in df.items():
        #do time series tests
        adf = adf_test(series)
        kpss =kpss_test(series)
        s = [adf[0], adf[1], kpss[0], kpss[1]]

        #check for cases
        #adf: when test statisitic is lower than critical value, reject null hypothesis and series is stationary
        #kpss: when test statistic is less than cricial value, fail to reject null hypothesis and series is stationary
        adf_crit = dict((k, v) for k, v in adf[4].items() if v <= adf[0]) #add any critical values to dictionary that a lower than test statistic
        kpss_crit = dict((k, v) for k, v in kpss[3].items() if v >= kpss[0]) #add any critical values to dictionary that a greater than test statistic
        adf_stationary= False
        kpss_stationary = False
        if adf[1] < 0.05 and len(adf_crit) == 0:
            adf_stationary = True
        if kpss[1] < 0.05 and len(kpss_crit) == 0:
            kpss_stationary = True

        if adf_stationary and kpss_stationary:
            s.append("Stationary")
        elif not adf_stationary and not kpss_stationary:
            s.append("Non-Stationary")
        elif not adf_stationary and kpss_stationary:
            s.append("Trend Stationry")
        else:
            s.append("Difference Stationry")

        stationarity[series_name] = pd.Series(s, index=series_index)

    #print out findings of stationarity tests
    stationarity = stationarity.transpose()
    if stationarity.Case.str.contains("Non-Stationary").sum() > 24:
        print("Likely Non-Stationary")
    elif stationarity.Case.str.contains("Stationary").sum() > 24:
        print("Likely Stationary")
    else:
        print("No meaningful conclusion")

    # print(stationarity)

