import build_xml_config
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_BECCS_integration(config, baseline=True):
    """
    build the BECCS integration policy configuration file from .csv files
    :param config: configuration file
    :param baseline: if this is a baseline file
    :return: dictionary of output information
    """
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    RES = ""
    tech = ""
    countersubsidy = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)

    # min-price is the lowest price of the subsidy to BECCS markets from CDR
    # max-price doesn't appear to do anything....
    if "RES_markets" in data:
        RES = data["RES_markets"]
    if "RES_tech_verify" in data:
        tech = data["RES_tech_verify"]
    if "countersubsidy" in data:
        countersubsidy = data["countersubsidy"]

    # build remainder of the file
    scenario = build_RES(RES)
    scenario = build_tech(scenario, tech)
    scenario = build_countersubsidy(scenario, countersubsidy)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "BECCS-integration")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "BECCS-integration")


def build_RES(file):
    """
    build the RES policy portfolio standrad
    :param file: input data file
    :return: root of the xml tree
    """
    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    for area in file:
        region = ET.SubElement(world, "region", name=str(area))

        # policy portfolio standard
        region_link = file[area]
        policy_portfolio_standard = ET.SubElement(region, "policy-portfolio-standard",
                                                  name=region_link["policy-portfolio-standard"])
        ET.SubElement(policy_portfolio_standard, "policyType").text = "RES"
        ET.SubElement(policy_portfolio_standard, "market").text = region_link["market"]
        ET.SubElement(policy_portfolio_standard, "constraint", fillout=str(region_link["constraint-fillout"]),
                      year=str(region_link["constraint-year"])).text = str(region_link["constraint"])

        # ghg policy
        ghg_policy = ET.SubElement(region, "ghgpolicy", name=region_link["ghgpolicy"])
        ET.SubElement(ghg_policy, "fixedTax", year=str(region_link["fixedTax-year"]),
                      fillout=str(region_link["fixedTax-fillout"])).text = str(region_link["fixedTax"])

        # sectors
        supply_sector = ET.SubElement(region, "supplysector", name=region_link["supplysector"])
        subsector = ET.SubElement(supply_sector, "subsector", name=region_link["subsector"])
        ET.SubElement(subsector, "stub-technology", name=region_link["stub-technology"])

    return scenario


def build_tech(scenario, file):
    """
    build the global technology database portion on the BECCS integration file
    :param scenario: root node of the ET
    :param file: input data
    :return: root node of the ET
    """
    world = scenario.find(".//world")
    global_tech = ET.SubElement(world, "global-technology-database")
    location = ET.SubElement(global_tech, "location-info", {"sector-name": "CDR_regional", "subsector-name": "CDR"})
    technology = ET.SubElement(location, "technology", name="BECCS")

    for year in file:
        link = file[year]
        period = ET.SubElement(technology, "period", year=str(year))
        ET.SubElement(period, "share-weight").text = str(link["shareweight"])
        minicam = ET.SubElement(period, "minicam-energy-input", name=link["minicam-energy-input"])
        ET.SubElement(minicam, "coefficient").text = str(link["coefficient"])

        # find all policy portfolio standards
        for policy_portfolio_standard in scenario.findall(".//policy-portfolio-standard"):
            ET.SubElement(policy_portfolio_standard, "min-price", fillout=str(0), year=str(year)).text = str(link["min-price"])

    return scenario


def build_countersubsidy(scenario, file):
    """
    builds the BECCS countersubisidy as defined in GCAM-CDR
    :param scenario: root node of the ET
    :param file: input data file
    :return: root node of the ET
    """
    global_tech = scenario.find(".//global-technology-database")

    for col_sector, col_subsector, technology, year in file:
        link = file[(col_sector, col_subsector, technology, year)]
        location = ET.SubElement(global_tech, "location-info",
                                 {"sector-name": col_sector, "subsector-name": col_subsector})
        tech = ET.SubElement(location, "technology", name=technology)
        period = ET.SubElement(tech, "period", year=str(year))
        res_sec = ET.SubElement(period, "res-secondary-output", name=link["res-secondary-output"])
        ET.SubElement(res_sec, "output-ratio").text = str(link["output-ratio"])
        ET.SubElement(res_sec, "pMultiplier").text = str(link["pMultiplier"])
        ctax = ET.SubElement(period, "ctax-input", name=link["ctax-input"])
        ET.SubElement(ctax, "fuel-C-coef").text = str(link["fuel-C-coef"])

    return scenario
