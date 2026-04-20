This software is provided 'as is' without any warranty 
of any kind, either expressed, implied, or statutory,
including, but not limited to, any warranty that the 
software will conform to specifications, any 
implied warranties of merchantability, fitness for a
particular purpose, and freedom from infringement, 
and any warranty that the documentation will conform
to the program, or any warranty that the software 
will be error free. In no event shall NASA be liable
for any damages, including, but not limited to,
direct, indirect, special or consequential damages,
arising out of, resulting from, or in any way
connected with this software, whether or not based
upon warranty, contract, tort, or otherwise, whether
or not injury was sustained by persons or property or
otherwise, and whether or not loss was sustained from,
or arose out of the result of, or use of, the 
software or services provided hereunder.

No copyright is claimed in the United States under 
Title 17, U.S. Code.


This file contains information on installing LEWICE, a 
description of the files on the CD-ROM and a contact list 
for updates and technical support.

Prior Versions

NASA does not have the staff to support previous versions
of LEWICE. Since the current version is an interim release,
some support may be provided for version 2.0 users. However, 
those users will be encouraged to use the upgrade. Additionally,
any user who received a beta version of the current release
should erase the beta version from disk and destroy the beta 
version CD-ROM. The beta version will no longer be supported by NASA.


Known Problems

See the file BUGS.TXT for a discussion of known problems 
with this release.

Installation

LEWICE is installed by simply copying all of the files 
and directories on the CD-ROM to an appropriate directory 
on the user's hard drive. 


Running LEWICE

LEWICE cannot be run from the CD-ROM.

The program can be started in two ways:

1) [Recommended] Open a DOS Shell in Windows. This can be performed by 
   selecting "DOS Shell" in the Start Menu under Windows98. In Windows XP,
   select Start, then select the "Programs" submenu, then select the 
   "Accessories" submenu, then select "Command Prompt". Change the directory 
   in the DOS Shell to the LEWICE directory (cd c:\My Documents\LEWICE for 
   example) and type "lewice" without the quotes. See the LEWICE User Manual 
   for further instruction on how to run LEWICE.

2) The PC executable provided on the disk can be run by double-clicking the 
   icon in Windows 3.1 or higher. A console shell will open for interactive 
   input and output. This console shell disappears when the run is 
   finished. For this reason, it is highly recommended hat the user run the 
   PC executable from a DOS Shell instead of from the console shell.

On unix systems, LEWICE is run by typing "lewice" without
the quotes from the shell prompt.


LEWICE Quick Start Guide

This section is intended for users unfamiliar with LEWICE 
and/or DOS Shell commands. Also see Chapter 3 in the 
LEWICE User Manual.

The commands below should be typed at the C:\ prompt in a DOS Shell 
window on a Windows95 machine ("Command Prompt" in Windows XP) . 
Alternatively, the user can use the Windows interface for any of the 
commands shown.

1) Create a directory on the hard drive to store output
	md lewice <return>

2) Insert the LEWICE CD-ROM and copy all files from this 
   disk to the lewice directory as described in the 
   Installation Procedure.

3) Inside the lewice directory, make additional 
   directories for each run 
	md case1 <return>

4) Run LEWICE
	lewice <return>
   - program will prompt for input file name. 
     Enter the following:
	Inputs/case1.inp <return>
   - after printing a copyright notice, the program will 
     prompt for a geometry file name. 
     Enter the following:
	Inputs/case1.xyd <return>
   - if any warning messages appear, type 
	Y <return> 
   to continue case

5) copy data files to the proper directory
	copy *.dat case1

6) repeat steps 3-5 for each case to be run

NOTE: 
If a user wishes to duplicate all of the example cases
given, simply type "examples" at the DOS prompt which will 
replace steps 3-6 above.


PC Requirements

Version 2.0 ran successfully on a Compaq Presario® 133MHz 
Pentium with 24MB RAM running Windows95 and took 
9 minutes to run the first example case provided. Lower end 
systems were not available for testing. It is believed 
that the program should run on at least a 486 and 
Windows 3.1. 

Version 2.2.2 and version 2.4 ran successfully on a Compaq 
DeskPro 550Mz Pentium with 512MB RAM running Windows98
and took 95 seconds to run the first example case provided.
Lower end systems were not available for testing. It is 
believed that the program should run on at least a 486 and 
Windows 3.1.

Version 3.0 and 3.2 ran successfully on a Dell Dimension
2.7GHz Pentium4 with 512MB RAM running WindowsXP
and took 6 seconds to run the first example case provided.
Lower end systems were not available for testing. It is 
believed that the program should run on at least a 486 and 
Windows 3.1.

Various changes were made in this program to 
make conversion to personal computers much easier. 
The validation report (NASA CR208690) shows comparisons of 
ice shape predictions on a personal computer and a Silicon 
Graphics workstation. The ice shape predictions on various 
PCs using the executable provided on the distribution disk 
were identical. 

Most of the output data is provided in columns of text, 
with a text header identifying the variable. This file 
format can be easily imported into any spreadsheet package 
for plotting. The program takes about 900 KB of hard disk 
space for the executable, and several megabytes for output 
files. The third example case shows the program's 
potential to produce large output files. The output files 
for this case take only 3.3 MB of disk space. However, 
several of the larger output files were not printed in this 
example and output was further reduced using the print 
flags in the main input file. If this same case were to be 
run with all of the outputs activated, the output for this 
case would occupy over 45 MB of disk space.


Contacts and Technical Support

Funding for LEWICE development comes from the NASA budget 
which is provided for by US tax dollars. LEWICE is 
therefore provided free of charge to US corporations, 
universities or individuals. A request letter such as that 
provided in the User Manual should be sent to the Icing 
Branch Chief. The letter may be sent by regular mail, 
electronic mail or fax. A current mailing address is 
provided below.

Current Address for Icing Code Requests

Mr. Thomas H. Bond
Branch Chief, Icing Branch
NASA Glenn Research Center
21000 Brookpark Rd.
MS 11-2
Cleveland OH 44135
E-mail: Thomas.H.Bond@grc.nasa.gov
Phone: (216) 433-3900
FAX: (216) 977-7469

The World Wide Web Address for the Icing Branch is at: 

http://icebox.grc.nasa.gov/

Technical support is available from 9AM to 5 PM Eastern 
time from the code developer(s). Questions on running the 
program or how to simulate difficult problems with LEWICE 
should be sent to:

William Wright
NASA Glenn Research Center
21000 Brookpark Rd.
MS 11-2
Cleveland OH 44135
E-mail: William.B.Wright@grc.nasa.gov
Phone: (216) 433-2161
FAX: (216) 977-7469

E-mail and fax are the preferred methods of communication. 
The user should provide a description of the problem and 
error messages obtained and also provide an input file 
(including geometry) so the error can be reproduced. 
Correspondence is confidential and will not be released. 
Code improvements including bug fixes which result from 
this correspondence will be incorporated into future code 
versions which can be released by NASA.

The code developers are involved only in technical support 
of the codes and are not directly involved in the 
distribution process. Questions concerning distribution 
should be sent to the branch office.


Disk Contents

The CD-ROM contains the following files and directories:

Files:

README.TXT   (this file)

BUGS.TXT     A brief discussion of potential problems with 
	     this release.
	     
EXAMPLES.BAT A batch file which can be  used to run all of
             the example cases on a PC.
             
LEWICE.EXE   LEWICE 3.0 PC executable

MANUAL.PDF   An electronic version of the LEWICE 3.0 
             User Manual in PDF (Portable Document Format).

Directories:

ACROBAT

Contains the file RP505ENU.EXE described below.

RP505ENU.EXE   An installation program for Adobe Acrobat 
               Reader which must be installed in order to 
               read the PDF files enclosed. Acrobat Reader 
               is supplied free courtesy of Adobe. Read the 
               licensing restrictions included in Acrobat 
               Reader software for further information.


BATCH

This directory contains files that can be ran by users to 
duplicate example cases or validation runs. The batch files
can be used as a guide by experienced users to set up
similar batch runs for other geometries and inputs. See the
README.TXT file in this directory for more details.


INPUTS

The directory INPUTS contains LEWICE input files for 22 
example test cases (23 on SGI systems). The cases are described 
in the User Manual. A procedure for running these cases is given 
in the file TESTS.PDF on the distribution CD-ROM.


LINUX

LEWICE 3.0 and utilities compiled using g77 linux compiler.


RESULTS

The directory RESULTS contains the LEWICE output files 
from the 23 example test cases. The cases are described 
in the User Manual. The user can run any or all of the 
23 test cases and compare the outputs to those on the 
distribution CD-ROM. The outputs have been placed in
subdirectories CASE1 through CASE22. CASE22P contains the 
potential flow results which are plotted with Example 
Case 22 in the User Manual.
Subdirectory EXCEL contains experimental data and outputs
which are plotted with the User Manual examples. The 
LEWICE 3.0 PC executable has been tested on several PCs. All 
test results to date show that the outputs for the test cases 
are exactly the same when the cases are run on the various 
machines.

REPORTS

This directory contains NASA reports on the thermal test 
and prior validation.

SGI

LEWICE 3.0 and utilities compiled using f77 IRIX 6.5 compiler.


SUN

LEWICE 3.0 and utilities compiled using f77 compiler.


UTILITY

The directory UTILITY contains the following PC utility 
programs described in the User Manual.

ANTICE.EXE    A program for analyzing 2D anti-icing cases.
	      This functionality is included in version 2.2.2,
	      but output from 2.2.2 is different from ANTICE.
	      Two Example Cases are included.

ANTICONV.EXE  Converts 3D flow and collection efficiency
	      data for use in LEWICE 2.2.2. See Example 18
	      in the User Manual for details.
	      
ANTICONV2.EXE Converts LEWICE 2.2.2 outputs and generates
	      3D geometry and temperature contours.
	      See Example 18 in the User Manual for details.
	            
CONDEICE.EXE  Converts LEWICE 2.2.2 de-ice input files into 3.0
              format. Users can manually change the de-icer inputs
              using the  description in Chapter 5 of the user
              manual.

CONVERT.EXE   Converts LEWICE 1.6 input files into 3.0
              format. Users can convert 2.0 input files
              by adding the following four lines to their 
              input files:

              &RDATA
              &END
              &BOOT
              &END

EXPAND.EXE    A utility program which can expand 
              (or contract) the point definition 
              of an input geometry.

REDUCE.EXE    Converts LEWICE 3.0 thermocouple data
	      to Fahrenheit and reduces output to 
	      once per second for easier comparison
	      with experimental data.

THICK.EXE     A utility program which generates an ice 
              thickness distribution from an input ice 
              shape and an input airfoil. The ice shape 
              may be from flight or tunnel tests as well 
              as from LEWICE.

TOASCII.EXE   A utility program to convert PLOT3D files 
              in BINARY format to ASCII format.
                   
TOBINARY.EXE  A utility program to convert PLOT3D files 
              in ASCII format to BINARY format.


TRAINING

This directory contains PDF versions of the presentations
made at the LEWICE workshop Sept. 23-24, 1999. The 
presentations are named sequential in the order presented.
For example, WRKSHP1.PDF contains the first presentation
and so forth.
                                      
                   Source Code Policy
                   
FORTRAN source code has not been released with this version 
of LEWICE as NASA does not have the staff to support 
modified versions of the code. Developers who are 
interested in obtaining source code should send their 
inquiries to the Icing Branch office with a letter 
describing their need for source code. Requests will be 
handled on a case by case basis.

Users who recompile LEWICE for other systems must run the 
benchmark test cases supplied on this CD-ROM to assess
differences in output when running on other platforms.

Developers who modify LEWICE for their own purposes are
reminded that the modified code is no longer version 3.2
of LEWICE. In order to revalidate the modified code,
developers should run the cases provided in the validation
report (NASA CR208690).
