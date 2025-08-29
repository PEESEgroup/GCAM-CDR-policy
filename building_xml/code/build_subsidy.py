import build_xml_config
import constants
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_subsidy(config, baseline=True):
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
    scenario = build_subsidies(data)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "subsidy policy")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "subsidy policy")


def build_subsidies(file):
    """
    add subsidies to a policy file
    :param file: a dict containing pertinent information to the creation of the xml file
    :return: the root of the xml node
    """
    # merge dataframes
    markets = {}
    subsidy = {}
    for key, value in file.items():
        if "link" in key:
            markets = file[key]
        if "amount" in key:
            subsidy = file[key]

    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    for area in markets:
        region = ET.SubElement(world, "region", name=str(area))

        # add technologies the subsidies apply to
        invalid_regions_and_tech = ["AKTEW", "NVOEW", "IDOEW", "MTOEW", "WYOEW", "UTOEW", "COOEW", "AZOEW", "NMOEW",
                                    "NDOEW", "SDOEW", "NEOEW", "KSOEW", "OKOEW", "MNOEW", "IAOEW", "MOOEW", "AROEW",
                                    "WIOEW", "MIOEW", "INOEW", "KYOEW", "TNOEW", "OHOEW", "WVOEW", "VTOEW"]
        seen = {}
        for r, year, sector, ss, tech in subsidy:
            subname = "_" + tech + "_subsidy"
            if area+tech not in invalid_regions_and_tech:
                if r + sector + ss + tech not in seen:
                    supply_sector = ET.SubElement(region, "supplysector", name=sector)
                    subsector = ET.SubElement(supply_sector, "subsector", name=ss)
                    technology = ET.SubElement(subsector, "technology", name=tech)
                    period = ET.SubElement(technology, "period", year=str(year))
                    ET.SubElement(period, "input-subsidy", name=subname)
                    seen[r + sector + ss + tech] = 0
                    # policy portfolio standard
                    region_link = markets[area]
                    policy_portfolio_standard = ET.SubElement(region, "policy-portfolio-standard", name=subname)
                    ET.SubElement(policy_portfolio_standard, "policyType").text = "subsidy"
                    ET.SubElement(policy_portfolio_standard, "market").text = region_link["market"]
                else:
                    # technology should be referenced before
                    period = ET.SubElement(technology, "period", year=str(year))
                    ET.SubElement(period, "input-subsidy", name=subname)

                if str(year)+subname not in seen:  # if the regions match
                    year_sub = subsidy[r, year, sector, ss, tech]
                    # convert from $2025 USD/t CO2-eq to $1975/kg C
                    ET.SubElement(policy_portfolio_standard, "fixedTax", year=str(year)).text = str(
                        year_sub["fixedTax"] * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC)
                    seen[str(year)+subname] = 0

    return scenario
