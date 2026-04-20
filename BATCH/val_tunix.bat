cp inputs/GEOMETRY/LEWICE/NACA0012.XYD geom.xyd
mkdir temps
mkdir data

mkdir temps/run01c
mkdir data/run01c
cp inputs/run01cd.inp deice.inp
cp inputs/run01c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run01c
mv *.dat data/run01c

mkdir temps/run01d
mkdir data/run01d
cp inputs/run01dd.inp deice.inp
cp inputs/run01d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run01d
mv *.dat data/run01d

mkdir temps/run02a
mkdir data/run02a
cp inputs/run02ad.inp deice.inp
cp inputs/run02a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run02a
mv *.dat data/run02a

mkdir temps/run02b
mkdir data/run02b
cp inputs/run02bd.inp deice.inp
cp inputs/run02b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run02b
mv *.dat data/run02b

mkdir temps/run03a
mkdir data/run03a
cp inputs/run03ad.inp deice.inp
cp inputs/run03a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run03a
mv *.dat data/run03a

mkdir temps/run03b
mkdir data/run03b
cp inputs/run03bd.inp deice.inp
cp inputs/run03b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run03b
mv *.dat data/run03b

mkdir temps/run04b
mkdir data/run04b
cp inputs/run04bd.inp deice.inp
cp inputs/run04b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run04b
mv *.dat data/run04b

mkdir temps/run04c
mkdir data/run04c
cp inputs/run04cd.inp deice.inp
cp inputs/run04c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run04c
mv *.dat data/run04c

mkdir temps/run04d
mkdir data/run04d
cp inputs/run04dd.inp deice.inp
cp inputs/run04d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run04d
mv *.dat data/run04d

mkdir temps/run05a
mkdir data/run05a
cp inputs/run05ad.inp deice.inp
cp inputs/run05a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run05a
mv *.dat data/run05a

mkdir temps/run05b
mkdir data/run05b
cp inputs/run05bd.inp deice.inp
cp inputs/run05b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run05b
mv *.dat data/run05b

mkdir temps/run07b
mkdir data/run07b
cp inputs/run07bd.inp deice.inp
cp inputs/run07b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run07b
mv *.dat data/run07b

mkdir temps/run07c
mkdir data/run07c
cp inputs/run07cd.inp deice.inp
cp inputs/run07c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run07c
mv *.dat data/run07c

mkdir temps/run08a
mkdir data/run08a
cp inputs/run08ad.inp deice.inp
cp inputs/run08a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run08a
mv *.dat data/run08a

mkdir temps/run08b
mkdir data/run08b
cp inputs/run08bd.inp deice.inp
cp inputs/run08b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run08b
mv *.dat data/run08b

mkdir temps/run09
mkdir data/run09
cp inputs/run09d.inp deice.inp
cp inputs/run09.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run09
mv *.dat data/run09

mkdir temps/run10a
mkdir data/run10a
cp inputs/run10ad.inp deice.inp
cp inputs/run10a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run10a
mv *.dat data/run10a

mkdir temps/run10b
mkdir data/run10b
cp inputs/run10bd.inp deice.inp
cp inputs/run10b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run10b
mv *.dat data/run10b

mkdir temps/run10c
mkdir data/run10c
cp inputs/run10cd.inp deice.inp
cp inputs/run10c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run10c
mv *.dat data/run10c

mkdir temps/run12a
mkdir data/run12a
cp inputs/run12ad.inp deice.inp
cp inputs/run12a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run12a
mv *.dat data/run12a

mkdir temps/run12b
mkdir data/run12b
cp inputs/run12bd.inp deice.inp
cp inputs/run12b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run12b
mv *.dat data/run12b

mkdir temps/run12c
mkdir data/run12c
cp inputs/run12cd.inp deice.inp
cp inputs/run12c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run12c
mv *.dat data/run12c

mkdir temps/run12d
mkdir data/run12d
cp inputs/run12dd.inp deice.inp
cp inputs/run12d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run12d
mv *.dat data/run12d

mkdir temps/run13a
mkdir data/run13a
cp inputs/run13ad.inp deice.inp
cp inputs/run13a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run13a
mv *.dat data/run13a

mkdir temps/run13b
mkdir data/run13b
cp inputs/run13bd.inp deice.inp
cp inputs/run13b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run13b
mv *.dat data/run13b

mkdir temps/run13c
mkdir data/run13c
cp inputs/run13cd.inp deice.inp
cp inputs/run13c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run13c
mv *.dat data/run13c

mkdir temps/run13d
mkdir data/run13d
cp inputs/run13dd.inp deice.inp
cp inputs/run13d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run13d
mv *.dat data/run13d

mkdir temps/run15a
mkdir data/run15a
cp inputs/run15ad.inp deice.inp
cp inputs/run15a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run15a
mv *.dat data/run15a

mkdir temps/run15b
mkdir data/run15b
cp inputs/run15bd.inp deice.inp
cp inputs/run15b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run15b
mv *.dat data/run15b

mkdir temps/run17
mkdir data/run17
cp inputs/run17d.inp deice.inp
cp inputs/run17.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run17
mv *.dat data/run17

mkdir temps/run18a
mkdir data/run18a
cp inputs/run18ad.inp deice.inp
cp inputs/run18a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run18a
mv *.dat data/run18a

mkdir temps/run18b
mkdir data/run18b
cp inputs/run18bd.inp deice.inp
cp inputs/run18b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run18b
mv *.dat data/run18b

mkdir temps/run18c
mkdir data/run18c
cp inputs/run18cd.inp deice.inp
cp inputs/run18c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run18c
mv *.dat data/run18c

mkdir temps/run18d
mkdir data/run18d
cp inputs/run18dd.inp deice.inp
cp inputs/run18d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run18d
mv *.dat data/run18d

mkdir temps/run20
mkdir data/run20
cp inputs/run20d.inp deice.inp
cp inputs/run20.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run20
mv *.dat data/run20

mkdir temps/run22a
mkdir data/run22a
cp inputs/run22ad.inp deice.inp
cp inputs/run22a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22a
mv *.dat data/run22a

mkdir temps/run22b
mkdir data/run22b
cp inputs/run22bd.inp deice.inp
cp inputs/run22b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22b
mv *.dat data/run22b

mkdir temps/run22c
mkdir data/run22c
cp inputs/run22cd.inp deice.inp
cp inputs/run22c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22c
mv *.dat data/run22c

mkdir temps/run22d
mkdir data/run22d
cp inputs/run22dd.inp deice.inp
cp inputs/run22d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22d
mv *.dat data/run22d

mkdir temps/run22e
mkdir data/run22e
cp inputs/run22ed.inp deice.inp
cp inputs/run22e.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22e
mv *.dat data/run22e

mkdir temps/run22f
mkdir data/run22f
cp inputs/run22fd.inp deice.inp
cp inputs/run22f.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run22f
mv *.dat data/run22f

mkdir temps/run24
mkdir data/run24
cp inputs/run24d.inp deice.inp
cp inputs/run24.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run24
mv *.dat data/run24

mkdir temps/run25
mkdir data/run25
cp inputs/run25d.inp deice.inp
cp inputs/run25.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run25
mv *.dat data/run25

mkdir temps/run26
mkdir data/run26
cp inputs/run26d.inp deice.inp
cp inputs/run26.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run26
mv *.dat data/run26

mkdir temps/run28
mkdir data/run28
cp inputs/run28d.inp deice.inp
cp inputs/run28.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run28
mv *.dat data/run28

mkdir temps/run29
mkdir data/run29
cp inputs/run29d.inp deice.inp
cp inputs/run29.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run29
mv *.dat data/run29

mkdir temps/run30
mkdir data/run30
cp inputs/run30d.inp deice.inp
cp inputs/run30.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run30
mv *.dat data/run30

mkdir temps/run32
mkdir data/run32
cp inputs/run32d.inp deice.inp
cp inputs/run32.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run32
mv *.dat data/run32

mkdir temps/run33
mkdir data/run33
cp inputs/run33d.inp deice.inp
cp inputs/run33.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run33
mv *.dat data/run33

mkdir temps/run34
mkdir data/run34
cp inputs/run34d.inp deice.inp
cp inputs/run34.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run34
mv *.dat data/run34

mkdir temps/run35a
mkdir data/run35a
cp inputs/run35ad.inp deice.inp
cp inputs/run35a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run35a
mv *.dat data/run35a

mkdir temps/run35b
mkdir data/run35b
cp inputs/run35bd.inp deice.inp
cp inputs/run35b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run35b
mv *.dat data/run35b

mkdir temps/run37
mkdir data/run37
cp inputs/run37d.inp deice.inp
cp inputs/run37.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run37
mv *.dat data/run37

mkdir temps/run38
mkdir data/run38
cp inputs/run38d.inp deice.inp
cp inputs/run38.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run38
mv *.dat data/run38

mkdir temps/run39
mkdir data/run39
cp inputs/run39d.inp deice.inp
cp inputs/run39.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run39
mv *.dat data/run39

mkdir temps/run41
mkdir data/run41
cp inputs/run41d.inp deice.inp
cp inputs/run41.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run41
mv *.dat data/run41

mkdir temps/run42
mkdir data/run42
cp inputs/run42d.inp deice.inp
cp inputs/run42.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run42
mv *.dat data/run42

mkdir temps/run43
mkdir data/run43
cp inputs/run43d.inp deice.inp
cp inputs/run43.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run43
mv *.dat data/run43

mkdir temps/run45
mkdir data/run45
cp inputs/run45d.inp deice.inp
cp inputs/run45.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run45
mv *.dat data/run45

mkdir temps/run46
mkdir data/run46
cp inputs/run46d.inp deice.inp
cp inputs/run46.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run46
mv *.dat data/run46

mkdir temps/run47
mkdir data/run47
cp inputs/run47d.inp deice.inp
cp inputs/run47.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run47
mv *.dat data/run47

mkdir temps/run48a
mkdir data/run48a
cp inputs/run48ad.inp deice.inp
cp inputs/run48a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run48a
mv *.dat data/run48a

mkdir temps/run48b
mkdir data/run48b
cp inputs/run48bd.inp deice.inp
cp inputs/run48b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run48b
mv *.dat data/run48b

mkdir temps/run50
mkdir data/run50
cp inputs/run50d.inp deice.inp
cp inputs/run50.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run50
mv *.dat data/run50

mkdir temps/run51
mkdir data/run51
cp inputs/run51d.inp deice.inp
cp inputs/run51.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run51
mv *.dat data/run51

mkdir temps/run52
mkdir data/run52
cp inputs/run52d.inp deice.inp
cp inputs/run52.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run52
mv *.dat data/run52

mkdir temps/run53a
mkdir data/run53a
cp inputs/run53ad.inp deice.inp
cp inputs/run53a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run53a
mv *.dat data/run53a

mkdir temps/run53b
mkdir data/run53b
cp inputs/run53bd.inp deice.inp
cp inputs/run53b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run53b
mv *.dat data/run53b

mkdir temps/run55
mkdir data/run55
cp inputs/run55d.inp deice.inp
cp inputs/run55.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run55
mv *.dat data/run55

mkdir temps/run56
mkdir data/run56
cp inputs/run56d.inp deice.inp
cp inputs/run56.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run56
mv *.dat data/run56

mkdir temps/run57
mkdir data/run57
cp inputs/run57d.inp deice.inp
cp inputs/run57.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run57
mv *.dat data/run57

mkdir temps/run58a
mkdir data/run58a
cp inputs/run58ad.inp deice.inp
cp inputs/run58a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run58a
mv *.dat data/run58a

mkdir temps/run58b
mkdir data/run58b
cp inputs/run58bd.inp deice.inp
cp inputs/run58b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run58b
mv *.dat data/run58b

mkdir temps/run60
mkdir data/run60
cp inputs/run60d.inp deice.inp
cp inputs/run60.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run60
mv *.dat data/run60

mkdir temps/run61
mkdir data/run61
cp inputs/run61d.inp deice.inp
cp inputs/run61.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run61
mv *.dat data/run61

mkdir temps/run62
mkdir data/run62
cp inputs/run62d.inp deice.inp
cp inputs/run62.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run62
mv *.dat data/run62

mkdir temps/run63a
mkdir data/run63a
cp inputs/run63ad.inp deice.inp
cp inputs/run63a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run63a
mv *.dat data/run63a

mkdir temps/run63b
mkdir data/run63b
cp inputs/run63bd.inp deice.inp
cp inputs/run63b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run63b
mv *.dat data/run63b

mkdir temps/run64
mkdir data/run64
cp inputs/run64d.inp deice.inp
cp inputs/run64.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run64
mv *.dat data/run64

mkdir temps/run65a
mkdir data/run65a
cp inputs/run65ad.inp deice.inp
cp inputs/run65a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run65a
mv *.dat data/run65a

mkdir temps/run65b
mkdir data/run65b
cp inputs/run65bd.inp deice.inp
cp inputs/run65b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run65b
mv *.dat data/run65b

mkdir temps/run66
mkdir data/run66
cp inputs/run66d.inp deice.inp
cp inputs/run66.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run66
mv *.dat data/run66

mkdir temps/run67a
mkdir data/run67a
cp inputs/run67ad.inp deice.inp
cp inputs/run67a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run67a
mv *.dat data/run67a

mkdir temps/run67b
mkdir data/run67b
cp inputs/run67bd.inp deice.inp
cp inputs/run67b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run67b
mv *.dat data/run67b

mkdir temps/run68
mkdir data/run68
cp inputs/run68d.inp deice.inp
cp inputs/run68.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run68
mv *.dat data/run68

mkdir temps/run69a
mkdir data/run69a
cp inputs/run69ad.inp deice.inp
cp inputs/run69a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run69a
mv *.dat data/run69a

mkdir temps/run69b
mkdir data/run69b
cp inputs/run69bd.inp deice.inp
cp inputs/run69b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run69b
mv *.dat data/run69b

mkdir temps/run70
mkdir data/run70
cp inputs/run70d.inp deice.inp
cp inputs/run70.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run70
mv *.dat data/run70

mkdir temps/run71a
mkdir data/run71a
cp inputs/run71ad.inp deice.inp
cp inputs/run71a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run71a
mv *.dat data/run71a

mkdir temps/run71b
mkdir data/run71b
cp inputs/run71bd.inp deice.inp
cp inputs/run71b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run71b
mv *.dat data/run71b

mkdir temps/run72
mkdir data/run72
cp inputs/run72d.inp deice.inp
cp inputs/run72.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run72
mv *.dat data/run72

mkdir temps/run73a
mkdir data/run73a
cp inputs/run73ad.inp deice.inp
cp inputs/run73a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run73a
mv *.dat data/run73a

mkdir temps/run73b
mkdir data/run73b
cp inputs/run73bd.inp deice.inp
cp inputs/run73b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run73b
mv *.dat data/run73b

mkdir temps/run74
mkdir data/run74
cp inputs/run74d.inp deice.inp
cp inputs/run74.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run74
mv *.dat data/run74

mkdir temps/run75a
mkdir data/run75a
cp inputs/run75ad.inp deice.inp
cp inputs/run75a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run75a
mv *.dat data/run75a

mkdir temps/run75b
mkdir data/run75b
cp inputs/run75bd.inp deice.inp
cp inputs/run75b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run75b
mv *.dat data/run75b

mkdir temps/run83
mkdir data/run83
cp inputs/run83d.inp deice.inp
cp inputs/run83.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run83
mv *.dat data/run83

mkdir temps/run84
mkdir data/run84
cp inputs/run84d.inp deice.inp
cp inputs/run84.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run84
mv *.dat data/run84

mkdir temps/run85
mkdir data/run85
cp inputs/run85d.inp deice.inp
cp inputs/run85.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run85
mv *.dat data/run85

mkdir temps/run86
mkdir data/run86
cp inputs/run86d.inp deice.inp
cp inputs/run86.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run86
mv *.dat data/run86

mkdir temps/run87
mkdir data/run87
cp inputs/run87d.inp deice.inp
cp inputs/run87.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run87
mv *.dat data/run87

mkdir temps/run88
mkdir data/run88
cp inputs/run88d.inp deice.inp
cp inputs/run88.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run88
mv *.dat data/run88

mkdir temps/run89a
mkdir data/run89a
cp inputs/run89ad.inp deice.inp
cp inputs/run89a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run89a
mv *.dat data/run89a

mkdir temps/run89b
mkdir data/run89b
cp inputs/run89bd.inp deice.inp
cp inputs/run89b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run89b
mv *.dat data/run89b

mkdir temps/run90
mkdir data/run90
cp inputs/run90d.inp deice.inp
cp inputs/run90.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run90
mv *.dat data/run90

mkdir temps/run91a
mkdir data/run91a
cp inputs/run91ad.inp deice.inp
cp inputs/run91a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run91a
mv *.dat data/run91a

mkdir temps/run91b
mkdir data/run91b
cp inputs/run91bd.inp deice.inp
cp inputs/run91b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
mv temps*a.dat temps/run91b
mv *.dat data/run91b
