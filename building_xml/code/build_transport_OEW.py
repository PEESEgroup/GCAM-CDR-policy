import build_xml_config
import constants
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_oew_transport(config, baseline=True):
    """
    build the BECCS integration policy configuration file
    :param config: configuration file
    :param baseline: if this is a baseline file
    :return: dictionary of output information
    """
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    # extract relevant data
    data = utilities.open_csv(input_filepath)

    # build remainder of the file
    scenario = build_transport(data)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "cdr_oae_usa")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "cdr_oae_usa")


def build_transport(file):
    """
    add subsidies to a policy file
    :param file: a dict containing pertinent information to the creation of the xml file
    :return: the root of the xml node
    """
    # merge dataframes
    amount = {}
    for key, value in file.items():
        if "amount" in key:
            amount = file[key]

    # open stub
    tree = ET.parse('./gcam/input/gcamdata/xml/OEW_USA_lime_semilocal.xml')
    root = tree.getroot()
    for elem in root.iter():
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()

    # iterate through the whole tree
    for i in constants.GCAMConstants.x:
        for year in root.iter('period'):
            if str(year.attrib["year"]) == str(i):
                for coefficient in year.iter("coefficient"):
                    for tech in amount:
                        coefficient.text = str(float(coefficient.text)*amount[tech][str(i)])

    return root
