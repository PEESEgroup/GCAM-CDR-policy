import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_GHG(config, baseline=True):
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    linked_ghg_data = ""
    constraint = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)

    if "linked_ghg_markets" in data:
        linked_ghg_data = data["linked_ghg_markets"]
    if "ghg_constraint" in data:
        constraint = data["ghg_constraint"]

    # TODO: add LUC tax???

    # build remainder of the file
    scenario = build_ghg_policy(linked_ghg_data)
    scenario = emissions_constraint(scenario, constraint)

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
                "descriptor": "GHG-constraint policy"}
    else:
        return {"build_file_type": "altered",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "GHG-constraint policy"}


def build_ghg_policy(file):
    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    for area in file:
        region = ET.SubElement(world, "region", name=str(area))

        # policy portfolio standard
        region_link = file[area]
        policy = ET.SubElement(region, "ghgpolicy", name=region_link["linked-policy"])
        ET.SubElement(policy, "market").text = region_link["market"]

    return scenario


def emissions_constraint(scenario, file):
    for year, r in file:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        ghg_policy = region.find(".//ghgpolicy")
        ET.SubElement(ghg_policy, "constraint", year=str(year)).text = str(file[(year, r)]["constraint"])

    return scenario
