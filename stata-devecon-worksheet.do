** author: George Tyler
** project: Development Economics Assignment 1
**Section 1: wbdr.dta
use "/Users/georgetyler/Documents/Documents – George’s MacBook Pro (2)/University/Melbourne 19-20/ECON40012/Assignment 1/wbdr.dta"
**EXTERNAL PACKAGES: estout, univar
**Question 1.1
estpost sum gnppc illit_f illit_m mort_inf
esttab ., cells("mean sd"), using a1tables.tex, label  title (World Bank Development Report) append
**Question 1.2 and 1.3
preserve
	drop if missing(gnppc)
	sum mort_inf illit_t, detail
	gsort gnppc
	estpost sum in 1/50
	esttab ., cells("mean min max"), using a1tables.tex, label  title(Top 50) append
	estpost sum in -50/l
	esttab ., cells("mean min max"), using a1tables.tex, label  title(Bottom 50) append
	univar gnppc
	hist gnppc
restore

**Question 1.4-1.6
reg illit_t gnppc
esttab using a1tables.tex, label  title(Regression 1.4\label{Reg1.4}) append
reg mort_inf gnppc
esttab using a1tables.tex, label  title(Regression 1.4\label{Reg1.4}) append
reg mort_inf illit_t
esttab using a1tables.tex, label  title(Regression 1.5\label{Reg1.5}) append 
twoway scatter mort_inf illit_t || lfit mort_inf illit_t 

**Question 4
use "/Users/georgetyler/Documents/Documents – George’s MacBook Pro (2)/University/Melbourne 19-20/ECON40012/Assignment 1/supas.dta"
**Question 4.a: DD estimation yeduc
preserve
	drop if intermed
	drop if veryold
	gen high_young = high*young
	reg yeduc high young high_young, r
**Question 4.b: DD estimation lwage
	reg lhwage high young high_young, r
	esttab using a1tables.tex, label  title(Regression 4b\label{Reg4b}) append 
restore
**Question 4.c: Indirect Least Squares
preserve
	gen educ_yng = yeduc if young==1
	gen educ_old = yeduc if old==1
	gen lhwage_yng = lhwage if young==1
	gen lhwage_old = lhwage if old==1
	collapse (mean) educ_old educ_yng lhwage_old lhwage_yng ch71 prog_int, by(ROB)
	gen educ_dif = educ_yng - educ_old 
	gen wage_dif = lhwage_yng - lhwage_old 
	reg educ_dif prog_int ch71, r 
	esttab using a1tables.tex, label  title(Regression 4ci\label{Reg4ci}) append
	reg wage_dif prog_int ch71, r
	esttab using a1tables.tex, label  title(Regression 4cii\label{Reg4cii}) append
	reg educ_dif prog_int ch71, r
	predict edif_pred
	reg wage_dif edif_pred ch71, r
	esttab using a1tables.tex, label  title(Regression 4cv\label{Reg4cv}) append
restore

**Question 4.d: 2 Stage Least Squares
gen d62=(YOB==62)
gen d63=(YOB==63)
gen d64=(YOB==64)
gen d65=(YOB==65)
gen d66=(YOB==66)
gen d67=(YOB==67)
gen d68=(YOB==68)
gen d69=(YOB==69)
gen d70=(YOB==70)
gen d71=(YOB==71)
gen d72=(YOB==72)

gen z62 = d62*prog_int
gen z63 = d63*prog_int
gen z64 = d64*prog_int
gen z65 = d65*prog_int
gen z66 = d66*prog_int
gen z67 = d67*prog_int
gen z68 = d68*prog_int
gen z69 = d69*prog_int
gen z70 = d70*prog_int
gen z71 = d71*prog_int
gen z72 = d72*prog_int

xi: reg yeduc z62 z63 z64 z65 z66 z67 z68 z69 z70 z71 z72 i.YOB*ch71, r

predict yeduc_fitted

xi: reg lhwage yeduc_fitted i.YOB*ch71, r
esttab, keep(yeduc_fitted), using a1tables.tex, label  title(Regression 4diii2 \label{Reg4diii2}) append
