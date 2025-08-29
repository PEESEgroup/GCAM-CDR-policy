import build_xml_config
import constants
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_tew_transport(config, baseline=True):
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
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "cdr_tew_usa")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "cdr_tew_usa")


def build_transport(file):
    """
    add subsidies to a policy file
    :param file: a dict containing pertinent information to the creation of the xml file
    :return: the root of the xml node
    """
    # merge dataframes
    markets = {}
    amount = {}
    for key, value in file.items():
        if "link" in key:
            markets = file[key]
        if "amount" in key:
            amount = file[key]

    # open stub
    tree = ET.parse('./gcam/input/gcamdata/xml/TEW_USA_stub.xml')
    root = tree.getroot()
    for elem in root.iter():
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()
    world = root.find(".//world")

    for area in markets:
        region = ET.SubElement(world, "region", name=str(area))

        # add base tech information
        supply_sector = ET.SubElement(region, "supplysector", name=markets[area]["supplysector"])
        rcl = ET.SubElement(supply_sector, "relative-cost-logit")
        ET.SubElement(rcl, "logit-exponent", fillout="1", year="1975").text = str(markets[area]["logit-exponent"])
        ET.SubElement(supply_sector, "output-unit").text = markets[area]["output-unit"]
        ET.SubElement(supply_sector, "input-unit").text = markets[area]["input-unit"]
        ET.SubElement(supply_sector, "price-unit").text = markets[area]["price-unit"]
        ET.SubElement(supply_sector, "keyword", final_energy=markets[area]["final-energy"])
        subsector = ET.SubElement(supply_sector, "subsector", name=markets[area]["subsector"])
        ssrcl = ET.SubElement(subsector, "relative-cost-logit")
        ET.SubElement(ssrcl, "logit-exponent", fillout="1", year="1975").text = str(markets[area]["subsector-logit-exponent"])
        ET.SubElement(subsector, "share-weight", fillout="1", year="1975").text = str(markets[area]["subsector-share-weight"])

    # add in the updated transportation distances
    for area, tech in amount:
        region = world.find(".//region[@name='" + area + "']")
        subsector = region.find(".//subsector[@name='TEW']")
        stub_tech = ET.SubElement(subsector, "stub-technology", name=tech)
        for i in constants.GCAMConstants.x:
            period = ET.SubElement(stub_tech, "period", year=str(i))
            minicam = ET.SubElement(period, "minicam-energy-input", name="trn_freight")
            ET.SubElement(minicam, "coefficient").text = str(amount[(area, tech)][str(i)])

    return root
