devtools::load_all()

### ADDITIONAL FILES DATA + SOURCES
## A_an_secout
#               source 1: Bentley, J. A. et al. Economics of Dairy Manure Management in Iowa. Iowa State University Animal Industry Report 13, (2016).
#               source 2: Malone, G. W. Nutrient Enrichment in integrated Broiler Production Systems. Poultry Science 71, 1117–1122 (1992).
#               source 3: https://www.fao.org/3/i6421e/i6421e.pdf
#               source 4: https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=201401&year2=197501
#               source 5: https://www.fao.org/3/t0279e/T0279E05.htm
#               source 9: Lefebvre, D. et al. Biomass residue to carbon dioxide removal: quantifying the global impact of manure_fuel. manure_fuel 5, 65 (2023).
#        poultry (units): 0.0273 (kg collectible manure solids /day /head) [9] * 1 (head) / 1.008 (kg meat/head) [3] * 51 day lifespan [2] = 1.381 Mt manure/Mt Poultry
#          dairy (units): 0.5391 (kg collectible manure solids /day /head) [9] * 1 (head) * 365 (days) / (23,578 (lbs milk/head/year) [1] * 0.453592 (kg/lbs))= 0.018 Mt manure/Mt dairy product
#           beef (units): 0.5391 (kg collectible manure solids /day /head) [9] * 1 (head) / 228 (kg meat/head) [5] * 3 (year lifespan) * 365 (days) [5] = 2.589 Mt manure/Mt Beef
#           pork (units): 0.0930 (kg collectible manure solids /day /head) [9] * 1 (head) / 55.76 (kg meat/head) [5] * 0.5 (year lifespan) * 365 (days) [5] = 0.304 Mt manure/Mt Pork
#           goat (units): 0.2433 (kg collectible manure solids /day /head) [9] * 1 (head) / 19.1 (kg meat/head) [5] * .667 (year lifespan) * 365 (days) [5] = 3.101 Mt manure/Mt Goat


## A_An_secout_prices:
# manure prices
#               source 1: Bentley, J. A. et al. Economics of Dairy Manure Management in Iowa. Iowa State University Animal Industry Report 13, (2016).
#               source 2: Bora, R. R. et al. Techno-Economic Feasibility and Spatial Analysis of Thermochemical Conversion Pathways for Regional Poultry Waste Valorization. ACS Sustainable Chem. Eng. 8, 5763-5775 (2020).
#               source 3: Baniasadi, M. et al. Waste to energy valorization of poultry litter by slow pyrolysis. Renewable Energy 90, 458–468 (2016).
#               source 4: https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1&year1=202001&year2=197501
#            all (units): 73.42 (2014$/cow/year) [1] * 1 (cow*year) / 0.5391 (kg collectible manure solids /day /head) [9] *365 (days) * 0.22 (1975$/2014$) [4] = 0.082 1975$/kg

## A21.secout_prices - don't need for this scenario
# manure_fuel: 330 2020$/ton bio-oil [2] / 15 GJ/ton bio-oil [3] *.20 (1975$/2020$) [4] = 4.40 $1975/GJ

### CHANGES TO A21 ###

#don't modify A21.rsrc_info b/c it controls secondary outputs, which there are none for this scenario

#modify A21.globaltech_cost.csv
example_file <- find_csv_file("energy/A21.globaltech_cost", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)

#               source: plant_costs.xlsx
tmp[14] <- "manure_fuel,manure_fuel,slow pyrolysis_poultry,non-energy,0.0557,0.0557"
tmp[15] <- "manure_fuel,manure_fuel,slow pyrolysis_pork,non-energy,0.0414,0.0414"
tmp[16] <- "manure_fuel,manure_fuel,slow pyrolysis_beef,non-energy,0.0455,0.0455"
tmp[17] <- "manure_fuel,manure_fuel,slow pyrolysis_dairy,non-energy,0.0414,0.0414"
tmp[18] <- "manure_fuel,manure_fuel,slow pyrolysis_goat,non-energy,0.0414,0.0414"
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
# original value (units): GJ/kg feedstock
#     used value (units): yield from plant_costs.csv
tmp[15] <- "manure_fuel,manure_fuel,slow pyrolysis_poultry,poultry manure,986,986,986" #[1]
tmp[16] <- "manure_fuel,manure_fuel,slow pyrolysis_pork,pork manure,732,732,732" # [4]
tmp[17] <- "manure_fuel,manure_fuel,slow pyrolysis_beef,beef manure,805,805,805" #[3]
tmp[18] <- "manure_fuel,manure_fuel,slow pyrolysis_dairy,dairy manure,732,732,732" #[2]
tmp[19] <- "manure_fuel,manure_fuel,slow pyrolysis_goat,goat manure,732,732,732" #[4]
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
tmp[14] <- "manure_fuel,manure_fuel,slow pyrolysis_beef,0,0,1,1"
tmp[15] <- "manure_fuel,manure_fuel,slow pyrolysis_dairy,0,0,1,1"
tmp[16] <- "manure_fuel,manure_fuel,slow pyrolysis_goat,0,0,1,1"
tmp[17] <- "manure_fuel,manure_fuel,slow pyrolysis_pork,0,0,1,1"
tmp[18] <- "manure_fuel,manure_fuel,slow pyrolysis_poultry,0,0,1,1"
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
tmp[9] <- "manure_fuel,manure_fuel,slow pyrolysis_beef,share-weight,initial-future-year,end-year,,fixed"
tmp[10] <- "manure_fuel,manure_fuel,slow pyrolysis_dairy,share-weight,initial-future-year,end-year,,fixed"
tmp[11] <- "manure_fuel,manure_fuel,slow pyrolysis_goat,share-weight,initial-future-year,end-year,,fixed"
tmp[12] <- "manure_fuel,manure_fuel,slow pyrolysis_pork,share-weight,initial-future-year,end-year,,fixed"
tmp[13] <- "manure_fuel,manure_fuel,slow pyrolysis_poultry,share-weight,initial-future-year,end-year,,fixed"
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
tmp[10] <- "manure_fuel,manure_fuel,share-weight,initial-future-year,end-year,,fixed,0" #TODO allowed traded
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
tmp[11] <- "manure_fuel,manure_fuel,initial-future-year,,1,0"
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
# original value (units): EJ, because the primary output of this sector is the manure_fuel which is used as a mass input to fertilizer production, and input from poultry is also in Mt
#     used value (units): otherwise, use same logit.exponents as the other considered technologies.
tmp[12] <- "manure_fuel,EJ,EJ,1975$/GJ,-3,0," #primary output is manure_fuel
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
tmp[11] <- "manure_fuel,manure_fuel,-6,0,"
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)



### CHANGES TO A22 (Refining) ###
# supplysector    subsector     technology    input.name
# refining         biomass liquids  manure_fuel   manure_fuel

#modify A22.globaltech_input_driver
example_file <- find_csv_file("energy/A22.globaltech_input_driver", FALSE)[[1]]
file.copy(from = example_file, to = paste0(example_file, ".bak"))

# Change one value in file, then rewrite to same path
tmp <- readr::read_lines(example_file)
print("\n file before changes")
print(tmp)
#               source 1: A21.secout.csv
# original value (units): secondary output to refining is manure_fuel, so that is what is used as the input here
#     used value (units):
tmp[24] <- "refining,biomass liquids,manure_fuel,manure_fuel"
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
tmp[27] <- "refining,biomass liquids,manure_fuel,non-energy,1.88,1.88,1.88,,,"
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
tmp[28] <- "refining,biomass liquids,manure_fuel,0,0,1,1,1,1"
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
tmp[13] <- "refining,biomass liquids,manure_fuel,share-weight,initial-future-year,end-year,fixed"
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
tmp[33] <- "refining,biomass liquids,manure_fuel,manure_fuel,1.0309,1.0309,1.03"
tmp[34] <- "refining,biomass liquids,manure_fuel,wholesale gas,0.057671,0.057671,0.06"
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
tmp[42] <- "refining,biomass liquids,manure_fuel,inital-future-year,45,,30,0.3,-0.1,10"
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
tmp[283] <- "refining,biomass liquids,manure_fuel,0.0075,0.0054,0.002,0,0,0"

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
tmp[280] <- "refining,biomass liquids,manure_fuel,3.5,3.5,3.5,3.5,3.5,3.5"
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
tmp[188] <- "refining,biomass liquids,manure_fuel,25,46,80,50,50,60"
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
# original value (units): refining same emissions as all other refining techs (kg per GJ?, except manure_fuel is in Mt)
#     used value (units): manure_fuel takes emissions (non-CO2) for the production of pyrolysis
#                   note: specific species of carbon (CO, CH4) are not included here because openLCA results are in kg CO2-eq, which is included in the next file
# from previous research: 13,894 kg SO2-eq, -141,067,036 kg CO2-eq, 9,283 kg NOx (particulate matter formation, human health) for the processing of 162732000 kg manure
# from previous reserach: assuming BC is black carbon/particulates, 5,992 kg PM2.5-eq from 162,732,000 kg manure
tmp[39] <- "refining,biomass liquids,manure_fuel,0.010085379,0.01,0.01005704,,0.0001,,0.00003682,0.0001,,,"
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

# original value (units): (Mt C per Mt manure supply)
#     used value (units): avoided biomass N2O CO2 CH4
#               source 6: Woolf, D., Amonette, J. E., Street-Perrott, F. A., Lehmann, J. & Joseph, S. Sustainable biochar to mitigate global climate change. Nat Commun 1, 56 (2010).
# Poultry: 2.44 g C avoided decomposition per g C sequestered in biochar [6]
#    Pork: 4.36 g C avoided decomposition per g C sequestered in biochar [6]
#    Beef: 2.54 g C avoided decomposition per g C sequestered in biochar [6]
#   Dairy: 2.54 g C avoided decomposition per g C sequestered in biochar (same as beef)
#    Goat: 2.54 g C avoided decomposition per g C sequestered in biochar (same as beef)

tmp[31] <- "poultry manure,-.160,0" # (1.63e9 [avoided Mg C] + 1.23e9 [net sequestered Mg C]) / 94 Tg *1000000 Mg/Tg [manure supply /year] * 100 years [beta secenario in 6, supplemental SI, supplemental .xlsx]
tmp[32] <- "pork manure,-.425,0" # (2.76e9 [avoided Mg C] + 9.01e8 [net sequestered Mg C]) / 63 Tg *1000000 Mg/Tg * 100 years
tmp[33] <- "beef manure,-.147,0" # (4.70e9 [avoided Mg C] + 3.33e9 [net sequestered Mg C]) / 294 Tg*1000000 Mg/Tg* 100 years
tmp[34] <- "dairy manure,-.147,0" # (4.70e9 [avoided Mg C] + 3.33e9 [net sequestered Mg C]) / 294 Tg*1000000 Mg/Tg* 100 years
tmp[35] <- "goat manure,-.425,0" # (same as swine)
print("\n file after changes")
print(tmp)
readr::write_lines(tmp, example_file)


### update xml files ###
devtools::load_all()
driver_drake()
