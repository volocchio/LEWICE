BATCH

This directory contains batch files which should prove useful in reducing the drudgery of running a large number of cases. All batch files should be checked for typos or other errors before using them. The function of each batch file is described below. Note that unix batch files need to be made executable - "chmod +x filename" to work. The batch files are text format and can be opened by 
any text editor or word processor. If a particular batch file does not work as expected, check the directory structure in the batch file versus the directory structure on your hard disk.


CASES.XLS (also CASESO.XLS)

See MACROPL.XLS


EXPPC.BAT

Generates ice shape parameters for each of the experimental ice shapes in the database on a UNIX operating system. Note that this step has already been performed, with the results residing in "expdata.xls". This script only takes 30 min. or so to run, so this script can be used to familiarize the user with the batch process. Final script results reside in "total.txt", with individual ice thickness profiles in the directory corresponding to the run number. A script
for unix operaating systems (exp_unix.bat) is also provided.

Steps:

1) Copy the files in subdirectory EXPDATA from the BATCH directory to hard
disk. For the purposes of this guide, the directory on the user's hard disk is 
labeled "EXPDATA" as well. Also copy the geometry files in 
BATCH\INPUTS\SHAPES\GEOMETRY to a directory called "GEOMETRY" in the 
EXPDATA subdirectory on the hard drive.

2) Copy the files EXPPC.BAT file and EXP.INP from the BATCH directory on the CD into the EXPDATA directory.

3) Copy THICK.EXE from the UTILITY directory on the CD into the EXPDATA
directory on the hard drive. 

4) Open a DOS Shell, change the directory to EXPDATA and enter "EXPPC" at
the prompt.

IMPORTANT NOTE: Do NOT use the geometries or ice shapes on the LEWICE validation CD since the THICK utility now uses a different file format.

MACROED.XLS

Contains a Microsoft Excel¨ macro written in Visual Basic for Applications¨. The macro automates the process of comparing results to the experimental data. The main output from the macro is the file "top_polished_done.xls" which contains comparison of each temperature for each thermocouple, summary information, and charts. By setting a flag, you can also print the charts as it makes them (lots of paper!). To use this macro, place the output files "temps1a.dat", "temps2a.dat" and "temps3a.dat" in a directory with the corresponding "fixed_data.xls" file. Run the macro, and select the "fixed_data.xls" file when it prompts you for a file. It will also prompt you for a run number for the charts. This macro is currently running on a Macintosh computer using Microsoft Excel. Minor changes may be needed for the macro to run on a PC. The experimental data files referenced here given in directory "THERMAL" on the
LEWICE 2.2 CD. Also note that Excel will warn the user about opening a macro,
since this is a popular way to spread viruses. There are no viruses in this file.


MACROPL.XLS 

Contains a Microsoft Excel¨ macro written in Visual Basic for Applications¨. The macro automates the process of plotting output files from LEWICE. Pressure coefficient, collection efficiency, heat transfer coefficient, ice thickness and ice shape are all plotted for each case listed in CASES.XLS. 

Steps:

1) Place CASES.XLS, MACROPL.XLS and TEMPLATE.XLS in a directory on your hard disk.

2) Place LEWICE output files into subdirectories named for each airfoil. The example uses the output from running VAL_PC.BAT below.

3) Open MACROPL.XLS in Microsoft Excel. Excel by default will warn the user about opening a macro since many macros contain viruses. This macro does not contain a virus. 

4) Run the macro in Excel. It will prompt the user for a file. CASES.XLS should be selected. Results are stored in a subdirectory called "OUTPUTS" in the same directory as the CASES.XLS file.

MACROPLO.XLS works the same as MACROPL.XLS, but does not plot ice thickness. CASESO.XLS lists the directories in the LEWOUTPUT directory on the LEWICE Validation CD. By using MACROPLO.XLS, CASESO.XLS and TEMPLATEO.XLS, the user can quickly create Excel files for all of the outputs on that CD.

NOTE: There is no error checking in the macros. If the file structure is not set
up exactly as specified, the macro may not run.


TEMPLATE.XLS (also TEMPLATO.XLS)

See MACROPL.XLS


VAL_PC.BAT

This file will run all of the LEWICE cases from the Validation CD and run THICK
on all of the resulting ice shapes. The steps for this procedure are similar to 
the steps for the EXPPC.BAT process above. This scrpit should run overnight
on most machines. The corresponding unix batch file is called VAL_UNIX.BAT.

Steps:

1) Copy the files in directory INPUTS\SHAPES from the LEWICE 2.2 CD to hard disk. For the purposes of this guide, the directory on the user's hard disk is labeled "VALDATA". Place the files in subdirectory "INPUTS" in the VALDATA
directory. 

2) Copy the files INPUT.INP and THICK.INP from the BATCH directory on the CD
into the VALDATA directory along with the VAL_PC.BAT file.

3) Copy THICK.EXE from the UTILITY directory and LEWICE.EXE on the CD into the VALDATA directory on the hard drive. 

4) Open a DOS Shell, change the directory to VALDATA and enter "VAL_PC" at
the prompt.

IMPORTANT NOTE: Since the input file format has changed from version 2.0, the
input files on the Validation CD can not be used with LEWICE 2.2. This script
however WILL work with LEWICE 2.0 and the input files on the Validation CD.

IMPORTANT NOTE: Batch processes such as this are more complicated to set up 
than it may first appear. All input files must be correct, the proper 
geometry must be referenced and the output data structure must be correct and 
logical. Setting up similar batch processes for your cases should only be 
attempted by experienced users.


VAL_TPC.BAT

This file will run all of the LEWICE cases for each of the thermal de-icer cases in the database. Directory "thermal" (created during the batch run) contains the temperature output files "temps1a.dat", "temps2a.dat", "temps3a.dat" in directories based on run number. Directory "data" contains other output files. This script takes 3-5 days to run, depending upon processor speed. The output directories are also quite large. The file "etmtrx3.xls" contains input conditions for each run, so the user can verify that the input files are correct. Experimental data which can be used for comparison is available in 
directory "THERMAL". The corresponding unix batch file is called VAL_TUNIX.BAT

Steps:

1) Copy the files in directory INPUTS\THERMAL from the LEWICE 2.2 CD to hard
disk. For the purposes of this guide, the directory on the user's hard disk is 
labeled "VALTHERM".

2) Copy the files INPUT.INP and THICK.INP from the BATCH directory on the CD
into the VALTHERM directory along with the VAL_TPC.BAT file.

3) Copy THICK.EXE from the UTILITY directory and LEWICE.EXE on the CD into the VALTHERM directory on the hard drive. 

4) Open a DOS Shell, change the directory to VALTHERM and enter "VAL_TPC" at
the prompt.

IMPORTANT NOTE: Batch processes such as this are more complicated to set up 
than it may first appear. All input files must be correct, the proper 
geometry must be referenced and the output data structure must be correct and 
logical. Setting up similar batch processes for your cases should only be 
attempted by experienced users.


BATCH\INPUTS

This directory contains input files which can be used with the batch scripts described above, or can be used for individual runs. Subdirectory "SHAPES" contains input files for each of the ice shape validation cases. Subdirectory "THERMAL" contains input files for the thermal deicer validation cases. Both the main input file and the deicer input file reside in this directory. Main input files have the nomenclature "run#.inp" while the thermal files are named "run#d.inp". NOTE: some run numbers end with "d" such as "run13d". The main input file is named "run13d.inp" and the deicer input file is named "run13dd.inp". The deicer input files are about four times as big if there is any confusion. Subdirectory "thermalt" contains the same input as directory "THERMAL" except the turbulent flag has been turned on.

BATCH\INPUTS\THERMAL

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
	
	
