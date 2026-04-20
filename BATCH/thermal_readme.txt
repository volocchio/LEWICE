
This directory contains LEWICE 2.2 input files for use in validating the thermal deicer model. The experimental data resides in BATCH\EXPDATA\THERMAL with a subdirectory for each run which contains a Microsoft Excel¨ file called "fixed_data.xls" which is described below.

Heater nomenclature: Section A is at leading edge. Also termed parting strip.
	Sections B & C are adjacent chordwise to section A, with B on the lower 
	surface.
	Section D is adjacent chordwise to section B.
	Section E is adjacent chordwise to section C.
	Section F is adjacent chordwise to section D.
	Section G is adjacent chordwise to section E.
	(See diagram in User Manual - Example 13. Also note that the actual 
	center of section A is offset slightly from the leading edge. This
	is accounted for in the input files.

Contents of fixed_data.xls

data_a sheet: Electrical heater power supplied (W/in^2) for each second. 
	Second set of values sets 0=FALSE so that average power density can be 
	calculated for input into program. Note that program power input is in 
	kW/m^2. (Averages in kW/m^2 are calculated in the spreadsheet.)
	
data_b sheet: Thermocouple output (deg_F) for each second. Nomenclature is: 
	tao = Temperature, section A, Outside surface
	tai = Temperature, section A, Inside surface
	tbo = Temperature, section B, Outside surface
	tbi = Temperature, section B, Inside surface
	tco = Temperature, section C, Outside surface
	tci = Temperature, section C, Inside surface
	tdo = Temperature, section D, Outside surface
	tdi = Temperature, section D, Inside surface
	teo = Temperature, section E, Outside surface
	tei = Temperature, section E, Inside surface
	tfo = Temperature, section F, Outside surface
	tfi = Temperature, section F, Inside surface
	tgo = Temperature, section G, Outside surface
	tgi = Temperature, section G, Inside surface
	
data_c sheet: RTD output (Deg_F) and heat flux gauge output (not functional) for 
	each second. This corresponds to the heater temperature for that 
	section. Nomenclature is:
	rta = RTD (heater) Tempetature, section A
	rtb = RTD (heater) Tempetature, section B
	rtc = RTD (heater) Tempetature, section C
	rtd = RTD (heater) Tempetature, section D
	rte = RTD (heater) Tempetature, section E
	rtf = RTD (heater) Tempetature, section F
	rtg = RTD (heater) Tempetature, section G
	Heat flux gauge output can be ignored.
	
data_e sheet: same as data_a sheet. Instrumentation existed in two spanwise 
	locations for two independantly controlled heater mats. Used to confirm 
	two-dimensionality of model
	
data_f sheet: same as data_b sheet. Instrumentation existed in two spanwise 
	locations for two independantly controlled heater mats. Used to confirm 
	two-dimensionality of model
	
data_g sheet: same as data_c sheet. Instrumentation existed in two spanwise 
	locations for two independantly controlled heater mats. Used to confirm 
	two-dimensionality of model
	
	
