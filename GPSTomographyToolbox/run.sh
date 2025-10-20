#!/bin/bash

#*****************************************************
#
# Running the GNSS-tomography processing script
#
#*****************************************************
echo "GNSSCT process start"

DIR="/home/$USER/projects/GeoPack/GPSTomographyToolbox/"
SATELLITE=$DIR"sample_data/orbit/"
VMF1GRID=$DIR"sample_data/vmf1/"
GRID=$DIR"sample_data/"
#TOMOGRAPHY=$DIR"sample_data"
INITIAL_VALUES=$DIR"sample_data/raobs/files/"
TRP=$DIR"sample_data/TRP/"


RAOB_STN="12843"

CTSCRIPT=$DIR


YEAR=$1
MONTH=$2
DAY=$3
HOUR=$4
MINUTE=0
SECOND=0
#YEAR=2024
#MONTH=2
#DAY=9
#HOUR=2
#MINUTE=0
#SECOND=0
FIRST_SEC_GPST=$(date -u -d"1980-1-6 0:0:0" +%s)
TSEC=$(date -u -d"$YEAR-$MONTH-$DAY $HOUR:$MINUTE:$SECOND" +%s)


SEC_FROM_FIRST_EPOCH=$(($TSEC-$FIRST_SEC_GPST))

GPSWEEK=$(($SEC_FROM_FIRST_EPOCH/(168*3600)))
TOW=$(($SEC_FROM_FIRST_EPOCH-($GPSWEEK*168*3600)))
DOW=$(($TOW/(24*3600)))
echo $SEC_FROM_FIRST_EPOCH
echo $GPSWEEK
echo $DOW
echo $TOW
#TSEC=$(date -u -d"-5 hour" +%s)
#GPSWEEK=$(((TSEC-315961200-3600)/86400/7))
#DOW=$(date -u -d"-5 hour" +%w)
#ORB_HOUR=`date -u -d"-5 hour" +%k`
#YEAR=`date -u -d"-1 hour" +%y`
#YEAR4=`date -u -d"-1 hour" +%Y`
#MONTH=`date -u -d"-1 hour" +%m`
#DAY=`date -u -d"-1 hour" +%d`
#DOY=`date -u -d"-1 hour" +%j`
#HOUR=`date -u -d"-1 hour" +%k`
#WOY=`date -u -d"-1 hour" +%U`


ORBITSTART=$((ORB_HOUR/6*6))
if [ $((ORBITSTART)) -lt 10 ]; then ORBITSTART=0${ORBITSTART}
fi
counter=0
while [ 1 ]
do
    RAOB_FILE=$INITIAL_VALUES$RAOB_STN"_"`date -u -d" -$counter hours $YEAR-$MONTH-$DAY $HOUR:$MINUTE:$SECOND" +%Y-%-m-%-d_%-k`.csv
    if `test -e $RAOB_FILE`
    then
        break
    fi
    
    counter=$(($counter+1))
    if [ $counter -gt 48 ]
    then 
        break
    fi
done





GRIDP=$DIR"sample_data/gridp.csv"
GRIDL=$DIR"sample_data/gridl.csv"
GRIDH=$DIR"sample_data/gridh.csv"

SATELLITE_FILE=$SATELLITE"CDU$GPSWEEK$DOW"_"$ORBITSTART.EPH"
STATIONS=$DIR"sample_data/WEEK2304.CRD"


EPOCH=$YEAR"-"$MONTH"-"$DAY"-"$HOUR"-0-0"
echo $EPOCH
cd $CTSCRIPT
CHAR=`awk -v n=$HOUR 'BEGIN{printf "%c", 65+n}'`

TRPFILE=$TRP"CO`date -u -d"$YEAR-$MONTH-$DAY $HOUR:$MINUTE:$SECOND" +%y%j`"$CHAR".TRP"


echo "gnssct.py --satellites=$TOMOGRAPHY$SATELLITE_FILE --stations=$STATIONS --tropofile=$TRPFILE --gridp=$GRIDP --gridl=$GRIDL --gridh=$GRIDH --vmf1loc=$VMF1GRID --epoch=$EPOCH --initial_w=$RAOB_FILE"
python3 gnssct.py --satellites=$TOMOGRAPHY$SATELLITE_FILE --stations=$STATIONS --tropofile=$TRPFILE --gridp=$GRIDP --gridl=$GRIDL --gridh=$GRIDH --vmf1loc=$VMF1GRID --epoch=$EPOCH --initial_w=$RAOB_FILE


echo "Done."

