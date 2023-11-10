import read_GCAM_DB
import process_GCAM_data
import process_world_map

if __name__ == '__main__':
    #TODO: double check constants.py before running this code to ensure correct file placement and contents
    read_GCAM_DB.main()
    process_GCAM_data.main()
    process_world_map.main()
