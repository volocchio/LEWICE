cp inputs\GEOMETRY\LEWICE\NACA0012.XYD geom.xyd
mkdir temps
mkdir data

mkdir temps\run01c
mkdir data\run01c
copy inputs\run01cd.inp deice.inp
copy inputs\run01c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run01c
move *.dat data\run01c

mkdir temps\run01d
mkdir data\run01d
copy inputs\run01dd.inp deice.inp
copy inputs\run01d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run01d
move *.dat data\run01d

mkdir temps\run02a
mkdir data\run02a
copy inputs\run02ad.inp deice.inp
copy inputs\run02a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run02a
move *.dat data\run02a

mkdir temps\run02b
mkdir data\run02b
copy inputs\run02bd.inp deice.inp
copy inputs\run02b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run02b
move *.dat data\run02b

mkdir temps\run03a
mkdir data\run03a
copy inputs\run03ad.inp deice.inp
copy inputs\run03a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run03a
move *.dat data\run03a

mkdir temps\run03b
mkdir data\run03b
copy inputs\run03bd.inp deice.inp
copy inputs\run03b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run03b
move *.dat data\run03b

mkdir temps\run04b
mkdir data\run04b
copy inputs\run04bd.inp deice.inp
copy inputs\run04b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run04b
move *.dat data\run04b

mkdir temps\run04c
mkdir data\run04c
copy inputs\run04cd.inp deice.inp
copy inputs\run04c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run04c
move *.dat data\run04c

mkdir temps\run04d
mkdir data\run04d
copy inputs\run04dd.inp deice.inp
copy inputs\run04d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run04d
move *.dat data\run04d

mkdir temps\run05a
mkdir data\run05a
copy inputs\run05ad.inp deice.inp
copy inputs\run05a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run05a
move *.dat data\run05a

mkdir temps\run05b
mkdir data\run05b
copy inputs\run05bd.inp deice.inp
copy inputs\run05b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run05b
move *.dat data\run05b

mkdir temps\run07b
mkdir data\run07b
copy inputs\run07bd.inp deice.inp
copy inputs\run07b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run07b
move *.dat data\run07b

mkdir temps\run07c
mkdir data\run07c
copy inputs\run07cd.inp deice.inp
copy inputs\run07c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run07c
move *.dat data\run07c

mkdir temps\run08a
mkdir data\run08a
copy inputs\run08ad.inp deice.inp
copy inputs\run08a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run08a
move *.dat data\run08a

mkdir temps\run08b
mkdir data\run08b
copy inputs\run08bd.inp deice.inp
copy inputs\run08b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run08b
move *.dat data\run08b

mkdir temps\run09
mkdir data\run09
copy inputs\run09d.inp deice.inp
copy inputs\run09.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run09
move *.dat data\run09

mkdir temps\run10a
mkdir data\run10a
copy inputs\run10ad.inp deice.inp
copy inputs\run10a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run10a
move *.dat data\run10a

mkdir temps\run10b
mkdir data\run10b
copy inputs\run10bd.inp deice.inp
copy inputs\run10b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run10b
move *.dat data\run10b

mkdir temps\run10c
mkdir data\run10c
copy inputs\run10cd.inp deice.inp
copy inputs\run10c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run10c
move *.dat data\run10c

mkdir temps\run12a
mkdir data\run12a
copy inputs\run12ad.inp deice.inp
copy inputs\run12a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run12a
move *.dat data\run12a

mkdir temps\run12b
mkdir data\run12b
copy inputs\run12bd.inp deice.inp
copy inputs\run12b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run12b
move *.dat data\run12b

mkdir temps\run12c
mkdir data\run12c
copy inputs\run12cd.inp deice.inp
copy inputs\run12c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run12c
move *.dat data\run12c

mkdir temps\run12d
mkdir data\run12d
copy inputs\run12dd.inp deice.inp
copy inputs\run12d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run12d
move *.dat data\run12d

mkdir temps\run13a
mkdir data\run13a
copy inputs\run13ad.inp deice.inp
copy inputs\run13a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run13a
move *.dat data\run13a

mkdir temps\run13b
mkdir data\run13b
copy inputs\run13bd.inp deice.inp
copy inputs\run13b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run13b
move *.dat data\run13b

mkdir temps\run13c
mkdir data\run13c
copy inputs\run13cd.inp deice.inp
copy inputs\run13c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run13c
move *.dat data\run13c

mkdir temps\run13d
mkdir data\run13d
copy inputs\run13dd.inp deice.inp
copy inputs\run13d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run13d
move *.dat data\run13d

mkdir temps\run15a
mkdir data\run15a
copy inputs\run15ad.inp deice.inp
copy inputs\run15a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run15a
move *.dat data\run15a

mkdir temps\run15b
mkdir data\run15b
copy inputs\run15bd.inp deice.inp
copy inputs\run15b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run15b
move *.dat data\run15b

mkdir temps\run17
mkdir data\run17
copy inputs\run17d.inp deice.inp
copy inputs\run17.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run17
move *.dat data\run17

mkdir temps\run18a
mkdir data\run18a
copy inputs\run18ad.inp deice.inp
copy inputs\run18a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run18a
move *.dat data\run18a

mkdir temps\run18b
mkdir data\run18b
copy inputs\run18bd.inp deice.inp
copy inputs\run18b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run18b
move *.dat data\run18b

mkdir temps\run18c
mkdir data\run18c
copy inputs\run18cd.inp deice.inp
copy inputs\run18c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run18c
move *.dat data\run18c

mkdir temps\run18d
mkdir data\run18d
copy inputs\run18dd.inp deice.inp
copy inputs\run18d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run18d
move *.dat data\run18d

mkdir temps\run20
mkdir data\run20
copy inputs\run20d.inp deice.inp
copy inputs\run20.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run20
move *.dat data\run20

mkdir temps\run22a
mkdir data\run22a
copy inputs\run22ad.inp deice.inp
copy inputs\run22a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22a
move *.dat data\run22a

mkdir temps\run22b
mkdir data\run22b
copy inputs\run22bd.inp deice.inp
copy inputs\run22b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22b
move *.dat data\run22b

mkdir temps\run22c
mkdir data\run22c
copy inputs\run22cd.inp deice.inp
copy inputs\run22c.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22c
move *.dat data\run22c

mkdir temps\run22d
mkdir data\run22d
copy inputs\run22dd.inp deice.inp
copy inputs\run22d.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22d
move *.dat data\run22d

mkdir temps\run22e
mkdir data\run22e
copy inputs\run22ed.inp deice.inp
copy inputs\run22e.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22e
move *.dat data\run22e

mkdir temps\run22f
mkdir data\run22f
copy inputs\run22fd.inp deice.inp
copy inputs\run22f.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run22f
move *.dat data\run22f

mkdir temps\run24
mkdir data\run24
copy inputs\run24d.inp deice.inp
copy inputs\run24.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run24
move *.dat data\run24

mkdir temps\run25
mkdir data\run25
copy inputs\run25d.inp deice.inp
copy inputs\run25.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run25
move *.dat data\run25

mkdir temps\run26
mkdir data\run26
copy inputs\run26d.inp deice.inp
copy inputs\run26.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run26
move *.dat data\run26

mkdir temps\run28
mkdir data\run28
copy inputs\run28d.inp deice.inp
copy inputs\run28.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run28
move *.dat data\run28

mkdir temps\run29
mkdir data\run29
copy inputs\run29d.inp deice.inp
copy inputs\run29.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run29
move *.dat data\run29

mkdir temps\run30
mkdir data\run30
copy inputs\run30d.inp deice.inp
copy inputs\run30.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run30
move *.dat data\run30

mkdir temps\run32
mkdir data\run32
copy inputs\run32d.inp deice.inp
copy inputs\run32.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run32
move *.dat data\run32

mkdir temps\run33
mkdir data\run33
copy inputs\run33d.inp deice.inp
copy inputs\run33.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run33
move *.dat data\run33

mkdir temps\run34
mkdir data\run34
copy inputs\run34d.inp deice.inp
copy inputs\run34.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run34
move *.dat data\run34

mkdir temps\run35a
mkdir data\run35a
copy inputs\run35ad.inp deice.inp
copy inputs\run35a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run35a
move *.dat data\run35a

mkdir temps\run35b
mkdir data\run35b
copy inputs\run35bd.inp deice.inp
copy inputs\run35b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run35b
move *.dat data\run35b

mkdir temps\run37
mkdir data\run37
copy inputs\run37d.inp deice.inp
copy inputs\run37.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run37
move *.dat data\run37

mkdir temps\run38
mkdir data\run38
copy inputs\run38d.inp deice.inp
copy inputs\run38.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run38
move *.dat data\run38

mkdir temps\run39
mkdir data\run39
copy inputs\run39d.inp deice.inp
copy inputs\run39.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run39
move *.dat data\run39

mkdir temps\run41
mkdir data\run41
copy inputs\run41d.inp deice.inp
copy inputs\run41.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run41
move *.dat data\run41

mkdir temps\run42
mkdir data\run42
copy inputs\run42d.inp deice.inp
copy inputs\run42.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run42
move *.dat data\run42

mkdir temps\run43
mkdir data\run43
copy inputs\run43d.inp deice.inp
copy inputs\run43.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run43
move *.dat data\run43

mkdir temps\run45
mkdir data\run45
copy inputs\run45d.inp deice.inp
copy inputs\run45.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run45
move *.dat data\run45

mkdir temps\run46
mkdir data\run46
copy inputs\run46d.inp deice.inp
copy inputs\run46.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run46
move *.dat data\run46

mkdir temps\run47
mkdir data\run47
copy inputs\run47d.inp deice.inp
copy inputs\run47.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run47
move *.dat data\run47

mkdir temps\run48a
mkdir data\run48a
copy inputs\run48ad.inp deice.inp
copy inputs\run48a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run48a
move *.dat data\run48a

mkdir temps\run48b
mkdir data\run48b
copy inputs\run48bd.inp deice.inp
copy inputs\run48b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run48b
move *.dat data\run48b

mkdir temps\run50
mkdir data\run50
copy inputs\run50d.inp deice.inp
copy inputs\run50.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run50
move *.dat data\run50

mkdir temps\run51
mkdir data\run51
copy inputs\run51d.inp deice.inp
copy inputs\run51.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run51
move *.dat data\run51

mkdir temps\run52
mkdir data\run52
copy inputs\run52d.inp deice.inp
copy inputs\run52.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run52
move *.dat data\run52

mkdir temps\run53a
mkdir data\run53a
copy inputs\run53ad.inp deice.inp
copy inputs\run53a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run53a
move *.dat data\run53a

mkdir temps\run53b
mkdir data\run53b
copy inputs\run53bd.inp deice.inp
copy inputs\run53b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run53b
move *.dat data\run53b

mkdir temps\run55
mkdir data\run55
copy inputs\run55d.inp deice.inp
copy inputs\run55.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run55
move *.dat data\run55

mkdir temps\run56
mkdir data\run56
copy inputs\run56d.inp deice.inp
copy inputs\run56.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run56
move *.dat data\run56

mkdir temps\run57
mkdir data\run57
copy inputs\run57d.inp deice.inp
copy inputs\run57.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run57
move *.dat data\run57

mkdir temps\run58a
mkdir data\run58a
copy inputs\run58ad.inp deice.inp
copy inputs\run58a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run58a
move *.dat data\run58a

mkdir temps\run58b
mkdir data\run58b
copy inputs\run58bd.inp deice.inp
copy inputs\run58b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run58b
move *.dat data\run58b

mkdir temps\run60
mkdir data\run60
copy inputs\run60d.inp deice.inp
copy inputs\run60.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run60
move *.dat data\run60

mkdir temps\run61
mkdir data\run61
copy inputs\run61d.inp deice.inp
copy inputs\run61.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run61
move *.dat data\run61

mkdir temps\run62
mkdir data\run62
copy inputs\run62d.inp deice.inp
copy inputs\run62.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run62
move *.dat data\run62

mkdir temps\run63a
mkdir data\run63a
copy inputs\run63ad.inp deice.inp
copy inputs\run63a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run63a
move *.dat data\run63a

mkdir temps\run63b
mkdir data\run63b
copy inputs\run63bd.inp deice.inp
copy inputs\run63b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run63b
move *.dat data\run63b

mkdir temps\run64
mkdir data\run64
copy inputs\run64d.inp deice.inp
copy inputs\run64.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run64
move *.dat data\run64

mkdir temps\run65a
mkdir data\run65a
copy inputs\run65ad.inp deice.inp
copy inputs\run65a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run65a
move *.dat data\run65a

mkdir temps\run65b
mkdir data\run65b
copy inputs\run65bd.inp deice.inp
copy inputs\run65b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run65b
move *.dat data\run65b

mkdir temps\run66
mkdir data\run66
copy inputs\run66d.inp deice.inp
copy inputs\run66.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run66
move *.dat data\run66

mkdir temps\run67a
mkdir data\run67a
copy inputs\run67ad.inp deice.inp
copy inputs\run67a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run67a
move *.dat data\run67a

mkdir temps\run67b
mkdir data\run67b
copy inputs\run67bd.inp deice.inp
copy inputs\run67b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run67b
move *.dat data\run67b

mkdir temps\run68
mkdir data\run68
copy inputs\run68d.inp deice.inp
copy inputs\run68.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run68
move *.dat data\run68

mkdir temps\run69a
mkdir data\run69a
copy inputs\run69ad.inp deice.inp
copy inputs\run69a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run69a
move *.dat data\run69a

mkdir temps\run69b
mkdir data\run69b
copy inputs\run69bd.inp deice.inp
copy inputs\run69b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run69b
move *.dat data\run69b

mkdir temps\run70
mkdir data\run70
copy inputs\run70d.inp deice.inp
copy inputs\run70.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run70
move *.dat data\run70

mkdir temps\run71a
mkdir data\run71a
copy inputs\run71ad.inp deice.inp
copy inputs\run71a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run71a
move *.dat data\run71a

mkdir temps\run71b
mkdir data\run71b
copy inputs\run71bd.inp deice.inp
copy inputs\run71b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run71b
move *.dat data\run71b

mkdir temps\run72
mkdir data\run72
copy inputs\run72d.inp deice.inp
copy inputs\run72.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run72
move *.dat data\run72

mkdir temps\run73a
mkdir data\run73a
copy inputs\run73ad.inp deice.inp
copy inputs\run73a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run73a
move *.dat data\run73a

mkdir temps\run73b
mkdir data\run73b
copy inputs\run73bd.inp deice.inp
copy inputs\run73b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run73b
move *.dat data\run73b

mkdir temps\run74
mkdir data\run74
copy inputs\run74d.inp deice.inp
copy inputs\run74.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run74
move *.dat data\run74

mkdir temps\run75a
mkdir data\run75a
copy inputs\run75ad.inp deice.inp
copy inputs\run75a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run75a
move *.dat data\run75a

mkdir temps\run75b
mkdir data\run75b
copy inputs\run75bd.inp deice.inp
copy inputs\run75b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run75b
move *.dat data\run75b

mkdir temps\run83
mkdir data\run83
copy inputs\run83d.inp deice.inp
copy inputs\run83.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run83
move *.dat data\run83

mkdir temps\run84
mkdir data\run84
copy inputs\run84d.inp deice.inp
copy inputs\run84.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run84
move *.dat data\run84

mkdir temps\run85
mkdir data\run85
copy inputs\run85d.inp deice.inp
copy inputs\run85.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run85
move *.dat data\run85

mkdir temps\run86
mkdir data\run86
copy inputs\run86d.inp deice.inp
copy inputs\run86.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run86
move *.dat data\run86

mkdir temps\run87
mkdir data\run87
copy inputs\run87d.inp deice.inp
copy inputs\run87.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run87
move *.dat data\run87

mkdir temps\run88
mkdir data\run88
copy inputs\run88d.inp deice.inp
copy inputs\run88.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run88
move *.dat data\run88

mkdir temps\run89a
mkdir data\run89a
copy inputs\run89ad.inp deice.inp
copy inputs\run89a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run89a
move *.dat data\run89a

mkdir temps\run89b
mkdir data\run89b
copy inputs\run89bd.inp deice.inp
copy inputs\run89b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run89b
move *.dat data\run89b

mkdir temps\run90
mkdir data\run90
copy inputs\run90d.inp deice.inp
copy inputs\run90.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run90
move *.dat data\run90

mkdir temps\run91a
mkdir data\run91a
copy inputs\run91ad.inp deice.inp
copy inputs\run91a.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run91a
move *.dat data\run91a

mkdir temps\run91b
mkdir data\run91b
copy inputs\run91bd.inp deice.inp
copy inputs\run91b.inp lewice.inp
lewice < input.inp
thick < thick.inp
reduce
move temps*a.dat temps\run91b
move *.dat data\run91b
