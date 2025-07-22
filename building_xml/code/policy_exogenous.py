import xml.etree.cElementTree as ET
from xml.dom import minidom
import utilities


def build(input_filepath, output_filepath):
    data = utilities.open_csv(input_filepath, index=["region"])

    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")

    # region specific data
    for area in data:
        region = ET.SubElement(world, "region", name=str(area))
        CDR_final_demand = ET.SubElement(region, "CDR-final-demand", name="CDR")
        demand_source = ET.SubElement(CDR_final_demand, "demand-source", name="exogenous")

        # year specific data
        for year in area:
            ET.SubElement(demand_source, "demand", year="2025").text=str(year)

    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)


if __name__ == '__main__':
    build("./../inputs/test_exo.csv", "./../../gcam/input/policy/CDR/test_exo.xml")
