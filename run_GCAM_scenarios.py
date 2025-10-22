import xml.etree.cElementTree as ET
from xml.dom import minidom
import multiprocessing
import subprocess
import os
import constants
import shutil
import process_GCAM_data
import produce_regional_queries
import read_GCAM_DB
import verification
import utilities
import plotting_script
from building_xml.code import build_CDR_demand, build_BECCS_integration, build_global_GHG, build_subsidy, \
    build_tech_costs, build_transport_TEW, build_transport_OEW, build_cstorage


def main(scenario, baseline, batch=False):
    """
    control program for setting up, running, validating, and analyzing the GCAM scenario
    :param scenario: scenario name
    :param baseline: baseline name
    :param batch: if this is a batch GCAM config file
    :return: N/A
    """
    # generate config files
    config_fname = build_config_file(scenario, baseline)

    # generate query files
    produce_regional_queries.main()

    # execute GCAM files
    execute_GCAM(baseline, batch, scenario, config_fname)

    # process output
    config_fname = config_fname.split(".")[0]
    xmldb_ops(config_fname)
    read_GCAM_DB.main(config_fname)
    process_GCAM_data.main(config_fname)
    verification.main(config_fname)
    plotting_script.main(config_fname, "2050")


def execute_GCAM(baseline, batch, scenario, config_fname):
    """
    run gcam using custom configuration on the command line
    :param baseline: baseline name
    :param batch: if this is a batch file
    :param scenario: scenario name
    :param config_fname: combination of the scenario and baseline name
    :return: N/A
    """
    # severe error: geothermal in US is not related to other activies just means that geothermal production is not
    # aggregated at the country level - geothermal is produced at the state level
    # water_td_USA: Hawaii doesn't exist - no irr water existing in hawaii for some reason

    # change directory if not already in the \gcam\exe folder
    if str(os.getcwd()).split("\\")[-1] != "exe":
        os.chdir("./gcam/exe/")
    # change the name of the config file in the .bat file
    bat_fname = 'run-gcam-cdr_' + scenario + "_" + baseline + ".bat"
    original_bat_fname = 'run-gcam-cdr.bat'
    lines = open(original_bat_fname, 'r').readlines()

    if batch:
        # open the configuration .xml file
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

        # write out file data
        with open(config_fname, "w+") as f:
            f.write("")
        tree.write(config_fname)

    # run GCAM-CDR from the os
    # now edit the appropriate line of the list of lines
    new_last_line = ("gcam-cdr.exe -C " + config_fname)
    lines[25] = new_last_line

    # now write the modified list back out to the file
    open(bat_fname, 'w').writelines(lines)

    # run the batch file
    subprocess.call([r'{}'.format(bat_fname)], creationflags=subprocess.CREATE_NEW_CONSOLE)

    # reset cwd
    if str(os.getcwd()).split("\\")[-1] == "exe":
        os.chdir("./../../")


def xmldb_ops(config_name):
    """
    manage output xmldb by renaming output directory and copying and empty directory and renaming it to the
    default output
    :param config_name: scenario name
    :return: N/A
    """
    output_dir = "gcam/output/database_basexdb-" + str(config_name)
    # delete existing output data folder (automatically overwrites data)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    # rename the output folder
    os.rename("gcam/output/database_basexdb", output_dir)

    # copy the empty folder and rename
    shutil.copytree("gcam/output/database_empty", "gcam/output/database_basexdb")


def build_config_file(scenario_name, baseline):
    """
    Build the main configuration file for GCAM
    :param scenario_name: the scenario name
    :param baseline: the baseline name
    :return: filename of the configuration file
    """
    # look up relevant files by scenario name
    original = []
    altered = []

    # build required xml files from raw data
    if scenario_name == baseline:
        # prevents duplication of scenario files when baseline scenario
        xml_baseline_files = utilities.build_from_scenario(baseline)
        xml_scenario_files = None
    else:
        xml_baseline_files = utilities.build_from_scenario(baseline)
        xml_scenario_files = utilities.build_from_scenario(scenario_name)

    baseline_files = build_files(xml_baseline_files, baseline=True)

    # there might be no scenario files
    if xml_scenario_files is None:
        scenario_files = []
    else:
        scenario_files = build_files(xml_scenario_files, baseline=False)

    # find out which files are new and which are altered
    for x in scenario_files:
        if "original" == str(x.build_file_type):
            original.append(x)
        elif "altered" == str(x.build_file_type):
            altered.append(x)
        else:
            print("wrong file type", str(x.build_file_type))

    # add default files
    config = default_config(scenario_name + "_" + baseline)
    scenario_components = config.find("ScenarioComponents")

    # add baseline files
    for file in baseline_files:
        # if it is a policy, put it at the end, otherwise, put it in the middle:
        if "policy" in str(file.descriptor).lower():
            ET.SubElement(scenario_components, "Value", name=file.descriptor).text = file.filepath
        else:
            # after cdr_resources
            element = ET.Element("Value", name=file.descriptor)
            element.text = file.filepath
            scenario_components.insert(100, element)

    # replace altered files
    for file in altered:
        # remove original entry
        original_entry = config.find(".//Value[@name='" + file.descriptor + "']")
        original_entry.text = file.filepath
        # scenario_components.remove(original_entry)
        # # add altered entry with default name
        # ET.SubElement(scenario_components, "Value", name=file.descriptor).text = file.filepath

    # add original files
    for file in original:
        ET.SubElement(scenario_components, "Value", name=file.descriptor).text = file.filepath

    # write out xml
    xmlstr = minidom.parseString(ET.tostring(config, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    config_fname = scenario_name + "_" + baseline + ".xml"
    with open("./gcam/exe/" + config_fname, "w+") as f:
        f.write(xmlstr)
    return config_fname


def build_files(xml_files_to_build, baseline):
    """
    build xml files based on the configuration type
    :param xml_files_to_build: a list of xml config objects to be built
    :param baseline: portion of config name (scenario or baseline) to use to build xml config files
    :return: a list of files that were built
    """
    files = []
    for k in xml_files_to_build:
        if k.xml_build_type == "CDR Policy":
            files.append(build_CDR_demand.build(k, baseline))
        if k.xml_build_type == "BECCS RES":
            files.append(build_BECCS_integration.build_BECCS_integration(k, baseline))
        if k.xml_build_type == "GHG constraint":
            files.append(build_global_GHG.build_GHG(k, baseline))
        if k.xml_build_type == "subsidy Policy":
            files.append(build_subsidy.build_subsidy(k, baseline))
        if k.xml_build_type == "tech_non-input_costs":
            files.append(build_tech_costs.build_tech_costs(k, baseline))
        if k.xml_build_type == "TEW Transport Cost Reduction":
            files.append(build_transport_TEW.build_tew_transport(k, baseline))
        if k.xml_build_type == "OEW Transport Cost Reduction":
            files.append(build_transport_OEW.build_oew_transport(k, baseline))
        if k.xml_build_type == "C Storage Cost Reduction":
            files.append(build_cstorage.build_cstorage(k, baseline))
        # TODO add more build types here

    return files


def default_config(config_name):
    """
    baseline: scenario name for baseline exogenous CDR demand
    :param config_name: scenario name
    :return:
    """
    configuration = ET.Element("Configuration")

    # add files
    files = ET.SubElement(configuration, "Files")
    ET.SubElement(files, "Value", name="xmlInputFileName").text = "../input/gcamdata/xml/modeltime.xml"
    ET.SubElement(files, "Value", name="BatchFileName").text = "batch_ag.xml"
    ET.SubElement(files, "Value", name="policy-target-file").text = "../input/policy/forcing_target_4p5.xml"
    ET.SubElement(files, "Value", name="GHGInputFileName").text = "../input/magicc/inputs/input_gases.emk"
    # 		<!--Value {"write-output":"1" "append-scenario-name":"0" "name":"xmldb-location"}).text = "D://database_usa</Value-->
    ET.SubElement(files, "Value", attrib={"write-output": "1", "append-scenario-name": "0",
                                          "name": "xmldb-location"}).text = "../output/database_basexdb"
    ET.SubElement(files, "Value", attrib={"write-output": "1", "append-scenario-name": "0",
                                          "name": "restart"}).text = "./restart/restart"
    ET.SubElement(files, "Value", attrib={"write-output": "1", "append-scenario-name": "0",
                                          "name": "xmlDebugFileName"}).text = "debug.xml"
    ET.SubElement(files, "Value",
                  attrib={"write-output": "1", "append-scenario-name": "0", "name": "climatFileName"}).text = "gas.emk"
    ET.SubElement(files, "Value", attrib={"write-output": "1", "append-scenario-name": "1",
                                          "name": "costCurvesOutputFileName"}).text = "cost_curves.xml"
    ET.SubElement(files, "Value", attrib={"write-output": "1", "append-scenario-name": "0",
                                          "name": "batchCSVOutputFile"}).text = "batch-csv-out.csv"
    ET.SubElement(files, "Value", attrib={"write-output": "0", "append-scenario-name": "0",
                                          "name": "supplyDemandOutputFileName"}).text = "SDCurves.csv"
    ET.SubElement(files, "Value", attrib={"write-output": "0", "append-scenario-name": "0",
                                          "name": "flow-graph"}).text = "gcam-flow-graph.dot"
    ET.SubElement(files, "Value", attrib={"write-output": "0", "append-scenario-name": "0",
                                          "name": "dependencyGraphName"}).text = "DependencyGraph.dot"
    ET.SubElement(files, "Value", attrib={"write-output": "0", "append-scenario-name": "0",
                                          "name": "landAllocatorGraphName"}).text = "LandAllocatorGraph.dot"

    # add scenario components
    scenario = ET.SubElement(configuration, "ScenarioComponents")
    ET.SubElement(scenario, "Value", name="climate").text = "../input/gcamdata/xml/no_climate_model.xml"
    ET.SubElement(scenario, "Value", name="socioeconomics").text = "../input/gcamdata/xml/socioeconomics_gSSP2.xml"

    ET.SubElement(scenario, "Value", name="resources").text = "../input/gcamdata/xml/resources.xml"
    ET.SubElement(scenario, "Value", name="energy_supply").text = "../input/gcamdata/xml/en_supply.xml"
    ET.SubElement(scenario, "Value", name="energy_transformation").text = "../input/gcamdata/xml/en_transformation.xml"
    # <!--Value name = "electricity").text = "../input/gcamdata/xml/electricity.xml"</Value-->
    ET.SubElement(scenario, "Value", name="elec_water_base").text = "../input/gcamdata/xml/electricity_water.xml"
    ET.SubElement(scenario, "Value", name="heat").text = "../input/gcamdata/xml/heat.xml"
    ET.SubElement(scenario, "Value", name="hydrogen").text = "../input/gcamdata/xml/hydrogen.xml"
    ET.SubElement(scenario, "Value", name="energy_distribution").text = "../input/gcamdata/xml/en_distribution.xml"
    ET.SubElement(scenario, "Value", name="industry").text = "../input/gcamdata/xml/industry.xml"
    ET.SubElement(scenario, "Value",
                  name="industry_income_elas").text = "../input/gcamdata/xml/industry_incelas_gssp2.xml"
    ET.SubElement(scenario, "Value", name="cement").text = "../input/gcamdata/xml/cement.xml"
    ET.SubElement(scenario, "Value", name="cement_income_elas").text = "../input/gcamdata/xml/cement_incelas_gssp2.xml"
    ET.SubElement(scenario, "Value", name="fertilizer_energy").text = "../input/gcamdata/xml/en_Fert.xml"
    ET.SubElement(scenario, "Value", name="hddcdd").text = "../input/gcamdata/xml/HDDCDD_constdd_no_GCM.xml"
    ET.SubElement(scenario, "Value", name="building").text = "../input/gcamdata/xml/building_det.xml"
    ET.SubElement(scenario, "Value", name="transportation").text = "../input/gcamdata/xml/transportation_UCD_CORE.xml"
    ET.SubElement(scenario, "Value", name="carbon_content").text = "../input/gcamdata/xml/Ccoef.xml"
    ET.SubElement(scenario, "Value", name="carbon_storage").text = "../input/gcamdata/xml/Cstorage.xml"

    ET.SubElement(scenario, "Value", name="ag_base").text = "../input/gcamdata/xml/ag_For_Past_bio_base_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="ag_cost").text = "../input/gcamdata/xml/ag_cost_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="ag_prodchange").text = "../input/gcamdata/xml/ag_prodchange_ref_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="residue_bio").text = "../input/gcamdata/xml/resbio_input_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="animal").text = "../input/gcamdata/xml/an_input.xml"
    ET.SubElement(scenario, "Value", name="fertilizer").text = "../input/gcamdata/xml/ag_Fert_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="land1").text = "../input/gcamdata/xml/land_input_1.xml"
    ET.SubElement(scenario, "Value", name="land2").text = "../input/gcamdata/xml/land_input_2.xml"
    ET.SubElement(scenario, "Value", name="land3").text = "../input/gcamdata/xml/land_input_3_IRR.xml"
    ET.SubElement(scenario, "Value", name="land4").text = "../input/gcamdata/xml/land_input_4_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="land5").text = "../input/gcamdata/xml/land_input_5_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="protected_land2").text = "../input/gcamdata/xml/protected_land_input_2.xml"
    ET.SubElement(scenario, "Value", name="protected_land3").text = "../input/gcamdata/xml/protected_land_input_3.xml"
    ET.SubElement(scenario, "Value", name="demand").text = "../input/gcamdata/xml/ag_an_demand_input.xml"
    ET.SubElement(scenario, "Value", name="bio_trade").text = "../input/gcamdata/xml/bio_trade.xml"
    ET.SubElement(scenario, "Value", name="ag_trade").text = "../input/gcamdata/xml/ag_trade.xml"

    ET.SubElement(scenario, "Value",
                  name="unlim_supply_water").text = "../input/gcamdata/xml/unlimited_water_supply.xml"
    ET.SubElement(scenario, "Value", name="water_supply").text = "../input/gcamdata/xml/water_supply_constrained.xml"
    ET.SubElement(scenario, "Value", name="water_desal").text = "../input/gcamdata/xml/desalination.xml"
    ET.SubElement(scenario, "Value", name="water_td").text = "../input/gcamdata/xml/water_td.xml"
    ET.SubElement(scenario, "Value", name="efw_coefs").text = "../input/gcamdata/xml/EFW_input_coefs.xml"
    ET.SubElement(scenario, "Value", name="efw_irr").text = "../input/gcamdata/xml/EFW_irrigation.xml"
    ET.SubElement(scenario, "Value", name="efw_mfg").text = "../input/gcamdata/xml/EFW_manufacturing.xml"
    ET.SubElement(scenario, "Value", name="efw_muni").text = "../input/gcamdata/xml/EFW_municipal.xml"
    ET.SubElement(scenario, "Value", name="ag_water").text = "../input/gcamdata/xml/ag_water_input_IRR_MGMT.xml"
    ET.SubElement(scenario, "Value", name="elec_water_coef").text = "../input/gcamdata/xml/electricity_water_coefs.xml"
    ET.SubElement(scenario, "Value", name="ind_water").text = "../input/gcamdata/xml/water_demand_industry.xml"
    ET.SubElement(scenario, "Value", name="an_water").text = "../input/gcamdata/xml/water_demand_livestock.xml"
    ET.SubElement(scenario, "Value", name="municipal_water").text = "../input/gcamdata/xml/water_demand_municipal.xml"
    ET.SubElement(scenario, "Value", name="primary_ene_water").text = "../input/gcamdata/xml/water_demand_primary.xml"

    ET.SubElement(scenario, "Value", name="bio_feedstock_limit").text = "../input/gcamdata/xml/liquids_limits.xml"
    ET.SubElement(scenario, "Value",
                  name="bio_elec_w_feed_limit").text = "../input/gcamdata/xml/water_elec_liquids_limits.xml"
    # <!-- ET.SubElement(scenario, "Value", name = "bio_neg_emiss_budget").text =
    #   "../input/gcamdata/xml/negative_emissions_budget_gSSP2.xml" -->
    ET.SubElement(scenario, "Value", name="wind_update").text = "../input/gcamdata/xml/onshore_wind.xml"

    ET.SubElement(scenario, "Value", name="socio_usa").text = "../input/gcamdata/xml/socioeconomics_USA.xml"
    ET.SubElement(scenario, "Value", name="resource_usa").text = "../input/gcamdata/xml/resources_USA.xml"
    ET.SubElement(scenario, "Value", name="Cstorage_usa").text = "../input/gcamdata/xml/Cstorage_USA.xml"
    ET.SubElement(scenario, "Value", name="prices_usa").text = "../input/gcamdata/xml/en_prices_USA.xml"
    ET.SubElement(scenario, "Value", name="en_transform_usa").text = "../input/gcamdata/xml/en_transformation_USA.xml"
    # <!--Value name = "elec_usa").text = "../input/gcamdata/xml/elec_segments_USA.xml"</Value-->
    ET.SubElement(scenario, "Value", name="elec_water_usa").text = "../input/gcamdata/xml/elec_segments_water_USA.xml"
    ET.SubElement(scenario, "Value", name="h2_usa").text = "../input/gcamdata/xml/hydrogen_USA.xml"
    ET.SubElement(scenario, "Value", name="elect_td_usa").text = "../input/gcamdata/xml/electd_USA.xml"
    ET.SubElement(scenario, "Value", name="trn_usa").text = "../input/gcamdata/xml/transportation_USA_CORE.xml"
    ET.SubElement(scenario, "Value", name="bld_usa").text = "../input/gcamdata/xml/building_USA.xml"
    ET.SubElement(scenario, "Value", name="dd_usa").text = "../input/gcamdata/xml/HDDCDD_constdds_USA.xml"
    ET.SubElement(scenario, "Value", name="ind_usa").text = "../input/gcamdata/xml/industry_USA.xml"
    ET.SubElement(scenario, "Value", name="ind_vintage_usa").text = "../input/gcamdata/xml/industry_vintage_USA.xml"
    ET.SubElement(scenario, "Value", name="cement_usa").text = "../input/gcamdata/xml/cement_USA.xml"
    ET.SubElement(scenario, "Value", name="fert_usa").text = "../input/gcamdata/xml/Fert_USA.xml"

    # <!-- NEW NESTING STRUCTURE -->
    ET.SubElement(scenario, "Value", name="solar_usa").text = "../input/gcamdata/xml/solar_reeds_USA.xml"
    ET.SubElement(scenario, "Value", name="wind_usa").text = "../input/gcamdata/xml/wind_reeds_USA.xml"
    ET.SubElement(scenario, "Value", name="hydro_usa").text = "../input/gcamdata/xml/elec_hydro_USA.xml"
    ET.SubElement(scenario, "Value", name="nuc_usa").text = "../input/gcamdata/xml/nuclear_USA.xml"
    ET.SubElement(scenario, "Value", name="no_new_coal_usa").text = "../input/gcamdata/xml/nonewcoal_USA.xml"
    ET.SubElement(scenario, "Value", name="ITC_usa").text = "../input/gcamdata/xml/elecS_costs_USA_itc.xml"
    ET.SubElement(scenario, "Value", name="PTC_usa").text = "../input/gcamdata/xml/elecS_costs_USA_ptc.xml"

    ET.SubElement(scenario, "Value", name="liq_lim_usa").text = "../input/gcamdata/xml/liquids_limits_USA.xml"
    ET.SubElement(scenario, "Value", name="USA_regional_bio").text = "../input/gcamdata/xml/regional_biomass_USA.xml"

    # <!--WATER DATA-->
    ET.SubElement(scenario, "Value", name="water_td_usa").text = "../input/gcamdata/xml/water_td_USA.xml"
    ET.SubElement(scenario, "Value",
                  name="municipal_water_usa").text = "../input/gcamdata/xml/water_demand_municipal_USA.xml"
    ET.SubElement(scenario, "Value", name="ind_water_usa").text = "../input/gcamdata/xml/water_demand_industry_USA.xml"
    ET.SubElement(scenario, "Value", name="solver").text = "../input/solution/cal_broyden_config.xml"

    # <!-- accelerate decarbonization -->
    ET.SubElement(scenario, "Value", name="adv_geothermal").text = "../input/gcamdata/xml/geo_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_solar").text = "../input/gcamdata/xml/solar_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_wind").text = "../input/gcamdata/xml/wind_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_nuclear").text = "../input/gcamdata/xml/nuclear_adv.xml"
    ET.SubElement(scenario, "Value", name="adv_EV").text = "../input/gcamdata/xml/transportation_USA_highEV.xml"

    # <!-- bioseparation -->
    ET.SubElement(scenario, "Value",
                  name="biosep_global").text = "../input/gcamdata/xml/bio_sep_final_final_final27.xml"
    ET.SubElement(scenario, "Value", name="biossep_limits").text = "../input/gcamdata/xml/bio_sep_liquids_limits.xml"
    ET.SubElement(scenario, "Value", name="biosep_liquids").text = "../input/gcamdata/xml/bio_sep_USA_liquids.xml"
    ET.SubElement(scenario, "Value", name="biosep_industry").text = "../input/gcamdata/xml/bio_sep_USA_industry.xml"
    ET.SubElement(scenario, "Value", name="biosep_gas").text = "../input/gcamdata/xml/bio_sep_USA_gas.xml"
    ET.SubElement(scenario, "Value", name="biosep_gas").text = "../input/gcamdata/xml/bio_sep_USA_elec_segments.xml"
    ET.SubElement(scenario, "Value", name="bio_water_usage").text = "../input/gcamdata/xml/electricity_water_coefs_bio.xml"

    # <!-- add primary CDR -->
    ET.SubElement(scenario, "Value", name="cdr_rampup").text = "../input/gcamdata/xml/CDR.xml"
    # ET.SubElement(scenario, "Value", name="cdr_discrete_choice").text = "../input/gcamdata/xml/CDR_discrete_choice.xml"
    ET.SubElement(scenario, "Value", name="cdr_trade").text = "../input/gcamdata/xml/CDR_traded.xml"
    ET.SubElement(scenario, "Value", name="cdr_dac").text = "../input/gcamdata/xml/DAC.xml"
    ET.SubElement(scenario, "Value", name="waste_heat").text = "../input/gcamdata/xml/waste_heat_endogenous.xml"
    ET.SubElement(scenario, "Value", name="cdr_ew").text = "../input/gcamdata/xml/TEW.xml"
    ET.SubElement(scenario, "Value", name="cdr_ew_limit").text = "../input/gcamdata/xml/limit_land.xml"
    ET.SubElement(scenario, "Value", name="cdr_oae").text = "../input/gcamdata/xml/OEW.xml"
    ET.SubElement(scenario, "Value", name="cdr_oae_shipping").text = "../input/gcamdata/xml/OEW_shipping.xml"
    ET.SubElement(scenario, "Value", name="cdr_resources").text = "../input/gcamdata/xml/resources_CDR.xml"

    # <!-- CDR in USA -->
    ET.SubElement(scenario, "Value", name="cdr_usa").text = "../input/gcamdata/xml/CDR_USA.xml"
    # ET.SubElement(scenario, "Value", name="growth_limit").text = "../input/gcamdata/xml/CDR_discrete_choice_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_trade_usa").text = "../input/gcamdata/xml/CDR_traded_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_dac_usa").text = "../input/gcamdata/xml/DAC_USA.xml"
    ET.SubElement(scenario, "Value", name="waste_heat_usa").text = "../input/gcamdata/xml/waste_heat_endogenous_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_tew_usa").text = "../input/gcamdata/xml/TEW_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_tew_resources").text = "../input/gcamdata/xml/TEW_USA_resource.xml"
    ET.SubElement(scenario, "Value", name="cdr_tew_silicate").text = "../input/gcamdata/xml/silicate_resource_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_ew_limit").text = "../input/gcamdata/xml/limit_land_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_oae_usa").text = "../input/gcamdata/xml/OEW_USA_lime_semilocal.xml"
    ET.SubElement(scenario, "Value", name="cdr_lime_usa").text = "../input/gcamdata/xml/lime_USA_localized.xml"
    ET.SubElement(scenario, "Value", name="cdr_oae_shipping_usa").text = "../input/gcamdata/xml/OEW_shipping_USA.xml"
    ET.SubElement(scenario, "Value", name="cdr_resources").text = "../input/gcamdata/xml/resources_USA_CDR.xml"
    ET.SubElement(scenario, "Value", name="ignore_beccs").text = "../input/policy/CDR/ignore_BECCS_in_CO2_constraint.xml"

    # policy is automatically handled elsewhere in the configuration process

    strings = ET.SubElement(configuration, "Strings")
    bools = ET.SubElement(configuration, "Bools")
    ints = ET.SubElement(configuration, "Ints")
    doubles = ET.SubElement(configuration, "Doubles")

    # <Strings>
    ET.SubElement(strings, "Value", name="scenarioName").text = config_name
    ET.SubElement(strings, "Value", name="debug-region").text = "CA"
    ET.SubElement(strings, "Value", name="MAGICC-input-dir").text = "../input/magicc/inputs"
    ET.SubElement(strings, "Value", name="MAGICC-output-dir").text = "../output"
    ET.SubElement(strings, "Value", name="AbatedGasForCostCurves").text = "CO2"
    # 	</Strings>
    # 	<Bools>
    ET.SubElement(bools, "Value", name="CalibrationActive").text = "1"
    ET.SubElement(bools, "Value", name="BatchMode").text = "0"
    ET.SubElement(bools, "Value", name="find-path").text = "0"
    ET.SubElement(bools, "Value", name="createCostCurve").text = "0"
    ET.SubElement(bools, "Value", name="debugChecking").text = "0"
    ET.SubElement(bools, "Value", name="simulActive").text = "1"
    ET.SubElement(bools, "Value", name="PrintValuesOnGraphs").text = "1"
    ET.SubElement(bools, "Value", name="ShowNullPaths").text = "0"
    ET.SubElement(bools, "Value", name="PrintPrices").text = "1"
    # 	</Bools>
    # 	<Ints>
    ET.SubElement(ints, "Value", name="numMarketsToFindSD").text = "10"
    ET.SubElement(ints, "Value", name="numPointsForSD").text = "21"
    ET.SubElement(ints, "Value", name="numPointsForCO2CostCurve").text = "5"
    ET.SubElement(ints, "Value", name="carbon-output-start-year").text = "1705"
    ET.SubElement(ints, "Value", name="climateOutputInterval").text = "5"
    ET.SubElement(ints, "Value", name="parallel-grain-size").text = "50"
    ET.SubElement(ints, "Value", name="stop-period").text = "-1"
    ET.SubElement(ints, "Value", name="stop-year").text = "2050"
    ET.SubElement(ints, "Value", name="restart-period").text = "-1"
    ET.SubElement(ints, "Value", name="restart-year").text = "-1"
    ET.SubElement(ints, "Value", name="max-parallelism").text = "3"

    return configuration


if __name__ == '__main__':
    current_configs = ["innovation-maintain_low", "innovation-triple_low", "innovation-DACHubs_low", "innovation-rhodium18b_low", "4gt_4gt"]  # use camelCase
    # the scenario and baseline name should match for any baseline scenario

    # for debugging
    for key in current_configs:
        i = key.split("_")[0]
        j = key.split("_")[1]
        main(i, j)

    # with multiprocessing.Pool(processes=3) as pool:
    #     result = pool.starmap(main, ((i, j) for i in current_configs for j in current_baseline))
