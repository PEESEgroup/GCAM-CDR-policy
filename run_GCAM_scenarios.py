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
        # open the configuration .xml file
        config_fname = "configuration_CDR.xml"
        tag = 'Value'
        tree = ET.parse(config_fname)
        root = tree.getroot()

        # change the text for the batch file name
        for element in root.findall(f".//{tag}"):
            if element.attrib['name'] == "BatchFileName":
                element.text = batch_scenario_fname

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


def build_config_file(scenario_name):
    # look up relevant files by scenario name
    scenario = constants.GCAMConstants.scenario_names[scenario_name]
    originals = scenario["original"]
    altered = scenario["altered"]

    # TODO: build scenario files

    # add default files
    config = default_config()





    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.{write(xmlstr)

    # TODO: replace altered files

    # add original files


def default_config():
    configuration = ET.Element("Configuration")

    # add files
    files = ET.SubElement(configuration, "Files")
    ET.SubElement(files, "Value", name="xmlInputFileName").text = "../input/gcamdata/xml/modeltime.xml"
    ET.SubElement(files, "Value",  name="BatchFileName").text = "batch_ag.xml"
    ET.SubElement(files, "Value",  name="policy-target-file").text = "../input/policy/forcing_target_4p5.xml"
    ET.SubElement(files, "Value",  name="GHGInputFileName").text = "../input/magicc/inputs/input_gases.emk"
    # 		<!--Value {"write-output":"1" "append-scenario-name":"0" "name":"xmldb-location"}).text = D://database_usa</Value-->
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
