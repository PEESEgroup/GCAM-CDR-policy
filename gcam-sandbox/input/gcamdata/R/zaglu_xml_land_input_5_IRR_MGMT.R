# Copyright 2019 Battelle Memorial Institute; see the LICENSE file.

#' module_aglu_land_input_5_IRR_MGMT_xml
#'
#' Construct XML data structure for \code{land_input_5_IRR_MGMT.xml}.
#'
#' @param command API command to execute
#' @param ... other optional parameters, depending on command
#' @return Depends on \code{command}: either a vector of required inputs,
#' a vector of output names, or (if \code{command} is "MAKE") all
#' the generated outputs: \code{land_input_5_IRR_MGMT.xml}. The corresponding file in the
#' original data system was \code{batch_land_input_5_IRR_MGMT_xml.R} (aglu XML).
module_aglu_land_input_5_IRR_MGMT_xml <- function(command, ...) {
  if(command == driver.DECLARE_INPUTS) {
    return(c("L2252.LN5_Logit",
             "L2252.LN5_HistMgdAllocation_crop",
             "L2252.LN5_MgdAllocation_crop",
             "L2252.LN5_HistMgdAllocation_bio",
             "L2252.LN5_MgdAllocation_bio",
             "L2252.LN5_MgdCarbon_crop",
             "L2252.LN5_MgdCarbon_bio",
             "L2252.LN5_LeafGhostShare",
             "L2252.LN5_NodeGhostShare"))
  } else if(command == driver.DECLARE_OUTPUTS) {
    return(c(XML = "land_input_5_IRR_MGMT.xml"))
  } else if(command == driver.MAKE) {

    all_data <- list(...)[[1]]

    # Load required inputs
    L2252.LN5_Logit <- get_data(all_data, "L2252.LN5_Logit")
    L2252.LN5_HistMgdAllocation_crop <- get_data(all_data, "L2252.LN5_HistMgdAllocation_crop")
    L2252.LN5_MgdAllocation_crop <- get_data(all_data, "L2252.LN5_MgdAllocation_crop")
    L2252.LN5_HistMgdAllocation_bio <- get_data(all_data, "L2252.LN5_HistMgdAllocation_bio")
    L2252.LN5_MgdAllocation_bio <- get_data(all_data, "L2252.LN5_MgdAllocation_bio")
    L2252.LN5_MgdCarbon_crop <- get_data(all_data, "L2252.LN5_MgdCarbon_crop")
    L2252.LN5_MgdCarbon_bio <- get_data(all_data, "L2252.LN5_MgdCarbon_bio")
    L2252.LN5_LeafGhostShare <- get_data(all_data, "L2252.LN5_LeafGhostShare")
    L2252.LN5_NodeGhostShare <- get_data(all_data, "L2252.LN5_NodeGhostShare")

    # ===================================================
    # normal land allocations for crops has reduced by 50%
    print(L2252.LN5_Logit) # no levels
    print(L2252.LN5_HistMgdAllocation_crop, n = 20) # wrong allocations due to biochar - fixing code
    print(L2252.LN5_MgdAllocation_crop) # has biochar with allocation
    print(L2252.LN5_HistMgdAllocation_bio) # has biochar with 0 allocation
    print(L2252.LN5_MgdAllocation_bio) # has biochar with 0 allocation
    print(L2252.LN5_MgdCarbon_crop) # has biochar - fix soil carbon density
    print(L2252.LN5_MgdCarbon_bio)
    print(L2252.LN5_LeafGhostShare %>% filter(level == "biochar")) # has biochar - fix ghost share
    print(L2252.LN5_NodeGhostShare) # no levels


    # Produce outputs
    create_xml("land_input_5_IRR_MGMT.xml") %>%
      add_logit_tables_xml(L2252.LN5_Logit, "LN5_Logit") %>%
      add_xml_data(L2252.LN5_HistMgdAllocation_crop, "LN5_HistMgdAllocation") %>%
      add_xml_data(L2252.LN5_MgdAllocation_crop, "LN5_MgdAllocation") %>%
      add_xml_data(L2252.LN5_HistMgdAllocation_bio, "LN5_HistMgdAllocation") %>%
      add_xml_data(L2252.LN5_MgdAllocation_bio, "LN5_MgdAllocation") %>%
      add_xml_data(L2252.LN5_MgdCarbon_crop, "LN5_MgdCarbon") %>%
      add_xml_data(L2252.LN5_MgdCarbon_bio, "LN5_MgdCarbon") %>%
      add_xml_data(L2252.LN5_LeafGhostShare, "LN5_LeafGhostShare") %>%
      add_xml_data(L2252.LN5_NodeGhostShare, "LN5_NodeGhostShare") %>%
      add_rename_landnode_xml() %>%
      add_precursors("L2252.LN5_Logit",
                     "L2252.LN5_HistMgdAllocation_crop",
                     "L2252.LN5_MgdAllocation_crop",
                     "L2252.LN5_HistMgdAllocation_bio",
                     "L2252.LN5_MgdAllocation_bio",
                     "L2252.LN5_MgdCarbon_crop",
                     "L2252.LN5_MgdCarbon_bio",
                     "L2252.LN5_LeafGhostShare",
                     "L2252.LN5_NodeGhostShare") ->
      land_input_5_IRR_MGMT.xml

    return_data(land_input_5_IRR_MGMT.xml)
  } else {
    stop("Unknown command")
  }
}
