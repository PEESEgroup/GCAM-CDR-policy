import build_xml_config
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_GHG(config, baseline=True):
    """
    build the configuration file for ghg emissions constraints and taxes
    :param config: xml config object
    :param baseline: boolean if this is a baseline file or an altered one
    :return: XMLOutput object containing relevant file types
    """
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    linked_ghg_data = ""
    constraint = ""
    tax = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)

    if "ghg_CDR_market_link" in data:
        linked_ghg_data = data["ghg_CDR_market_link"]
    if "ghg_constraint_verify" in data:
        constraint = data["ghg_constraint_verify"]
    if "ghg_tax_verify" in data:
        tax = data["ghg_tax_verify"]

    # build remainder of the file
    scenario = build_ghg_policy(linked_ghg_data)
    scenario = emissions_constraint(scenario, constraint)
    scenario = emissions_tax(scenario, tax)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "GHG emissions policy")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "GHG emissions policy")


def build_ghg_policy(file):
    """
    build the ghg emissions policy
    :param file: dictionary containing relevant ghg information
    :return: ET tree root
    """
    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    for area in file:
        region = ET.SubElement(world, "region", name=str(area))

        # policy portfolio standard
        region_link = file[area]
        policy = str(region_link["linked-policy"]).split(";")
        for p in policy:
            policy = ET.SubElement(region, "ghgpolicy", name=p)
            ET.SubElement(policy, "market").text = region_link["market"]

    return scenario


def emissions_constraint(scenario, file):
    """
    add a ghg emissions constraing to the file
    :param scenario: root of the xml tree
    :param file: file containing ghg emissions constraint information
    :return: root of the xml tree
    """
    for year, r, ghg in file:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        ghg_policy = region.find(".//ghgpolicy[@name='" + ghg + "']")
        ET.SubElement(ghg_policy, "constraint", year=str(year)).text = str(file[(year, r, ghg)]["constraint"])

    return scenario


def emissions_tax(scenario, file):
    """
    adds an emissions tax policy to certain regions
    :param scenario: the root of the xml tree
    :param file: the dict which contains information for ghg emissions tax policies
    :return: root of the xml tree
    """
    for year, r, ghg in file:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        ghg_policy = region.find(".//ghgpolicy[@name='" + ghg + "']")
        ET.SubElement(ghg_policy, "fixedTax", year=str(year)).text = str(file[(year, r, ghg)]["fixedTax"])

    return scenario
