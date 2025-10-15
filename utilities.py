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
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
    elif "nzn" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
    elif "excess" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_veryhigh.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
    elif "4gt" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_4Gt.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
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
    elif "s2" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_s2.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={"CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify_s2.csv",
                            "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_high.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh_s2.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "verify-2025" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh_2025-verify.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_verify-2025.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_2025tax.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_CtaxUSA2025.xml"
            ),
        ]
    elif "s1n" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing_s1.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1n.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-itc-n" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1n.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procure-n" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing_s1.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1n.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_s1.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1l.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procure-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_s1.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1l.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-itc-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1l.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-noBECCSitc-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1l.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1noBECCS.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced_noBECCS_l.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_s1.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procureScaling-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_scaling.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_scalingdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procure3B-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_3B.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_3Bdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procureRhodium-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_rhodium.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_rhodium.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procureScaling-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_scaling.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_scalingdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procure3B-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_3B.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_3Bdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-procureRhodium-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_rhodium.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_rhodium.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "s1-itc-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high.csv",
                            "elastic_CDR_demand_verify": "./building_xml/inputs/Elastic_CDR_demand_verify_19.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h.xml"
            ),
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_enhanced-45Q_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_enhanced.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"TEW_transport_link": "./building_xml/inputs/TEW_sector_info.csv",
                            "TEW_transport_amount": "./building_xml/inputs/TEW_sector_links.csv",
                            "TEW_transport_saving": "./building_xml/inputs/TEW_transport_savings_20.csv"},
                xml_build_type="TEW Transport Cost Reduction",
                output_fname="TEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"OEW_transport_amount": "./building_xml/inputs/OEW_transport_coef_20.csv"},
                xml_build_type="OEW Transport Cost Reduction",
                output_fname="OEW_CR_USA.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    else:
        return []
