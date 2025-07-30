import constants


class XMLConfig:
    def __init__(
            self,
            data_files,
            xml_build_type,
            output_fname,
            **kwargs):
        self.xml_build_type = xml_build_type
        self.data_files = data_files
        self.output_fname = output_fname

        # set output directory path
        if "policy" in str(xml_build_type).lower():
            self.output_dir = "./gcam/input/policy/"
            self.config_dir = "../input/policy/"
        else:
            self.output_dir = "./gcam/input/gcamdata/xml/"
            self.config_dir = "../input/gcamdata/xml/"

        # set relevant region information
        for key, value in kwargs:
            if key == "region":
                if value == "USA":
                    self.region = constants.GCAMConstants.USA_region
                elif value == "GCAM":
                    self.region = constants.GCAMConstants.GCAM_region
                else:
                    self.region = value


class XMLOutput:
    def __init__(self, build_file_type, filepath, descriptor):
        self.build_file_type = build_file_type
        self.filepath = filepath
        self.descriptor = descriptor

