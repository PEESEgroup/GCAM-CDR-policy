import pandas as pd


def open_csv(fname, index):
    """
    extract the region, years, and values
    :param fname:
    :return:
    """
    df = pd.read_csv(fname, skiprows=1)  # skip the top row: source
    df = df.set_index(index)
    values = df.to_dict(orient="index")
    return values

