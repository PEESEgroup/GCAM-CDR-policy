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
        return \
            [build_xml_config.XMLConfig(
                data_files={"exo_linked_ghg": "./building_xml/inputs/exo_linked_ghg_usa_base.csv",
                            "exo_demand": "./building_xml/inputs/USA_EXO_CDR_demand.csv"},
                xml_build_type="Exogenous Policy",
                output_fname="default_USA_CDR_demand.xml",
                region="USA"
            ),
                build_xml_config.XMLConfig(
                    data_files={"exo_linked_ghg": "./building_xml/inputs/exo_linked_ghg_gcam_base.csv",
                                "exo_demand": "./building_xml/inputs/GCAM_EXO_CDR_demand.csv"},
                    xml_build_type="Exogenous Policy",
                    output_fname="default_GCAM_CDR_demand.xml",
                    region="GCAM"
                )]
