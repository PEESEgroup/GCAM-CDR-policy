import constants


def main(config_name):
    # deconstruct scenario and baseline information
    split = config_name.split("_")
    scenario_name = split[0]
    baseline_name = split[1]

    # get list of original and altered scenario files
    verification_files = []
    scenario_files = constants.GCAMConstants.scenario_names[scenario_name]
    verification_files.extend(scenario_files["original"])
    for entry in scenario_files["altered"]:
        verification_files.append(entry["altered"])

    # TODO: for each file, run verification


if __name__ == '__main__':
    main("alteredTest_default")