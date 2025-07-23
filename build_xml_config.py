import constants


class XMLConfig:
    def __init__(
            self,
            data_files,
            xml_build_type,
            USA_regions=constants.GCAMConstants.USA_region,
            GCAM_regions=constants.GCAMConstants.GCAM_region):
        self.xml_build_type = xml_build_type
        self.data_files = data_files
        self.USA_regions = USA_regions
        self.GCAM_regions = GCAM_regions

