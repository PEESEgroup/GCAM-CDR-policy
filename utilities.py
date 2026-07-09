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
        if isinstance(fname[i], list):
            out_list = []
            for j in fname[i]:
                with open(j, mode='r', newline='') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    index_num = int(next(csv_reader)[1])
                df = pd.read_csv(j, skiprows=2)  # skip the top row because it is the source information

                # reset the index for eventual dict conversion - default is first column
                if "index" in kwargs:
                    df = df.set_index(kwargs["index"])
                else:
                    index = [df.columns[k] for k in range(index_num)]
                    df = df.set_index(index)
                values = df.to_dict(orient="index")
                out_list.append(values)

            # add data to the dictionary
            info[str(i)] = out_list
        else:
            with open(fname[i], mode='r', newline='') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                index_num = int(next(csv_reader)[1])
            df = pd.read_csv(fname[i], skiprows=2)  # skip the top row because it is the source information

            # reset the index for eventual dict conversion - default is first column
            if "index" in kwargs:
                df = df.set_index(kwargs["index"])
            else:
                index = [df.columns[k] for k in range(index_num)]
                df = df.set_index(index)
            values = df.to_dict(orient="index")

            # add data to the dictionary
            info[str(i)] = values
    return info


def build_from_scenario(scenario_name):
    """
    a lookup function to find the list of files that need to be built given a scenario name
    :param scenario_name: the scenario name (or baseline pathway) from which assumption files are converted into xml files
    :return: list of build_xml_config objects.
    """
    ### WHEN RUNNING MULTIPLE SCENARIOS, ENSURE THAT ALL FILES HAVE DIFFERENT OUTPUT_FNAMES ###
    if "4100Mt-noCostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_4Gt.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_4gt.xml"
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
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "2400Mt-noCostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_veryhigh.csv"},
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
    elif "1500Mt-noCostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high.csv"},
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
    elif "500Mt-noCostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_low.xml"
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
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low.csv"},
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
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            )
        ]
    elif "100Mt-noCostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing.csv"},
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
    elif "4100Mt-CostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_4Gt.csv"},
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
            ),
            build_xml_config.XMLConfig(
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_4100Mt.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_4100_CD.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_4100Mt.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_4100_CD.xml"
            )
        ]
    elif "2400Mt-CostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_veryhigh.csv"},
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
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_2400Mt.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_2400_CD.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_2400Mt.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_2400_CD.xml"
            )
        ]
    elif "1500Mt-CostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_high.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high.csv"},
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
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_1500_CD.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv"],
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_1500_CD.xml"
            )
        ]
    elif "500Mt-CostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_low.xml"
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
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low.csv"},
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
                data_files={"USA_Cstorage_amount": "./building_xml/inputs/C_storage_sector_info_20.csv"},
                xml_build_type="C Storage Cost Reduction",
                output_fname="USA_C_Storage.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_500_CD.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_500_CD.xml"
            )
        ]
    elif "100Mt-CostDecrease" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "ghg_constraint_verify": "./building_xml/inputs/GHG_constraint_verify_lowhigh.csv"},
                xml_build_type="GHG constraint",
                output_fname="default_GHGPolicies_nothing.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_nothing.csv"},
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
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_100Mt.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_100_CD.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_100Mt.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_100_CD.xml"
            )
        ]
    elif "innovation-rhodium6b-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_rhodium6b.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium6b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium6b_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium6b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium6b_l.xml"
            )
        ]
    elif "innovation-rhodium6b-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_rhodium6b.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium6b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium6b_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium6b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium6b_h.xml"
            )
        ]
    elif "innovation-maintain-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_maintain.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_maintain.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_maintain_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_maintain.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_maintain_l.xml"
            )
        ]
    elif "innovation-maintain-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_maintain.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_maintain.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_maintain_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_maintain.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_maintain_h.xml"
            )
        ]
    elif "innovation-triple-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_triple.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_triple.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_triple_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_triple.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_triple_l.xml"
            )
        ]
    elif "innovation-triple-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_triple.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_triple.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_triple_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_triple.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_triple_h.xml"
            )
        ]
    elif "innovation-DACHubs-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_DACHubs.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_DAC-HUBS.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_DACHubs_l.xml"
            )
        ]
    elif "innovation-DACHubs-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_DACHubs.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_DAC-HUBS.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_DACHubs_h.xml"
            )
        ]
    elif "innovation-rhodium18b-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_rhodium18b.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium18b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium18b_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium18b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium18b_l.xml"
            )
        ]
    elif "innovation-rhodium18b-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"exogenous_investment": "./building_xml/inputs/exogenous_subsector_investment_rhodium18b.csv"},
                xml_build_type="exogenous investment",
                output_fname=""
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium18b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium18b_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_rhodium18b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium18b_h.xml"
            )
        ]
    elif "45Q-2040-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2040_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2040.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2040-l.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_45Q_2040_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2040-l.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_45Q_2040_l.xml"
            )
        ]
    elif "45Q-2040-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2040_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2040.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2040-h.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_45Q_2040_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2040-h.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_45Q_2040_l.xml"
            )
        ]
    elif "45Q-2040-noCR" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2040_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2040.xml"
            )
        ]
    elif "45Q-2050-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2050.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2050-l.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_45Q_2050_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2050-l.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_45Q_2050_l.xml"
            )
        ]
    elif "45Q-2050-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2050.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2050-h.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_45Q_2050_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_45Q-2050-h.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_45Q_2050_h.xml"
            )
        ]
    elif "45Q-2050-noCR" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_45Q-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="45Q_2050.xml"
            )
        ]
    elif "CDRIA-2035-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2035.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2035-l.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_CDRIA_2035_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2035-l.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_CDRIA_2035_l.xml"
            )
        ]
    elif "CDRIA-2035-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2035.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2035-h.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_CDRIA_2035_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2035-h.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_CDRIA_2035_h.xml"
            )
        ]
    elif "CDRIA-2035-noCR" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2035.xml"
            )
        ]
    elif "CDRIA-2050-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2050.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2050-l.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_CDRIA_2050_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2050-l.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_CDRIA_2050_l.xml"
            )
        ]
    elif "CDRIA-2050-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2050.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2050-h.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_CDRIA_2050_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_CDRIA-2050-h.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_CDRIA_2050_h.xml"
            )
        ]
    elif "CDRIA-2050-noCR" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                # <tech>_subsidy_link
                data_files={"DAC_subsidy_link": "./building_xml/inputs/DAC_links.csv",
                            "DAC_subsidy_amount_verify": "./building_xml/inputs/subsidy_CDRIA-2050_verify_s1.csv"},
                xml_build_type="subsidy Policy",
                output_fname="CDRIA_2050.xml"
            )
        ]
    elif "procure-scaling-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_scaling.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_scalingdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurescaling.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_scaling_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurescaling.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_scaling_h.xml"
            )
        ]
    elif "procure-3B-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_3B.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_3Bdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procure3b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_3B_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procure3b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_3B_h.xml"
            )
        ]
    elif "procure-Rhodium-h" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_high_rhodium.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_rhodium.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurerhodium.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium_h.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_1500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurerhodium.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium_h.xml"
            )
        ]
    elif "procure-scaling-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_scaling.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_scalingdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurescaling.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_scaling_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurescaling.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_scaling_l.xml"
            )
        ]
    elif "procure-3B-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_3B.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_3Bdemand.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procure3b.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_3B_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procure3b.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_3B_l.xml"
            )
        ]
    elif "procure-Rhodium-l" in scenario_name:
        return [
            build_xml_config.XMLConfig(
                data_files={"ghg_CDR_market_link": "./building_xml/inputs/linked_ghg_CDR_base_verify.csv",
                            "exo_CDR_demand_verify": "./building_xml/inputs/EXO_CDR_demand_verify_low_rhodium.csv"},
                xml_build_type="CDR Policy",
                output_fname="default_CDRDemand_s1h_rhodium.xml"
            ),
            build_xml_config.XMLConfig(
                data_files={
                    "CDR_non-input_tech_costs_verify": "./building_xml/inputs/tech-non-input-cost_verify.csv",
                    "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurerhodium.csv"],
                    "CDR_non-input_tech_link": "./building_xml/inputs/tech-non-input-cost_links.csv"},
                xml_build_type="tech_non-input_costs",
                output_fname="CDR_Costs_Calculated_rhodium_l.xml"
            ),  # update BECCS costs as well
            build_xml_config.XMLConfig(
                data_files={"RES_markets": "./building_xml/inputs/BECCS_RES_base_verify.csv",
                            "Cost Decrease": ["./building_xml/inputs/cost_decrease_500Mt.csv",
                                      "./building_xml/inputs/cost_decrease_procurerhodium.csv"],
                            "RES_tech_verify": "./building_xml/inputs/BECCS_tech_base_nlh.csv",
                            "countersubsidy": "./building_xml/inputs/BECCS_countersubsidy_base.csv"},
                xml_build_type="BECCS RES",
                output_fname="default_BECCSIntegration_rhodium_l.xml"
            )
        ]
    else:
        return []
