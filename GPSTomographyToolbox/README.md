# An Open Source Toolbox for Atmospheric Tomography

## Description
OpAtom toolbox provides a tomographic algorithm that capable of estimate a 3D wet refractivity model in Eastern Europe. The sizes of the tomographic grid are specified in the input files listed below. This algorithm uses an approximate cartesian reference system in which the length of the rays can be easily calculated. This Cartesian reference system is defined in the getlocal.py file and must be modified in case it is used in another area.
### Related studies:
https://doi.org/10.1007/s10291-025-01960-3 \
https://doi.org/10.3311/PPci.20559
### Detailed documentation
is avaialbale at http://gpsmet.geod.bme.hu/gps_toolbox/index.html

## Requirements
The toolbox has been tested on Ubuntu 20.04 using python 3.8. Module dependencies:
- NumPy
- SciPy
- Wget
- Matplotlib
## Usage
```
-s, --satellites   location of the satellite orbits file in .SP3 format
-S, --stations     location of the station coordinates file in Bernese .CRD format
    --gridp        location of the grid file in North-South direvtion in .csv format (degrees)
    --gridl        location of the grid file in East-West direction in .csv format (degrees)
    --gridh        location of the elevation grid file .csv format (metres)
-v, --vmf1loc      location of the VMF1 parameters grid files directory
-i, --initial_w    location of the initial wet refractivity values in .csv format
-e, --epoch        epoch in format YYYY-MM-DD-hh-mm-ss

python3 gnssct.py --satellites=./sample_data/orbit/CDU23005_00.EPH --stations=./sample_data/METEONET.CRD --tropofile=./sample_data/TRP/CO24040C.TRP --gridp=./sample_data/gridp.csv --gridl=./sample_data/gridl.csv --gridh=./sample_data/gridh.csv --vmf1loc=./sample_data/vmf1/ --epoch=2024-2-9-2-0-0 --initial_w=./sample_data/raobs/files/12843_2024-2-8_11.csv
```
The VMF1 parameters grid files must be placed in this directory, and the name format must be: YYYY/VMFG_YYYYMMDD.Hhh
## Input files
For the tomographic processing, the following input files are required:

  - The tomographic grid file (csv format)
      - Latitude
      - Longitude
      - Height
  - GNSS station coordinates file (Bernese CRD format)
  - Tropospheric delays file (Bernese TRP format)
  - VMF1 grid parameters file (VMF1 grid file)
  - Satellite orbit file (SP3 format)
  - Initial wet refractivity values (csv format)
## Tomographic grid files

Tomographic grid files define the size of the cells in each direction (latitude, longitude, height borders) over the entire area. Each file is a list of coordinates. In the case of latitude and longitude, the script expects the coordinates in degrees (WGS84), and the heights to be in meters.
```
45.5
46.2
46.9
47.6
48.3
49.0
49.7
```
## GNSS station coordinates file
The GNSS station coordinates file contains all the GNSS stations and their coordinates for the given epoch in Bernese CRD format.

```

Weekly solution for Week 2310                                     04-FEB-24 05:50 
--------------------------------------------------------------------------------- 
LOCAL GEODETIC DATUM: IGS14             EPOCH: 2024-01-31 12:00:00 

NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG 

  1  BAIA              3945839.43919  1720428.58296  4691082.90436    A 
143  BAJ1              4183093.74170  1439191.16597  4579512.35582    A 
  2  BAJA              4183094.39352  1439190.59467  4579511.94882 
140  BARA              3805783.52640  1629895.39810  4835969.94890 
  4  BBYS              3980358.47759  1382292.41144  4772772.14404    A 
```
## Tropospheric delay file
For calculating Slant Wet Delay (SWD) values, the Zenith Wet Delays (ZWD) and Tropospheric Gradient Values are required for each station. These files must be in Bernese TRP format, where ZWDs are in column CORR_U and Tropospheric gradients are in CORR_E and CORR_N. 
```
                                                                 09-FEB-24 02:42
 ------------------------------------------------------------------------------------------------------------------------------------
 A PRIORI MODEL:  -17   MAPPING FUNCTION:    8   GRADIENT MODEL:    4   MIN. ELEVATION:    5   TABULAR INTERVAL:  3600 / 86400
 STATION NAME     FLG   YYYY MM DD HH MM SS   YYYY MM DD HH MM SS   MOD_U   CORR_U  SIGMA_U TOTAL_U  CORR_N  SIGMA_N  CORR_E  SIGMA_E
 BAIA              A    2024 02 08 13 00 00                         2.2278  0.09318 0.00093 2.32095 -0.00005 0.00007 -0.00068 0.00007
 BAIA              A    2024 02 08 14 00 00                         2.2278  0.10194 0.00059 2.32972 -0.00008 0.00006 -0.00068 0.00006
 BAIA              A    2024 02 08 15 00 00                         2.2278  0.09959 0.00062 2.32738 -0.00010 0.00005 -0.00067 0.00006
 BAIA              A    2024 02 08 16 00 00                         2.2278  0.10264 0.00064 2.33044 -0.00012 0.00004 -0.00067 0.00005
 BAIA              A    2024 02 08 17 00 00                         2.2278  0.10729 0.00050 2.33509 -0.00015 0.00004 -0.00066 0.00004
 BAIA              A    2024 02 08 18 00 00                         2.2278  0.10523 0.00063 2.33304 -0.00017 0.00003 -0.00065 0.00004
 BAIA              A    2024 02 08 19 00 00                         2.2271  0.11471 0.00059 2.34182 -0.00019 0.00004 -0.00065 0.00004
 BAIA              A    2024 02 08 20 00 00                         2.2264  0.11173 0.00053 2.33814 -0.00022 0.00004 -0.00064 0.00005
 BAIA              A    2024 02 08 21 00 00                         2.2257  0.12048 0.00065 2.34619 -0.00024 0.00005 -0.00063 0.00005
 BAIA              A    2024 02 08 22 00 00                         2.2250  0.11663 0.00057 2.34164 -0.00026 0.00005 -0.00063 0.00006
 BAIA              A    2024 02 08 23 00 00                         2.2243  0.11885 0.00075 2.34317 -0.00029 0.00006 -0.00062 0.00007
 BAIA              A    2024 02 09 00 00 00                         2.2236  0.11231 0.00087 2.33593 -0.00031 0.00007 -0.00061 0.00008
 BAIA              A    2024 02 09 01 00 00                         2.2236  0.11582 0.00167 2.33945  0.00096 0.00017 -0.00177 0.00028
 BAJ1              A    2024 02 08 13 00 00                         2.2590  0.10221 0.00085 2.36121 -0.00009 0.00006 -0.00084 0.00006
 BAJ1              A    2024 02 08 14 00 00                         2.2587  0.10047 0.00055 2.35917 -0.00010 0.00005 -0.00075 0.00005
 BAJ1              A    2024 02 08 15 00 00                         2.2584  0.10198 0.00058 2.36038 -0.00012 0.00005 -0.00066 0.00004
 BAJ1              A    2024 02 08 16 00 00                         2.2581  0.09861 0.00056 2.35672 -0.00013 0.00004 -0.00057 0.00004
 BAJ1              A    2024 02 08 17 00 00                         2.2578  0.09972 0.00045 2.35753 -0.00014 0.00003 -0.00048 0.00003
 BAJ1              A    2024 02 08 18 00 00                         2.2575  0.09471 0.00058 2.35222 -0.00016 0.00003 -0.00039 0.00003
 BAJ1              A    2024 02 08 19 00 00                         2.2572  0.09693 0.00050 2.35413 -0.00017 0.00003 -0.00030 0.00003
 BAJ1              A    2024 02 08 20 00 00                         2.2569  0.09271 0.00049 2.34961 -0.00018 0.00003 -0.00021 0.00003
 BAJ1              A    2024 02 08 21 00 00                         2.2566  0.09063 0.00060 2.34723 -0.00020 0.00004 -0.00012 0.00004
 ...
```
## VMF1 grid files
The calculation of the SWDs requires a mapping function. For this purpose, the script uses the VMF1, which needs the aw coefficients. These coefficients are available on the website of the Vienna University of Technology. These parameters are provided in grid files for every hours. For the hourly interpolation in time, the script expects two files.  
```
! Version:            1.0 
! Source:             J. Boehm, TU Vienna (created: 2024-02-14) 
! Data_types:         VMF1 (lat lon ah aw zhd zwd) 
! Epoch:              2024 02 15 00 00  0.0 
! Scale_factor:       1.e+00        
! Range/resolution:   -90 90 0 360 2 2.5 
! Comment:            http://vmf.geo.tuwien.ac.at/trop_products/GRID/2.5x2/VMF1/VMF1_OP/ 
 90.0   0.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0   2.5 0.00117044  0.00060490  2.2998  0.0204 
 90.0   5.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0   7.5 0.00117044  0.00060490  2.2998  0.0204 
 90.0  10.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0  12.5 0.00117044  0.00060490  2.2998  0.0204 
 90.0  15.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0  17.5 0.00117044  0.00060490  2.2998  0.0204 
 90.0  20.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0  22.5 0.00117044  0.00060490  2.2998  0.0204 
 90.0  25.0 0.00117044  0.00060490  2.2998  0.0204 
 90.0  27.5 0.00117044  0.00060490  2.2998  0.0204 
. . . 
```
## Satellite orbit file
To calculate the azimuth and elevation angle from the station to the satellite, besides the station coordinates, the satellite orbits are also required in SP3 format. The ultra-rapid satellite orbits for GPS, GLONASS, and Galileo constellations are available from the Center for Orbit Determination in Europe at the University of Bern. 
```
#cP2024  2 12 18  0  0.00000000     577 d+D   IGS20 EXT AIUB 
## 2301 151200.00000000   300.00000000 60352 0.7500000000000 
+   78   G01G02G03G04G05G06G07G08G09G10G11G12G13G14G15G16G17 
+        G18G19G20G21G22G23G24G25G26G27G28G29G30G31G32R01R02 
+        R03R04R05R07R08R09R11R12R13R14R15R16R17R18R19R20R21 
+        R22R24E02E03E04E05E07E08E09E10E11E12E13E14E15E18E19 
+        E21E24E25E26E27E30E31E33E34E36  0  0  0  0  0  0  0 
++         5  7  6  6  7  6  7  6  6  6  7  7  6  6  7  7  7 
++         7  7  7  7  7  6  6  7  6  6  6  7  5  7  6  9  7 
++         8  8  8  8  8  7  6  7  7  6  6  6  8  7  9  9  8 
++         7  8  6  6  6  6  7  6  7  7  7  6  6  7  7  7  6 
++         6  6  6  7  6 10  6  7  6  7  0  0  0  0  0  0  0 
%c M  cc GPS ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc 
%c cc cc ccc ccc cccc cccc cccc cccc ccccc ccccc ccccc ccccc 
%f  1.2500000  1.025000000  0.00000000000  0.000000000000000 
%f  0.0000000  0.000000000  0.00000000000  0.000000000000000 
%i    0    0    0    0      0      0      0      0         0 
%i    0    0    0    0      0      0      0      0         0 
/* Center for Orbit Determination in Europe (CODE)           
/* Ultra-rapid GRE orbits starting year-day 24043 18 hour    
/* Observed/predicted: 24/24 hours (data used up to 044R)    
/* PCV:IGS20      OL/AL:FES2014b NONE     YN ORB:CoN CLK:BRD 
*  2024  2 12 18  0  0.00000000 
PG01  10017.227962 -21757.155189 -11451.757387    169.286245 
PG02  14675.739771 -21822.976616  -2052.019267   -486.484832 
PG03   8469.065183 -12995.901194 -21686.432325    188.867787 
PG04   3600.602597 -22237.722088 -13945.053317    290.029824 
PG05 -20341.276134   7377.183933  15289.811367   -161.559994 
PG06 -16369.020521  -2296.830107 -20745.620735    409.693247 
PG07  -1894.045106 -18515.401534  19259.776594    -60.352554 
PG08   8973.397509 -15470.338889  19399.830924   -166.689337 
PG09  -7116.144195 -25433.994890  -2585.513683     89.933932 
PG10  22629.595338  10998.556186   9210.119432      0.062606 
PG11 -21242.149685   8170.890518 -13627.298892   -573.517674 
PG12  -9883.448912  12694.506995 -21410.063052   -477.323298 
PG13 -13937.859196   5903.727931  21603.132559    624.913034 
PG14 -19730.979185 -13446.930472  11852.906315    323.976361 
PG15  -7222.733526  16617.677119  18862.775701    127.009782 
PG16  24409.248046   -401.590168  10670.590254   -364.118237 
. . . 
```
## Initial wet refractivity file
The initial values of the 3D Wet Refractivity model are necessary to solve the equation system with the MART algorithm. Radiosonde (RS) profiles are used to calculate these values, and these profiles are expanded to cover the entire area. After the calculation of the Wet refractivity values, they are stored in csv format (Fig7).
```
WMOID,HEIGHT,DATE,TIME,HEIGHT,N_DRY,N_WET,TEMPERATURE,PRESSURE,DEWPOINT,RHOWV 
12843,139,2024-02-01,11:00:00,139,279.0515,31.90512,278.56,10080,273.56,0.004893853 
12843,209,2024-02-01,11:00:00,209,278.1079,30.57998,277.36,10000,272.86,0.00467139 
12843,250,2024-02-01,11:00:00,250,276.9208,30.4007,277.16,9950,272.76,0.00464082 
12843,440,2024-02-01,11:00:00,440,267.8434,32.1,279.76,9720,273.76,0.004943895 
12843,601,2024-02-01,11:00:00,601,262.9998,31.27059,279.36,9530,273.36,0.004809611 
12843,846,2024-02-01,11:00:00,846,257.0624,31.71184,277.36,9250,273.36,0.004844292 
12843,1496,2024-02-01,11:00:00,1496,241.7266,25.98888,272.26,8530,270.16,0.003900615 
. . . 
```
## Results
The results of the Tomographic Reconstruction are stored in .npy (NumPy) format as a 3D matrix in the results directory (results/refractivity/refractivity_YYYY-MM-DD-hh.npy). The matrix values represent the wet refractivity values. The matrix indexes are in the following order: latitude, longitude, height. The indices represent the number of the voxel in the specified direction corresponding to the given tomographic grid files.
## Licenses
 OpATOM project is under MIT license.
## References
 - Bender M, Dick G, Ge M, Deng Z, Wickert J, Kahle HG, Raabe A, Tetzlaff G (2011) Development of a GNSS water vapour tomography system using algebraic reconstruction techniques. Adv Space Res 47:1704–1720. https://doi.org/10.1016/j.asr.2010.05.034 
 - Boehm J, Kouba J, Schuh H (2009) Forecast Vienna mapping functions 1 for real-time analysis of space geodetic observations. J Geod 83:397–401. https://doi.org/10.1007/s00190-008-0216-y 
 - Dach R, Lutz S, Walser P, Fridez P (2015) Bernese GNSS Software Version 5.2 User manual. https://doi.org/10.7892/boris.72297
 - Hilla S (2016) The extended standard product 3 orbit format (SP3-d). https://files.igs.org/pub/data/format/sp3d.pdf 
 - Horváth T, Viengdavanh R, Rózsa S (2014) Négydimenziós vízgőzmodellek előállítása GNSS tomográfiával (Construction of 4D water vapour models by means of GNSS tomography). Geomat Közlem 17:69–78. https://geomatika.epss.hun-ren.hu/storage/volumes/gk_XVII_1.pdf 
 - Lutz S, Beutler G, Schaer S, Dach R, Jäggi A (2014) CODE’s new ultra-rapid orbit and ERP products for the IGS. GPS Solut 20:239–250. https://doi.org/10.1007/s10291-014-0432-2 
 - Niell AE (1996) Global mapping functions for the atmosphere delay at radio wavelengths. J Geophys Res Solid Earth 101:3227–3246. https://doi.org/10.1029/95JB03048 
 - re3data.org: VMF Data Server; editing status 2020-12-14 (2020) re3data.org–Registry of Research Data Repositories. https://doi.org/10.17616/R3RD2H 
 - Rózsa S, Khaldi A, Ács Á, Turák B (2021) Multi-GNSS near real-time precipitable water vapour estimation for severe weather prediction. Bull Științ Univ Nord Baia Mare Ser D 35:777–786. https://www.researchgate.net/publication/369649633_MULTI-GNSS_NEAR_REAL TIME_PRECIPITABLE_WATER_VAPOUR_ESTIMATION_FOR_SEVERE_WEATHER_PREDICTION
 - Turák B, Khaldi A, Rózsa S (2024) Tomographic reconstruction of atmospheric water vapor profiles using multi-GNSS observations. Period Polytech Civ Eng 68:155–168. https://doi.org/10.3311/PPci.20559 
 - Weber J (2024) GSL Radiosonde Database. https://ruc.noaa.gov/raobs/General_Information.html 
## Authors
 - Bence Turák - Budapest University of Technology and Economics
 - Abir Khaldi - Budapest University of Technology and Economics
 - Szabolcs Rózsa - Budapest University of Technology and Economics
 
