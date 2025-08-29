import build_xml_config
import constants
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_cstorage(config, baseline=True):
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
    scenario = build_c_storage(data)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "Cstorage_usa")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "Cstorage_usa")


def build_c_storage(file):
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
    tree = ET.parse('./gcam/input/gcamdata/xml/Cstorage_USA_stub.xml')
    root = tree.getroot()
    for elem in root.iter():
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()
    world = root.find(".//world")

    for area in amount:
        region = ET.SubElement(world, "region", name=str(area))
        resource = ET.SubElement(region, "resource", name="onshore carbon-storage")
        ET.SubElement(resource, "output-unit", amount[area]["output-unit"])
        ET.SubElement(resource, "price-unit", amount[area]["price-unit"])
        ET.SubElement(resource, "market", amount[area]["market"])
        subresource = ET.SubElement(resource, "subresource", name="onshore carbon-storage")
        grade_1 = ET.SubElement(subresource, "grade", name="grade 1")
        ET.SubElement(grade_1, "available").text = str(amount[area]["grade-1-available"])
        ET.SubElement(grade_1, "extractioncost").text = str(amount[area]["grade-1-extraction"])
        grade_2 = ET.SubElement(subresource, "grade", name="grade 2")
        ET.SubElement(grade_2, "available").text = str(amount[area]["grade-2-available"])
        ET.SubElement(grade_2, "extractioncost").text = str(amount[area]["grade-2-extraction"])
        grade_3 = ET.SubElement(subresource, "grade", name="grade 3")
        ET.SubElement(grade_3, "available").text = str(amount[area]["grade-3-available"])
        ET.SubElement(grade_3, "extractioncost").text = str(amount[area]["grade-3-extraction"])
        grade_4 = ET.SubElement(subresource, "grade", name="grade 4")
        ET.SubElement(grade_4, "available").text = str(amount[area]["grade-4-available"])
        ET.SubElement(grade_4, "extractioncost").text = str(amount[area]["grade-4-extraction"])

    return root
