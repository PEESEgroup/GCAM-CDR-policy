import pandas as pd
import build_xml_config


def open_csv(fname, index):
    """
    extract the region, years, and values
    :param fname:
    :return:
    """
    info = {}
    for i in fname:
        df = pd.read_csv(fname, skiprows=1)  # skip the top row: source
        df = df.set_index(index)
        values = df.to_dict(orient="index")
        info[str(i)] = values
    return info


def build_from_scenario(scenario_name):
    if scenario_name == "exoTest":
        return \
            [build_xml_config.XMLConfig(
                data_files=["GCAM_EXO_CDR_demand.xml"],
                xml_build_type="Exogenous"
            ),
                build_xml_config.XMLConfig(
                    data_files=["USA_EXO_CDR_demand.xml"],
                    xml_build_type="Exogenous"
                )]
