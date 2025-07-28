import utilities


def main(scenario_name):
    # get a list of files that need verification
    xml_files_to_build = utilities.build_from_scenario(scenario_name)
    files_to_verify = {}

    # TODO: may need to group certain types of files (i.e. CDR demand) together
    for file in xml_files_to_build:
        for key, value in file.data_files:
            if "verify" in str(value).lower():
                files_to_verify[key] = value

    # for each file to verify, open the original .csv file and extract relevant data
    for key, value in files_to_verify:
        if key == "exo_CDR_demand":
            pass
        if key == "elastic_CDR_demand":
            pass
        if key == "RES_markets":
            pass
        if key == "ghg_constraint":
            pass
        if key == "ghg_tax":
            pass
        # TODO: add more file types


    # TODO: for each file, run verification


if __name__ == '__main__':
    main("alteredTest_default")