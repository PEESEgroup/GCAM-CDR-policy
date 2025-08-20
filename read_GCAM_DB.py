import xml.etree.cElementTree as ET
from xml.dom import minidom
import subprocess
import constants as c
import os


def build_batch_query(xml_fname, config_fname):
    """
    Builds a batch query file with all the necessary things.
    :param xml_fname: filename of the xml file
    :param config_fname: the policy scenario and baseline information
    :return: directory path and file name of output file to be created if not already exist
    """
    root = ET.Element("ModelInterfaceBatch")
    dbviewer = ET.SubElement(root, "class", name="ModelInterface.ModelGUI2.DbViewer")
    command = ET.SubElement(dbviewer, "command", name="XMLDB Batch File")
    ET.SubElement(command, "scenario", name=str(config_fname))
    ET.SubElement(command, "queryFile").text = "xml/query_list.xml"

    outdir = "data/gcam_out/" + str(config_fname).replace("_", "/")
    outfile = outdir + "/ref.csv"

    ET.SubElement(command, "outFile").text = outfile
    ET.SubElement(command, "xmldbLocation").text = c.GCAMConstants.XML_DB_loc + config_fname

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(xml_fname, "w") as f:
        f.write(xmlstr)

    return outdir, outfile


def main(config_fname):
    """
    control program for querying GCAM databases
    :param config_fname configuration name for the scenario/baseline combination
    """
    # build a batch file for every database
    filename = "xml/xmldb_batch_" + str(config_fname) + ".xml"
    print(filename)
    out_dir, out_file = build_batch_query(filename, config_fname)

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
    main("default_default")

