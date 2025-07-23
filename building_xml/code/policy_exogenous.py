import xml.etree.cElementTree as ET
from xml.dom import minidom
import utilities
import build_xml_config
import constants


def build(config):
    # unpack the config object
    input_filepath = config.data_files
    output_filepath = config.output_dir + config.output_fname

    # extract relevant data
    data = utilities.open_csv(input_filepath)
    linked_ghg_data = data["exo_linked_ghg"]
    demand = data["exo_demand"]

    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    # if this is the GCAM-USA region, delete USA supply sector
    if config.region == constants.GCAMConstants.USA_region:
        region = ET.SubElement(world, "region", name="USA")
        supply_sector = ET.SubElement(region, "supplysector", name="CDR_traded")
        ET.SubElement(supply_sector, "subsector", delete="1", name="CDR_USA")

    # region specific data
    counter = 0
    for area in config.region:
        region = ET.SubElement(world, "region", name=str(area))
        CDR_final_demand = ET.SubElement(region, "CDR-final-demand", name="CDR")
        demand_source = ET.SubElement(CDR_final_demand, "demand-source", name="exogenous")

        # year specific data - only needs to be entered once, unless it is state-specific
        if counter > 0:
            for year in demand:
                ET.SubElement(demand_source, "demand", year=year).text = str(data[year])

        # linked ghg policy
        link = ET.SubElement(region, "linked-ghg-policy", name="CO2_CDR")
        ET.SubElement(link, "price-adjust")

    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")


if __name__ == '__main__':
    config = utilities.build_from_scenario("exoTest")
    for j in config:
        build(j)
