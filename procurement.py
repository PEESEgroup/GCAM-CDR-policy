import pandas as pd
import constants


def main(scenario):
    """
    method to calculate amount of procurement based on CDR price
    :param scenario: name of scenario
    :return: output .csv file in the supplementary tables
    """
    baseline_df = pd.read_csv("data/data_analysis/supplementary_tables/"+scenario+"/"+scenario+"/sorted price and supply of CDR by technology.csv")

    # calculate total cost
    for j in constants.GCAMConstants.plotting_x:
        baseline_df[str(j)+"total_cost"] = baseline_df[str(j)+"_price"] * baseline_df[str(j)+"_supply"]

    # group and get total supply
    baseline_df = baseline_df.groupby(["Units_price", "Units_supply"]).sum(min_count=1)

    # calculate average price by year
    for j in constants.GCAMConstants.plotting_x:
        baseline_df[str(j)+"_avgCost"] = baseline_df[str(j)+"total_cost"] / baseline_df[str(j)+"_supply"]

    # output calculations
    baseline_df.to_csv("data/data_analysis/supplementary_tables/"+scenario+"/"+scenario+"/procurement_price.csv")


if __name__ == '__main__':
    for i in ["nothing", "low", "high"]:
        main(i)
