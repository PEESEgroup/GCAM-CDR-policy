import xml.etree.cElementTree as ET
from xml.dom import minidom
import constants
import utilities


def build(config, baseline=False):
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname
    print(output_filepath)

    exo_demand = ""
    elastic_demand = ""
    offset_demand = ""
    acc_demand = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)
    linked_ghg_data = data["linked_ghg_markets"]

    if "exo_demand" in data:
        exo_demand = data["exo_demand"]
    if "elastic_demand" in data:
        elastic_demand = data["elastic_demand"]
    if "offset_demand" in data:
        offset_demand = data["offset_demand"]
    if "acc_demand" in data:
        acc_demand = data["acc_demand"]

    #TODO: combine multiple sources of exogenous demand

    # build remainder of the file
    scenario = build_markets(linked_ghg_data)
    scenario = add_exo_demand(scenario, exo_demand)
    scenario = add_elastic_demand(scenario, elastic_demand)
    scenario = add_offset_demand(scenario, offset_demand)
    scenario = add_accumulated_demand(scenario, acc_demand)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return {"build_file_type": "baseline",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "CDR-Demand"}
    else:
        return {"build_file_type": "altered",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "CDR-Demand"}


def build_markets(linked_ghg_data):
    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    # CDR-demand by default does not include the USA as a region
    region = ET.SubElement(world, "region", name="USA")
    supply_sector = ET.SubElement(region, "supplysector", name="CDR_traded")
    ET.SubElement(supply_sector, "subsector", delete="1", name="CDR_USA")

    # region specific data
    for area in linked_ghg_data:
        region = ET.SubElement(world, "region", name=str(area))

        # linked ghg policy
        region_link = linked_ghg_data[area]
        link = ET.SubElement(region, "linked-ghg-policy", name="CO2_CDR")
        ET.SubElement(link, "price-adjust", fillout=str(region_link["price-adjust-fillout"]),
                      year=str(region_link["price-adjust-start-year"])).text = str(region_link["price-adjust"])
        ET.SubElement(link, "demand-adjust", fillout=str(region_link["demand-adjust-fillout"]),
                      year=str(region_link["demand-adjust-start-year"])).text = str(region_link["demand-adjust"])
        ET.SubElement(link, "market").text = str(region_link["market"])
        ET.SubElement(link, "linked-policy").text = str(region_link["linked-policy"])
        ET.SubElement(link, "price-unit").text = str(region_link["price-unit"])
        ET.SubElement(link, "output-unit").text = str(region_link["output-unit"])

    return scenario


def add_exo_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    for year, r in demand:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        CDR_final_demand = ET.SubElement(region, "CDR-final-demand", name="CDR")
        demand_source = ET.SubElement(CDR_final_demand, "demand-source", name="exogenous")
        ET.SubElement(demand_source, "demand", year=str(year)).text = str(demand[(year, r)]["demand"])

    return scenario


def add_elastic_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    return scenario


def add_offset_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    return scenario


def add_accumulated_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    return scenario


if __name__ == '__main__':
    config = utilities.build_from_scenario("exoTest")
    for j in config:
        build(j)
