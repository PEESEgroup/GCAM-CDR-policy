#TODO
# 1. Get rid of fertilizer sector - here - DONE
# 2. Update assumptions on avoided/sequestered C emissions - here
# 3. Build new land use nodes - land_input_5_IRR_MGMT - L2252.LN5_*
# 3.1. land allocation - land_input_5_IRR_MGMT - L2252.LN5_*
# 3.2. carbon densities, mature age - land_input_5_IRR_MGMT  - L2252.LN5_*
# 3c. update logits - land_input_5_IRR_MGMT  - L2252.LN5_*
# 3d. update share-weights - land_input_5_IRR_MGMT - L2252.LN5_*
# 3a. nonLandVariableCost same as others - ag_cost_IRR_MGMT - L2062.AgCost_ag_irr_mgmt_adj - L142.ag_Fert_IO_R_C_Y_GLU - L100.LDS_ag_prod_t
#                                                           - L2052.AgCalMinProfitRate - L161.ag_irrProd_Mt_R_C_Y_GLU - L152.ag_*
# 3b. set minicam-energy-input name to biochar in addition to N fertilizer - ag_Fert_IRR_MGMT - L142.ag_Fert_IO_R_C_Y_GLU - L100.LDS_ag_prod_t
# 3b1. get coefficients for biochar demand - ag_Fert_IRR_MGMT - L2062.AgCoef_Fert_ag_irr_mgmt - L142.ag_Fert_IO_R_C_Y_GLU - L100.LDS_ag_prod_t
# 3e. update agProdChange - ag_prodchange_ssp2_IRR_MGMT - L2052.AgProdChange_ag_irr_ref
#                                                       - L2052.AgProdChange_bio_irr_ref
# 3g. update biophysical water consumption - ag_water_input_IRR_MGMT - L2072.AgCoef_*_ag_mgmt
# 3i. update bio_externality_cost - bio_externality - L270.AGCoef_bioext
# 3f. update biomass emissions - all_aglu_emissions_IRR_MGMT - L252.AgMAC - L211.AGREmissions - L122.ghg_tg_R_agr_C_Y_GLU
# 3h. update MAC coefficients - all_aglu_emissions_IRR_MGMT - L252.AgMAC - L211.AGREmissions - L122.ghg_tg_R_agr_C_Y_GLU
# 3j. update residue biomass-production - resbio_input_IRR_MGMT - L2042.AgResBio_ag_irr_mgmt - L101.ag_Prod_Mt_R_C_Y_GLU - "aglu/FAO/FAO_ag_items_PRODSTAT" OR "aglu/LDS/LDS_land_types"
# 3k. update locations where certain land nodes cannot exist - prune_empty_ag - L240.TechCoef_tra - aglu/A_agTradedTechnology
# 4. find which R files correspond to what xml output files


devtools::load_all()

# supply sector   subsector   technology
# poultry_biochar biochar     slow pyrolysis
# dairy_biochar biochar     slow pyrolysis
# beef_biochar biochar     slow pyrolysis
# pork_biochar biochar     slow pyrolysis
# goat_biochar biochar     slow pyrolysis

# conversions
# 1e6 tons = 1 Mt
# 1e12 MJ = 1 EJ

### ADDITIONAL FILES DATA + SOURCES
## A_an_secout (original calculations):
#               source 1: Bentley, J. A. et al. Economics of Dairy Manure Management in Iowa. Iowa State University Animal Industry Report 13, (2016).
#               source 2: Malone, G. W. Nutrient Enrichment in integrated Broiler Production Systems. Poultry Science 71, 1117–1122 (1992).
#               source 3: https://www.fao.org/3/i6421e/i6421e.pdf
#               source 4: Junior, C. C. et al. Brazilian beef cattle feedlot manure management: A country survey. Journal of Animal Science 91, 1811–1818 (2013).
#               source 5: https://www.fao.org/3/t0279e/T0279E05.htm
#               source 6: Nguyen, T. L. T., Hermansen, J. E. & Mogensen, L. Environmental costs of meat production: the case of typical EU pork production. Journal of Cleaner Production 28, 168–176 (2012).
#               source 7: J. A. Ogejo, S. Wildeus, P. Knight, & R. B. Wilke. Technical Note: Estimating Goat and Sheep Manure Production and their Nutrient Contribution in the Chesapeake Bay Watershed. Applied Engineering in Agriculture 26, 1061–1065 (2010).
#               source 8: Glimp, H. A. Meat goat production and marketing. Journal of Animal Science 73, 291–295 (1995).
#        poultry (units): 1 metric ton manure per 1000 broilers per flock [2]
#        poultry (units): 1008 g poultry meat per broiler [3] yields 1/1.008 = .992 Mt manure per Mt Poultry kg
#          dairy (units): 10.35 (tons/cow/year) [1] * 0.9072 (metric tons/imperial tons) /(23,578 (lbs milk/cow/year) * 0.000453592 (lbs/metric ton))= 0.878 Mt manure/Mt dairy product
#           beef (units): 3 (kg manure/days in feedlot) [4] * 100 (days/ feedlot) [4] / 252 (kg meat / cow) [5] = 1.19 Mt manure/Mt Beef
#           pork (units): 552 kg manure [6] / 750 kg carcass [6] * 75 kg carcass [5] / 57.4 (kg meat) [5] = 0.961 Mt manure/Mt Pork
#           goat (units): Goat manure is almost never collected [8]

## A_an_secout (Prof. Lehmann recommendations)
#               source 9: Lefebvre, D. et al. Biomass residue to carbon dioxide removal: quantifying the global impact of biochar. Biochar 5, 65 (2023).
#        poultry (units): 0.0273 (kg collectible manure solids /day /head) [9] * 1 (head) / 1.008 (kg meat) [3] * 51 day lifespan = 1.381 Mt manure/Mt Poultry
#          dairy (units): 10.35 (tons/cow/year) [1] * 0.9072 (metric tons/imperial tons) /(23,578 (lbs milk/cow/year) * 0.000453592 (lbs/metric ton))= 0.878 Mt manure/Mt dairy product
#           beef (units): 0.5391 (kg collectible manure solids /day /head) [9] * 1 (head) / 228 (kg meat) [5] * 3 (year lifespan) * 365 (days) [5] = 2.589 Mt manure/Mt Beef
#           pork (units): 0.0930 (kg collectible manure solids /day /head) [9] * 1 (head) / 55.76 (kg meat) [5] * 0.5 (year lifespan) * 365 (days) [5] = 0.304 Mt manure/Mt Pork
#           goat (units): 0.2433 (kg collectible manure solids /day /head) [9] * 1 (head) / 19.1 (kg meat) [5] * .667 (year lifespan) * 365 (days) [5] = 3.101 Mt manure/Mt Goat


## A_An_secout_prices:
# manure prices

## A21.secout_prices
# natural gas: 1.746 1975$/GJ - 2010 price when solved in market, which is the same for all regions

### CHANGES TO A21 ###

#modify A21.globaltech_secout.csv
example_file <- find_csv_file("energy/A21.globaltech_secout", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
#               source 2: Santos, T. M., Silva, W. R. da, Carregosa, J. de C. & Wisniewski, A. Comprehensive characterization of cattle manure bio-oil for scale-up assessment comparing non-equivalent reactor designs. Journal of Analytical and Applied Pyrolysis 162, 105465 (2022).
#               source 3: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
#               source 4: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
# original value (units): unitless
#  poultry value (units): (10000 MJ/ton syngas * 0.18 ton syngas/ton feedstock -939 MJ/ton feedstock) * 1e-12 * 1e6 = 0.000861 EJ natural gas/Mt feedstock (processed at 500 C)
#  poultry value (units): 15000 MJ/ton bio-oil * 0.26 ton bio-oil/ton feedstock * 1e-12 * 1e6 = 0.0039 EJ manure fuel feedstock/Mt feedstock (processed at 500 C)
#  poultry value (units): heating requirement of 939 MJ/ton feedstock
tmp[4] <- "# Column types: ccccnnn"
tmp[10] <- "poultry_biochar,biochar,slow pyrolysis,manure fuel feedstock,0.0039,0.0039,0.0039"
tmp[11] <- "beef_biochar,biochar,slow pyrolysis,manure fuel feedstock,0.00477,0.00477,0.00477" # yield of 31.82% [2], but no gas/bio-oil HHV present, so use values from [1]
tmp[12] <- "pork_biochar,biochar,slow pyrolysis,manure fuel feedstock,0.00525,0.00525,0.00525" # yield of 35% [3], but no bio-oil HHV present
tmp[13] <- "dairy_biochar,biochar,slow pyrolysis,manure fuel feedstock,0.00525,0.00525,0.00525" #yield of 35% [4], but no gas/bio-oil HHV present, so use values from [1]
tmp[14] <- "goat_biochar,biochar,slow pyrolysis,manure fuel feedstock,0.00525,0.00525,0.00525" #yield of 35% [3], but no bio-oil HHV present
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.rsrc_info.csv
example_file <- find_csv_file("energy/A21.rsrc_info", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source 1: A21.rsrc_info
# original value (units): EJ
#     used value (units): EJ
tmp[8] <- "manure fuel feedstock,regional,EJ,1975$/GJ"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.globaltech_cost.csv
example_file <- find_csv_file("energy/A21.globaltech_cost", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source 1: Bridgwater, A. V., Toft, A. J. & Brammer, J. G. A techno-economic comparison of power production by biomass fast pyrolysis with gasification and combustion. Renewable and Sustainable Energy Reviews 6, 181–246 (2002).
#               source 2: Bora, R. R. et al. Techno-Economic Feasibility and Spatial Analysis of Thermochemical Conversion Pathways for Regional Poultry Waste Valorization. ACS Sustainable Chem. Eng. 8, 5763–5775 (2020).
#               source 3: Santos, T. M., Silva, W. R. da, Carregosa, J. de C. & Wisniewski, A. Comprehensive characterization of cattle manure bio-oil for scale-up assessment comparing non-equivalent reactor designs. Journal of Analytical and Applied Pyrolysis 162, 105465 (2022).
#               source 4: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
#               source 5: A22.globaltech_retirement (halflife of 30 years)
#               source 6: KPMG. Cost of Capital Study 2022. (2022).
#               source 7: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
#               source 8: Lima, I. M., McAloon, A. & Boateng, A. A. Activated carbon from broiler litter: Process description and cost of production. Biomass and Bioenergy 32, 568–572 (2008).
#               source 9: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
# original value (units): cost curves are ignored, so a facility size with 1,980 tons per month (3 dry tons per hour) [1], 9% annual TPC as OPEX [2], with input already given in kg
#          capital costs: 40.8*(3*1000)^0.6194 = TPC
#        operating costs: sum_n=1^30 {0.09*TPC+1.04*3^0.475}/(1+0.07)^n = OPEX
#     biochar production: 3 (tons/hr) * 24 (hours/day) * 330 (days/year) [8] * 0.47 (biochar yield) [4] *1000kg/ton = 11167200 - poultry
#     biochar production: 3 (tons/hr) * 24 (hours/day) * 330 (days/year) [8] * 0.468 (biochar yield) [9] *1000kg/ton = 11119680 - pork
#     biochar production: 3 (tons/hr) * 24 (hours/day) * 330 (days/year) [8] * 0.4584 (biochar yield) [3] *1000kg/ton = 10891584 - beef
#     biochar production: 3 (tons/hr) * 24 (hours/day) * 330 (days/year) [8] * 0.475 (biochar yield) [7] *1000kg/ton = 11286000 - dairy
#        converted costs: (TPC + OPEX)*1000 (to convert from kEuros to Euros) /0.9233 (to 2000$) * 0.32 (to 1975$) = $4,272,142.60 - to EAUW: $344,276.1
tmp[14] <- "poultry_biochar,biochar,slow pyrolysis,non-energy,0.0308,0.0308"
tmp[15] <- "pork_biochar,biochar,slow pyrolysis,non-energy,0.0310,0.0310"
tmp[16] <- "beef_biochar,biochar,slow pyrolysis,non-energy,0.0316,0.0316"
tmp[17] <- "dairy_biochar,biochar,slow pyrolysis,non-energy,0.0305,0.0305"
tmp[18] <- "goat_biochar,biochar,slow pyrolysis,non-energy,0.0123,0.0123"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.globaltech_coef.csv
example_file <- find_csv_file("energy/A21.globaltech_coef", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source 1: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
#               source 2: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
#               source 3: Santos, T. M., Silva, W. R. da, Carregosa, J. de C. & Wisniewski, A. Comprehensive characterization of cattle manure bio-oil for scale-up assessment comparing non-equivalent reactor designs. Journal of Analytical and Applied Pyrolysis 162, 105465 (2022).
#               source 4: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).
# original value (units): unitless
#     used value (units): 47% yield implies 2.1276 Mt feedstock / Mt biochar
tmp[15] <- "poultry_biochar,biochar,slow pyrolysis,poultry manure,2.1276,2.1276,2.1276" #[1]
tmp[16] <- "pork_biochar,biochar,slow pyrolysis,pork manure,2.136,2.136,2.136" # [4]
tmp[17] <- "beef_biochar,biochar,slow pyrolysis,beef manure,2.1815,2.1815,2.1815" #[3]
tmp[18] <- "dairy_biochar,biochar,slow pyrolysis,dairy manure,2.1052,2.1052,2.1052" #[2]
tmp[19] <- "goat_biochar,biochar,slow pyrolysis,goat manure,2.055,2.055,2.055" #[4]
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.globaltech_shrwt.csv
example_file <- find_csv_file("energy/A21.globaltech_shrwt", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
tmp[4] <- "# Column types: ccciiii"
tmp[6] <- "supplysector,subsector,technology,1971,2015,2020,2100"
tmp[7] <- "regional biomass,regional biomass,regional biomass,1,1,1,1"
tmp[8] <- "regional corn for ethanol,regional corn for ethanol,regional corn for ethanol,1,1,1,1"
tmp[9] <- "regional sugar for ethanol,regional sugar for ethanol,regional sugar for ethanol,1,1,1,1"
tmp[10] <- "regional biomassOil,regional biomassOil,biomassOil,0,0,0,0"
tmp[11] <- "regional biomassOil,regional biomassOil,OilCrop,0,0,0,0"
tmp[12] <- "regional biomassOil,regional biomassOil,OilPalm,0,0,0,0"
tmp[13] <- "regional biomassOil,regional biomassOil,Soybean,0,0,0,0"
#               source 1: A322.globaltech_shrwt
# original value (units): same assumptions as fertilizer production from hydrogen
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[14] <- "poultry_biochar,biochar,slow pyrolysis,0,0,1,1"
tmp[15] <- "pork_biochar,biochar,slow pyrolysis,0,0,1,1"
tmp[16] <- "beef_biochar,biochar,slow pyrolysis,0,0,1,1"
tmp[17] <- "dairy_biochar,biochar,slow pyrolysis,0,0,1,1"
tmp[18] <- "goat_biochar,biochar,slow pyrolysis,0,0,1,1"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.globaltech_interp.csv
example_file <- find_csv_file("energy/A21.globaltech_interp", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source 1: A322.globaltech_shrwt
#               source 2: Woolf, D., Amonette, J. E., Street-Perrott, F. A., Lehmann, J. & Joseph, S. Sustainable biochar to mitigate global climate change. Nat Commun 1, 56 (2010).
# original value (units): s-curve following [2]
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[9] <- "poultry_biochar,biochar,slow pyrolysis,share-weight,initial-future-year,end-year,,fixed"
tmp[10] <- "pork_biochar,biochar,slow pyrolysis,share-weight,initial-future-year,end-year,,fixed"
tmp[11] <- "beef_biochar,biochar,slow pyrolysis,share-weight,initial-future-year,end-year,,fixed"
tmp[12] <- "dairy_biochar,biochar,slow pyrolysis,share-weight,initial-future-year,end-year,,fixed"
tmp[13] <- "goat_biochar,biochar,slow pyrolysis,share-weight,initial-future-year,end-year,,fixed"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.subsector_interp
example_file <- find_csv_file("energy/A21.subsector_interp", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A322.globaltech_shrwt
# original value (units): same assumptions as fertilizer production from hydrogen
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[10] <- "poultry_biochar,biochar,share-weight,initial-future-year,end-year,,fixed,0" #TODO allowed traded
tmp[11] <- "pork_biochar,biochar,share-weight,initial-future-year,end-year,,fixed,0"
tmp[12] <- "beef_biochar,biochar,share-weight,initial-future-year,end-year,,fixed,0"
tmp[13] <- "dairy_biochar,biochar,share-weight,initial-future-year,end-year,,fixed,0"
tmp[14] <- "goat_biochar,biochar,share-weight,initial-future-year,end-year,,fixed,0"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.subsector_shrwt
example_file <- find_csv_file("energy/A21.subsector_shrwt", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A322.globaltech_shrwt
# original value (units): same assumptions as fertilizer production from hydrogen
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[11] <- "poultry_biochar,biochar,initial-future-year,,1,0" #TODO added trading
tmp[12] <- "pork_biochar,biochar,initial-future-year,,1,0"
tmp[13] <- "beef_biochar,biochar,initial-future-year,,1,0"
tmp[14] <- "dairy_biochar,biochar,initial-future-year,,1,0"
tmp[15] <- "goat_biochar,biochar,initial-future-year,,1,0"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A21.sector
example_file <- find_csv_file("energy/A21.sector", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source 1: A21.Sector
# original value (units): Mt, because the primary output of this sector is the biochar which is used as a mass input to fertilizer production, and input from poultry is also in Mt
#     used value (units): otherwise, use same logit.exponents as the other considered technologies.
tmp[12] <- "poultry_biochar,Mt,Mt,1975$/kg,-3,0," #primary output is biochar
tmp[13] <- "pork_biochar,Mt,Mt,1975$/kg,-3,0," #primary output is biochar
tmp[14] <- "beef_biochar,Mt,Mt,1975$/kg,-3,0," #primary output is biochar
tmp[15] <- "dairy_biochar,Mt,Mt,1975$/kg,-3,0," #primary output is biochar
tmp[16] <- "goat_biochar,Mt,Mt,1975$/kg,-3,0," #primary output is biochar
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)


#modify A21.subsector_logit
example_file <- find_csv_file("energy/A21.subsector_logit", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A21.subsector_logit
# original value (units): same values as other supply sectors
#     used value (units):
tmp[11] <- "poultry_biochar,biochar,-6,0,"
tmp[12] <- "pork_biochar,biochar,-6,0,"
tmp[13] <- "beef_biochar,biochar,-6,0,"
tmp[14] <- "dairy_biochar,biochar,-6,0,"
tmp[15] <- "goat_biochar,biochar,-6,0,"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



### CHANGES TO A22 (Refining) ###
# supplysector    subsector     technology    input.name
# refining         biomass liquids  manure fuel   manure fuel feedstock

#modify A22.globaltech_input_driver
example_file <- find_csv_file("energy/A22.globaltech_input_driver", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A21.secout.csv
# original value (units): secondary output to refining is manure fuel feedstock, so that is what is used as the input here
#     used value (units):
tmp[24] <- "refining,biomass liquids,manure fuel,manure fuel feedstock"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A22.globaltech_cost
example_file <- find_csv_file("energy/A22.globaltech_cost", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: Janarthanam, H. et al. Production and experimental analysis of poultry litter biofuel in DI diesel engine. AIP Conference Proceedings 2311, 020015 (2020).
# original value (units): poultry manure bio-oil is primary used as bio-diesel, so we use the same costs as associated with processing biodiesel
#     used value (units):
tmp[27] <- "refining,biomass liquids,manure fuel,non-energy,1.88,1.88,1.88,,,"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A22.globaltech_shrwt
example_file <- find_csv_file("energy/A22.globaltech_shrwt", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A322.globaltech_shrwt
# original value (units): same assumptions as fertilizer production from hydrogen
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[28] <- "refining,biomass liquids,manure fuel,0,0,1,1,1,1"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A22.globaltech_interp
example_file <- find_csv_file("energy/A22.globaltech_interp", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A322.globaltech_shrwt
# original value (units): same assumptions as fertilizer production from hydrogen
#     used value (units): same assumptions as fertilizer production from hydrogen
tmp[13] <- "refining,biomass liquids,manure fuel,share-weight,initial-future-year,end-year,fixed"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A22.globaltech_coef
example_file <- find_csv_file("energy/A22.globaltech_coef", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A22.globaltech_coef
# original value (units): follows biodiesel in A22.globaltech_coef (since the bio-oil is being upgraded into biodiesel too I guess)
#     used value (units):
tmp[33] <- "refining,biomass liquids,manure fuel,manure fuel feedstock,1.0309,1.0309,1.03"
tmp[34] <- "refining,biomass liquids,manure fuel,wholesale gas,0.057671,0.057671,0.06"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A22.globaltech_retirement
example_file <- find_csv_file("energy/A22.globaltech_retirement", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A22.globaltech_retirement
# original value (units): same values as other biomass liquids technologies
#     used value (units):
tmp[42] <- "refining,biomass liquids,manure fuel,inital-future-year,45,,30,0.3,-0.1,10"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)

#A22.globaltech_emissions is not modified because carbon capture happens in A_PrimaryFuelCCoef.csv




### CHANGES TO A51 (emissions) ###
#modify A51.min_coeff
example_file <- find_csv_file("emissions/A51.min_coeff", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A51.min_coeff
# original value (units): refining same emissions as all other refining techs
#     used value (units):
tmp[283] <- "refining,biomass liquids,manure fuel,0.0075,0.0054,0.002,0,0,0"

print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A51.steepness
example_file <- find_csv_file("emissions/A51.steepness", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A51.steepness
# original value (units): refining same emissions as all other refining techs
#     used value (units): fertilizer embodies the emissions from pyrolysis, since emissions cannot be applied to a pass through sector
tmp[280] <- "refining,biomass liquids,manure fuel,3.5,3.5,3.5,3.5,3.5,3.5"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A51.max_reduction
example_file <- find_csv_file("emissions/A51.max_reduction", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A51.max_reduction
# original value (units): refining same emissions as all other refining techs
#     used value (units): fertilizer embodies the emissions from pyrolysis, since emissions cannot be applied to a pass through sector
tmp[188] <- "refining,biomass liquids,manure fuel,25,46,80,50,50,60"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A41.tech_coeff
#this is where I assume the emissions factors for pyrolysis itself should kept.  Refining emissions included too because lmao there's already a lot of refining techs here
example_file <- find_csv_file("emissions/A41.tech_coeff", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A41.tech_coeff
# original value (units): refining same emissions as all other refining techs (kg per GJ?, except biochar is in Mt)
#     used value (units): biochar_sup takes emissions (non-CO2) for the production of pyrolysis
#                   note: specific species of carbon (CO, CH4) are not included here because openLCA results are in kg CO2-eq, which is included in the next file
# from previous research: 13,894 kg SO2-eq, -141,067,036 kg CO2-eq, 9,283 kg NOx (particulate matter formation, human health) for the processing of 162732000 kg manure
# from previous reserach: assuming BC is black carbon/particulates, 5,992 kg PM2.5-eq from 162,732,000 kg manure
tmp[39] <- "refining,biomass liquids,manure fuel,0.010085379,0.01,0.01005704,,0.0001,,0.00003682,0.0001,,,"
#emissions for the pyrolysis are added here to the base refining tech, although they do not introduce any significant changes

print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



#modify A_PrimaryFuelCCoef.csv
#this is where I assume the emissions factors for pyrolysis itself should kept.
example_file <- find_csv_file("emissions/A_PrimaryFuelCCoef.csv", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
# using approach 3 from [0] as it has the highest amount of carbon sequestration for the highest accuracy and quantifiability
#               source 0: Lehmann, J. et al. Biochar in climate change mitigation. Nat. Geosci. 14, 883–892 (2021).
#               source 1: Leng, L., Huang, H., Li, H., Li, J. and Zhou, W., 2019. Biochar stability assessment methods: a review. Science of the total environment, 647, pp.210-222.
#               source 2: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
#               source 3: Atienza-Martínez, M., Ábrego, J., Gea, G. & Marías, F. Pyrolysis of dairy cattle manure: evolution of char characteristics. Journal of Analytical and Applied Pyrolysis 145, 104724 (2020).
#               source 4: Enders, A., Hanley, K., Whitman, T., Joseph, S. & Lehmann, J. Characterization of biochars to evaluate recalcitrance and agronomic performance. Bioresource Technology 114, 644–653 (2012).
#               source 5: Poddar, S. & Sarat Chandra Babu, J. Modelling and optimization of a pyrolysis plant using swine and goat manure as feedstock. Renewable Energy 175, 253–269 (2021).

# original value (units): (Mt C per Mt manure supply)
#     used value (units): Carbon sequestration potential of biochar as calculated by Leng - other emissions for natural gas, etc., are embodied in refining emissiosn
# Poultry: (-63.5*(0.3 H/C atomic ratio) + 104) * 782 [C mass percentage] / 100 = .664
#    Pork: (-63.5*(1.96 [H atomic ratio] / (38.6/12) [C atomic ratio]) + 104)*.386 [C mass percentage] / 100 = .252
#    Beef: (-63.5*(2.6 [H atomic ratio] / (74.1/12) [C atomic ratio]) + 104)*.741 [C mass percentage] / 100 = .572
#   Dairy: (-63.5*(.85 [H atomic ratio] / (39.6/12) [C atomic ratio]) + 104)*.396 [C mass percentage] / 100 = .347
#    Goat: (-63.5*(1.88 [H atomic ratio] / (42.0/12) [C atomic ratio]) + 104)*.420 [C mass percentage] / 100 = .293

# original value (units): (Mt C per Mt manure supply)
#     used value (units): avoided biomass N2O CO2 CH4
#               source 6: Woolf, D., Amonette, J. E., Street-Perrott, F. A., Lehmann, J. & Joseph, S. Sustainable biochar to mitigate global climate change. Nat Commun 1, 56 (2010).
# Poultry: 2.44 g C avoided decomposition per g C sequestered in biochar [6]
#    Pork: 4.36 g C avoided decomposition per g C sequestered in biochar [6]
#    Beef: 2.54 g C avoided decomposition per g C sequestered in biochar [6]
#   Dairy: 2.54 g C avoided decomposition per g C sequestered in biochar (same as beef)
#    Goat: 2.54 g C avoided decomposition per g C sequestered in biochar (same as beef)

tmp[31] <- "poultry manure,-1.073,0" # .664 * (1 + 2.44) * .47 [2] (yield)
tmp[32] <- "pork manure,-0.632,0" # .252 * (1 + 4.36) * .468 [yield] [5]
tmp[33] <- "beef manure,-0.927,0" # .572 * (1 + 2.54) * .4584 [yield] [4]
tmp[34] <- "dairy manure,-0.583,0" # .347 * (1 + 2.54) * .475 [yield] [3]
tmp[35] <- "goat manure,-1.376,0" # .293 * (1 + 2.54) * .486 [yield] [5]
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)


### update xml files ###
devtools::load_all()
driver_drake()
