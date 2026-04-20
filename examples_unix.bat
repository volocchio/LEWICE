mkdir output
mkdir output/lewice
mkdir output/thick

cp examples/case1.inp input.inp
cp examples/case1.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case1
mkdir output/thick/case1
mv *.dat output/lewice/case1
mv fort.* output/lewice/case1
cp output/lewice/case1/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case1

cp examples/case2.inp input.inp
cp examples/case2.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case2
mkdir output/thick/case2
mv *.dat output/lewice/case2
mv fort.* output/lewice/case2
cp output/lewice/case2/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case2

cp examples/case3.inp input.inp
cp examples/case3.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case3
mkdir output/thick/case3
mv *.dat output/lewice/case3
mv fort.* output/lewice/case3
cp output/lewice/case3/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case3

cp examples/case4.inp input.inp
cp examples/case4.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case4
mkdir output/thick/case4
mv *.dat output/lewice/case4
mv fort.* output/lewice/case4
cp output/lewice/case4/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case4

cp examples/case5.inp input.inp
cp examples/case5.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case5
mkdir output/thick/case5
mv *.dat output/lewice/case5
mv fort.* output/lewice/case5
cp output/lewice/case5/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case5

cp examples/case6.inp input.inp
cp examples/case6.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case6
mkdir output/thick/case6
mv *.dat output/lewice/case6
mv fort.* output/lewice/case6
cp output/lewice/case6/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case6

cp examples/case7.inp input.inp
cp examples/case7.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case7
mkdir output/thick/case7
mv *.dat output/lewice/case7
mv fort.* output/lewice/case7
cp output/lewice/case7/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case7

cp examples/case8.inp input.inp
cp examples/case8.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case8
mkdir output/thick/case8
mv *.dat output/lewice/case8
mv fort.* output/lewice/case8
cp output/lewice/case8/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case8

cp examples/case9.inp input.inp
cp examples/case9.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case9
mkdir output/thick/case9
mv *.dat output/lewice/case9
mv fort.* output/lewice/case9
cp output/lewice/case9/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case9

cp examples/case10.inp input.inp
cp examples/case10.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case10
mkdir output/thick/case10
mv *.dat output/lewice/case10
mv fort.* output/lewice/case10
cp output/lewice/case10/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case10

cp examples/case10a.inp input.inp
LEWICE < lewice.inp
mkdir output/lewice/case10a
mkdir output/thick/case10a
mv *.dat output/lewice/case10a
mv fort.* output/lewice/case10a
cp output/lewice/case10a/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case10a

cp examples/case11.inp input.inp
cp examples/case11a.xyd geom1.xyd
cp examples/case11b.xyd geom2.xyd
cp examples/case11b.xyd geom3.xyd
LEWICE < lewice11.inp
mkdir output/lewice/case11
mkdir output/thick/case11a
mkdir output/thick/case11b
mkdir output/thick/case11c
mv *.dat output/lewice/case11
mv fort.* output/lewice/case11
cp output/lewice/case11/final1.dat final1.dat
thick < thick1.inp
mv *.dat output/thick/case11a
cp output/lewice/case11/final2.dat final2.dat
thick < thick2.inp
mv *.dat output/thick/case11b
cp output/lewice/case11/final3.dat final3.dat
thick < thick3.inp
mv *.dat output/thick/case11c

cp examples/case12.inp input.inp
cp examples/case12.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case12
mkdir output/thick/case12
mv *.dat output/lewice/case12
mv fort.* output/lewice/case12
cp output/lewice/case12/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case12

cp examples/case12a.inp input.inp
LEWICE < lewice.inp
mkdir output/lewice/case12a
mkdir output/thick/case12a
mv *.dat output/lewice/case12a
mv fort.* output/lewice/case12a
cp output/lewice/case12a/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case12a

cp examples/case13.inp input.inp
cp examples/case13d.inp deice.inp
cp examples/hi13.inp hi.inp
cp examples/case13.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case13
mkdir output/thick/case13
mv *.dat output/lewice/case13
mv fort.* output/lewice/case13
cp output/lewice/case13/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case13

cp examples/case14.inp input.inp
cp examples/case14d.inp deice.inp
cp examples/case14.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case14
mkdir output/thick/case14
mv *.dat output/lewice/case14
mv fort.* output/lewice/case14
cp output/lewice/case14/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case14

cp examples/case15.inp input.inp
cp examples/case15d.inp deice.inp
cp examples/case15.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case15
mkdir output/thick/case15
mv *.dat output/lewice/case15
mv fort.* output/lewice/case15
cp output/lewice/case15/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case15

cp examples/case16.inp input.inp
cp examples/case16d.inp deice.inp
cp examples/case16.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case16
mkdir output/thick/case16
mv *.dat output/lewice/case16
mv fort.* output/lewice/case16
cp output/lewice/case16/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case16

cp examples/case17.inp input.inp
cp examples/case17d.inp deice.inp
cp examples/case17.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case17
mkdir output/thick/case17
mv *.dat output/lewice/case17
mv fort.* output/lewice/case17
cp output/lewice/case17/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case17

cp examples/case18.inp input.inp
cp examples/case18d.inp deice.inp
cp examples/case18.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case18
mkdir output/thick/case18
mv *.dat output/lewice/case18
mv fort.* output/lewice/case18
cp output/lewice/case18/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case18

cp examples/case19.inp input.inp
cp examples/case19d.inp deice.inp
cp examples/case19.xyd geom.xyd
cp examples/hi19.inp hi.inp
LEWICE < lewice.inp
mkdir output/lewice/case19
mkdir output/thick/case19
mv *.dat output/lewice/case19
mv fort.* output/lewice/case19
cp output/lewice/case19/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case19

cp examples/case20.inp input.inp
cp examples/case20d.inp deice.inp
cp examples/case20.xyd geom.xyd
LEWICE < lewice.inp
mkdir output/lewice/case20
mkdir output/thick/case20
mv *.dat output/lewice/case20
mv fort.* output/lewice/case20
cp output/lewice/case20/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case20

cp examples/case21-1.inp input.inp
cp examples/case21d-1.inp deice.inp
cp examples/case21-1.xyd geom.xyd
cp examples/rflow21-1.inp rflow.inp
cp examples/rbeta21-1.inp rbeta.inp
cp examples/rhtc21-1.inp rhtc.inp
cp examples/stream21-1.inp stream.inp
LEWICE < lewice.inp
mkdir output/lewice/case21-1
mkdir output/thick/case21-1
mv *.dat output/lewice/case21-1
mv fort.* output/lewice/case21-1
cp output/lewice/case21-1/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case21-1

cp examples/case21-2.inp input.inp
cp examples/case21d-2.inp deice.inp
cp examples/case21-2.xyd geom.xyd
cp examples/rflow21-2.inp rflow.inp
cp examples/rbeta21-2.inp rbeta.inp
cp examples/rhtc21-2.inp rhtc.inp
cp examples/stream21-2.inp stream.inp
LEWICE < lewice.inp
mkdir output/lewice/case21-2
mkdir output/thick/case21-2
mv *.dat output/lewice/case21-2
mv fort.* output/lewice/case21-2
cp output/lewice/case21-2/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case21-2

cp examples/case21-3.inp input.inp
cp examples/case21d-3.inp deice.inp
cp examples/case21-3.xyd geom.xyd
cp examples/rflow21-3.inp rflow.inp
cp examples/rbeta21-3.inp rbeta.inp
cp examples/rhtc21-3.inp rhtc.inp
cp examples/stream21-3.inp stream.inp
LEWICE < lewice.inp
mkdir output/lewice/case21-3
mkdir output/thick/case21-3
mv *.dat output/lewice/case21-3
mv fort.* output/lewice/case21-3
cp output/lewice/case21-3/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case21-3

cp examples/case21-4.inp input.inp
cp examples/case21d-4.inp deice.inp
cp examples/case21-4.xyd geom.xyd
cp examples/rflow21-4.inp rflow.inp
cp examples/rbeta21-4.inp rbeta.inp
cp examples/rhtc21-4.inp rhtc.inp
cp examples/stream21-4.inp stream.inp
LEWICE < lewice.inp
mkdir output/lewice/case21-4
mkdir output/thick/case21-4
mv *.dat output/lewice/case21-4
mv fort.* output/lewice/case21-4
cp output/lewice/case21-4/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case21-4

cp examples/case21-5.inp input.inp
cp examples/case21d-5.inp deice.inp
cp examples/case21-5.xyd geom.xyd
cp examples/rflow21-5.inp rflow.inp
cp examples/rbeta21-5.inp rbeta.inp
cp examples/rhtc21-5.inp rhtc.inp
cp examples/stream21-5.inp stream.inp
LEWICE < lewice.inp
mkdir output/lewice/case21-5
mkdir output/thick/case21-5
mv *.dat output/lewice/case21-5
mv fort.* output/lewice/case21-5
cp output/lewice/case21-5/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case21-5

cp examples/case22.inp input.inp
cp examples/case22.xyd geom.xyd
cp examples/q.plt q.plt
cp examples/xy.plt xy.plt
LEWICE < lewice.inp
mkdir output/lewice/case22
mkdir output/thick/case22
mv *.dat output/lewice/case22
mv fort.* output/lewice/case22
cp output/lewice/case12/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case22
erase *.plt

cp examples/case22p.inp input.inp
LEWICE < lewice.inp
mkdir output/lewice/case22p
mkdir output/thick/case22p
mv *.dat output/lewice/case22p
mv fort.* output/lewice/case22p
cp output/lewice/case22p/final1.dat final1.dat
thick < thick.inp
mv *.dat output/thick/case22p