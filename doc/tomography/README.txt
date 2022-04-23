Tomography processing is a python3 compatible script on linux OS. (On Ubuntu OS is surely stable.)

Usage:
gnssct.py  [OPTION]
    -s,  --satellites      location of satellite orbits file in .SP3 format
    -S,  --stations        location of the station coordinates file in Bernese .CRD format
         --gridp           location of grid file in the direction of North-South in .csv format (degrees)
         --gridl           location of grid file in the direction of East-West in .csv format (degrees)
         --gridh           location of elevation grid file .csv format (metres)
    -v,  --vmf1loc         location of VMF1 parameters grid files directory
    -i,  --initial_w       location of the initial wet refractivity values in .npy format
         --initial_h       location of the initial hydrostatic refractivity values in .npy format
    -e,  --epoch           epoch in format YYYY-MM-DD-hh-mm-ss
    -d,  --database        name of the python modul for the database configuration


Although, all of the input parameters are required, the --initial_h is not used.
The initial values are overwritten with the last result of the tomography after every calculation.

The grid files define the tomography voxels.
The VMF1 parameters grid files hes to be given in this directory and the name format has to be:
YYYY/VMFG_YYYYMMDD.Hhh'
The script able to use more VMF1 grid file for the interpollation.

The tropospheric delay data come from mysql database and the wet refractivity results are saved in the database.
Example:

python3 gnssct.py --satellites=tomography/CDU22066_00.SP3 --stations=tomography/METEONET.CRD --gridp=tomography/gridp.csv --gridl=tomography/gridl.csv --gridh=tomography/gridh.csv --vmf1loc=tomography/vmf1/ --epoch=2022-04-23-8-0-0 --initial_w=tomography/initial_w.npy --initial_h=tomography/initial_h.npy  --database=dbconfig

required python modules:
wget
NumPy
scipy
mysql.connector
