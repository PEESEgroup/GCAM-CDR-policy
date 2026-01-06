import process_GCAM_data
import read_GCAM_DB
import verification

for config_fname in ["nzn_nzn", "nothing_nothing", "low_low", "high_high", "excess_excess", "4gt_4gt",
                     "s1-procureScaling-n_nothing", "s1-procure3B-n_nothing", "s1-procureRhodium-n_nothing",
                     "s1-procureScaling-l_low", "s1-procure3B-l_low", "s1-procureRhodium-l_low",
                     "s1-procureScaling-h_high", "s1-procure3B-h_high", "s1-procureRhodium-h_high",
                     "45Q-2040_low", "45Q-2050_low", "CDRIA-2035_low", "CDRIA-2050_low",
                     "45Q-2040_high", "45Q-2050_high", "CDRIA-2035_high", "CDRIA-2050_high",
                     "innovation-DACHubs_low", "innovation-maintain_low", "innovation-rhodium6b_low",
                     "innovation-rhodium18b_low", "innovation-triple_low",
                     "innovation-DACHubs_high", "innovation-maintain_high", "innovation-rhodium6b_high",
                     "innovation-rhodium18b_high", "innovation-triple_high", "CDRIA-rhodium18b_low",
                     "CDRIA-rhodium18b_high"]:
    read_GCAM_DB.main(config_fname)
    process_GCAM_data.main(config_fname)
    verification.main(config_fname)
