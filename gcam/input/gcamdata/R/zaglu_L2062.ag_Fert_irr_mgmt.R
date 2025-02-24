# this file has been edited

# Copyright 2019 Battelle Memorial Institute; see the LICENSE file.

#' module_aglu_L2062.ag_Fert_irr_mgmt
#'
#' Specifies fertilizer coefficients for all technologies; adjusts nonLandVariableCost to remove fertilizer cost.
#'
#' @param command API command to execute
#' @param ... other optional parameters, depending on command
#' @return Depends on \code{command}: either a vector of required inputs,
#' a vector of output names, or (if \code{command} is "MAKE") all
#' the generated outputs: \code{L2062.AgCoef_Fert_ag_irr_mgmt}, \code{L2062.AgCoef_Fert_bio_irr_mgmt}, \code{L2062.AgCost_ag_irr_mgmt_adj}, \code{L2062.AgCost_bio_irr_mgmt_adj}. The corresponding file in the
#' original data system was \code{L2062.ag_Fert_irr_mgmt.R} (aglu level2).
#' @details This chunk maps the fertilizer coefficients calculated in LB142 to all agricultural technologies.
#' We assume coefficients (in kgN per kgCrop) are equal for all four technologies (irr v rfd; hi v lo).
#' Adjust nonLandVariableCost to remove the now explicitly computed fertilizer cost.
#' @importFrom assertthat assert_that
#' @importFrom dplyr bind_rows filter if_else left_join mutate select
#' @importFrom tidyr replace_na
#' @importFrom tibble tibble
#' @author KVC June 2017
module_aglu_L2062.ag_Fert_irr_mgmt <- function(command, ...) {

  MODULE_INPUTS <-
    c(FILE = "aglu/FAO/FAO_ag_items_PRODSTAT",
      FILE = "common/iso_GCAM_regID",
      FILE = "aglu/AGLU_ctry",
      FILE = "common/GCAM_region_names",
       FILE = "water/basin_to_country_mapping",
       FILE = "aglu/A_Fodderbio_chars",
       "L142.ag_Fert_IO_R_C_Y_GLU",
      "L142.ag_Fert_IO_R_C_Y_GLU_K2O",
      "L142.ag_Fert_IO_R_C_Y_GLU_P2O5",
      "L142.ag_Fert_IO_R_C_Y_GLU_biochar",
       "L2052.AgCost_ag_irr_mgmt",
       "L2052.AgCost_bio_irr_mgmt",
       "L171.ag_rfdEcYield_kgm2_R_C_Y_GLU",
      "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level",
      "L181.ag_kgbioha_R_C_Y_GLU_irr_level",
      "L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU")

  MODULE_OUTPUTS <-
    c("L2062.AgCoef_Fert_ag_irr_mgmt",
      "L2062.AgCoef_Fert_bio_irr_mgmt",
      "L2062.AgCost_ag_irr_mgmt_adj",
      "L2062.AgCost_bio_irr_mgmt_adj")

  if(command == driver.DECLARE_INPUTS) {
    return(MODULE_INPUTS)
  } else if(command == driver.DECLARE_OUTPUTS) {
    return(MODULE_OUTPUTS)
  } else if(command == driver.MAKE) {

    all_data <- list(...)[[1]]

    year <- value <- GCAM_region_ID <- GCAM_commodity <- GLU <- GLU_name <- IRR_RFD <-
      MGMT <- region <- AgSupplySector <- AgSupplySubsector <- AgProductionTechnology <-
      minicam.energy.input <- coefficient <- WaterContent <- nonLandVariableCost <-
      FertCost <- GCAM_subsector <- NULL  # silence package check notes

    # Load required inputs ----
    get_data_list(all_data, MODULE_INPUTS, strip_attributes = TRUE)


    # Process Fertilizer Coefficients: Copy coefficients to all four technologies (irr/rfd + hi/lo)
    L142.ag_Fert_IO_R_C_Y_GLU %>%
      filter(year %in% MODEL_BASE_YEARS) %>%
      left_join_error_no_match(GCAM_region_names, by = "GCAM_region_ID") %>%
      left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%

      # Copy coefficients to all four technologies
      repeat_add_columns(tibble(IRR_RFD = c("IRR", "RFD"))) %>%
      repeat_add_columns(tibble(MGMT = c("hi", "lo", "biochar"))) -> L2062.ag_Fert_MGMT

    L2062.ag_Fert_MGMT%>% filter(MGMT == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% mutate(IRR_RFD = toupper(Irr_Rfd)),
                  by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "year", "MGMT"="level", "IRR_RFD")) %>%
      dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      mutate(value = value.x) %>%
      select(-Irr_Rfd, -value.y, -value.x) %>%
      bind_rows(L2062.ag_Fert_MGMT %>%
                  filter(MGMT != "biochar")) ->L2062.ag_Fert_MGMT # at this point, L2062.ag_Fert_MGMT should have only biochar regions for which biochar can be applied

    L2062.ag_Fert_MGMT%>%
      mutate(minicam.energy.input = "N fertilizer") -> # Add name of minicam.energy.input
      L2062.ag_Fert_MGMT # units still in kg N/kg crop



    # same calcs for K2O
    L142.ag_Fert_IO_R_C_Y_GLU_K2O %>%
      filter(year %in% MODEL_BASE_YEARS) %>%
      left_join_error_no_match(GCAM_region_names, by = "GCAM_region_ID") %>%
      left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%

      # Copy coefficients to all four technologies
      repeat_add_columns(tibble(IRR_RFD = c("IRR", "RFD"))) %>%
      repeat_add_columns(tibble(MGMT = c("hi", "lo", "biochar"))) -> L2062.ag_Fert_MGMT_K2O

    L2062.ag_Fert_MGMT_K2O%>% filter(MGMT == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% mutate(IRR_RFD = toupper(Irr_Rfd)),
                by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "year", "MGMT"="level", "IRR_RFD")) %>%
      dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      mutate(value = value.x) %>%
      select(-Irr_Rfd, -value.y, -value.x) %>%
      bind_rows(L2062.ag_Fert_MGMT_K2O %>%
                  filter(MGMT != "biochar")) ->L2062.ag_Fert_MGMT_K2O

    L2062.ag_Fert_MGMT_K2O%>%
      mutate(minicam.energy.input = "K2O fertilizer") -> L2062.ag_Fert_MGMT_K2O



    # same calcs for P2O5
    L142.ag_Fert_IO_R_C_Y_GLU_P2O5 %>%
      filter(year %in% MODEL_BASE_YEARS) %>%
      left_join_error_no_match(GCAM_region_names, by = "GCAM_region_ID") %>%
      left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%

      # Copy coefficients to all four technologies
      repeat_add_columns(tibble(IRR_RFD = c("IRR", "RFD"))) %>%
      repeat_add_columns(tibble(MGMT = c("hi", "lo", "biochar"))) -> L2062.ag_Fert_MGMT_P2O5

    L2062.ag_Fert_MGMT_P2O5%>% filter(MGMT == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% mutate(IRR_RFD = toupper(Irr_Rfd)),
                by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "year", "MGMT"="level", "IRR_RFD")) %>%
      dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      mutate(value = value.x) %>%
      select(-Irr_Rfd, -value.y, -value.x) %>%
      bind_rows(L2062.ag_Fert_MGMT_P2O5 %>%
                  filter(MGMT != "biochar")) ->L2062.ag_Fert_MGMT_P2O5

    L2062.ag_Fert_MGMT_P2O5%>%
      mutate(minicam.energy.input = "P2O5 fertilizer") -> L2062.ag_Fert_MGMT_P2O5

    print(L142.ag_Fert_IO_R_C_Y_GLU_biochar %>% filter(kg_biochar_kg_crop_limited == 0))
    print(L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU)

    # same calcs for biochar application rate
    L142.ag_Fert_IO_R_C_Y_GLU_biochar %>%
      filter(year %in% MODEL_BASE_YEARS) %>%
      select(-kg_biochar_kg_crop_limited) %>% # remove wrong application rates
      left_join(L181.ag_C_GLU_kgbiochar_kgcrop_R_C_Y_GLU, by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU")) %>% # merge in correct application rates
      drop_na() %>% #drop regions without biochar application
      left_join_error_no_match(GCAM_region_names, by = "GCAM_region_ID") %>%
      left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%
      # Copy coefficients to all four technologies
      repeat_add_columns(tibble(IRR_RFD = c("IRR", "RFD"))) %>%
      repeat_add_columns(tibble(MGMT = c("biochar"))) -> L2062.ag_Fert_MGMT_biochar

    print(L2062.ag_Fert_MGMT_biochar)
    print(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level)
    L2062.ag_Fert_MGMT_biochar%>% filter(MGMT == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% mutate(IRR_RFD = toupper(Irr_Rfd)),
                by=c("GCAM_region_ID", "GCAM_commodity", "GCAM_subsector", "GLU", "year", "MGMT"="level", "IRR_RFD")) %>%
      dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      select(-Irr_Rfd, -value) %>%
      mutate(minicam.energy.input = "biochar") ->
      L2062.ag_Fert_MGMT_biochar


    # because these fert inputs lower fixed costs by the amount of fertilizer applied
    # delay the reduction in N fert inputs due to higher N use efficiency until after
    # the variables costs have been calculated
    L2062.ag_Fert_MGMT%>% #combine fert and biochar demands
      # Add sector, subsector, technology names
      mutate(AgSupplySector = GCAM_commodity,
             AgSupplySubsector = paste(GCAM_subsector, GLU_name, sep = aglu.CROP_GLU_DELIMITER),
             AgProductionTechnology = paste(paste(AgSupplySubsector, IRR_RFD, sep = aglu.IRR_DELIMITER),
                                            MGMT, sep = aglu.MGMT_DELIMITER)) %>%
      rename(coefficient = value) %>% #remove inclusion of minicam energy input here because it was added earlier
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, minicam.energy.input, year, coefficient) ->
      L2062.AgCoef_Fert_ag_irr_mgmt

    # same calcs for biochar
    L2062.ag_Fert_MGMT_biochar %>%
      mutate(AgSupplySector = GCAM_commodity,
             AgSupplySubsector = paste(GCAM_subsector, GLU_name, sep = aglu.CROP_GLU_DELIMITER),
             AgProductionTechnology = paste(paste(AgSupplySubsector, IRR_RFD, sep = aglu.IRR_DELIMITER),
                                            MGMT, sep = aglu.MGMT_DELIMITER)) %>%
      rename(coefficient = kg_biochar_kg_crop) %>% # copy over biochar coefficient
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, minicam.energy.input, year, coefficient) ->
      L2062.AgCoef_biochar_ag_irr_mgmt

    # merge biochar and N fertilizer inputs together
    bind_rows(L2062.AgCoef_Fert_ag_irr_mgmt, L2062.AgCoef_biochar_ag_irr_mgmt) -> L2062.AgCoef_Fert_ag_irr_mgmt

    print(L2062.AgCoef_Fert_ag_irr_mgmt %>%
            filter(grepl("biochar", AgProductionTechnology)) %>%
            left_join(L2062.AgCoef_biochar_ag_irr_mgmt, by=c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
            filter(if_any(everything(), is.na)) %>%
            filter(year==2015), n=100) # biochar should be demanded in all time periods after 2015
    print(L2062.AgCoef_Fert_ag_irr_mgmt %>%
            filter(grepl("biochar", AgProductionTechnology)) %>%
            left_join(L2062.AgCoef_biochar_ag_irr_mgmt, by=c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
            filter(coefficient.y == 0, coefficient.x > 0) %>% # check for 0 biochar application rates in some regions where N fertilizer is also applied
            filter(year==2015), n=100) # biochar should be demanded in all time periods after 2015

    # Copy final base year coefficients to all future years, bind with historic coefficients, then remove zeroes
    # Note: this assumes constant fertilizer coefficients in the future ----
    L2062.AgCoef_Fert_ag_irr_mgmt %>%
      filter(year == max(MODEL_BASE_YEARS)) %>%
      select(-year) %>% # might need to put biochar inputs in past years. currently starts in 2015
      repeat_add_columns(tibble(year = MODEL_FUTURE_YEARS)) %>%
      bind_rows(L2062.AgCoef_Fert_ag_irr_mgmt) %>%
      filter(coefficient > 0) ->
      L2062.AgCoef_Fert_ag_irr_mgmt



    L2062.ag_Fert_MGMT_K2O%>% #combine fert and biochar demands
      # Add sector, subsector, technology names
      mutate(AgSupplySector = GCAM_commodity,
             AgSupplySubsector = paste(GCAM_subsector, GLU_name, sep = aglu.CROP_GLU_DELIMITER),
             AgProductionTechnology = paste(paste(AgSupplySubsector, IRR_RFD, sep = aglu.IRR_DELIMITER),
                                            MGMT, sep = aglu.MGMT_DELIMITER)) %>%
      rename(coefficient = value) %>% #remove inclusion of minicam energy input here because it was added earlier
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, minicam.energy.input, year, coefficient) ->
      L2062.AgCoef_Fert_ag_irr_mgmt_K2O

    # Copy final base year coefficients to all future years, bind with historic coefficients, then remove zeroes
    # Note: this assumes constant fertilizer coefficients in the future ----
    L2062.AgCoef_Fert_ag_irr_mgmt_K2O %>%
      filter(year == max(MODEL_BASE_YEARS)) %>%
      select(-year) %>%
      repeat_add_columns(tibble(year = MODEL_FUTURE_YEARS)) %>%
      bind_rows(L2062.AgCoef_Fert_ag_irr_mgmt_K2O) %>%
      filter(coefficient > 0) ->
      L2062.AgCoef_Fert_ag_irr_mgmt_K2O

    L2062.ag_Fert_MGMT_P2O5%>%
      # Add sector, subsector, technology names
      mutate(AgSupplySector = GCAM_commodity,
             AgSupplySubsector = paste(GCAM_subsector, GLU_name, sep = aglu.CROP_GLU_DELIMITER),
             AgProductionTechnology = paste(paste(AgSupplySubsector, IRR_RFD, sep = aglu.IRR_DELIMITER),
                                            MGMT, sep = aglu.MGMT_DELIMITER)) %>%
      rename(coefficient = value) %>% #remove inclusion of minicam energy input here because it was added earlier
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, minicam.energy.input, year, coefficient) ->
      L2062.AgCoef_Fert_ag_irr_mgmt_P2O5

    # Copy final base year coefficients to all future years, bind with historic coefficients, then remove zeroes
    # Note: this assumes constant fertilizer coefficients in the future ----
    L2062.AgCoef_Fert_ag_irr_mgmt_P2O5 %>%
      filter(year == max(MODEL_BASE_YEARS)) %>%
      select(-year) %>%
      repeat_add_columns(tibble(year = MODEL_FUTURE_YEARS)) %>%
      bind_rows(L2062.AgCoef_Fert_ag_irr_mgmt_P2O5) %>%
      filter(coefficient > 0) ->
      L2062.AgCoef_Fert_ag_irr_mgmt_P2O5



    # Calculate fertilizer coefficients for grassy bioenergy crops
    A_Fodderbio_chars %>%
      filter(GCAM_commodity == "biomassGrass") %>%
      mutate(coefficient = (aglu.BIO_GRASS_FERT_IO_GNM2 * CONV_G_KG / aglu.BIO_GRASS_YIELD_KGCM2    # Convert from application per unit area to per unit carbon
                            * aglu.CCONTENT_CELLULOSE * (1 - WaterContent))                         # Convert from carbon to wet biomass
             / (aglu.BIO_ENERGY_CONTENT_GJT * CONV_KG_T)) ->                         # Convert from biomass to energy
      bio_grass_coef

    # Calculate fertilizer coefficients for tree bioenergy crops
    A_Fodderbio_chars %>%
      filter(GCAM_commodity == "biomassTree") %>%
      mutate(coefficient = (aglu.BIO_TREE_FERT_IO_GNM2 * CONV_G_KG / aglu.BIO_TREE_YIELD_KGCM2    # Convert from application per unit area to per unit carbon
                            * aglu.CCONTENT_CELLULOSE * (1 - WaterContent))                         # Convert from carbon to wet biomass
             / (aglu.BIO_ENERGY_CONTENT_GJT * CONV_KG_T)) ->                         # Convert from biomass to energy
      bio_tree_coef

    # Map fertilizer coefficients to all bioenergy technologies
    L2052.AgCost_bio_irr_mgmt %>%
      select(-nonLandVariableCost) %>%                  # We are just using this data.frame to get the region/sector/tech names
      mutate(minicam.energy.input = "N fertilizer",
             coefficient = if_else(grepl("^biomassGrass", AgSupplySubsector),
                                   bio_grass_coef$coefficient, bio_tree_coef$coefficient)) ->
      L2062.AgCoef_Fert_bio_irr_mgmt
    # biochar not applied to bioenergy crops because grasslands have a recommended fertilizer addition of 0Kg/ha P




    # Adjust nonLandVariableCost to separate fertilizer cost (which is accounted for specifically) ----
    # Note that fertilizer price is determined by supply in calibration
    L2052.AgCost_ag_irr_mgmt %>%
      # Note: using left_join because there are instances with cost but no fertilizer use.
      left_join(L2062.AgCoef_Fert_ag_irr_mgmt,
                by = c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
      # Set fertilizer coefficient to zero when missing. This will lead to zero fertilizer cost.
      replace_na(list(coefficient = 0)) %>%
      # if we calcualte the nonLandVariableCost for biochar separately, it will be lower due to inputs of both fertilizer and biochar, but this is incorrect
      # set biochar nonLandVariableCost to that of the lo/hi mgmt methods by removing biochar from the minicam.energy.input
      filter(minicam.energy.input != "biochar") %>%
      # Calculate fertilizer cost using a fixed value (specified in constants.R in current $ per ton of NH3)
      # and the fertilizer coefficient calculated above. Subtract from original nonLandVariableCost.
      mutate(FertCost = coefficient * aglu.FERT_PRICE * gdp_deflator(1975, aglu.FERT_PRICE_YEAR) * CONV_KG_T / CONV_NH3_N) %>%
      # If we wanted we could apply regional fertilizer adjustments here.
      # Since we are handling negative profits with the min cal profit rate there is no pressing need at the moment.
      mutate(nonLandVariableCost = round(nonLandVariableCost - FertCost, aglu.DIGITS_CALPRICE)) %>%
      select(-minicam.energy.input, -coefficient, -FertCost) ->
      L2062.AgCost_ag_irr_mgmt_adj_old


    # load agronomic benefits from replace P and K fertilizers. There benefits aren't limited by amount of biochar applied to land
    #subtract K2O costs from existing ag costs
    L2062.AgCost_ag_irr_mgmt_adj_old %>%
      # Note: using left_join because there are instances with cost but no fertilizer use.
      left_join(L2062.AgCoef_Fert_ag_irr_mgmt_K2O,
                by = c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
      # Set fertilizer coefficient to zero when missing. This will lead to zero fertilizer cost.
      replace_na(list(coefficient = 0)) %>%
      # Calculate fertilizer cost using a fixed value (specified in constants.R in current $ per ton of NH3)
      # and the fertilizer coefficient calculated above. Subtract from original nonLandVariableCost.
      mutate(FertCost = if_else(grepl("biochar", AgProductionTechnology), coefficient * aglu.FERT_PRICE_K2O * gdp_deflator(1975, aglu.FERT_PRICE_YEAR) * CONV_KG_T, 0)) %>% # if it isn't a biochar land, 0 cost reduction
      # If we wanted we could apply regional fertilizer adjustments here.
      # Since we are handling negative profits with the min cal profit rate there is no pressing need at the moment.
      mutate(nonLandVariableCost = round(nonLandVariableCost - FertCost, aglu.DIGITS_CALPRICE)) %>%
      select(-minicam.energy.input, -coefficient, -FertCost) ->
      L2062.AgCost_ag_irr_mgmt_adj
    # and P2O5

    L2062.AgCost_ag_irr_mgmt_adj %>%
      # Note: using left_join because there are instances with cost but no fertilizer use.
      left_join(L2062.AgCoef_Fert_ag_irr_mgmt_P2O5,
                by = c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
      # Set fertilizer coefficient to zero when missing. This will lead to zero fertilizer cost.
      replace_na(list(coefficient = 0)) %>%
      # Calculate fertilizer cost using a fixed value (specified in constants.R in current $ per ton of NH3)
      # and the fertilizer coefficient calculated above. Subtract from original nonLandVariableCost.
      mutate(FertCost = if_else(grepl("biochar", AgProductionTechnology), coefficient * aglu.FERT_PRICE_P2O5 * gdp_deflator(1975, aglu.FERT_PRICE_YEAR) * CONV_KG_T, 0)) %>% # if it isn't a biochar land, 0 cost reduction
      # If we wanted we could apply regional fertilizer adjustments here.
      # Since we are handling negative profits with the min cal profit rate there is no pressing need at the moment.
      mutate(nonLandVariableCost = round(nonLandVariableCost - FertCost, aglu.DIGITS_CALPRICE)) %>%
      select(-minicam.energy.input, -coefficient, -FertCost) ->
      L2062.AgCost_ag_irr_mgmt_adj



    # if the ratio is too large, replace with the average reduction in price
    # assuming 2018 USDA NASS fertilizers as average percent of production expenses at 10.9%
    L2062.AgCost_ag_irr_mgmt_adj %>%
      left_join(L2062.AgCost_ag_irr_mgmt_adj_old, by=c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year"))%>%
      mutate(ratio = 100*(nonLandVariableCost.x-nonLandVariableCost.y)/nonLandVariableCost.y,
             nonLandVariableCost = nonLandVariableCost.x) %>% # calculate percentage reduction in crop costs
      mutate(nonLandVariableCost = if_else(nonLandVariableCost.y == 0, nonLandVariableCost.y, nonLandVariableCost)) %>% # remove cost reductions if theres a divide by 0 error and replace with original
      mutate(nonLandVariableCost = if_else(ratio < -2*10.9, -.109*nonLandVariableCost.y, nonLandVariableCost)) %>%# replace outliers on cost reduction with average fertilizer expenditures
      mutate(nonLandVariableCost = if_else(is.na(nonLandVariableCost), nonLandVariableCost.y, nonLandVariableCost)) %>% # remove NA values
      select(-nonLandVariableCost.y, -nonLandVariableCost.x, -ratio) -> L2062.AgCost_ag_irr_mgmt_adj



    L2052.AgCost_bio_irr_mgmt %>%
      # Note: using left_join because there are instances with cost but no fertilizer use
      left_join(L2062.AgCoef_Fert_bio_irr_mgmt,
                by = c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology", "year")) %>%
      # Set fertilizer coefficient to zero when missing. This will lead to zero fertilizer cost.
      replace_na(list(coefficient = 0)) %>%
      # if we calcualte the nonLandVariableCost for biochar separately, it will be lower due to inputs of both fertilizer and biochar, but this is incorrect
      # set biochar nonLandVariableCost to that of the lo/hi mgmt methods by removing biochar from the minicam.energy.input
      filter(minicam.energy.input != "biochar") %>%
      # Calculate fertilizer cost using a fixed value (specified in constants.R in current $ per ton of NH3)
      # and the fertilizer coefficient calculated above. Subtract from original nonLandVariableCost.
      mutate(FertCost = coefficient * aglu.FERT_PRICE * gdp_deflator(1975, aglu.FERT_PRICE_YEAR) * CONV_KG_T / CONV_NH3_N) %>%
      # If we wanted we could apply regional fertilizer adjustments here.
      # Since we are handling negative profits with the min cal profit rate there is no pressing need at the moment.
      mutate(nonLandVariableCost = round(nonLandVariableCost - FertCost, aglu.DIGITS_CALPRICE)) %>%
      select(-minicam.energy.input, -coefficient, -FertCost) ->
      L2062.AgCost_bio_irr_mgmt_adj

    # Woolf, D., Amonette, J. E., Street-Perrott, F. A., Lehmann, J. & Joseph, S. Sustainable biochar to mitigate global climate change. Nat Commun 1, 56 (2010).
    # assumes a 50% increase in N use efficiency due to biochar application - this is modeled by reducing the N fertilizer requirement by 2
    # get right columns in the biochar app rate dataframe
    L181.ag_kgbioha_R_C_Y_GLU_irr_level %>%
      left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%
      mutate(MGMT = "biochar") %>%
      mutate(level = "biochar") %>%
      filter(kg_bio_ha > 0) %>%
      mutate(IRR_RFD = toupper(Irr_Rfd)) %>%
      # Add sector, subsector, technology names
      mutate(AgSupplySector = GCAM_commodity,
             AgSupplySubsector = paste(GCAM_subsector, GLU_name, sep = aglu.CROP_GLU_DELIMITER),
             AgProductionTechnology = paste(paste(AgSupplySubsector, IRR_RFD , sep = aglu.IRR_DELIMITER),
                                            MGMT, sep = aglu.MGMT_DELIMITER)) %>%
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, kg_bio_ha) ->
      L181.ag_kgbioha_R_C_Y_GLU_irr_level

    # decrease fert consumption for biochar lands with sufficient app rate
    L2062.AgCoef_Fert_ag_irr_mgmt %>%
      left_join(L181.ag_kgbioha_R_C_Y_GLU_irr_level, by=c("region", "AgSupplySector", "AgSupplySubsector", "AgProductionTechnology")) %>%
      replace_na(list(kg_bio_ha = 0)) %>% # replace NA with 0 - will exclude based on logic in following line of code
      mutate(coefficient = if_else(grepl("biochar", AgProductionTechnology) & (kg_bio_ha > aglu.BIOCHAR_LOWER_APP_RATE) & (minicam.energy.input == "N fertilizer"), coefficient/2, coefficient)) %>%
      select(-kg_bio_ha)->
      L2062.AgCoef_Fert_ag_irr_mgmt

    print(L2062.AgCoef_Fert_ag_irr_mgmt)


    # Produce outputs
    L2062.AgCoef_Fert_ag_irr_mgmt %>%
      add_title("Fertilizer coefficients for agricultural technologies") %>%
      add_units("kgN per kg crop") %>%
      add_comments("Map fertilizer coefficients in L142.ag_Fert_IO_R_C_Y_GLU to all technologies") %>%
      add_comments("Note: we are using the same coefficient for all four management technologies (irrigated, rainfed, hi and lo") %>%
      add_legacy_name("L2062.AgCoef_Fert_ag_irr_mgmt") %>%
      add_precursors("common/GCAM_region_names",
                     "water/basin_to_country_mapping",
                     "L142.ag_Fert_IO_R_C_Y_GLU",
                     "L171.ag_rfdEcYield_kgm2_R_C_Y_GLU") ->
      L2062.AgCoef_Fert_ag_irr_mgmt
    L2062.AgCoef_Fert_bio_irr_mgmt %>%
      add_title("Fertilizer coefficients for bioenergy technologies") %>%
      add_units("kgN per GJ") %>%
      add_comments("Compute bioenergy fertilizer coefficients from read-in constants") %>%
      add_comments("Note: L2052.AgCost_bio_irr_mgmt is only used to identify all bioenergy technologies") %>%
      add_legacy_name("L2062.AgCoef_Fert_bio_irr_mgmt") %>%
      add_precursors("aglu/A_Fodderbio_chars",
                     "L2052.AgCost_bio_irr_mgmt") ->
      L2062.AgCoef_Fert_bio_irr_mgmt
    L2062.AgCost_ag_irr_mgmt_adj %>%
      add_title("Adjusted non-land variable cost for agricultural technologies") %>%
      add_units("1975$ per kg") %>%
      add_comments("Subtract cost of fertilizer from non-land variable cost.") %>%
      add_comments("Fertilizer costs is computed using a fixed NH3 cost and the fertilizer coefficient") %>%
      add_legacy_name("L2062.AgCost_ag_irr_mgmt_adj") %>%
      same_precursors_as(L2062.AgCoef_Fert_ag_irr_mgmt) %>%
      add_precursors("L2052.AgCost_ag_irr_mgmt") ->
      L2062.AgCost_ag_irr_mgmt_adj
    L2062.AgCost_bio_irr_mgmt_adj %>%
      add_title("Adjusted non-land variable cost for agricultural technologies") %>%
      add_units("1975$ per GJ") %>%
      add_comments("Subtract cost of fertilizer from non-land variable cost.") %>%
      add_comments("Fertilizer costs is computed using a fixed NH3 cost and the fertilizer coefficient") %>%
      add_legacy_name("L2062.AgCost_bio_irr_mgmt_adj") %>%
      same_precursors_as(L2062.AgCoef_Fert_bio_irr_mgmt) %>%
      add_precursors("L2052.AgCost_bio_irr_mgmt")  ->
      L2062.AgCost_bio_irr_mgmt_adj

    return_data(MODULE_OUTPUTS)
  } else {
    stop("Unknown command")
  }
}
