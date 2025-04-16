# this file has been edited

# Copyright 2019 Battelle Memorial Institute; see the LICENSE file.

#' module_aglu_L181.ag_R_C_Y_GLU_irr_mgmt
#'
#' Calculates the economic yields, cropland cover and production by GCAM region / commodity / year / GLU / irrigation / mgmt level.
#'
#' @param command API command to execute
#' @param ... other optional parameters, depending on command
#' @return Depends on \code{command}: either a vector of required inputs,
#' a vector of output names, or (if \code{command} is "MAKE") all
#' the generated outputs: \code{L181.LC_bm2_R_C_Yh_GLU_irr_level}, \code{L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level}, \code{L181.ag_Prod_Mt_R_C_Y_GLU_irr_level}, \code{L181.YieldMult_R_bio_GLU_irr}, \code{L181.LandShare_R_bio_GLU_irr}. The corresponding file in the
#' original data system was \code{LB181.ag_R_C_Y_GLU_irr_mgmt.R} (aglu level1).
#' @details This chunk calculates the economic yields, cropland cover and production by GCAM region / commodity / year / GLU / irrigation / mgmt level.
#' Currently the yield multipliers by high and low yield management are set at the same value for all region / commodity / year / GLU / irrigation,
#' and the land share by high and low yield management is 50 percent by each. But this chunk is also a placeholder for a generic method of calculating specific
#' yield multipliers and land shares for each region / commodity / GLU / irrigation level.
#' @importFrom assertthat assert_that
#' @importFrom dplyr bind_rows filter left_join mutate select
#' @importFrom tidyr gather
#' @author RC May 2017
module_aglu_L181.ag_R_C_Y_GLU_irr_mgmt <- function(command, ...) {
  if(command == driver.DECLARE_INPUTS) {
    return(c(FILE = "common/GCAM_region_names",
             FILE = "aglu/A_agBiocharCropYieldIncrease",
             FILE = "aglu/A_recommended_nutrient_rates",
             FILE = "aglu/FAO/FAO_ag_items_PRODSTAT",
             "L142.ag_Fert_IO_R_C_Y_GLU_biochar",
             "L171.LC_bm2_R_rfdHarvCropLand_C_Yh_GLU",
             "L171.LC_bm2_R_irrHarvCropLand_C_Yh_GLU",
             "L171.ag_irrEcYield_kgm2_R_C_Y_GLU",
             "L171.ag_rfdEcYield_kgm2_R_C_Y_GLU"))
  } else if(command == driver.DECLARE_OUTPUTS) {
    return(c("L181.LC_bm2_R_C_Yh_GLU_irr_level",
             "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level",
             "L181.ag_Prod_Mt_R_C_Y_GLU_irr_level",
             "L181.YieldMult_R_bio_GLU_irr",
             "L181.LandShare_R_bio_GLU_irr",
             "L181.ag_kgbioha_R_C_Y_GLU_irr_level",
             "L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU"))
  } else if(command == driver.MAKE) {

    all_data <- list(...)[[1]]

    EcYield_kgm2_hi <- EcYield_kgm2_lo <- GCAM_commodity <- GCAM_region_ID <- GLU <-
      Irr_Rfd <- LC_bm2_hi <- LC_bm2_lo <- landshare_hi <- landshare_lo <- level <- value <-
      year <- yield <- yieldmult_hi <- yieldmult_lo <- GCAM_subsector <- NULL  # silence package check notes

    # Load required inputs
    L171.LC_bm2_R_rfdHarvCropLand_C_Yh_GLU <- get_data(all_data, "L171.LC_bm2_R_rfdHarvCropLand_C_Yh_GLU")
    L171.LC_bm2_R_irrHarvCropLand_C_Yh_GLU <- get_data(all_data, "L171.LC_bm2_R_irrHarvCropLand_C_Yh_GLU")
    L171.ag_irrEcYield_kgm2_R_C_Y_GLU <- get_data(all_data, "L171.ag_irrEcYield_kgm2_R_C_Y_GLU")
    L171.ag_rfdEcYield_kgm2_R_C_Y_GLU <- get_data(all_data, "L171.ag_rfdEcYield_kgm2_R_C_Y_GLU")
    A_agBiocharCropYieldIncrease <- get_data(all_data, "aglu/A_agBiocharCropYieldIncrease")
    A_recommended_nutrient_rates <- get_data(all_data, "aglu/A_recommended_nutrient_rates")
    FAO_ag_items_PRODSTAT <- get_data(all_data, "aglu/FAO/FAO_ag_items_PRODSTAT")
    L142.ag_Fert_IO_R_C_Y_GLU_biochar <- get_data(all_data, "L142.ag_Fert_IO_R_C_Y_GLU_biochar")
    GCAM_region_names <- get_data(all_data, "common/GCAM_region_names")

    # In order to calculate weighted yield levels for aggregation, we don't want to be using the raw yields, as our
    # GCAM commodities may include a blend of heterogeneous yielding commodities. For example, cucumber yields are in
    # excess of 400 tonnes/hectare in some places, whereas pulses tend to be about 2. In a non-indexed aggregation,
    # the cucumbers would be the only crop that matters for the final yields, and the yield of the "high" technology
    # would not be representative of a biophysically attainable yield for the commodity class as a whole.

    # Therefore, apply yield multipliers to the baseline historical economic yields.
    # Multipliers are applied to economic yields (kg/m2/yr, not kg/m2/harvest), and shares are applied to land areas.

    # First, calculate the new EcYields as the former yields times the yield mults, for high and low
    L171.ag_rfdEcYield_kgm2_R_C_Y_GLU %>%
      mutate(Irr_Rfd = "rfd") %>%
      # Combine rainfed and irrigated data
      bind_rows(mutate(L171.ag_irrEcYield_kgm2_R_C_Y_GLU, Irr_Rfd = "irr")) %>%
      filter(year %in% aglu.AGLU_HISTORICAL_YEARS) %>%
      # SET THE SAME YIELD MULTIPLIERS EVERYWHERE, 1 plus or minus an adj fraction.
      mutate(yieldmult_hi = 1 + aglu.MGMT_YIELD_ADJ, yieldmult_lo = 1 - aglu.MGMT_YIELD_ADJ, yieldmult_biochar = 1 + aglu.MGMT_YIELD_ADJ,
             # high and low yields are now calculated as the observed yield times the multipliers
             EcYield_kgm2_lo = value * yieldmult_lo, EcYield_kgm2_hi = value * yieldmult_hi, EcYield_kgm2_biochar = yieldmult_hi) %>% # assuming that biochar gets yield increases
      select(GCAM_region_ID, GCAM_commodity, GCAM_subsector, GLU, Irr_Rfd, year, EcYield_kgm2_hi, EcYield_kgm2_lo, EcYield_kgm2_biochar) %>%
      gather(level, value, -GCAM_region_ID, -GCAM_commodity, -GCAM_subsector, -GLU, -Irr_Rfd, -year) %>%
      mutate(level = sub("EcYield_kgm2_", "", level)) ->
      L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level

    #read in Marianna's data
    A_recommended_nutrient_rates %>%
      # map using FAO codes - find missing terms
      left_join(FAO_ag_items_PRODSTAT, by=c("FAO_crop_class_corresponding_to_the_number_code_in_SPAM_20161" = "item")) %>%
      group_by(GCAM_commodity) %>% # choose the median value for each class of crops
      # Calculate the median application for each class of crops
      summarise(Elemental_phosphorus_rate_in_kg_ha_recommended_by_IFA4 = median(Elemental_phosphorus_rate_in_kg_ha_recommended_by_IFA4, na.rm=TRUE),
                Elemental_potassium_rate_in_kg_ha_recommended_by_IFA4 = median(Elemental_potassium_rate_in_kg_ha_recommended_by_IFA4, na.rm=TRUE)) %>%
      ungroup() %>%
      drop_na %>%
      select(GCAM_commodity, Elemental_phosphorus_rate_in_kg_ha_recommended_by_IFA4, Elemental_potassium_rate_in_kg_ha_recommended_by_IFA4) ->
      L181.ag_FAOrecNutrientRates_kgha

    print(L181.ag_FAOrecNutrientRates_kgha)

    # map to regional yields
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      filter(level=="biochar", year == 2015) %>%
      #map new data to the existing yields
      left_join(L181.ag_FAOrecNutrientRates_kgha, by=c("GCAM_commodity")) %>%
      # calculate kg biochar/kg crop
      mutate(kg_K_kg_crop = Elemental_potassium_rate_in_kg_ha_recommended_by_IFA4/value/CONV_HA_M2, #[kg K/ha]/[kg crop/m2] = kg K/kg crop
             kg_P_kg_crop = Elemental_phosphorus_rate_in_kg_ha_recommended_by_IFA4/value/CONV_HA_M2) %>%
      select(-Elemental_potassium_rate_in_kg_ha_recommended_by_IFA4, -Elemental_phosphorus_rate_in_kg_ha_recommended_by_IFA4) ->
      L181.ag_recPK_IO_R_C_Y_CLU_irr_biochar

    # why is the number of rows in the table increasing?
    print(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
            filter(level=="biochar", year == 2015))
    print(L181.ag_recPK_IO_R_C_Y_CLU_irr_biochar)


    # calculate biochar yields
    K_K2O = 1.2046
    P_P2O5 = 2.2951

    # [kg K2O/kg K]*[kg K/ kg crop] / [kg K2O / kg biochar] = kg biochar/kg crop
    # kg/biochar/kg crop * kg K2O/kg biochar * kg K/kg K2O = kg K/kg crop
    L181.ag_recPK_IO_R_C_Y_CLU_irr_biochar %>%
      left_join(L142.ag_Fert_IO_R_C_Y_GLU_biochar, by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "year")) %>%
      mutate(kg_biochar_kg_crop_K_limit = K_K2O*kg_K_kg_crop/rep_K2O,# above dimensional analysis
             kg_biochar_kg_crop_P_limit = P_P2O5*kg_P_kg_crop/rep_P2O5, # above dimensional analysis
             kg_biochar_kg_crop_limited_recommended = pmin(kg_biochar_kg_crop_K_limit, kg_biochar_kg_crop_P_limit),# choose whatever nutrient limits first
             kg_biochar_kg_crop = pmax(kg_biochar_kg_crop_limited_recommended, kg_biochar_kg_crop_limited), # choose the higher number between the recommended and the actual
             kg_P_kg_crop_biochar_limited = kg_biochar_kg_crop * rep_P2O5/P_P2O5) %>% # convert recommended biochar amount back to P amount
      select(GCAM_region_ID, GCAM_commodity, GCAM_subsector, GLU, kg_biochar_kg_crop, kg_P_kg_crop_biochar_limited) %>% distinct() ->
      L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU

    #calculate biochar application rates - this is calculated before the yield increases induced by biochar
    # kg crop/m2 * kg biochar/kg crop * m2/ha = kg biochar/ha
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      filter(level=="biochar", year == 2015) %>%
      left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")) %>%
      mutate(AgSupplySector = GCAM_commodity) %>%
      left_join(L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU, by = c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU")) %>%
      mutate(kg_bio_ha = value*kg_biochar_kg_crop*CONV_HA_M2,
             kg_P_ha = value*kg_P_kg_crop_biochar_limited*CONV_HA_M2) %>%
      replace_na(list(kg_bio_ha = 0)) %>%
      select(region, GCAM_region_ID, GCAM_commodity, GCAM_subsector, GLU, Irr_Rfd, kg_bio_ha, kg_P_ha)->
      L181.ag_kgbioha_R_C_Y_GLU_irr_level

    print(L181.ag_kgbioha_R_C_Y_GLU_irr_level)

    L181.ag_kgbioha_R_C_Y_GLU_irr_level %>%
      write.csv('./inst/extdata/aglu/A_ag_kgbioha_R_C_Y_GLU_irr_level_yield_various.csv')

    L181.ag_kgbioha_R_C_Y_GLU_irr_level %>% select(-kg_P_ha) -> L181.ag_kgbioha_R_C_Y_GLU_irr_level

    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% filter(level!="biochar") ->
      L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_lohi

    # biochar land regions should not exist if 0 biochar is applied to them
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      filter(level=="biochar") %>%
      left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")) %>%
      mutate(AgSupplySector = GCAM_commodity) %>%
      left_join(L181.ag_kgbioha_R_C_Y_GLU_irr_level, by = c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "Irr_Rfd", "region")) %>%
      drop_na() %>% filter(kg_bio_ha > 0) %>% # keep only land use types where non-zero biochar is applied to land
      left_join_error_no_match(A_agBiocharCropYieldIncrease, by=c("GCAM_commodity" ="AgSupplySector"))%>% # copy in yield increase data
      # this adds yield increases only to biochar lands with greater than 1t/ha or 1000kg/ha, due to the number of land types with near 0 application rates
      # to be clear, those lands gain the other agronomic benefits
      mutate(value = if_else(kg_bio_ha > aglu.BIOCHAR_LOWER_APP_RATE, value*Yield.Increase, value)) %>%
      select(-region, -AgSupplySector, -kg_bio_ha, -Yield.Increase) -> L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_biochar # include yield increases

    print(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_biochar %>% filter(GCAM_subsector == "MiscCropTree", year == 2015, level=="biochar"), n=20) # this should be half the length of the other table
    print(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_lohi)

    bind_rows(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_biochar, L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_lohi) -> L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level

    # Second, apply land shares to disaggregate low- and high-input land
     L171.LC_bm2_R_rfdHarvCropLand_C_Yh_GLU %>%
      mutate(Irr_Rfd = "rfd") %>%
      # Combine rainfed and irrigated data
      bind_rows(mutate(L171.LC_bm2_R_irrHarvCropLand_C_Yh_GLU, Irr_Rfd = "irr")) %>%
      filter(year %in% aglu.LAND_COVER_YEARS) %>%
      # SET THE SAME YIELD MULTIPLIERS EVERYWHERE, 1 plus or minus an adj fraction.
      mutate(yieldmult_hi = 1 + aglu.MGMT_YIELD_ADJ, yieldmult_lo = 1 - aglu.MGMT_YIELD_ADJ,
             # Calculate the land shares to allocate to low, and high is the rest (currently the shares are set at 0.5/0.5 to all)
             landshare_lo = (1 - yieldmult_hi) / (yieldmult_lo - yieldmult_hi), landshare_hi = 1 - landshare_lo,
             # low- and high-input land are calculated as the total times the shares
             LC_bm2_lo = value * landshare_lo, LC_bm2_hi = value * landshare_hi, LC_bm2_biochar=value * landshare_hi) %>% # update biochar land shares here (currently 0.5)
      select(GCAM_region_ID, GCAM_commodity, GCAM_subsector, GLU, Irr_Rfd, year, LC_bm2_hi, LC_bm2_lo, LC_bm2_biochar) %>%
      gather(level, value, -GCAM_region_ID, -GCAM_commodity, -GCAM_subsector, -GLU, -Irr_Rfd, -year) %>%
      mutate(level = sub("LC_bm2_", "", level)) -> # value here is the yield, which we don't want to set to 0
      L181.LC_bm2_R_C_Yh_GLU_irr_level

     print(L181.LC_bm2_R_C_Yh_GLU_irr_level)

    # ensure that other land data contains biochar land areas which have non-zero biochar demand
     L181.LC_bm2_R_C_Yh_GLU_irr_level %>%
       filter(level == "biochar") %>% # get biochar data
       left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level, by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "Irr_Rfd", "year", "level")) %>% # if there isn't biochar land use, don't include as empty node
       drop_na() %>% # remove land leafs without valid biochar application
       mutate(value = value.x) %>% # rename rows for rowbind
       select(-value.x, -value.y) %>%
       bind_rows(L181.LC_bm2_R_C_Yh_GLU_irr_level %>% filter(level != "biochar")) -> L181.LC_bm2_R_C_Yh_GLU_irr_level
    print(L181.LC_bm2_R_C_Yh_GLU_irr_level)

    # Third, calculate production: economic yield times land area
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      rename(yield = value) %>%
      left_join_error_no_match(L181.LC_bm2_R_C_Yh_GLU_irr_level,
                               by = c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector",
                                      "GLU", "Irr_Rfd", "year", "level")) %>%
      # apply land area rounding (and cutoff) for production consistency
      mutate(value = round(value, digits = aglu.DIGITS_LAND_USE) * yield) %>%
      select(-yield) ->
      L181.ag_Prod_Mt_R_C_Y_GLU_irr_level

    # Calculate bioenergy yield levels
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      # Only where production (and harvested area) is non-zero
      filter(value > 0) %>%
      select(GCAM_region_ID, GLU, Irr_Rfd) %>%
      unique() %>%
      # SET THE SAME YIELD MULTIPLIERS EVERYWHERE
      # give biochar the benefit of high yield
      mutate(yieldmult_hi = 1 + aglu.MGMT_YIELD_ADJ, yieldmult_lo = 1 - aglu.MGMT_YIELD_ADJ) ->
      L181.YieldMult_R_bio_GLU_irr

    print(L181.YieldMult_R_bio_GLU_irr)

    # Calculate bioenergy land shares
    L181.LC_bm2_R_C_Yh_GLU_irr_level %>%
      filter(value > 0) %>%
      select(GCAM_region_ID, GLU, Irr_Rfd) %>%
      unique() %>%
      # SET THE SAME LADN SHARE, even including biochar
      mutate(landshare_lo = 0.5, landshare_hi = 0.5) ->
      L181.LandShare_R_bio_GLU_irr

    print(L181.LandShare_R_bio_GLU_irr)

    # Produce outputs
    L181.LC_bm2_R_C_Yh_GLU_irr_level %>%
      add_title("Cropland cover by GCAM region / commodity / year / GLU / irrigation / mgmt level") %>%
      add_units("bm2") %>%
      add_comments("Cropland cover by high and low management levels are currently set at the share of 50% by each.") %>%
      add_legacy_name("L181.LC_bm2_R_C_Yh_GLU_irr_level") %>%
      add_precursors("L171.LC_bm2_R_rfdHarvCropLand_C_Yh_GLU",
                     "L171.LC_bm2_R_irrHarvCropLand_C_Yh_GLU") ->
      L181.LC_bm2_R_C_Yh_GLU_irr_level

    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>%
      add_title("Economic yield by GCAM region / commodity / year / GLU / irrigation / mgmt level") %>%
      add_units("kg/bm2") %>%
      add_comments("Economic yields are calculated as the observed yields times a mutiplier for high or low mgmt level.") %>%
      add_comments("Currently the same yield mutipliers are set for all region/commodity/GLU/irrigation.") %>%
      add_legacy_name("L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level") %>%
      add_precursors("L171.ag_irrEcYield_kgm2_R_C_Y_GLU",
                     "L171.ag_rfdEcYield_kgm2_R_C_Y_GLU",
                     "aglu/A_agBiocharCropYieldIncrease",
                     "L142.ag_Fert_IO_R_C_Y_GLU_biochar") ->
      L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level

    L181.ag_Prod_Mt_R_C_Y_GLU_irr_level %>%
      add_title("Agricultural production by GCAM region / commodity / year / GLU / irrigation / mgmt level") %>%
      add_units("Mt") %>%
      add_comments("Agricultural production are calculated as the economic yield times cropland cover.") %>%
      add_legacy_name("L181.ag_Prod_Mt_R_C_Y_GLU_irr_level") %>%
      add_precursors()  ->
      L181.ag_Prod_Mt_R_C_Y_GLU_irr_level

    L181.YieldMult_R_bio_GLU_irr %>%
      add_title("Yield multipliers for bioenergy by region / GLU / irrigation / mgmt level") %>%
      add_units("Unitless") %>%
      add_comments("Yield mutipliers for bioenergy high and low management level are set at the same values for all region/commodity/GLU/irrigation.") %>%
      add_legacy_name("L181.YieldMult_R_bio_GLU_irr") %>%
      add_precursors() ->
      L181.YieldMult_R_bio_GLU_irr

    L181.LandShare_R_bio_GLU_irr %>%
      add_title("Ghost land shares for bioenergy by region / GLU / irrigation / mgmt level") %>%
      add_units("Unitless") %>%
      add_comments("Ghost land shares for bioenergy by high and low management levels are currently set at the share of 50% by each.") %>%
      add_legacy_name("L181.LandShare_R_bio_GLU_irr") %>%
      add_precursors() ->
      L181.LandShare_R_bio_GLU_irr

    L181.ag_kgbioha_R_C_Y_GLU_irr_level %>%
      add_title("application rates for biochar by region / GLU / irrigation / mgmt level") %>%
      add_units("kg/ha") %>%
      add_legacy_name("L181.ag_kgbioha_R_C_Y_GLU_irr_level") %>%
      add_precursors("L142.ag_Fert_IO_R_C_Y_GLU_biochar") ->
      L181.ag_kgbioha_R_C_Y_GLU_irr_level

    L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU %>%
      add_title("application rates for biochar by region / GLU / irrigation / mgmt level") %>%
      add_units("kg/ha") %>%
      add_legacy_name("L181.ag_kgbioha_R_C_Y_GLU_irr_level") %>%
      add_precursors("L142.ag_Fert_IO_R_C_Y_GLU_biochar") ->
      L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU


    return_data(L181.LC_bm2_R_C_Yh_GLU_irr_level, L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level, L181.ag_Prod_Mt_R_C_Y_GLU_irr_level, L181.YieldMult_R_bio_GLU_irr, L181.LandShare_R_bio_GLU_irr, L181.ag_kgbioha_R_C_Y_GLU_irr_level, L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU)
  } else {
    stop("Unknown command")
  }
}
