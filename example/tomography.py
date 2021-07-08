import sys
sys.path.append('../src')
sys.path.append('../src/bernese_formats')
import broadcastnavreader
import readcrd
import readtrp
import epoch
import numpy as np



#input files
source_dir = '../data/tomography/'
#station coordinate file CRD
station_coords = source_dir+'HCONTROL.CRD'
#troposphere files
#Bernese troposphere file TRP
bernese_tropo = source_dir+'.TRP'
#VMF1 grid file
vmf1_grid = source_dir+'VMFG_20201102.H00'
#satellite broadcast files
brdc_mixed = source_dir+'BRDC00WRD_S_20211840000_01D_MN.rnx'

#epoch of the calculation
ep = epoch.Epoch(np.array([2021,7,3,6,0,0]))

#list of satellites
sat_list = ['G01', 'G02', 'G03', 'G04', 'G05', 'G06','G07', 'G08', 'G09', 'G10',
            'G11', 'G12', 'G13', 'G14', 'G15', 'G16','G17', 'G18', 'G19', 'G20',
            'G21', 'G22', 'G23', 'G24', 'G25', 'G26','G27', 'G28', 'G29', 'G30',
            'G31', 'G32', 'G33', 'G34', 'G35', 'G36','G37', 'G38', 'G39', 'G40',
            'R01', 'R02', 'R03', 'R04', 'R05', 'R06','R07', 'R08', 'R09', 'R10',
            'R11', 'R12', 'R13', 'R14', 'R15', 'R16','R17', 'R18', 'R19', 'R20',
            'R21', 'R22', 'R23', 'R24', 'R25', 'R26','R27', 'R28', 'R29', 'R30',
            'R31', 'R32', 'R33', 'R34', 'R35', 'R36','R37', 'R38', 'R39', 'R40',
            'E01', 'E02', 'E03', 'E04', 'E05', 'E06','E07', 'E08', 'E09', 'E10',
            'E11', 'E12', 'E13', 'E14', 'E15', 'E16','E17', 'E18', 'E19', 'E20',
            'E21', 'E22', 'E23', 'E24', 'E25', 'E26','E27', 'E28', 'E29', 'E30',
            'E31', 'E32', 'E33', 'E34', 'E35', 'E36','E37', 'E38', 'E39', 'E40']

network = readcrd.ReadCRD(station_coords).network
brdc = broadcastnavreader.BroadcastNavReader(brdc_mixed)


for sta in stations.getStations():
    print(sta)

exit()

for prn in sat_list:
    try:
        sat = brdc.getSatellite(prn)
        print(prn)
        print(sat.getSatPos(ep).getPLH())
    except epoch.TimeError as er:
        print(er)
    except KeyError as er:
        print(er)
