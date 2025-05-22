import xml.etree.cElementTree as ET
import multiprocessing
import subprocess
import os

def main(batch_scenario_fname):
    """
    control program for running a GCAM scenario
    """
    # change directory
    os.chdir("./gcam/exe")

    # open the configuration .xml file
    config_fname = "configuration_CDR.xml"
    tag = 'Value'
    tree = ET.parse(config_fname)
    root = tree.getroot()

    # change the text
    for element in root.findall(f".//{tag}"):
        if element.attrib['name'] == "BatchFileName":
            element.text = batch_scenario_fname

    # write out the updated configuration file to a new file name
    config_fname = "scenario-config/config_" + batch_scenario_fname

    # write out file data
    with open(config_fname, "w+") as f:
        f.write("")
    tree.write(config_fname)

    # run GCAM-CDR from the os

    # change the name of the config file in the .bat file
    bat_fname = 'run-gcam-cdr_' + batch_scenario_fname.split(".")[0] + ".bat"
    original_bat_fname = 'run-gcam-cdr.bat'

    lines = open(original_bat_fname, 'r').readlines()

    # now edit the appropriate line of the list of lines
    new_last_line = ("gcam-cdr.exe -C " + config_fname)
    lines[25] = new_last_line

    print(lines[25])

    # now write the modified list back out to the file
    open(bat_fname, 'w').writelines(lines)

    # change the name of the .bat file
    subprocess.call([r'{}'.format(bat_fname)], creationflags = subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    SSP_configs = ["batch_SSP_SPA1_CDR.xml", "batch_SSP_SPA23_CDR.xml",
                   "batch_SSP_SPA4_CDR.xml", "batch_SSP_SPA5_CDR.xml"]

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(main, SSP_configs)
