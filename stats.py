import pandas as pd
from pylab import *
import statsmodels.formula.api as smf
import statsmodels.api as sm
import plotting as plotting
from statsmodels.tsa.stattools import adfuller, kpss


def plot_correlation(dataframe, years, SSP, xlabel, ylabel, label_location):
    """
    Plots the correlation between two varaibles
    :param dataframe: merged dataframe containing data from two GCAM products
    :param years: the years of which the correlation is analyzes
    :param SSP: the SSPs for which this correlation is analyzed
    :param legend_location: the location of hte legend for the plot
    :param xlabel: the x label for the plot
    :param ylabel: the y label for the plot
    :return: N/A
    """
    sunspots = sm.datasets.sunspots.load_pandas().data
    sunspots.index = pd.Index(sm.tsa.datetools.dates_from_range("1700", "2008"))
    del sunspots["YEAR"]
    adf_test(sunspots["SUNACTIVITY"])

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
    #print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    #print(kpss_output)
    return kpsstest


def stationarity_test(dataframe):
    #convert the dataframe to have time as an index and region as the columns
    df = dataframe.transpose() # transpose dataframe
    df.columns=df.loc['GCAM'] # rename columns
    df = df[:21] #trim other label information from dataframe
    df.index = pd.to_datetime(df.index)
    #TODO keep only years 2025-2050???

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

