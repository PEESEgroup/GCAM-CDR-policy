import os
import plotting
import data_manipulation
import constants as c
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
from scipy import stats


def main(reference_year):
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    config_fname = ["45Q-2040-h_1500Mt-CostDecrease",
              "45Q-2050-h_1500Mt-CostDecrease",
              "CDRIA-2035-h_1500Mt-CostDecrease",
              "CDRIA-2050-h_1500Mt-CostDecrease",
              "innovation-DACHubs-h_1500Mt-CostDecrease",
              "innovation-maintain-h_1500Mt-CostDecrease",
              "innovation-rhodium6b-h_1500Mt-CostDecrease",
              "innovation-rhodium18b-h_1500Mt-CostDecrease",
              "innovation-triple-h_1500Mt-CostDecrease",
              "procure-3B-h_1500Mt-CostDecrease",
              "procure-Rhodium-h_1500Mt-CostDecrease",
              "procure-scaling-h_1500Mt-CostDecrease",
              "45Q-2040-l_500Mt-CostDecrease",
              "45Q-2050-l_500Mt-CostDecrease",
              "CDRIA-2035-l_500Mt-CostDecrease",
              "CDRIA-2050-l_500Mt-CostDecrease",
              "innovation-DACHubs-l_500Mt-CostDecrease",
              "innovation-maintain-l_500Mt-CostDecrease",
              "innovation-rhodium6b-l_500Mt-CostDecrease",
              "innovation-rhodium18b-l_500Mt-CostDecrease",
              "innovation-triple-l_500Mt-CostDecrease",
              "procure-3B-l_500Mt-CostDecrease",
              "procure-Rhodium-l_500Mt-CostDecrease",
              "procure-scaling-l_500Mt-CostDecrease",
              "100Mt-CostDecrease_100Mt-CostDecrease",
              "500Mt-CostDecrease_500Mt-CostDecrease",
              "1500Mt-CostDecrease_1500Mt-CostDecrease",
              "2400Mt-CostDecrease_2400Mt-CostDecrease",
              "4100Mt-CostDecrease_4100Mt-CostDecrease",
              "45Q-2040-maintain-l_500Mt-CostDecrease",
              "procure-scaling-maintain-h_1500Mt-CostDecrease"
              ]
    # os.makedirs("./data/data_analysis/images/" + config_fname + "/", exist_ok=True)
    # many methods are commented out, but to run them just uncomment and run
    # marginal_supply()
    # tech_neutrality()
    # compare_policy_costs("45Q-2040-l_500Mt-CostDecrease", "45Q-2040-maintain-l_500Mt-CostDecrease")
    # compare_policy_costs( "innovation-maintain-h_1500Mt-CostDecrease", "procure-scaling-maintain-h_1500Mt-CostDecrease")
    # CAGR(config_fname, "2050")
    # land_allocation(config_fname, "2050")
    # cement(config_fname, "2050")
    # electricity(config_fname, "2050")
    # state_CDR(config_fname, "2050")
    # C_tax(config_fname, reference_year)
    # C_prices(config_fname, reference_year)
    # CDR_subsidies(config_fname, "2035", "2040")
    # npv_breakdown()


def npv_breakdown():
    """
    calculates which categories contribute to npv
    :return: plot of relevant data
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    # get CDR data
    all_data = pd.DataFrame()
    for nonBaselineScenario in scenarios:
        nonBaselineScenario = str(nonBaselineScenario).replace("_", "/")
        fpath = "./data/data_analysis/supplementary_tables/" + nonBaselineScenario + "/interpolated costs of achieving net zero.csv"
        pyrolysis_df = pd.read_csv(fpath)
        baseline = nonBaselineScenario.split("/")[1]
        pyrolysis_df["scenario"] = nonBaselineScenario.split("/")[0]
        pyrolysis_df["baseline"] = baseline
        # avoids having to merge tables but kinda ugly
        pyrolysis_df[
            "CDR (Mt)"] = 100 if baseline == "nzn" else 500 if baseline == "low" else 1500 if baseline == "high" else 2400 if baseline == "excess" else 4100
        if pyrolysis_df["scenario"].unique()[0] in ["low", "high", "nzn", "excess", "4gt"]:
            pyrolysis_df["scenario"] = pyrolysis_df["CDR (Mt)"].astype(str) + " Mt Baseline"

        # fix some typesetting
        pyrolysis_df["cost_type"] = pyrolysis_df["cost_type"].str.title().str.replace('Cdr', 'CDR')
        pyrolysis_df["scenario"] = pyrolysis_df["scenario"].str.replace('s1-', '')

        if all_data.empty:
            all_data = pyrolysis_df
        else:
            all_data = pd.concat([all_data, pyrolysis_df])
    CDR = all_data[["cost_type", "npv_0.12", "scenario", "baseline", "CDR (Mt)"]]

    # group by 'scenario' and 'baseline' to calculate the total/percentage NPV for each group
    CDR["total_NPV"] = CDR.groupby(['scenario', 'baseline'])['npv_0.12'].transform('sum')

    # Pivot the data
    plot_df = CDR.pivot_table(
        index=['baseline', 'scenario', 'CDR (Mt)', "total_NPV"],
        columns='cost_type',
        values='npv_0.12'
    ).reset_index()

    # Set up the GridSpec with height ratios
    baselines = plot_df['baseline'].unique()
    height_counts = [len(plot_df[plot_df['baseline'] == bl]) for bl in baselines]

    n_cols = 2
    n_rows = (len(baselines) + 1) // n_cols

    row_height_ratios = []
    for i in range(0, len(height_counts), n_cols):
        chunk = height_counts[i: i + n_cols]
        row_height_ratios.append(max(chunk))

    # set the figure size
    fig = plt.figure(figsize=(14, sum(row_height_ratios) * 0.4))
    gs = gridspec.GridSpec(n_rows, n_cols, height_ratios=row_height_ratios)

    # set some values for the plotting
    cost_categories = ['Deadweight Loss', 'CDR Market', 'Subsidy', 'Procurement Costs',
                       'Investment In R&D']  # CDR['cost_type'].unique()
    main_ax = None  # Placeholder to hold the first axis for sharing
    colors = ["#0047BB", "#00B5E2", "#c22a90", "#00AE8D", "#8AB7E9"]

    # Plotting with sharex
    for i, bl in enumerate(baselines):
        # Initialize the first axis, then share all subsequent axes with it
        if i == 0:
            ax = fig.add_subplot(gs[i // n_cols, i % n_cols])
            main_ax = ax
        else:
            ax = fig.add_subplot(gs[i // n_cols, i % n_cols], sharex=main_ax)

        # get the subset of policy scenarios in a given baseline
        subset = plot_df[plot_df['baseline'] == bl]

        # make sure the baseline is actually the first one to be plotted
        baseline = subset[subset['scenario'].str.contains("Baseline")].copy(deep=True)
        rest = subset[~subset['scenario'].str.contains("Baseline")].copy(deep=True)
        rest = rest.sort_values(by='total_NPV', ascending=False)
        subset = pd.concat([rest, baseline])
        subset = subset.set_index('scenario')

        subset[cost_categories].plot(kind='barh', stacked=True, ax=ax, legend=False, width=0.8, color=colors)
        ax.set_ylabel('')
        ax.set_xlim(-.1, 1.4)  # Hard-code x-axis limit
        # Remove the top and right lines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # show x-axis labels on the bottom-most subplots
        if (i // n_cols) < (n_rows - 1):
            plt.setp(ax.get_xticklabels(), visible=False)
            ax.set_xlabel('')
        else:
            ax.set_xlabel('NPV (Trillion USD)')

    handles, labels = main_ax.get_legend_handles_labels()
    fig.legend(handles, labels, title='Cost Type', ncol=3, loc='center left', bbox_to_anchor=(0.55, 0.1))
    plt.tight_layout()
    plt.savefig('./data/data_analysis/images/stacked_cost_contribution.png')
    plt.show()


def marginal_supply():
    """
    calculate the marginal supply in a combination of policy scenarios
    :return: plot showing results
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high", "nzn_nzn",
                 "excess_excess", "4gt_4gt"]

    # get CDR data
    all_data = pd.DataFrame()
    for nonBaselineScenario in scenarios:
        nonBaselineScenario = str(nonBaselineScenario).replace("_", "/")
        fpath = "./data/data_analysis/supplementary_tables/" + nonBaselineScenario + "/policy cost by technology.csv"
        pyrolysis_df = pd.read_csv(fpath)
        if all_data.empty:
            all_data = pyrolysis_df
        else:
            all_data = pd.concat([all_data, pyrolysis_df])
    CDR = all_data[["2025_supply", "2030_supply", "2035_supply", "2040_supply", "2045_supply", "2050_supply",
                    "scenario", "baseline", "product", "Units"]]
    CDR = CDR[CDR["product"].isin(["BECCS", "DAC", "OEW", "TEW"])]
    CDR = CDR.fillna(0)

    # scenario pairs
    scenario_pairs = [('nzn', 'low'),
                      ('low', 's1-procureScaling-l'),
                      ('low', 's1-procure3B-l'),
                      ('low', 's1-procureRhodium-l'),
                      ('low', 'high'),
                      ('high', 's1-procureScaling-h'),
                      ('high', "s1-procure3B-h"),
                      ('high', "s1-procureRhodium-h"),
                      ('high', 'excess'),
                      ('excess', '4gt')]
    year_cols = ['2030_supply', '2035_supply', '2040_supply', '2045_supply', '2050_supply']
    id_cols = 'product'

    # a list to store results
    delta_results = []

    # get the source data (smallest scenario for each year)
    source = CDR[CDR['scenario'] == "nzn"].copy(deep=True).set_index(id_cols)[year_cols]
    source = source.div(source.sum())
    source['comparison'] = "nzn"
    delta_results.append(source.reset_index())

    for s1, s2 in scenario_pairs:
        # filter and set index to align rows for subtraction
        df1 = CDR[CDR['scenario'] == s1].set_index(id_cols)[year_cols]
        df2 = CDR[CDR['scenario'] == s2].set_index(id_cols)[year_cols]

        # subtract (Scenario 2 - Scenario 1) because S2 is always larger, then normalize to sum to 1
        diff = df2.sub(df1, fill_value=0)
        diff = diff.div(diff.sum())

        # label the new data with the paired name
        diff['comparison'] = f"<{s2}, {s1}>"

        # reset index to bring id_cols back as columns
        delta_results.append(diff.reset_index())

    # get the target data (largest scenario for each year)
    source = CDR[CDR['scenario'] == "4gt"].copy(deep=True).set_index(id_cols)[year_cols]
    source = source.div(source.sum())
    source['comparison'] = "4gt"
    delta_results.append(source.reset_index())

    # combine into a final DataFrame
    df_deltas = pd.concat(delta_results, ignore_index=True)
    df_deltas["2030"] = df_deltas["2030_supply"]
    df_deltas["2035"] = df_deltas["2035_supply"]
    df_deltas["2040"] = df_deltas["2040_supply"]
    df_deltas["2045"] = df_deltas["2045_supply"]
    df_deltas["2050"] = df_deltas["2050_supply"]
    # add a mask
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-l, low>', '2040'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-h, high>', '2040'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-l, low>', '2040'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-h, high>', '2040'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-l, low>', '2045'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-h, high>', '2045'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-l, low>', '2045'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-h, high>', '2045'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-l, low>', '2050'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procureScaling-h, high>', '2050'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-l, low>', '2050'] = np.nan
    df_deltas.loc[df_deltas['comparison'] == '<s1-procure3B-h, high>', '2050'] = np.nan
    df_deltas = df_deltas[["comparison", "product", "2030", "2035", "2040", "2045", "2050"]]

    # set up plot
    years = ['2030', '2035', '2040', '2045', '2050']
    all_comparisons = list(df_deltas['comparison'].unique())
    products = list(df_deltas['product'].unique())
    colors = ["#BFBE43", "#74A751", "#698FC6", "#DD9452"]

    # set up the grid (3 rows, 2 columns)
    fig, axes = plt.subplots(2, 3, figsize=(20, 12), sharex=False, sharey=True, layout="tight")
    axes_flat = axes.flatten()

    for i, year in enumerate(years):
        ax = axes_flat[i]

        # Filter valid comparisons for the specific year
        valid_comps = [c for c in all_comparisons if not df_deltas[df_deltas['comparison'] == c][year].isna().all()]

        x_pos = np.arange(len(valid_comps))
        starts_pos = np.zeros(len(valid_comps))
        starts_neg = np.zeros(len(valid_comps))

        for p_idx, product in enumerate(products):
            # Extract values
            values = []
            for comp in valid_comps:
                val = df_deltas[(df_deltas['comparison'] == comp) & (df_deltas['product'] == product)][year].sum()
                values.append(0 if np.isnan(val) else val)

            values = np.array(values)
            current_bottom = np.where(values >= 0, starts_pos, starts_neg)

            # Plot bars
            bars = ax.bar(x_pos, values, bottom=current_bottom, color=colors[p_idx],
                          edgecolor='white', width=0.8, label=product if i == 0 else "")

            # Add Value Labels
            for j, bar in enumerate(bars):
                val = values[j]
                if abs(val) > 0.1:  # label segments larger than 10% for readability
                    # Position text in the middle of the segment
                    text_y = current_bottom[j] + (val / 2)
                    ax.text(bar.get_x() + bar.get_width() / 2, text_y, f'{val:.2f}',
                            ha='center', va='center', color='white', fontweight='bold', fontsize=9)

            starts_pos += np.maximum(0, values)
            starts_neg += np.minimum(0, values)

        # Formatting Subplot
        ax.set_title(f"{year}", fontsize=14, fontweight='bold')
        ax.axhline(0, color='black', linewidth=1)
        ax.set_xticks(x_pos)
        # Rename all the comparisons to make for pretty labeling
        valid_comps = [
            i.replace("s1-", "").replace("nzn", "100 Mt").replace("low", "500 Mt").replace("high", "1500 Mt").
            replace("excess", "2400 Mt").replace("4gt", "4100 Mt") for i in valid_comps]
        ax.set_xticklabels(valid_comps, rotation=30, ha='right', fontsize=11)
        ax.set_ylabel("Normalized Delta")
        ax.grid(axis='y', linestyle=':', alpha=0.6)

    # add legend to 6th axis
    legend_ax = axes_flat[5]
    legend_ax.axis('off')  # Hide the plot lines/grid

    # Create custom legend handles
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=colors[i], label=products[i]) for i in range(len(products))]

    legend_ax.legend(handles=legend_elements, title="CDR Technologies",
                     loc='center', fontsize=14, title_fontsize=16, frameon=False)

    plt.savefig("data/data_analysis/images/Marginal_Supply_Grid.png", dpi=300, bbox_inches='tight')
    plt.show()


def tech_neutrality():
    """
    method to calculate the extent to which policies are technically neutral by measuring changes in market supply
    :return: plot of relevant data
    """
    scenarios = ["low_low", "high_high",
                 "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high",
                 "CDRIA-2050_low", "CDRIA-2050_high",
                 "s1-procureRhodium-l_low", "s1-procureRhodium-h_high",
                 "s1-procureScaling-l_low", "s1-procure3B-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high",
                 "CDRIA-2035_low", "CDRIA-2035_high"]

    # get CDR data
    all_data = pd.DataFrame()
    for nonBaselineScenario in scenarios:
        nonBaselineScenario = str(nonBaselineScenario).replace("_", "/")
        fpath = "./data/data_analysis/supplementary_tables/" + nonBaselineScenario + "/policy cost by technology.csv"
        pyrolysis_df = pd.read_csv(fpath)
        if all_data.empty:
            all_data = pyrolysis_df
        else:
            all_data = pd.concat([all_data, pyrolysis_df])
    CDR = all_data[["2025_supply", "2030_supply", "2035_supply", "2040_supply", "2045_supply", "2050_supply",
                    "2025", "2030", "2035", "2040", "2045", "2050",
                    "scenario", "baseline", "product", "Units"]]
    CDR = CDR[CDR["product"].isin(["BECCS", "DAC", "OEW", "TEW"])]
    CDR = CDR.fillna(0)  # fill na with 0

    # subtract the effects of the baseline scenarios to find the impacts of policy
    baselines = CDR[(CDR["scenario"] == "low") | (CDR["scenario"] == "high")].copy(deep=True)
    CDR = CDR[~CDR["scenario"].isin(["low", "high"])]
    CDR = pd.merge(CDR, baselines, "left", ["baseline", "product", "Units"], suffixes=("_original", "_baseline"))
    CDR["scenario"] = CDR["scenario_original"]

    # calculate the changes in supply
    for i in c.GCAMConstants.plotting_x:
        CDR[str(i) + "_supply"] = CDR[str(i) + "_supply_original"] - CDR[str(i) + "_supply_baseline"]
    CDR = CDR[["2025_supply", "2030_supply", "2035_supply", "2040_supply", "2045_supply", "2050_supply",
               "scenario", "baseline", "product", "Units"]]

    # calculate spend and supply and which technology it is applied to
    for i in c.GCAMConstants.plotting_x:
        supply_sums = CDR.groupby(['scenario', "baseline"])[str(i) + "_supply"].transform(lambda x: x.abs().sum())
        CDR[str(i)] = CDR[str(i) + "_supply"] / supply_sums
        # what is the impact of policy on supply of CDR by technology compared to baseline?

    # mask data
    # no 2025 data
    CDR["2025"] = np.nan
    # procure scaling/3B have no 2040+ data
    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2040'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2040'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2040'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2040'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2040'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2045'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2045'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2045'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2045'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2045'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2050'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2050'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2050'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2050'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2050'] = np.nan

    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2040_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2040_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2040_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2040_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2040_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2045_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2045_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2045_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2045_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2045_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-l', '2050_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procureScaling-h', '2050_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 'CDRIA-2035', '2050_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-l', '2050_supply'] = np.nan
    CDR.loc[CDR['scenario'] == 's1-procure3B-h', '2050_supply'] = np.nan

    # group by policy type
    # set new column as policy type
    CI_data = pd.DataFrame()
    CDR["%Label"] = CDR.apply(lambda row: "Procurement" if "procure" in row['scenario'] else "Innovation" if
    "innovation" in row['scenario'] else "CDRIA", axis=1)
    CDR["MtLabel"] = CDR.apply(lambda row: row['scenario'] if "procure" in row['scenario'] else "Innovation" if
    "innovation" in row['scenario'] else "CDRIA",
                               axis=1)  # do not want to aggregate procurement scenarios by Mt basis because CI would be nonsense
    for bl in CDR["baseline"].unique():
        baseline = CDR[CDR["baseline"] == bl]
        for product in baseline["product"].unique():
            technology = baseline[baseline["product"] == product].copy(
                deep=True)  # filter data by baseline and product before doing CI work
            for year in c.GCAMConstants.plotting_x:
                percent = technology.groupby('%Label')[str(year)].apply(get_min_max).unstack().reset_index(
                    names="Policy Type")
                percent["baseline"] = bl
                percent["product"] = product
                percent["year"] = str(year)
                MT = technology.groupby('MtLabel')[str(year) + "_supply"].apply(get_min_max).unstack().reset_index(
                    names="Policy Type")
                MT["baseline"] = bl
                MT["product"] = product
                MT["year"] = str(year) + "_supply"
                CI_data = pd.concat([CI_data, percent, MT])

    # iterate through baselines and supply type
    for baseline in ["low", "high"]:
        for suffix in ["_supply", ""]:
            CDR_baseline = CI_data[CI_data["baseline"] == baseline]
            years = ['2030' + suffix, '2040' + suffix, '2050' + suffix]
            scenarios = CDR_baseline['Policy Type'].unique()
            products = CDR_baseline['product'].unique()

            # set up the grid: Rows = Scenarios, Columns = Years
            if suffix == "":
                fig, axes = plt.subplots(3, 3, figsize=(14, 4), sharey=True, sharex=True, layout="constrained")
            else:
                fig, axes = plt.subplots(3, len(scenarios), figsize=(14, 4), sharey=True, sharex=True,
                                         layout="constrained")

            colors = ["#BFBE43", "#74A751", "#698FC6", "#DD9452"]
            for row_idx, scenario_name in enumerate(scenarios):
                if not (suffix == "" and "s1-" in scenario_name):
                    if not (suffix == "_supply" and scenario_name == "Procurement"):
                        scenario_df = CDR_baseline[CDR_baseline['Policy Type'] == scenario_name]

                        # reformat the table to have years as columns
                        scenario_df_mean = scenario_df.pivot(index=['product', "baseline", "Policy Type"],
                                                             columns='year', values='mean').reset_index()
                        scenario_df_low = scenario_df.pivot(index=['product', "baseline", "Policy Type"],
                                                            columns='year',
                                                            values='minimum').reset_index()
                        scenario_df_high = scenario_df.pivot(index=['product', "baseline", "Policy Type"],
                                                             columns='year',
                                                             values='maximum').reset_index()

                        for col_idx, year in enumerate(years):
                            ax = axes[col_idx, row_idx] if len(scenarios) > 1 else axes[col_idx]

                            if not scenario_df_mean[year].isna().all():
                                # if there is data, extract it for plotting
                                product_totals = scenario_df_mean.groupby('product')[str(year)].sum().reindex(products)
                                minimum = scenario_df_low.groupby('product')[str(year)].sum(min_count=1).reindex(
                                    products).dropna()
                                maximum = scenario_df_high.groupby('product')[str(year)].sum(min_count=1).reindex(
                                    products).dropna()
                                bars = ax.barh(products, product_totals, color=colors, edgecolor='black', alpha=0.8)
                                scatter_low = ax.scatter(minimum, minimum.index.tolist(), color='black', zorder=3,
                                                         marker="x")
                                scatter_high = ax.scatter(maximum, maximum.index.tolist(), color='black', zorder=3,
                                                          marker="x")
                                for i in minimum.index.tolist():  # draw a line that connects
                                    ax.plot([minimum[i], maximum[i]], [i, i], zorder=4, color="grey")

                                v_line_pos = 0 if "Innovation" in scenario_name or "CDRIA" in scenario_name else 0.25
                                if suffix == "_supply":
                                    if v_line_pos == 0:  # don't put line on procurement graphs for Mt supply
                                        ax.axvline(x=v_line_pos, color='black', linestyle='-', linewidth=2,
                                                   label='Tech-Neutral Target')
                                else:
                                    ax.axvline(x=v_line_pos, color='black', linestyle='-', linewidth=2,
                                               label='Tech-Neutral Target')

                                # label only certain subplots
                                if row_idx == 0:
                                    if suffix == "_supply":
                                        year = year.split("_")[0]
                                    ax.set_ylabel(f"{year}", fontweight='bold', fontsize=12)

                                if col_idx == 0:
                                    ax.set_title(
                                        f"{scenario_name.replace('s1-', '').replace('-l', '-500 Mt').replace('-h', '-1500 Mt')}",
                                        fontsize=10, fontweight='bold')

                                if col_idx == 2:
                                    if suffix == "_supply":
                                        ax.set_xlabel("Mt")
                                    else:
                                        ax.set_xlabel("relative change")

                                ax.grid(axis='x', linestyle='--', alpha=0.6)
                            else:
                                # delete plot
                                fig.delaxes(ax)

            # add a single legend
            legend_elements = [Line2D([0], [0], color=colors[i], lw=4, label=p) for i, p in enumerate(products)]
            fig.legend(handles=legend_elements, title="CDR Technologies", loc='outside upper center',
                       ncol=2, title_fontsize=15, fontsize=12)
            plt.savefig(f"data/data_analysis/images/CDR-Technologies-{baseline}-{suffix}.png", dpi=300)
            plt.show()


def get_min_max(x):
    # Calculate sample statistics
    x = x.dropna()
    if len(x) == 0:
        return pd.Series({'mean': np.nan, 'minimum': np.nan, 'maximum': np.nan})
    elif len(x) == 1:
        return pd.Series({'mean': np.mean(x), 'minimum': np.nan, 'maximum': np.nan})
    else:
        return pd.Series({'mean': np.mean(x), 'minimum': np.min(x), 'maximum': np.max(x)})


def CAGR(config_fname, reference_year):
    """
    calculates the compound annual growth rate for each technology for the baseline scenarios
    :param config_fname: not needed
    :param reference_year: not needed
    :return: N/A
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low",
                 "45Q-2040_high", "45Q-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    CDR = data_manipulation.get_sensitivity_data(scenarios, "CDR_by_tech")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]
    CDR = data_manipulation.group(CDR, ["baseline", "scenario", "technology"])
    CDR["GCAM"] = "USA"
    CDR["Units"] = "CAGR (%)"

    # CAGR calculations
    for i in c.GCAMConstants.plotting_x:
        # rename columns
        CDR[str(i) + "_original"] = CDR[str(i)]

    for i in c.GCAMConstants.plotting_x:
        # calculate CAGR
        if i > 2025:
            # (new/old)^(1/t [5 years]) -1     -> *100 to go to %
            CDR[str(i)] = 100 * ((CDR[str(i) + "_original"] / CDR[str(i - 5) + "_original"]) ** (1 / 5) - 1)
        else:
            CDR[str(i)] = np.nan

    CDR_DAC = CDR[CDR["technology"] == "DAC"].copy(deep=True)
    CDR_BECCS = CDR[CDR["technology"] == "BECCS"].copy(deep=True)
    CDR_OEW = CDR[CDR["technology"] == "OEW"].copy(deep=True)
    CDR_TEW = CDR[CDR["technology"] == "TEW"].copy(deep=True)

    plotting.plot_line_product_CI(CDR_DAC, "baseline", "CAGR for DAC by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_BECCS, "baseline", "CAGR for BECCS by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_OEW, "baseline", "CAGR for OEW by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(CDR_TEW, "baseline", "CAGR for TEW by baseline scenario", region=["USA"])


def land_allocation(config_fname, reference_year):
    """
    calculates the land allocation by type
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant data
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    allocation = data_manipulation.get_sensitivity_data(scenarios, "aggregated_land_allocation", "masked")
    allocation = allocation[allocation["GCAM"] == "USA"]
    allocation = allocation.drop('Unnamed: 0', axis=1)
    allocation["Units"] = "Land (thousand km$^2$)"

    biomass_allocation = allocation[allocation["LandLeaf"] == "biomass"].copy(deep=True)
    managed_forests = allocation[allocation["LandLeaf"] == "forest (managed)"].copy(deep=True)
    unmanaged_forests = allocation[allocation["LandLeaf"] == "forest (unmanaged)"].copy(deep=True)

    plotting.plot_line_product_CI(biomass_allocation, "baseline",
                                  "Land allocated to bioenergy crops by baseline scenario", region=["USA"])
    plotting.plot_line_product_CI(managed_forests, "baseline", "Land allocated to managed forests by baseline scenario",
                                  region=["USA"])
    plotting.plot_line_product_CI(unmanaged_forests, "baseline",
                                  "Land allocated to unmanaged forests by baseline scenario", region=["USA"])


def C_tax(config_fname, reference_year):
    """
    calculate size of C tax revenue
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant information
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]
    CO2_emissions = data_manipulation.get_sensitivity_data(scenarios, "CO2_emissions_by_sector")
    CO2_emissions = CO2_emissions[CO2_emissions["GCAM"].isin(c.GCAMConstants.USA_region)]
    CO2_emissions = CO2_emissions[CO2_emissions["sector"] != "CDR_regional"]  # excluded from the C tax
    CO2_emissions = CO2_emissions.groupby(["scenario", "baseline", "Units"]).sum(min_count=1).reset_index()
    # get a baseline CO2 emissions
    baseline_emissions = pd.read_csv("data/data_analysis/baseline_co2_emissions.csv")
    # process emissions revenue
    CO2_prices = data_manipulation.get_sensitivity_data(scenarios, "CO2_prices")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_tax_revenue = pd.merge(CO2_emissions, CO2_prices, "left", ["baseline", "scenario"],
                               suffixes=("_supply", "_price"))
    for i in c.GCAMConstants.plotting_x:
        # (Mt C * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        CO2_tax_revenue[str(i)] = (CO2_tax_revenue[str(i) + "_supply"] / c.GCAMConstants.CO2_to_C) * (
                CO2_tax_revenue[str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC) / 1000  # to billion
    # process deadweight loss
    CO2_tax_price = pd.merge(CO2_emissions, CO2_prices, "left", ["baseline", "scenario"],
                             suffixes=("_supply", "_price"))
    CO2_tax_price["Units"] = "MTC"
    deadweight_loss = pd.merge(CO2_tax_price, baseline_emissions, "left", "Units", suffixes=("_actual", "_baseline"))
    for i in c.GCAMConstants.plotting_x:
        # ((Mt C - Mt C) * CO2 / C = Mt CO2) * (1990$/tC * 2025$/tC /1990$/tC = 2025$t C * CO2 /C = 2025$/t CO2) = (Mt CO2 * 2025$/t CO2) = M 2025$
        deadweight_loss[str(i)] = (
                                          0.5 * (deadweight_loss[str(i)] - deadweight_loss[
                                      str(i) + "_supply"]) / c.GCAMConstants.CO2_to_C *
                                          (deadweight_loss[
                                               str(i) + "_price"] / c.GCAMConstants.USD2025_tCO2_to_1990_tC)) / 1000  # to billion

    deadweight_loss = deadweight_loss[["scenario", "baseline", "2025", "2030", "2035", "2040", "2045", "2050"]]
    CO2_tax_revenue = CO2_tax_revenue[["scenario", "baseline", "2025", "2030", "2035", "2040", "2045", "2050"]]
    deadweight_loss["Units"] = "Billion 2025$USD/yr"
    CO2_tax_revenue["Units"] = "Billion 2025$USD/yr"
    deadweight_loss["product"] = "Deadweight Loss"
    CO2_tax_revenue["product"] = "C Tax Revenue"
    deadweight_loss["GCAM"] = "USA"
    CO2_tax_revenue["GCAM"] = "USA"

    plotting.plot_line_product_CI(deadweight_loss, "baseline", "Deadweight loss by baseline scenario", region=["USA"],
                                  skip_years=2)
    plotting.plot_line_product_CI(CO2_tax_revenue, "baseline", "C tax revenue by baseline scenario", region=["USA"],
                                  skip_years=2)


def C_prices(config_fname, reference_year):
    """
    calculate how the C prices change by scenario
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant information
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high", "nzn_nzn", "excess_excess", "4gt_4gt"]

    CO2_prices = data_manipulation.get_sensitivity_data(scenarios, "CO2_prices", "masked")
    CO2_prices = CO2_prices[(CO2_prices["GCAM"] == "USA") & (CO2_prices["product"] == "CO2")]
    CO2_prices = CO2_prices.drop('Unnamed: 0', axis=1)
    CO2_prices["Units"] = "C Tax (USD/t CO$_{2}$-eq)"

    for i in c.GCAMConstants.plotting_x:
        CO2_prices[str(i)] = CO2_prices[str(i)] / c.GCAMConstants.USD2025_tCO2_to_1990_tC

    plotting.plot_line_product_CI(CO2_prices, "baseline", "C tax prices by baseline scenario", region=["USA"])


def state_CDR(config_fname, reference_year):
    """
    calculate the status of CDR markets at the state level
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant information
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    supply = data_manipulation.get_sensitivity_data(scenarios, "CDR_by_tech", source="masked")
    price = data_manipulation.get_sensitivity_data(scenarios, "prices_of_all_markets", source="masked")

    price = price[price["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price[price["product"].isin(["DAC", "TEW", "OEW", "BECCS"])]
    price["Units"] = "2025$/t CDR"
    supply = supply[supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price.drop('Unnamed: 0', axis=1)
    supply = supply.drop('Unnamed: 0', axis=1)
    supply["product"] = supply["technology"]

    for i in c.GCAMConstants.plotting_x:
        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=197501&year2=202501
        price[str(i)] = price[str(i)] / c.GCAMConstants.USD2025_tCO2_to_1975_kgC
        supply[str(i)] = supply[str(i)] / c.GCAMConstants.CO2_to_C

    # sort by baseline
    CDR_price_low = price[price["baseline"] == "low"].copy(deep=True)
    CDR_price_high = price[price["baseline"] == "high"].copy(deep=True)
    CDR_supply_low = supply[supply["baseline"] == "low"].copy(deep=True)
    CDR_supply_high = supply[supply["baseline"] == "high"].copy(deep=True)

    # market sizes
    CDR_market_low = pd.merge(CDR_price_low, CDR_supply_low, "right", on=["GCAM", "baseline", "scenario", "product"],
                              suffixes=("_price", "_supply"))
    CDR_market_high = pd.merge(CDR_price_high, CDR_supply_high, "right", on=["GCAM", "baseline", "scenario", "product"],
                               suffixes=("_price", "_supply"))
    # calculate size of markets and remove outliers
    for i in c.GCAMConstants.plotting_x:
        CDR_market_low[str(i)] = CDR_market_low[str(i) + "_price"] * CDR_market_low[str(i) + "_supply"]
        CDR_market_low[str(i) + "_price"] = CDR_market_low.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        CDR_market_low[str(i) + "_supply"] = CDR_market_low.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)
        CDR_market_high[str(i)] = CDR_market_high[str(i) + "_price"] * CDR_market_high[str(i) + "_supply"]
        CDR_market_high[str(i) + "_price"] = CDR_market_high.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_price"), axis=1)
        CDR_market_high[str(i) + "_supply"] = CDR_market_high.apply(
            lambda row: data_manipulation.remove_price_supply_outliers(str(i), row, "_supply"), axis=1)

        # still some rare price outliers
        CDR_market_low[str(i) + "_price"] = CDR_market_low.apply(
            lambda row: row[str(i) + "_price"] if row[str(i) + "_price"] < 1000 else np.nan, axis=1)
        CDR_market_high[str(i) + "_price"] = CDR_market_high.apply(
            lambda row: row[str(i) + "_price"] if row[str(i) + "_price"] < 1000 else np.nan, axis=1)

    # add units
    CDR_market_low["Units"] = "Million USD/yr"
    CDR_market_high["Units"] = "Million USD/yr"

    # split back into price and supply markets
    CDR_price_low = CDR_market_low.copy(deep=True)
    CDR_supply_low = CDR_market_low.copy(deep=True)
    CDR_price_high = CDR_market_high.copy(deep=True)
    CDR_supply_high = CDR_market_high.copy(deep=True)

    for i in c.GCAMConstants.plotting_x:
        CDR_price_low[str(i)] = CDR_price_low[str(i) + "_price"]
        CDR_supply_low[str(i)] = CDR_supply_low[str(i) + "_supply"]
        CDR_price_high[str(i)] = CDR_price_high[str(i) + "_price"]
        CDR_supply_high[str(i)] = CDR_supply_high[str(i) + "_supply"]

    # update units
    CDR_price_low["Units"] = "$/t CDR"
    CDR_supply_low["Units"] = "log$_{10}$(Mt CDR)"
    CDR_price_high["Units"] = "$/t CDR"
    CDR_supply_high["Units"] = "log$_{10}$(Mt CDR)"
    CDR_market_low["Units"] = "Million USD/yr"
    CDR_market_high["Units"] = "Million USD/yr"

    # only include necessary information
    plotting_cols = ["2025", "2030", "2035", "2040", "2045", "2050", "GCAM", "product", "baseline", "scenario", "Units"]
    CDR_price_low = CDR_price_low[plotting_cols]
    CDR_price_high = CDR_price_high[plotting_cols]
    CDR_supply_low = CDR_supply_low[plotting_cols]
    CDR_supply_high = CDR_supply_high[plotting_cols]
    CDR_market_low = CDR_market_low[plotting_cols]
    CDR_market_high = CDR_market_high[plotting_cols]

    # take log of supply and market size
    for i in c.GCAMConstants.plotting_x:
        CDR_supply_low[str(i)] = np.log10(CDR_supply_low[str(i)])
        CDR_supply_high[str(i)] = np.log10(CDR_supply_high[str(i)])

    # plotting graphs
    plotting.plot_line_product_CI(CDR_price_low, "product", "CDR prices in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_price_high, "product", "CDR prices in high baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_supply_low, "product", "CDR supply in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_supply_high, "product", "CDR supply in high baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_market_low, "product", "CDR markets in low baseline", skip_years=0)
    plotting.plot_line_product_CI(CDR_market_high, "product", "CDR markets in high baseline", skip_years=0)


def cement(config_fname, reference_year):
    """
    calcualte statistics for cement production
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant information
    """
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    supply = data_manipulation.get_sensitivity_data(scenarios, "cement_production_by_tech_conv_and_ccs",
                                                    source="masked")
    price = data_manipulation.get_sensitivity_data(scenarios, "cement_prices", source="masked")
    for i in c.GCAMConstants.plotting_x:
        price[str(i)] = price.apply(lambda row: row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 if row[
                                                                                                        str(i)] * c.GCAMConstants.USD1975_to_USD2025 < 1000 else np.nan,
                                    axis=1)

    price = price[price["GCAM"].isin(c.GCAMConstants.USA_region)]
    price["Units"] = "2025$/kg"
    supply = supply[supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    price = price.drop('Unnamed: 0', axis=1)
    supply = supply.drop('Unnamed: 0', axis=1)

    # sort by baseline
    cement_price_low = price[price["baseline"] == "low"].copy(deep=True)
    cement_price_high = price[price["baseline"] == "high"].copy(deep=True)
    cement_supply_low = supply[supply["baseline"] == "low"].copy(deep=True)
    cement_supply_high = supply[supply["baseline"] == "high"].copy(deep=True)

    plotting.plot_line_product_CI(cement_price_low, "sector", "cement prices in low baseline")
    plotting.plot_line_product_CI(cement_price_high, "sector", "cement prices in high baseline")
    plotting.plot_line_product_CI(cement_supply_low, "technology", "cement supply in low baseline")
    plotting.plot_line_product_CI(cement_supply_high, "technology", "cement supply in high baseline")


def electricity(config_fname, reference_year):
    """
    return information on state-level electricity markets
    :param config_fname: not needed
    :param reference_year: not needed
    :return: plot of relevant information
    """
    # get scenario data
    scenarios = ["low_low", "high_high", "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                 "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                 "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                 "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                 "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                 "innovation-rhodium18b_low", "innovation-triple_low",
                 "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                 "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                 "CDRIA-rhodium18b_high"]
    elec_supply = data_manipulation.get_sensitivity_data(scenarios, "elec_gen_by_subsector", source="masked")
    elec_price = data_manipulation.get_sensitivity_data(scenarios, "elec_prices_by_sector", source="masked")
    # convert to modern moneys and eliminate outliers
    for i in c.GCAMConstants.plotting_x:
        elec_price[str(i)] = elec_price.apply(
            lambda row: row[str(i)] * c.GCAMConstants.USD1975_to_USD2025 / 0.277778 if row[
                                                                                           str(i)] * c.GCAMConstants.USD1975_to_USD2025 / 0.277778 < 1000 else np.nan,
            axis=1)

    # focus on US regions
    elec_price["Units"] = "2025$/MWh"
    elec_price = elec_price[elec_price["GCAM"].isin(c.GCAMConstants.USA_region)]
    elec_supply = elec_supply[elec_supply["GCAM"].isin(c.GCAMConstants.USA_region)]
    elec_price = elec_price.drop('Unnamed: 0', axis=1)
    elec_supply = elec_supply.drop('Unnamed: 0', axis=1)

    # rename and group elec techs
    elec_supply["subsector"] = elec_supply.apply(lambda row: data_manipulation.elec_supply_sectors(row), axis=1)
    elec_supply = data_manipulation.group(elec_supply, ["subsector", "scenario", "baseline", "Units"])
    elec_supply["GCAM"] = elec_supply["baseline"]

    # sort by baseline
    elec_price_low = elec_price[elec_price["baseline"] == "low"].copy(deep=True)
    elec_price_high = elec_price[elec_price["baseline"] == "high"].copy(deep=True)

    plotting.plot_line_product_CI(elec_price_low, "fuel", "electricity prices in low baseline")
    plotting.plot_line_product_CI(elec_price_high, "fuel", "electricity prices in high baseline")
    plotting.plot_line_product_CI(elec_supply, "subsector", "national electricity supply",
                                  region=elec_supply["baseline"].unique())


def CDR_subsidies(config_fname, year1, year2):
    """
    calculate the changes in CDR subsidies year over year
    :param config_fname: scenario information
    :param year1: first year
    :param year2: second year
    :return: plot of differences in subsidy
    """
    # data processing
    CDR = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech", "masked")
    CDR = CDR[CDR[['GCAM']].isin(c.GCAMConstants.USA_region).any(axis=1)]
    CDR = CDR[CDR['technology'] != "unsatisfied CDR demand"]

    CDR["plot"] = CDR[year2] - CDR[year1]

    if config_fname.split("/")[1] == "nothing":
        # no BECCS in the nothing baseline
        CDR = CDR[CDR["technology"] != "BECCS"]

    # choropleth map
    plotting.plot_regional_hist_avg(CDR, 'plot',
                                    "change in size of CDR markets from 2035 to 2040",
                                    "technology", config_fname)
    plotting.plot_world_by_products(CDR, "technology", ["plot"],
                                    "Change in CDR (Mt) from " + year1 + " to year " + year2, config_fname)


def compare_policy_costs(scenario1, scenario2):
    """
    compares the total annual policy costs between two scenarios
    :param scenario1: old scenario
    :param scenario2: new scenario
    :return: graph new-old scenario
    """
    scenario1 = scenario1.replace("_", "/")
    scenario2 = scenario2.replace("_", "/")
    scenario = scenario1.split("_")[0]
    dataframe = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario2 +
                            "/policy cost by technology.csv")
    cost_diff = pd.read_csv("data/data_analysis/supplementary_tables/" + scenario1 +
                            "/policy cost by technology.csv")
    cost_diff = pd.merge(cost_diff, dataframe, "outer", on=["product", "baseline"], suffixes=("_old", "_new"))
    cost_diff = cost_diff[cost_diff["product"] != "C Tax Revenue"]
    cost_diff["Units"] = "Million 2025$USD/yr"
    for i in c.GCAMConstants.plotting_x:
        # if a year has been masked from the data, don't fill na
        no_subsidy = cost_diff[cost_diff["scenario_new"] == scenario]
        if no_subsidy[str(i) + "_new"].isnull().all() or no_subsidy[str(i) + "_old"].isnull().all():
            cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
        else:
            cost_diff[str(i)] = cost_diff[str(i) + "_new"].fillna(0) - cost_diff[str(i) + "_old"].fillna(0)
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                      "change in policy cost by year " + scenario2.replace("/",
                                                                                           "_") + " - " + scenario1.replace(
                                          "/", "_"),
                                      scenario2)

    # no C tax
    cost_diff = cost_diff[cost_diff["product_price_old"] != "CO2"]
    plotting.plot_stacked_bar_product(cost_diff, c.GCAMConstants.plotting_x, "product",
                                      "change in policy cost by year (no C tax) " + scenario2.replace("/",
                                                                                                      "_") + " - " + scenario1.replace(
                                          "/", "_"),
                                      scenario2)


if __name__ == '__main__':
    main("2050")
