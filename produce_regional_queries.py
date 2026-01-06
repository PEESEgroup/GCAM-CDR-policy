import constants as c
import xml.etree.cElementTree as ET
from xml.dom import minidom


def main():
    new_file = ""
    with (open("xml/to_regionalize.xml", "r") as f):
        entry = f.read()

        # get list of regions
        regions = []
        regions.extend(c.GCAMConstants.GCAM_region)
        regions.extend(c.GCAMConstants.USA_region)
        # regions.extend(c.GCAMConstants.grid_region)  # don't query the grids for anything

        # iterate through all regions
        for i in regions:
            new_region = entry
            new_region = new_region.replace("Global", str(i))
            new_file = new_file + new_region

        # remove instances of </queries><queries> and extra whitespace
        new_file = new_file.replace("\n</queries>\n<queries>\n", "\n").replace("\n", ""). replace("  ", "")

        # append to query list
        root = ET.fromstring(new_file)

        # read in the queries that are supposed to be global in scope
        with (open("xml/global_queries.xml", "r") as global_queries):
            queries = global_queries.read()
            queries = queries.replace("\n", ""). replace("  ", "")
            tree = ET.fromstring(queries)

            childNodeList = root.findall(".//aQuery")
            for node in childNodeList:
                tree.append(node)

            # write out file
            xmlstr = minidom.parseString(ET.tostring(tree, encoding="UTF-8", xml_declaration=True)).toprettyxml(
                indent="   ")

            with open("xml/query_list.xml", "w+") as f:
                f.write(xmlstr)


if __name__ == '__main__':
    main()