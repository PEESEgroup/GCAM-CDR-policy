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
    ### WHEN RUNNING MULTIPLE SCENARIOS, ENSURE THAT ALL FILES HAVE DIFFERENT OUTPUT_FNAMES ###
    if "nothing" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_nothing.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_DACS_45Q_verify.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_DACS_nothing.xml"
            ),
            build_xml_config.XMLConfig(
            data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                        "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                        "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
            xml_build_type="BECCS RES",
            output_fname="default_BECCSIntegration_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                            "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_nothing.xml"
            )
        ]
    elif "low" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_low.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_34.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_low.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_DACS_45Q_verify.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_DACS_low.xml"
            ),
            build_xml_config.XMLConfig(
            data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                        "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                        "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
            xml_build_type="BECCS RES",
            output_fname="default_BECCSIntegration_low.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                            "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_low.xml"
            )
        ]
    elif "high" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_34.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_high.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_DACS_45Q_verify.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_DACS_high.xml"
            ),
            build_xml_config.XMLConfig(
            data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                        "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                        "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
            xml_build_type="BECCS RES",
            output_fname="default_BECCSIntegration_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                            "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_high.xml"
            )
        ]
    elif "testsubsidy" in scenario_name:
        return [build_xml_config.XMLConfig(
            # <tech>_subsidy_link
            data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                        "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_DACS_verify.csv"},
            xml_build_type="subsidy Policy",
            output_fname="test_subsidy_DACS.xml"
        ),
            build_xml_config.XMLConfig(
                data_files={"TEW_subsidy_link": "./building_xml/inputs/TEW_links.csv",
                            "TEW_subsidy_amount_verify": "./building_xml/inputs/subsidy_TEW_verify.csv"},
                xml_build_type="subsidy Policy",
                output_fname="test_subsidy_TEW.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            )
        ]
    else:
        return []
