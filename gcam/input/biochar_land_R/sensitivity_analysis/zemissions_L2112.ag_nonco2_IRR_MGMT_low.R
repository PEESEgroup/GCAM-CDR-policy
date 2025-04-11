# Copyright 2019 Battelle Memorial Institute; see the LICENSE file.

#' module_emissions_L2112.ag_nonco2_IRR_MGMT
#'
#' Disaggregate non-CO2 agricultural emissions by production technology
#'
#' @param command API command to execute
#' @param ... other optional parameters, depending on command
#' @return Depends on \code{command}: either a vector of required inputs,
#' a vector of output names, or (if \code{command} is "MAKE") all
#' the generated outputs: \code{object}, \code{L2112.AWBEmissions}, \code{L2112.AGREmissions}. The corresponding file in the
#' original data system was \code{L2112.ag_nonco2_IRR_MGMT.R} (emissions level2).
#' @details Disaggregates agricultural emissions the basis of production by scaling emissions by a technology factor
#' @importFrom assertthat assert_that
#' @importFrom dplyr bind_rows filter if_else group_by left_join mutate select summarise
#' @importFrom tidyr replace_na unite
#' @author KD July 2017
module_emissions_L2112.ag_nonco2_IRR_MGMT <- function(command, ...) {
  if(command == driver.DECLARE_INPUTS) {
    return(c(FILE = "common/GCAM_region_names",
             FILE = "water/basin_to_country_mapping",
             "L2111.AGREmissions",
             "L2111.AGRBio",
             "L2111.AWB_BCOC_EmissCoeff",
             "L2111.nonghg_max_reduction",
             "L2111.nonghg_steepness",
             "L2111.AWBEmissions",
             "L2012.AgProduction_ag_irr_mgmt",
             "L2012.AgProduction_ag_irr_mgmt_no_biochar",
             "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level",
             "L181.ag_kgbioha_R_C_Y_GLU_irr_level"))
  } else if(command == driver.DECLARE_OUTPUTS) {
    return(c("L2112.AGRBio", "L2112.AWB_BCOC_EmissCoeff", "L2112.nonghg_max_reduction",
             "L2112.nonghg_steepness", "L2112.AWBEmissions", "L2112.AGREmissions", "L2112.AWBEmissions_biochar", "L2112.AGREmissions_biochar"))
  } else if(command == driver.MAKE) {

    all_data <- list(...)[[1]]

    AgProductionTechnology <- level <- year <- region <- AgSupplySector <- AgSupplySubsector <-
      AgProductionTechnology_nolvl <- calOutputValue <- AgProductionTechnology_lvl <- total <-
      share_tech <- input.emissions <- Non.CO2 <- NULL  # silence package check notes

    # Load required inputs
    L2111.AWBEmissions <- get_data(all_data, "L2111.AWBEmissions")
    L2111.AGREmissions <- get_data(all_data, "L2111.AGREmissions")
    L2111.AGRBio <- get_data(all_data, "L2111.AGRBio")
    L2111.AWB_BCOC_EmissCoeff <- get_data(all_data, "L2111.AWB_BCOC_EmissCoeff")
    L2111.nonghg_max_reduction <- get_data(all_data, "L2111.nonghg_max_reduction")
    L2111.nonghg_steepness <- get_data(all_data, "L2111.nonghg_steepness")
    L2012.AgProduction_ag_irr_mgmt <- get_data(all_data, "L2012.AgProduction_ag_irr_mgmt", strip_attributes = TRUE)
    L2012.AgProduction_ag_irr_mgmt_no_biochar <- get_data(all_data, "L2012.AgProduction_ag_irr_mgmt_no_biochar", strip_attributes = TRUE)
    L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level <- get_data(all_data, "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level")
    L181.ag_kgbioha_R_C_Y_GLU_irr_level <- get_data(all_data, "L181.ag_kgbioha_R_C_Y_GLU_irr_level")
    GCAM_region_names <- get_data(all_data, "common/GCAM_region_names")
    basin_to_country_mapping <- get_data(all_data, "water/basin_to_country_mapping")

    # ===================================================
    # For all of the animal emission tables add high and low management level
    #L2111.AGRBio %>%
    #  repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
    #  unite(AgProductionTechnology, AgProductionTechnology, level, sep = "_") ->
    #  L2112.AGRBio
    L2111.AGRBio %>%
      repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>% filter(level == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")),# only need one match
                by=c("AgSupplySector"="GCAM_commodity", "region", "year", "level")) %>%
      dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar (in this case its biomass, so it doesn't have biochar anyways)
      select(-GCAM_region_ID, -GCAM_subsector, -GLU, -Irr_Rfd, -value) %>%
      bind_rows(L2111.AGRBio %>%
                  repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
                  filter(level != "biochar"))%>%
      unite(AgProductionTechnology, AgProductionTechnology, level, sep = "_") %>%
      dplyr::distinct_all() ->
      L2112.AGRBio

    L2111.AWB_BCOC_EmissCoeff %>%
      repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>% filter(level == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")),# only need one match
                by=c("AgSupplySector"="GCAM_commodity", "region", "year", "level")) %>% dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      select(-GCAM_region_ID, -GCAM_subsector, -GLU, -Irr_Rfd, -value) %>%
      bind_rows(L2111.AWB_BCOC_EmissCoeff %>%
                  repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
                  filter(level != "biochar"))%>%
      unite(AgProductionTechnology, AgProductionTechnology, level, sep = "_") %>%
      dplyr::distinct_all() ->
      L2112.AWB_BCOC_EmissCoeff

    L2111.nonghg_max_reduction  %>%
      repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>% filter(level == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")),# only need one match
                by=c("AgSupplySector"="GCAM_commodity", "region", "year", "level")) %>% dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      select(-GCAM_region_ID, -GCAM_subsector, -GLU, -Irr_Rfd, -value) %>%
      bind_rows(L2111.nonghg_max_reduction %>%
                  repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
                  filter(level != "biochar"))%>%
      unite(AgProductionTechnology, AgProductionTechnology, level, sep = "_") %>%
      dplyr::distinct_all() ->
      L2112.nonghg_max_reduction

    L2111.nonghg_steepness  %>%
      repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>% filter(level == "biochar") %>%
      left_join(L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level %>% left_join_error_no_match(GCAM_region_names, by=c("GCAM_region_ID")),# only need one match
                by=c("AgSupplySector"="GCAM_commodity", "region", "year", "level")) %>% dplyr::distinct_all() %>%
      drop_na() %>% #drop rows for crops that don't need biochar
      select(-GCAM_region_ID, -GCAM_subsector, -GLU, -Irr_Rfd, -value) %>%
      bind_rows(L2111.nonghg_steepness %>%
                  repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
                  filter(level != "biochar"))%>%
      unite(AgProductionTechnology, AgProductionTechnology, level, sep = "_") %>%
      dplyr::distinct_all() ->
      L2112.nonghg_steepness


    # For the tables whose emissions are read as quantities rather than rates,
    # disaggregate emissions on the basis of production.

    # First calculate the total emissions for each region, supply sector, subsector,
    # technology level in the most recent model base year. This total will latter be
    # used to  calculate share weights.
    print(L2012.AgProduction_ag_irr_mgmt_no_biochar)
    L2012.AgProduction_ag_irr_mgmt_no_biochar %>%
      filter(year == max(MODEL_BASE_YEARS)) %>%
      mutate(AgProductionTechnology_nolvl = gsub("_hi|_lo|_biochar", "", AgProductionTechnology)) %>%
      group_by(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology_nolvl, year) %>%
      summarise(total = sum(calOutputValue)) %>%
      ungroup() ->
      L2112.AgProduction_ag_irr_nomgmt_aggergate

    # Now subset the table of agricultural production for the most recent model base year
    # and format the data frame so that so that the AgProductionTechnology_level column
    # will match the column in the aggeregated data frame.
    L2012.AgProduction_ag_irr_mgmt_no_biochar %>%
      filter(year == max(MODEL_BASE_YEARS)) %>%
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology_lvl = AgProductionTechnology, year, calOutputValue) %>%
      mutate(AgProductionTechnology_nolvl = gsub("_hi|_lo|_biochar", "", AgProductionTechnology_lvl)) ->
      L2112.AgProduction_ag

    # Calculate the share weights or the fraction of emissions for each region, sector, subsector,
    # technology and level for the using the aggrated total emissions determined above.
    # Eventually these emission shares will be used as a factor to disaggregate the emissions input.
    L2112.AgProduction_ag %>%
      left_join_error_no_match(L2112.AgProduction_ag_irr_nomgmt_aggergate,
                               by = c("region", "AgSupplySector", "year", "AgSupplySubsector", c("AgProductionTechnology_nolvl"))) %>%
      mutate(share_tech = calOutputValue / total) ->
      L2112.AgProduction_ag_share

    # Combine non agricultural waste burning emissions and agricultural waste burning
    # emissions into a single data frame. Add management level information to production
    # technology column.
    L2111.AWBEmissions %>%
      bind_rows(L2111.AGREmissions) %>%
      repeat_add_columns(tibble(level = c("hi", "lo", "biochar"))) %>%
      unite(AgProductionTechnology_lvl, AgProductionTechnology, level, sep = "_", remove = FALSE) ->
      L2112.awb_agr_emissions

    # Match the shares(fraction of emissions) to the data frames containing
    # emissions quantities for the agricultural water burning and agricultural
    # non waste burning emissions.
    L2112.AgProduction_ag_share %>%
      select(-year, -AgSupplySubsector) %>%
      left_join(L2112.awb_agr_emissions, by = c("region", "AgSupplySector", "AgProductionTechnology_lvl")) ->
      L2112.awb_agr_emissions


    # Where shares allocated to lo/hi are NA but emissions are positive, split it 50/50 between
    # the techs. For all others, set share to zero. Then scale the input emissions by the emission
    # shares.
    print(L2112.awb_agr_emissions %>% filter(level=="biochar"))
    L2112.awb_agr_emissions %>%
      mutate(share_tech = if_else(level == "biochar" & input.emissions > 1e-6, 0.5, share_tech)) %>% #ensure biochar land has associated ag emissions
      mutate(share_tech = if_else(is.na(share_tech) & input.emissions > 1e-6, 0.5, share_tech)) %>%
      replace_na(list(share_tech = 0)) %>%
      mutate(input.emissions  = input.emissions * share_tech) %>% #biochar has a share_tech of 0
      select(region, AgSupplySector, AgProductionTechnology = AgProductionTechnology_lvl, AgSupplySubsector,
             year, Non.CO2, input.emissions, level) ->
      L2112.awb_agr_emissions_disag

    # The disaggregated agricultural waste burning emissions.
    L2112.awb_agr_emissions_disag %>%
      filter(grepl("AWB", Non.CO2)) %>%
      filter(level != "biochar")->
      L2112.AWBEmissions # no biochar

    L2112.awb_agr_emissions_disag %>%
      filter(!grepl("AWB", Non.CO2)) %>%
      filter(level != "biochar")->
      L2112.AGREmissions # no biochar

    print(L181.ag_kgbioha_R_C_Y_GLU_irr_level %>%
            left_join_error_no_match(basin_to_country_mapping[ c("GLU_code", "GLU_name")], by = c("GLU" = "GLU_code")) %>%
            mutate(MGMT = "biochar"))
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
      select(region, AgSupplySector, AgSupplySubsector, AgProductionTechnology, kg_bio_ha, level) ->
      L181.ag_kgbioha_R_C_Y_GLU_irr_level

    # The disaggregated non agricultural waste burning emissions.
    L2112.AWBEmissions %>%
      filter(level == "hi") %>% #use hi as a baseline for biochar in line with other assumptions elsewhere in GCAM R files
      mutate(level = "biochar",
             AgProductionTechnology = gsub("_hi", "_biochar", AgProductionTechnology)) %>%
      left_join(L181.ag_kgbioha_R_C_Y_GLU_irr_level, by=c("region", "AgSupplySector", "AgProductionTechnology", "AgSupplySubsector", "level")) %>%
      drop_na() %>% # remove wrong biochar regions
      # Cayuela, M.L., Van Zwieten, L., Singh, B.P., Jeffery, S., Roig, A. and Sanchez-Monedero, M.A., 2014. Biochar's role in mitigating soil nitrous oxide emissions: A review and meta-analysis. Agriculture, Ecosystems & Environment, 191, pp.5-16.
      mutate(input.emissions = if_else(level=="biochar" & Non.CO2 == "N2O_AGR"& (kg_bio_ha > aglu.BIOCHAR_LOWER_APP_RATE), input.emissions*1.39, input.emissions)) %>%
      mutate(emiss.coef = input.emissions) %>% #rename coefficients so that they function as coefficients matching
      filter(year == 1975) %>% # to match biomassGrass etc. config files which work
      select(-kg_bio_ha, -input.emissions) ->
      L2112.AWBEmissions_biochar

    # The disaggregated non agricultural waste burning emissions.
    L2112.AGREmissions %>%
      filter(level == "hi") %>% #use hi as a baseline for biochar in line with other assumptions elsewhere in GCAM R files
      mutate(level = "biochar",
             AgProductionTechnology = gsub("_hi", "_biochar", AgProductionTechnology)) %>%
      left_join(L181.ag_kgbioha_R_C_Y_GLU_irr_level, by=c("region", "AgSupplySector", "AgProductionTechnology", "AgSupplySubsector", "level")) %>%
      drop_na() %>% # remove wrong biochar regions
      # Cayuela, M.L., Van Zwieten, L., Singh, B.P., Jeffery, S., Roig, A. and Sanchez-Monedero, M.A., 2014. Biochar's role in mitigating soil nitrous oxide emissions: A review and meta-analysis. Agriculture, Ecosystems & Environment, 191, pp.5-16.
      mutate(input.emissions = if_else(level=="biochar" & Non.CO2 == "N2O_AGR"& (kg_bio_ha > aglu.BIOCHAR_LOWER_APP_RATE), input.emissions*1.39, input.emissions)) %>%
      mutate(emiss.coef = input.emissions) %>% #rename coefficients so that they function as coefficients matching
      filter(year == 1975) %>% # to match biomassGrass etc. config files which work
      select(-kg_bio_ha, -input.emissions) ->
      L2112.AGREmissions_biochar

    print(L2112.AWBEmissions_biochar)
    print(L2112.AGREmissions_biochar)

    print(L2112.AGRBio) #TODO: biochar needs to have the same data structure as this (units of this are kg GHG/GJ energy)



    # ===================================================
    # Produce outputs
    L2112.AGRBio %>%
      add_title("Bio N2O Coefficients by region, technology, and management level ") %>%
      add_units("kg N2O per GJ bioenergy") %>%
      add_comments("L211.AGRBio repeated by IRR and RFD technologies") %>%
      add_legacy_name("L2112.AGRBio") %>%
      add_precursors("L2111.AGRBio") ->
      L2112.AGRBio

    L2112.AWB_BCOC_EmissCoeff %>%
      add_title("Agricultural Waste Burning BC/OC Emissions Coefficients by management") %>%
      add_units("kt/Mt") %>%
      add_comments("L2111.AWB_BCOC_EmissCoeff repeated high and low management") %>%
      add_legacy_name("L2112.AWB_BCOC_EmissCoeff") %>%
      add_precursors("L2111.AWB_BCOC_EmissCoeff", "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level") ->
      L2112.AWB_BCOC_EmissCoeff

    L2112.nonghg_max_reduction %>%
      add_title("Non-GHG maximum emissions coefficient reduction by agricultural technology and management") %>%
      add_units("Percent reduction from base-year emissions coefficient") %>%
      add_comments("L2111.nonghg_max_reduction repeated by high and low management") %>%
      add_legacy_name("L2112.nonghg_max_reduction") %>%
      add_precursors("L2111.nonghg_max_reduction", "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level") ->
      L2112.nonghg_max_reduction

    L2112.nonghg_steepness %>%
      add_title("Steepness of non-GHG emissions reduction for agricultural technologies") %>%
      add_units("Unitless") %>%
      add_comments("L2111.nonghg_steepness repeated by high and low management level") %>%
      add_legacy_name("L2112.nonghg_steepness") %>%
      add_precursors("L2111.nonghg_steepness", "L181.ag_EcYield_kgm2_R_C_Y_GLU_irr_level") ->
      L2112.nonghg_steepness

    L2112.AWBEmissions %>%
      add_title("Input table of agricultural waste burning emissions by production") %>%
      add_units("Tg") %>%
      add_comments("Production share weights are set for irrigated vs. rainfed, same for high and low management.") %>%
      add_legacy_name("L2112.AWBEmissions") %>%
      add_precursors("L2111.AWBEmissions", "L2012.AgProduction_ag_irr_mgmt") ->
      L2112.AWBEmissions

    L2112.AGREmissions %>%
      add_title("Input table for the agricultural emissions by production") %>%
      add_units("Tg") %>%
      add_comments("Production share weights are set for irrigated vs. rainfed, same for high and low management.") %>%
      add_legacy_name("L2112.AGREmissions") %>%
      add_precursors("L2111.AGREmissions", "L2012.AgProduction_ag_irr_mgmt") ->
      L2112.AGREmissions

    L2112.AWBEmissions_biochar %>%
      add_title("Input table of agricultural waste burning emissions by production") %>%
      add_units("kg/kg") %>%
      add_comments("GHG emissions per unit crop producted on biochar managed lands") %>%
      add_legacy_name("L2112.AWBEmissions") %>%
      add_precursors("L2111.AWBEmissions", "L2012.AgProduction_ag_irr_mgmt", "L181.ag_kgbioha_R_C_Y_GLU_irr_level") ->
      L2112.AWBEmissions_biochar

    L2112.AGREmissions_biochar %>%
      add_title("Input table for the agricultural emissions by production") %>%
      add_units("kg/kg") %>%
      add_comments("Production share weights are set for irrigated vs. rainfed, same for high and low management.") %>%
      add_legacy_name("L2112.AGREmissions") %>%
      add_precursors("L2111.AGREmissions", "L2012.AgProduction_ag_irr_mgmt", "L181.ag_kgbioha_R_C_Y_GLU_irr_level") ->
      L2112.AGREmissions_biochar

    return_data(L2112.AGRBio, L2112.AWB_BCOC_EmissCoeff, L2112.nonghg_max_reduction, L2112.AWBEmissions,
                L2112.nonghg_steepness, L2112.AGREmissions, L2112.AGREmissions_biochar, L2112.AWBEmissions_biochar)

  } else {
    stop("Unknown command")
  }
}
