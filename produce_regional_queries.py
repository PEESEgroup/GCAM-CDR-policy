import constants as c
import xml.etree.cElementTree as ET
from xml.dom import minidom

new_file = ""
with open("xml/to_regionalize.xml", "r") as f:
    entry = f.read()
    print(entry)

    for i in c.GCAMConstants.GCAM_region.extend(c.GCAMConstants.USA_region).extend(c.GCAMConstants.grid_region):
        new_region = entry
        new_region = new_region.replace("Global", str(i))
        new_file = new_file + new_region

    # append to query list
    root = ET.fromstring(new_file)

    # read in the queries that are supposed to be global in
    tree = ET.parse('/xml/global_queries.xml')
    tree = tree.getroot()
    childNodeList = root.findall(".//aQuery")
    for node in childNodeList:
        tree.append(node)

    # write out file
    xmlstr = minidom.parseString(ET.tostring(tree, encoding="UTF-8", xml_declaration=True)).toprettyxml(
        indent="   ")
    with open("xml/query_list.xml", "w+") as f:
        f.write(xmlstr)
