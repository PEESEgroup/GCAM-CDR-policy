import build_xml_config
import constants
import utilities
from xml.dom import minidom
import xml.etree.cElementTree as ET


def build_tech_costs(config, baseline=True):
    """
    build the tech cost policy configuration file from .csv files
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
    scenario = build_non_input_tech_costs(data, output_filepath)

    # write file out
    xmlstr = minidom.parseString(ET.tostring(scenario, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open(output_filepath, "w+") as f:
        f.write(xmlstr)
    print("wrote file")

    # return dict of output files created -see constants for example
    if baseline:
        return build_xml_config.XMLOutput("baseline", config.config_dir + config.output_fname, "CDR_tech_non-input_costs")
    else:
        return build_xml_config.XMLOutput("altered", config.config_dir + config.output_fname, "CDR_tech_non-input_costs")


def build_non_input_tech_costs(file, output_fpath):
    """
    add the non-input tech costs to a xml file from scenario files
    :param file: file containing parameters for the tech costs
    :return: root node of the xml file
    """
    # merge dataframes
    links = {}
    costs = {}
    cost_decrease = []
    for key, value in file.items():
        if "link" in key:
            links = file[key]
        if "verify" in key:
            costs = file[key]
        if "Cost Decrease" in key:
            cost_decrease = file[key]

    # high level
    scenario = ET.Element("scenario")
    world = ET.SubElement(scenario, "world")
    gtb = ET.SubElement(world, "global-technology-database")

    for sector, subsector, tech in links:
        location = ET.SubElement(gtb, "location-info", {"sector-name": sector, "subsector-name": subsector})
        technology = ET.SubElement(location, "technology", name=tech)
        for year in costs:
            # get cost reduction
            reduced_cost = 1
            DAC_reduced_cost = 1
            nonDAC_reduced_cost = 1
            counter = 0
            for i in cost_decrease:
                if year in [2025, 2030, 2035, 2040, 2045, 2050]:
                    if "DACHubs" in output_fpath:
                        if "DAC" in tech:
                            DAC_reduced_cost = DAC_reduced_cost * (1-i[year]['reduction']) # DAC gets both cost decreases
                            print(f"{year} DAC reduced_cost: {DAC_reduced_cost}")
                        else:
                            # non-DAC gets only the first cost decrease, which is hard coded and derives from 45Q
                            if counter < 1:
                                nonDAC_reduced_cost = nonDAC_reduced_cost*(1 - i[year]['reduction'])
                                print(f"{year} non DAC reduced cost: {nonDAC_reduced_cost}")
                    else:
                        reduced_cost = reduced_cost * (1-i[year]['reduction'])
                        #print(f"{year} reduced_cost: {reduced_cost}")
                counter = counter + 1

            # add cost decrease to xml
            period = ET.SubElement(technology, "period", year=str(year))
            minicam = ET.SubElement(period, "minicam-non-energy-input", name="non-energy")
            if "DACHubs" in output_fpath:
                # if this is DAC hubs, then only cost reductions if tech is DAC
                if "DAC" in tech:
                    ET.SubElement(minicam, "input-cost").text = str(costs[year][tech] * DAC_reduced_cost * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC)
                else:
                    ET.SubElement(minicam, "input-cost").text = str(
                        costs[year][tech] * nonDAC_reduced_cost * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC)
            else:
                ET.SubElement(minicam, "input-cost").text = str(
                    costs[year][tech] * reduced_cost * constants.GCAMConstants.USD2025_tCO2_to_1975_kgC)

    return scenario
