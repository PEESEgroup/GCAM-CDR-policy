import constants


class XMLConfig:
    def __init__(
            self,
            data_files,
            xml_build_type,
            output_fname,
            region,
            **kwargs):
        self.xml_build_type = xml_build_type
        self.data_files = data_files
        self.output_fname = output_fname

        # set output directory path
        if "policy" in str(xml_build_type).lower():
            self.output_dir = "../input/policy/"
        else:
            self.output_dir = ""

        # set relevant region information
        if region == "USA":
            self.region = constants.GCAMConstants.USA_region,
        elif region == "GCAM":
            self.region = constants.GCAMConstants.GCAM_region
        else:
            self.region = region

        for key, value in kwargs:
            if key == "test":
                self.temp = ""

