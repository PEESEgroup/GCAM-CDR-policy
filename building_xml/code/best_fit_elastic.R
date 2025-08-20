library(pracma)

AIM_19_Cprice <- c(0, 3.64895, 25.50257, 570.00273, 1129.58132, 1639.50747, 2717.42901, 3392.36118, 4006.11123, 4382.32382, 4544.59438)
AIM_19_CDR <- c(0, 0, 0, 1999.27, 5900.007, 14644.779, 14198.607, 15403.617, 15984.186, 16699.087, 17693.129)
AIM_19_Emissions <- c(34373.935, 38205.41, 43338.076, 20138.552, 8223.192, 399.238, -4896.106, -7038.618, -7989.183, -8407.267, -8986.86)
GCAM_19_Cprice <- c(0, 0, 0, 94.27985, 260.83897, 424.88474, 692.00792, 1127.57732, 1836.55745, 2991.16205, 4872.34357)
GCAM_19_CDR <- c(0, 1813.315, 2538.611, 6355.715, 16501.207, 21107.522, 23090.494, 23796.549, 25214.182, 29787.47, 37466.046)
GCAM_19_Emissions <- c(0, 35775.429, 41337.663, 36001.981, 9535.74, -7452.197, -13187.103, -14127.611, -18177.965, -23522.443, -31683.696)
REMIND_19_Cprice <-c(0, 0, 12.24611, 297.761, 965.928, 1568.965, 2798.92, 3854.36, 6254.15, 9936.5, 15409.09)
REMIND_19_CDR <-c(0, 0, 2.49, 1020, 8130, 12800, 14100, 14800, 15400, 15700, 15900)
REMIND_19_Emissions <-c(35090, 37010, 42310, 31110, 8623, -7250, -10480, -12620, -13640, -13240, -14180)

AIM_34_Cprice <- c(0, 10.23877, 26.07705, 54.0078, 97.93381, 124.8158, 171.80292, 221.47206, 282.79446, 345.26248, 414.57917)
GCAM_34_Cprice <- c(0, 0, 0, 0, 72.94226, 118.81549, 193.53797, 315.25425, 513.51498, 836.46292, 1362.50958)
IMAGE_34_Cprice <- c(0, 0, 0, 0, 82.49299, 163.82366, 261.89274, 300.60167, 626.79108, 864.60409, 505.15162)
REMIND_34_Cprice <- c(0, 0, 12.24611, 32.9324, 83.3497, 135.6875, 240.313, 332.33, 538.909, 847.024, 1320.135)
WITCH_34_Cprice <- c(0, 0, 11.00363, 129.44337, 205.12944, 359.62615, 592.06009, 929.522, 1404.66539, 2055.94702, 2927.64527)
AIM_34_CDR <- c(0, 0, 0, 404.484, 3314.264, 7996.719, 14266.959, 18548.475, 21405.461, 22750.365, 24146.946)
GCAM_34_CDR <- c(0, 1813.315, 2539.362, 3488.421, 5788.717, 9794.48, 14039.781, 17881.797, 21823.41, 24310.683, 25691.698)
IMAGE_34_CDR <- c(0, 0, 3.261, 360.319, 2276.436, 4677.586, 8551.529, 11140.517, 14094.723, 19365.635, 23038.692)
REMIND_34_CDR <- c(0, 0, 2.49, 239, 2150, 7190, 11700, 13800, 14300, 14400, 14600)
WITCH_34_CDR <- c(3.075, 1.358, 199.113, 2331.023, 4560.211, 6738.694, 9106.811, 12868.552, 16221.647, 20477.616, 16482.092)

years <- c(2005, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100)
AIM_19_elastic <- data.frame(cprice = AIM_19_Cprice, CDR = AIM_19_CDR)
GCAM_19_elastic <- data.frame(cprice = GCAM_19_Cprice, CDR = GCAM_19_CDR)
REMIND_19_elastic <- data.frame(cprice = REMIND_19_Cprice, CDR = REMIND_19_CDR)

AIM_34_elastic <- data.frame(cprice = AIM_34_Cprice, CDR = AIM_34_CDR)
GCAM_34_elastic <- data.frame(cprice = GCAM_34_Cprice, CDR = GCAM_34_CDR)
IMAGE_34_elastic <- data.frame(cprice = IMAGE_34_Cprice, CDR = IMAGE_34_CDR)
REMIND_34_elastic <- data.frame(cprice = REMIND_34_Cprice, CDR = REMIND_34_CDR)
WITCH_34_elastic <- data.frame(cprice = WITCH_34_Cprice, CDR = WITCH_34_CDR)

### Log fit - be sure to use quotes around the variable names in
### the call
log.fit <- function(dep, ind, yourdata, model_name){
  #Self-starting ...

  y <- yourdata[, dep]
  x <- yourdata[, ind]

  log.ss <- nls(y ~ SSlogis(x, phi1, phi2, phi3))
  print(summary(log.ss))

  #C
  C <- summary(log.ss)$coef[1]
  #a
  A <- summary(log.ss)$coef[2]
  A_1 <- exp((summary(log.ss)$coef[2]) * (1/summary(log.ss)$coef[3]))
  #k
  K <- (1 / summary(log.ss)$coef[3])

  plot(y ~ x, main = paste("Logistic Function -", model_name), xlab=ind, ylab=dep)
  lines(0:max(x), predict(log.ss, data.frame(x=0:max(x))), col="red")
  x_2 <- linspace(0, max(x), 500)
  y_2 <- C / (1 + exp((0-K) * (x_2 - A)))
  lines(x_2,y_2, col="blue")

  r1 <- sum((x - mean(x))^2)
  r2 <- sum(residuals(log.ss)^2)

  r_sq <- (r1 - r2) / r1

  out <- data.frame(cbind(c(C=C, a=A, k=K, R.value=sqrt(r_sq))))
  names(out)[1] <- paste("Logistic Curve -", model_name)

  return(out)
}

AIM19_out = log.fit("CDR", "cprice", AIM_19_elastic, "AIM SSP2 1.9")
GCAM19_out = log.fit("CDR", "cprice", GCAM_19_elastic, "GCAM SSP2 1.9")
REMIND19_out = log.fit("CDR", "cprice", REMIND_19_elastic, "REMIND SSP2 1.9")

AIM34_out = log.fit("CDR", "cprice", AIM_34_elastic, "AIM SSP2 3.4")
GCAM34_out = log.fit("CDR", "cprice", GCAM_34_elastic, "GCAM SSP2 3.4")
IMAGE34_out = log.fit("CDR", "cprice", IMAGE_34_elastic, "IMAGE SSP2 3.4")
REMIND34_out = log.fit("CDR", "cprice", REMIND_34_elastic, "REMIND SSP2 3.4")
WITCH34_out = log.fit("CDR", "cprice", WITCH_34_elastic, "WITCH SSP2 3.4")

print(AIM19_out)
print(GCAM19_out)
print(REMIND19_out)

print(AIM34_out)
print(GCAM34_out)
print(IMAGE34_out)
print(REMIND34_out)
print(WITCH34_out)
