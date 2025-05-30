import xml.etree.cElementTree as ET
import multiprocessing
import subprocess
import os

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

        # write out file data
        with open(config_fname, "w+") as f:
            f.write("")
        tree = ET.parse(batch_scenario_fname)
        tree.write(config_fname)

        # use configuration file as-is
        new_last_line = ("gcam-cdr.exe -C " + config_fname)
        lines[25] = new_last_line

        print(lines[25])

        # now write the modified list back out to the file
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

        # write out the updated configuration file to a new file name
        config_fname = config_dir + "config_" + batch_scenario_fname

        # write out file data
        with open(config_fname, "w+") as f:
            f.write("")
        tree.write(config_fname)

        # run GCAM-CDR from the os
        # now edit the appropriate line of the list of lines
        new_last_line = ("gcam-cdr.exe -C " + config_fname)
        lines[25] = new_last_line

        print(lines[25])

        # now write the modified list back out to the file
        open(bat_fname, 'w').writelines(lines)

    # change the name of the .bat file
    subprocess.call([r'{}'.format(bat_fname)], creationflags = subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
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

    ### PARALELLIZATION ###
    # the worry is with parallelization is that restarts, etc. won't work right because multiple instances of GCAM will overwrite files
    with multiprocessing.Pool(processes=1) as pool:
        results = pool.map(main, SSP_configs)
