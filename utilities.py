import pandas as pd
import build_xml_config


def open_csv(fname, **kwargs):
    """
    extract the region, years, and values
    :param fname:
    :return:
    """
    info = {}
    for i in fname:
        df = pd.read_csv(fname[i], skiprows=1)  # skip the top row because it is the source information

        # reset the index for eventual dict conversion - default is first column
        if "index" in kwargs:
            df = df.set_index(kwargs["index"])
        else:
            df = df.set_index(df.columns[0])
        values = df.to_dict(orient="index")

        # add data to the dictionary
        info[str(i)] = values
    return info


def build_from_scenario(scenario_name):
    if scenario_name == "exoTest":
        return [build_xml_config.XMLConfig(
            data_files={"linked_ghg_markets": "./building_xml/inputs/linked_ghg_base.csv",
                        "exo_demand": "./building_xml/inputs/EXO_CDR_demand.csv",
                        "elastic_demand": "./building_xml/inputs/Elastic_CDR_demand.csv"},
            xml_build_type="CDR Policy",
            output_fname="exoTest_CDR_demand.xml"
        )]
