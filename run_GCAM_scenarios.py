import xml.etree.cElementTree as ET
from xml.dom import minidom
import subprocess
import constants as c
import os

def main(batch_scenario_fname):
    """
    control program for running a GCAM scenario
    """
    # open the configuration .xml file
    config_fname = "./gcam/exe/configuration_CDR.xml"
    tag = 'Value name="BatchFileName"'
    tree = ET.parse(config_fname)
    root = tree.getroot()

    for element in root.findall(f".//{tag}"):
        element.text = batch_scenario_fname

    tree.write(config_fname)


    for i in range(len(c.GCAMConstants.version)):
        # build a batch file for every database
        filename = "xml/xmldb_batch_" + str(c.GCAMConstants.version[i][0]) + "_" + str(
            c.GCAMConstants.version[i][1]) + ".xml"
        print(filename)
        out_dir, out_file = build_batch_query(c.GCAMConstants.version[i][0], c.GCAMConstants.version[i][1], filename)

        # create output directory
        os.makedirs(out_dir, exist_ok=True)
        with open(out_file, "w") as f:
            f.write("foo")

        # edit the batch file to include the right xml query file
        # read the file into a list of lines
        bat_file = "xml/launch_model_interface.bat"
        lines = open(bat_file, 'r').readlines()

        # now edit the last line of the list of lines
        new_last_line = ("java ModelInterface.InterfaceMain -b " + filename)
        lines[-1] = new_last_line

        print(lines[-1])

        # now write the modified list back out to the file
        open(bat_file, 'w').writelines(lines)

        # execute the batch query on the command line
        subprocess.call([r'xml\launch_model_interface.bat'])


if __name__ == '__main__':
    main()
