import xml.etree.cElementTree as ET
from xml.dom import minidom
import utilities


def build(config, baseline=True):
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    exo_demand = ""
    elastic_demand = ""
    offset_demand = ""
    acc_demand = ""

    # extract relevant data
    data = utilities.open_csv(input_filepath)
    linked_ghg_data = data["linked_ghg_markets"]

    if "exo_CDR_demand_verify" in data:
        exo_demand = data["exo_CDR_demand_verify"]
    if "elastic_CDR_demand_verify" in data:
        elastic_demand = data["elastic_CDR_demand_verify"]
    # TODO: add config files for these types of demand
    if "offset_demand" in data:
        offset_demand = data["offset_CDR_demand_verify"]
    if "acc_demand" in data:
        acc_demand = data["acc_CDR_demand_verify"]

    # TODO: combine multiple sources of exogenous demand

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
                "descriptor": "CDR-Demand-Policy"}
    else:
        return {"build_file_type": "altered",
                "filepath": config.config_dir + config.output_fname,
                "descriptor": "cdr_demand_usa"}


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
        policy = str(region_link["linked-policy"]).split(";")
        for p in policy:
            ET.SubElement(link, "linked-policy").text = str(p)
        ET.SubElement(link, "price-unit").text = str(region_link["price-unit"])
        ET.SubElement(link, "output-unit").text = str(region_link["output-unit"])

    return scenario


def add_exo_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    counter = 0
    for year, r in demand:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        CDR_final_demand = ET.Element("CDR-final-demand", name="CDR")
        region.insert(counter, CDR_final_demand)
        demand_source = ET.SubElement(CDR_final_demand, "demand-source", name=str(demand[(year, r)]["name"]))
        ET.SubElement(demand_source, "demand", year=str(year)).text = str(demand[(year, r)]["demand"])
        counter += 1

    return scenario


def add_elastic_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    for r in demand:
        # find region from scenario that matches the region name
        region = scenario.find(".//region[@name='" + r + "']")
        CDR_final_demand = ET.Element("CDR-final-demand", name="CDR")
        region.insert(0, CDR_final_demand)
        demand_source = ET.SubElement(CDR_final_demand, "elastic-demand-source", name="elastic")
        ET.SubElement(demand_source, "max-demand").text = str(demand[r]["max-demand"])
        ET.SubElement(demand_source, "steepness").text = str(demand[r]["steepness"])
        ET.SubElement(demand_source, "midpoint").text = str(demand[r]["midpoint"])
        ET.SubElement(demand_source, "min-price").text = str(demand[r]["min-price"])

    return scenario


def add_offset_demand(scenario, demand):
    # if there is no demand of this type to add, don't add it
    if demand == "":
        return scenario

    for r, year in demand:
        region = scenario.find(".//region[@name='" + r + "']")
        CDR_final_demand = ET.Element("CDR-final-demand", name="CDR")
        region.insert(0, CDR_final_demand)
        demand_source = ET.SubElement(CDR_final_demand, "offset-demand-source", name="offset")
        ET.SubElement(demand_source, "offset-fraction", year=str(demand[(r, year)])).text = str(demand[(r, year)]["offset-fraction"])
        ET.SubElement(demand_source, "market-name").text = str(demand[(r, year)]["market-name"])
        ET.SubElement(demand_source, "max-offset").text = str(demand[(r, year)]["max-offset"])

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
