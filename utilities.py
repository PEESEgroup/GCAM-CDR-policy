import pandas as pd
import build_xml_config
import csv


def open_csv(fname, **kwargs):
    """
    extract the region, years, and values
    :param fname:
    :return:
    """
    info = {}
    for i in fname:
        with open(fname[i], mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            index_num = int(next(csv_reader)[1])
        df = pd.read_csv(fname[i], skiprows=2)  # skip the top row because it is the source information

        # reset the index for eventual dict conversion - default is first column
        if "index" in kwargs:
            df = df.set_index(kwargs["index"])
        else:
            index = [df.columns[i] for i in range(index_num)]
            df = df.set_index(index)
        values = df.to_dict(orient="index")

        # add data to the dictionary
        info[str(i)] = values
    return info


def build_from_scenario(scenario_name):
    if "default" in scenario_name:
        return [build_xml_config.XMLConfig(
            data_files={"RES_markets_verify": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                        "tech": "./building_xml/inputs/BECCS_tech_base.csv",
                        "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
            xml_build_type="BECCS RES",
            output_fname="default_BECCSIntegration.xml"
            ),
            # important to build links before CDR demand
            build_xml_config.XMLConfig(
                data_files={"linked_ghg_markets": "./building_xml/inputs/linked_ghg_base.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify.csv"},
                            # "ghg_tax_verify": "./building_xml/inputs/GHG_tax_verify.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"linked_ghg_markets": "./building_xml/inputs/linked_ghg_base.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand.xml"
            )
        ]
    else:
        return None
