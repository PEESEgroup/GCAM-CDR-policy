import utilities
import minidom
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
    scenario = build_tech(tech)
    scenario = build_countersubsidy(countersubsidy)

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
                "descriptor": "cdr_demand_usa"}

def build_RES(file):
    pass

def build_tech(file):
    pass

def build_countersubsidy(file):
    pass