import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_BECCS_integration(config, baseline=False):
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    RES = ""
    tech = ""
    countersubsidy = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)

    if "RES" in data:
        RES = data["RES"]
    if "tech" in data:
        tech = data["tech"]
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
        return {"build_file_type": "baseline",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "BECCS-integration"}
    else:
        return {"build_file_type": "altered",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "BECCS-integration"}


def build_RES(file):
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
        ET.SubElement(policy_portfolio_standard, "min-price", fillout=str(region_link["min-price-fillout"]),
                      year=str(region_link["min-price-year"])).text = str(region_link["min-price"])
        ET.SubElement(policy_portfolio_standard, "max-price", fillout=str(region_link["max-price-fillout"]),
                      year=str(region_link["max-price-year"])).text = str(region_link["max-price"])
        ET.SubElement(policy_portfolio_standard, "constraint", fillout=str(region_link["constraint"]),
                      year=str(region_link["constraint"])).text = str(region_link["constraint"])

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
    world = scenario.find(".//region")
    global_tech = ET.SubElement(world, "global-technology-database")
    location = ET.SubElement(global_tech, "location-info", {"sector-name": "CDR_regional", "subsector-name": "CDR"})
    technology = ET.SubElement(location, "technology", name="BECCS")

    for year in file:
        link = file[str(year)]
        period = ET.SubElement(technology, "period", year=str(year))
        ET.SubElement(year, "share-weight").text = link["shareweight"]
        minicam = ET.SubElement(period, "minicam-energy-input", name=link["minicam-energy-input"])
        ET.SubElement(minicam, "coefficient").text = str(link["coefficient"])

    return scenario


def build_countersubsidy(scenario, file):
    return scenario
