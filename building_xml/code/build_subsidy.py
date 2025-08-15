import pandas as pd
import build_xml_config
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
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "subsidies")
    else:
        return build_xml_config.XMLOutput("original", config.config_dir + config.output_fname, "subsidies")


def build_subsidies(file):
    # merge dataframes
    markets = file["subsidy"]
    subsidy = file["subsidy_amount"]

    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    for area in markets:
        region = ET.SubElement(world, "region", name=str(area))

        # policy portfolio standard
        region_link = markets[area]
        policy_portfolio_standard = ET.SubElement(region, "policy-portfolio-standard",
                                                  name=region_link["policy-portfolio-standard"])
        ET.SubElement(policy_portfolio_standard, "policyType").text = "subsidy"
        ET.SubElement(policy_portfolio_standard, "market").text = region_link["market"]

        # add in the tax data
        for region, year, sector, subsector, tech in subsidy:
            if region == area:  # if the regions match
                year_sub = subsidy[region, year, sector, subsector, tech]
                ET.SubElement(policy_portfolio_standard, "fixedTax", year=str(year)).text = str(year_sub["fixedTax"])

        # sectors
        supply_sector = ET.SubElement(region, "supplysector", name=region_link["supplysector"])
        subsector = ET.SubElement(supply_sector, "subsector", name=region_link["subsector"])
        ET.SubElement(subsector, "stub-technology", name=region_link["stub-technology"])

    return scenario
