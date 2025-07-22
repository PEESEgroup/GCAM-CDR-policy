import xml.etree.cElementTree as ET
import multiprocessing
import subprocess
import os

import constants


def main(batch_scenario_fname, batch=True):
    """
    control program for running a GCAM scenario
    """
    # change directory if not already in the \gcam\exe folder
    if str(os.getcwd()).split("\\")[-1] != "exe":
        os.chdir("./gcam/exe")

    config_dir = "scenario-config/"

    # change the name of the config file in the .bat file
    bat_fname = 'run-gcam-cdr_' + batch_scenario_fname.split(".")[0] + ".bat"
    original_bat_fname = 'run-gcam-cdr.bat'

    lines = open(original_bat_fname, 'r').readlines()

    if not batch:
        # copy the config file to the config dir
        config_fname = config_dir + "config_" + batch_scenario_fname

        # {write out file data
        with open(config_fname, "w+") as f:
            f.write("")
        tree = ET.parse(batch_scenario_fname)
        tree.write(config_fname)

        # use configuration file as-is
        new_last_line = ("gcam-cdr.exe -C " + config_fname)
        lines[25] = new_last_line

        print(lines[25])

        # now {write the modified list back out to the file
        open(bat_fname, 'w').writelines(lines)

    else:
        # open the configuration .xml" file
        config_fname = "configuration_CDR.xml"
        tag = 'Value'
        tree = ET.parse(config_fname)
        root = tree.getroot()

        # change the text for the batch file name
        for element in root.findall(f".//{tag}"):
            if element.attrib['name'] == "BatchFileName":
                element.text = "batch_scenario_fname"

        # change mode to batch mode
        for element in root.findall(f".//{tag}"):
            if element.attrib['name'] == "BatchMode":
                element.text = "1"

        # {write out the updated configuration file to a new file name
        config_fname = config_dir + "config_" + batch_scenario_fname

        # {write out file data
        with open(config_fname, "w+") as f:
            f.write("")
        tree.write(config_fname)

        # run GCAM-CDR from the os
        # now edit the appropriate line of the list of lines
        new_last_line = ("gcam-cdr.exe -C " + config_fname)
        lines[25] = new_last_line

        print(lines[25])

        # now {write the modified list back out to the file
        open(bat_fname, 'w').writelines(lines)

    # change the name of the .bat file
    subprocess.call([r'{}'.format(bat_fname)], creationflags = subprocess.CREATE_NEW_CONSOLE)


def build_config_file(scenario_name, baseline):
    # look up relevant files by scenario name
    scenario = constants.GCAMConstants.scenario_names[scenario_name]
    originals = scenario["original"]
    altered = scenario["altered"]

    # TODO: build scenario files

    # add default files
    config = default_config(baseline)





    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.{write(xmlstr)

    # TODO: replace altered files

    # add original files


def default_config(baseline):
    """
    baseline: scenario name for baseline exogenous CDR demand
    :param baseline:
    :return:
    """
    configuration = ET.Element("Configuration")

    # add files
    files = ET.SubElement(configuration, "Files")
    ET.SubElement(files, "Value", name="xmlInputFileName").text = "../input/gcamdata/xml/modeltime.xml"
    ET.SubElement(files, "Value",  name="BatchFileName").text = "batch_ag.xml"
    ET.SubElement(files, "Value",  name="policy-target-file").text = "../input/policy/forcing_target_4p5.xml"
    ET.SubElement(files, "Value",  name="GHGInputFileName").text = "../input/magicc/inputs/input_gases.emk"
    # 		<!--Value {"write-output":"1" "append-scenario-name":"0" "name":"xmldb-location"}).text = "D://database_usa</Value-->
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"xmldb-location"}).text = "../output/database_basexdb"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"xmldb-location"}).text = "../output/database_basexdb"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"restart"}).text = "./restart/restart"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"xmlDebugFileName"}).text = "debug.xml"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"climatFileName"}).text = "gas.emk"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"1", "name":"costCurvesOutputFileName"}).text = "cost_curves.xml"
    ET.SubElement(files, "Value",  attrib={"write-output":"1", "append-scenario-name":"0", "name":"batchCSVOutputFile"}).text = "batch-csv-out.csv"
    ET.SubElement(files, "Value",  attrib={"write-output":"0", "append-scenario-name":"0", "name":"supplyDemandOutputFileName"}).text = "SDCurves.csv"
    ET.SubElement(files, "Value",  attrib={"write-output":"0", "append-scenario-name":"0", "name":"flow-graph"}).text = "gcam-flow-graph.dot"
    ET.SubElement(files, "Value",  attrib={"write-output":"0", "append-scenario-name":"0", "name":"dependencyGraphName"}).text = "DependencyGraph.dot"
    ET.SubElement(files, "Value",  attrib={"write-output":"0", "append-scenario-name":"0", "name":"landAllocatorGraphName"}).text = "LandAllocatorGraph.dot"

    # add scenario components
    scenario = ET.SubElement(configuration, "ScenarioComponents")
    ET.SubElement(scenario, "Value", name = "climate").text = "../input/gcamdata/xml/no_climate_model.xml"
    ET.SubElement(scenario, "Value", name = "socioeconomics").text = "../input/gcamdata/xml/socioeconomics_gSSP2.xml"

    ET.SubElement(scenario, "Value", name = "resources").text = "../input/gcamdata/xml/resources.xml"
    ET.SubElement(scenario, "Value", name = "energy_supply").text = "../input/gcamdata/xml/en_supply.xml"
    ET.SubElement(scenario, "Value", name = "energy_transformation").text = "../input/gcamdata/xml/en_transformation.xml"
    # <!--Value name = "electricity").text = "../input/gcamdata/xml/electricity.xml"</Value-->
    ET.SubElement(scenario, "Value", name = "elec_water_base").text = "../input/gcamdata/xml/electricity_water.xml"
    ET.SubElement(scenario, "Value", name = "heat").text = "../input/gcamdata/xml/heat.xml"
    ET.SubElement(scenario, "Value", name = "hydrogen").text = "../input/gcamdata/xml/hydrogen.xml"
    ET.SubElement(scenario, "Value", name = "energy_distribution").text = "../input/gcamdata/xml/en_distribution.xml"
    ET.SubElement(scenario, "Value", name = "industry").text = "../input/gcamdata/xml/industry.xml"
    ET.SubElement(scenario, "Value", name = "industry_income_elas").text = "../input/gcamdata/xml/industry_incelas_gssp2.xml"
    ET.SubElement(scenario, "Value", name = "cement").text = "../input/gcamdata/xml/cement.xml"
    ET.SubElement(scenario, "Value", name = "cement_income_elas").text = "../input/gcamdata/xml/cement_incelas_gssp2.xml"
    ET.SubElement(scenario, "Value", name = "fertilizer_energy").text = "../input/gcamdata/xml/en_Fert.xml"
    ET.SubElement(scenario, "Value", name = "hddcdd").text = "../input/gcamdata/xml/HDDCDD_constdd_no_GCM.xml"
    ET.SubElement(scenario, "Value", name = "building").text = "../input/gcamdata/xml/building_det.xml"
    ET.SubElement(scenario, "Value", name = "transportation").text = "../input/gcamdata/xml/transportation_UCD_CORE.xml"
    ET.SubElement(scenario, "Value", name = "carbon_content").text = "../input/gcamdata/xml/Ccoef.xml"
    ET.SubElement(scenario, "Value", name = "carbon_storage").text = "../input/gcamdata/xml/Cstorage.xml"


    ET.SubElement(scenario, "Value", name = "ag_base").text = "../input/gcamdata/xml/ag_For_Past_bio_base_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "ag_cost").text = "../input/gcamdata/xml/ag_cost_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "ag_prodchange").text = "../input/gcamdata/xml/ag_prodchange_ref_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "residue_bio").text = "../input/gcamdata/xml/resbio_input_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "animal").text = "../input/gcamdata/xml/an_input.xml"
    ET.SubElement(scenario, "Value", name = "fertilizer").text = "../input/gcamdata/xml/ag_Fert_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "land1").text = "../input/gcamdata/xml/land_input_1.xml"
    ET.SubElement(scenario, "Value", name = "land2").text = "../input/gcamdata/xml/land_input_2.xml"
    ET.SubElement(scenario, "Value", name = "land3").text = "../input/gcamdata/xml/land_input_3_IRR.xml"
    ET.SubElement(scenario, "Value", name = "land4").text = "../input/gcamdata/xml/land_input_4_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "land5").text = "../input/gcamdata/xml/land_input_5_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "protected_land2").text = "../input/gcamdata/xml/protected_land_input_2.xml"
    ET.SubElement(scenario, "Value", name = "protected_land3").text = "../input/gcamdata/xml/protected_land_input_3.xml"
    ET.SubElement(scenario, "Value", name = "demand").text = "../input/gcamdata/xml/ag_an_demand_input.xml"
    ET.SubElement(scenario, "Value", name = "bio_trade").text = "../input/gcamdata/xml/bio_trade.xml"
    ET.SubElement(scenario, "Value", name = "ag_trade").text = "../input/gcamdata/xml/ag_trade.xml"

    ET.SubElement(scenario, "Value", name = "unlim_supply_water").text = "../input/gcamdata/xml/unlimited_water_supply.xml"
    ET.SubElement(scenario, "Value", name = "water_supply").text = "../input/gcamdata/xml/water_supply_constrained.xml"
    ET.SubElement(scenario, "Value", name = "water_desal").text = "../input/gcamdata/xml/desalination.xml"
    ET.SubElement(scenario, "Value", name = "water_td").text = "../input/gcamdata/xml/water_td.xml"
    ET.SubElement(scenario, "Value", name = "efw_coefs").text = "../input/gcamdata/xml/EFW_input_coefs.xml"
    ET.SubElement(scenario, "Value", name = "efw_irr").text = "../input/gcamdata/xml/EFW_irrigation.xml"
    ET.SubElement(scenario, "Value", name = "efw_mfg").text = "../input/gcamdata/xml/EFW_manufacturing.xml"
    ET.SubElement(scenario, "Value", name = "efw_muni").text = "../input/gcamdata/xml/EFW_municipal.xml"
    ET.SubElement(scenario, "Value", name = "ag_water").text = "../input/gcamdata/xml/ag_water_input_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name = "elec_water_coef").text = "../input/gcamdata/xml/electricity_water_coefs.xml"
    ET.SubElement(scenario, "Value", name = "ind_water").text = "../input/gcamdata/xml/water_demand_industry.xml"
    ET.SubElement(scenario, "Value", name = "an_water").text = "../input/gcamdata/xml/water_demand_livestock.xml"
    ET.SubElement(scenario, "Value", name = "municipal_water").text = "../input/gcamdata/xml/water_demand_municipal.xml"
    ET.SubElement(scenario, "Value", name = "primary_ene_water").text = "../input/gcamdata/xml/water_demand_primary.xml"
    
    ET.SubElement(scenario, "Value", name = "bio_feedstock_limit").text = "../input/gcamdata/xml/liquids_limits.xml"
    ET.SubElement(scenario, "Value", name = "bio_elec_w_feed_limit").text = "../input/gcamdata/xml/water_elec_liquids_limits.xml"
    #<!-- ET.SubElement(scenario, "Value", name = "bio_neg_emiss_budget").text = "../input/gcamdata/xml/negative_emissions_budget_gSSP2.xml" -->
    ET.SubElement(scenario, "Value", name = "wind_update").text = "../input/gcamdata/xml/onshore_wind.xml"


    ET.SubElement(scenario, "Value", name = "socio_usa").text = "../input/gcamdata/xml/socioeconomics_USA.xml"
    ET.SubElement(scenario, "Value", name = "resource_usa").text = "../input/gcamdata/xml/resources_USA.xml"
    ET.SubElement(scenario, "Value", name = "Cstorage_usa").text = "../input/gcamdata/xml/Cstorage_USA.xml"
    ET.SubElement(scenario, "Value", name = "prices_usa").text = "../input/gcamdata/xml/en_prices_USA.xml"
    ET.SubElement(scenario, "Value", name = "en_transform_usa").text = "../input/gcamdata/xml/en_transformation_USA.xml"
    #<!--Value name = "elec_usa").text = "../input/gcamdata/xml/elec_segments_USA.xml"</Value-->
    ET.SubElement(scenario, "Value", name = "elec_water_usa").text = "../input/gcamdata/xml/elec_segments_water_USA.xml"
    ET.SubElement(scenario, "Value", name = "h2_usa").text = "../input/gcamdata/xml/hydrogen_USA.xml"
    ET.SubElement(scenario, "Value", name = "elect_td_usa").text = "../input/gcamdata/xml/electd_USA.xml"
    ET.SubElement(scenario, "Value", name = "trn_usa").text = "../input/gcamdata/xml/transportation_USA_CORE.xml"
    ET.SubElement(scenario, "Value", name = "bld_usa").text = "../input/gcamdata/xml/building_USA.xml"
    ET.SubElement(scenario, "Value", name = "dd_usa").text = "../input/gcamdata/xml/HDDCDD_constdds_USA.xml"
    ET.SubElement(scenario, "Value", name = "ind_usa").text = "../input/gcamdata/xml/industry_USA.xml"
    ET.SubElement(scenario, "Value", name = "ind_vintage_usa").text = "../input/gcamdata/xml/industry_vintage_USA.xml"
    ET.SubElement(scenario, "Value", name = "cement_usa").text = "../input/gcamdata/xml/cement_USA.xml"
    ET.SubElement(scenario, "Value", name = "fert_usa").text = "../input/gcamdata/xml/Fert_USA.xml"

    #<!-- NEW NESTING STRUCTURE -->
    ET.SubElement(scenario, "Value", name = "solar_usa").text = "../input/gcamdata/xml/solar_reeds_USA.xml"
    ET.SubElement(scenario, "Value", name = "wind_usa").text = "../input/gcamdata/xml/wind_reeds_USA.xml"
    ET.SubElement(scenario, "Value", name = "hydro_usa").text = "../input/gcamdata/xml/elec_hydro_USA.xml"
    ET.SubElement(scenario, "Value", name = "nuc_usa").text = "../input/gcamdata/xml/nuclear_USA.xml"
    ET.SubElement(scenario, "Value", name = "no_new_coal_usa").text = "../input/gcamdata/xml/nonewcoal_USA.xml"
    ET.SubElement(scenario, "Value", name = "ITC_usa").text = "../input/gcamdata/xml/elecS_costs_USA_itc.xml"
    ET.SubElement(scenario, "Value", name = "PTC_usa").text = "../input/gcamdata/xml/elecS_costs_USA_ptc.xml"

    ET.SubElement(scenario, "Value", name = "liq_lim_usa").text = "../input/gcamdata/xml/liquids_limits_USA.xml"
    ET.SubElement(scenario, "Value", name = "USA_regional_bio").text = "../input/gcamdata/xml/regional_biomass_USA.xml"
    
    #<!--WATER DATA-->
    ET.SubElement(scenario, "Value", name = "water_td_usa").text = "../input/gcamdata/xml/water_td_USA.xml"
    ET.SubElement(scenario, "Value", name = "municipal_water_usa").text = "../input/gcamdata/xml/water_demand_municipal_USA.xml"
    ET.SubElement(scenario, "Value", name = "ind_water_usa").text = "../input/gcamdata/xml/water_demand_industry_USA.xml"
    ET.SubElement(scenario, "Value", name = "solver").text = "../input/solution/cal_broyden_config.xml"
    
    #<!-- accelerate decarbonization -->
    ET.SubElement(scenario, "Value", name="adv_geothermal").text = "../input/gcamdata/xml/geo_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_solar").text = "../input/gcamdata/xml/solar_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_wind").text = "../input/gcamdata/xml/wind_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_nuclear").text = "../input/gcamdata/xml/nuclear_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_EV").text = "../input/gcamdata/xml/transportation_USA_highEV.xml"
    
    # <!-- bioseparation -->
    ET.SubElement(scenario, "Value", name = "biosep_global").text = "../input/gcamdata/xml/bio_sep_final_final_final27.xml"
    ET.SubElement(scenario, "Value", name = "biossep_limits").text = "../input/gcamdata/xml/bio_sep_liquids_limits.xml"
    ET.SubElement(scenario, "Value", name = "biosep_liquids").text = "../input/gcamdata/xml/bio_sep_USA_liquids.xml"
    ET.SubElement(scenario, "Value", name = "biosep_industry").text = "../input/gcamdata/xml/bio_sep_USA_industry.xml"
    ET.SubElement(scenario, "Value", name = "biosep_gas").text = "../input/gcamdata/xml/bio_sep_USA_gas.xml"
    ET.SubElement(scenario, "Value", name = "biosep_gas").text = "../input/gcamdata/xml/bio_sep_USA_elec_segments.xml"

    # <!-- add primary CDR -->
    ET.SubElement(scenario, "Value", name = "cdr_rampup").text = "../input/gcamdata/xml/CDR.xml"
    ET.SubElement(scenario, "Value", name = "growth_limit").text = "../input/gcamdata/xml/CDR_growth_limit.xml"
    ET.SubElement(scenario, "Value", name = "cdr_trade").text = "../input/gcamdata/xml/CDR_traded.xml"
    ET.SubElement(scenario, "Value", name = "cdr_dac").text = "../input/gcamdata/xml/DAC.xml"
    ET.SubElement(scenario, "Value", name = "waste_heat").text = "../input/gcamdata/xml/waste_heat_endogenous.xml"
    ET.SubElement(scenario, "Value", name = "cdr_ew").text = "../input/gcamdata/xml/TEW.xml"
    ET.SubElement(scenario, "Value", name = "cdr_ew_limit").text = "../input/gcamdata/xml/limit_land.xml"
    ET.SubElement(scenario, "Value", name = "cdr_oae").text = "../input/gcamdata/xml/OEW.xml"
    ET.SubElement(scenario, "Value", name = "cdr_oae_shipping").text = "../input/gcamdata/xml/OEW_shipping.xml"
    ET.SubElement(scenario, "Value", name = "cdr_nonenergy").text = "../input/gcamdata/xml/CDR_costs.xml"
    ET.SubElement(scenario, "Value", name = "cdr_resources").text = "../input/gcamdata/xml/resources_CDR.xml"
    
    ET.SubElement(scenario, "Value", name = "beccs_integration_global").text = "../input/gcamdata/xml/BECCS_integration.xml"
    
    # <!-- CDR in USA -->
    ET.SubElement(scenario, "Value", name = "cdr_usa").text = "../input/gcamdata/xml/CDR_USA.xml"
    ET.SubElement(scenario, "Value", name = "growth_limit").text = "../input/gcamdata/xml/CDR_growth_limit_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_trade_usa").text = "../input/gcamdata/xml/CDR_traded_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_dac_usa").text = "../input/gcamdata/xml/DAC_USA.xml"
    ET.SubElement(scenario, "Value", name = "waste_heat_usa").text = "../input/gcamdata/xml/waste_heat_endogenous_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_tew_usa").text = "../input/gcamdata/xml/TEW_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_tew_resources").text = "../input/gcamdata/xml/TEW_USA_resource.xml"
    ET.SubElement(scenario, "Value", name = "cdr_tew_silicate").text = "../input/gcamdata/xml/silicate_resource_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_ew_limit").text = "../input/gcamdata/xml/limit_land_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_oae_usa").text = "../input/gcamdata/xml/OEW_USA_lime_semilocal.xml"
    ET.SubElement(scenario, "Value", name = "cdr_lime_usa").text = "../input/gcamdata/xml/lime_USA_localized.xml"
    ET.SubElement(scenario, "Value", name = "cdr_oae_shipping_usa").text = "../input/gcamdata/xml/OEW_shipping_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_nonenergy").text = "../input/gcamdata/xml/CDR_costs_USA.xml"
    ET.SubElement(scenario, "Value", name = "cdr_resources").text = "../input/gcamdata/xml/resources_USA_CDR.xml"
    
    # <!-- BECCS integration -->
    ET.SubElement(scenario, "Value", name = "beccs_integration_usa").text = "../input/gcamdata/xml/BECCS_integration_USA.xml"
    ET.SubElement(scenario, "Value", name = "beccs_countersubsidy").text = "../input/policy/CDR/counteract_BECCS_subsidy_USA.xml"



if __name__ == '__main__':
    all_configs = []
    SSP_configs = ["batch_SSP_SPA1_CDR.xml", "batch_SSP_SPA2_CDR.xml", "batch_SSP_SPA3_CDR.xml",
                   "batch_SSP_SPA4_CDR.xml", "batch_SSP_SPA5_CDR.xml"]
    default_configs = ["configuration_core.xml", "configuration_CDR_ref.xml", "configuration_CDR_policy_playground.xml"]

    main("configuration_usa.xml", False)
    main("configuration_CDR_policy_playground.xml", False) # elastic setting
    main("configuration_core.xml", False)
    main("configuration_CDR_ref.xml", False)

    for i in SSP_configs:
        main(str(i))

    for i in default_configs:
        main(str(i), False)

    """
    ### PARALELLIZATION ###
    # the worry is with parallelization is that restarts, etc. won't work right because multiple instances of GCAM will over{write files
    with multiprocessing.Pool(processes=1) as pool:
        results = pool.map(main, SSP_configs)
    """
