import constants as c

new_file = ""
with open("xml/global_queries.xml", "r") as f:
    entry = f.read()
    print(entry)

    for i in c.GCAMConstants.GCAM_region:
        new_region = entry
        new_region = new_region.replace("Global", str(i))
        new_file = new_file + new_region

    with open("xml/regional_queries.xml", "w") as f2:
        f2.write(new_file)
