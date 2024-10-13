import sys
sys.path.append('../../../src')
sys.path.append('../../../src/bernese_formats')
import epoch
import numpy as np
import refractivityprofile
from scipy import interpolate
#input files
code_letter = 'ABCDEFGHIJKLMNOPQRSTUVWX'

#source_dir = '../../data/tomography/2021/'
#output_dir = '../../data/tomography/2021/result/'

#station coordinate file CRD
#station_coords = source_dir+'METEONET.CRD'
#troposphere files
root_dir = "sample_data/"
gridp_file = root_dir + 'gridp.csv'
gridl_file = root_dir + 'gridl.csv'
gridh_file = root_dir + 'gridh.csv'
gridp = np.loadtxt(gridp_file)*np.pi/180#np.arange(min[0], max[0], 0.6*np.pi/180)
gridl = np.loadtxt(gridl_file)*np.pi/180#np.arange(min[1], max[1], 1.449*np.pi/180)
gridh = np.loadtxt(gridh_file)

gridlc = np.empty((0,))
gridpc = np.empty((0,))
gridhc = np.empty((0,))

for i in range(0,np.shape(gridl)[0]-1):
    gridlc=np.append(gridlc, (gridl[i] + gridl[i+1])/2)

for i in range(0,np.shape(gridp)[0]-1):
    gridpc=np.append(gridpc, (gridp[i] + gridp[i+1])/2)

for i in range(0,np.shape(gridh)[0]-1):
    gridhc=np.append(gridhc, (gridh[i] + gridh[i+1])/2)


raob_dir=root_dir+"raobs/files/"
refractivity_dir="results/refractivity/"


#ep_start = epoch.Epoch(np.array([2022,3,1,0,0,0]))
ep_start = epoch.Epoch(np.array([2024,2,4,1,0,0]))
ep_end = epoch.Epoch(np.array([2024,2,28,23,0,0]))
#ep_end = epoch.Epoch(np.array([2022,4,11,23,0,0]))

ep = ep_start

eps = []

sondes = [
#{'id': 10393, 'phi': 52.22, 'lam': 14.12},
#{'id': 10584, 'phi': 50.57, 'lam': 10.37},
#{'id': 10739, 'phi': 48.83, 'lam': 9.20},
#{'id': 10868, 'phi': 48.25, 'lam': 11.55},
{'id': 11747, 'phi': 49.45, 'lam': 17.13},
#{'id': 12374, 'phi': 52.40, 'lam': 20.97},
{'id': 14240, 'phi': 45.82, 'lam': 16.03},
#{'id': 15420, 'phi': 44.50, 'lam': 26.13},
{'id': 12843, 'phi': 47.43, 'lam': 19.18},
{'id': 12982, 'phi': 46.25, 'lam': 20.10},
{'id': 11952, 'phi': 49.03, 'lam': 20.32}



]


while ep <= ep_end:


    eps.append(ep)

    ep = ep + epoch.Epoch(np.array([0,0,0,1,0,0]))

initial_ep = ep_start - epoch.Epoch(np.array([0,0,0,1,0,0]))
for ep in eps:
    print(ep)
    print('BBBBBBBBBB')
    initial_ep_temp = initial_ep

    epForRequest = ep
    #sql = "SELECT HEIGHT, N_WET FROM RAOBSREFR WHERE DATE='"+epForRqeuest.date()+"' AND TIME='"+epForRqeuest.time()+"' ORDER BY HEIGHT ASC"
    
    #read initial wet refractivity valus (last available RS file) Budapest RAOB statio
    x0_3D_w_profile = np.empty((0,2))
    while(1):
        epForRequest = epForRequest - epoch.Epoch(np.array([0,0,0,1,0,0]))
        raob_file=raob_dir+"12843_{:d}-{:d}-{:d}_{:d}.csv".format(epForRequest.dt[0], epForRequest.dt[1], epForRequest.dt[2], epForRequest.dt[3])
        try:
            x0_3D_w_profile = np.loadtxt(raob_file, delimiter=",", usecols=(1,6), skiprows=1)        
        except FileNotFoundError as err:
            print(err)
        '''
        sql = "SELECT HEIGHT, N_WET FROM RAOBSREFR WHERE DATE='"+epForRequest.date()+"' AND TIME='"+epForRequest.time()+"' AND WMOID="+ str(12843) +" ORDER BY HEIGHT ASC"
        dbcursor = dbconfig.database.cursor()
        dbcursor.execute(sql)

        x0_3D_w_profile = np.empty((0,2))
        for s in dbcursor.fetchall():

            x0_3D_w_profile = np.append(x0_3D_w_profile, [[s[0], s[1]]], axis=0)
        '''
        if(np.shape(x0_3D_w_profile)[0] > 0):
            break
    print('AAA')
    
    initial_profile_val = np.empty((len(gridh)-1,))
    nanret = False
    for i in range(0,len(gridh)-1):
        layer = x0_3D_w_profile[np.all((x0_3D_w_profile[:,0]>=gridh[i],x0_3D_w_profile[:,0]<=gridh[i+1]),axis=0)]
        N = np.mean(layer[:,1])
        if not np.isnan(N):
            initial_profile_val[i] = N
            if nanret:
                initial_profile_val[i-1] = N
                nanret = False

        else:
            if i > 0:
                initial_profile_val[i] = initial_profile_val[i-1]
            else:
                nanret = True

    try:
        refractivity_file=refractivity_dir+"refractivity_{0:4d}-{1:02d}-{2:02d}-{3:02d}.npy".format(ep.dt[0], ep.dt[1], ep.dt[2], ep.dt[3])
        tomography_3D= np.load(refractivity_file)
    except Exception as err:
        #print(err)
        continue
    for RS in sondes:
        tomography_profile=np.empty((0,2))
        for i in range(0, np.shape(gridhc)[0]):
            f_Nw = interpolate.interp2d(gridlc, gridpc,tomography_3D[:,:,i], kind='linear')
            Nw = f_Nw(RS['lam']*np.pi/180, RS['phi']*np.pi/180)[0]
            tomography_profile = np.append(tomography_profile, [[gridhc[i], Nw]], axis=0)


        initial_profile = np.append([tomography_profile[:,0]], [initial_profile_val], axis=0).T

        if np.shape(tomography_profile)[0] == 0:
            continue
        initial_ep_temp = ep


        raob_file=raob_dir+str(RS["id"])+"_{:d}-{:d}-{:d}_{:d}.csv".format(ep.dt[0], ep.dt[1], ep.dt[2], ep.dt[3])
        
        try:
            sonde_profile = np.loadtxt(raob_file, delimiter=",", usecols=(1,6), skiprows=1)  
        except:
            continue

        if np.shape(sonde_profile)[0] == 0:
            continue

        profile_output = "results/figures/profiles/profile_{4:4d}_{0:4d}-{1:02d}-{2:02d}-{3:02d}.tif".format(ep.dt[0], ep.dt[1], ep.dt[2], ep.dt[3], RS["id"])
        refractivityprofile.refractivityProfile(('Radiosonde', 'Initial', 'Tomography'), (sonde_profile, initial_profile, tomography_profile), str(RS["id"]), profile_output, ep)

        stat_sonde = sonde_profile[np.all((sonde_profile[:,0] >= 500 , sonde_profile[:,0] <= 10000), axis=0), :]

        interp_tomography = interpolate.interp1d(tomography_profile[:,0],tomography_profile[:,1], kind="linear")

        stat_tomography = stat_sonde[:,0]

        stat_tomography = np.append([stat_tomography], [interp_tomography(stat_tomography)], axis=0).T


        v = stat_sonde[:,1] - stat_tomography[:,1]

        stdev = np.std(v)
        mean = np.mean(v)


        fid = open('results/figures/profiles/profile_statistics.csv', 'a')

        print(str(RS["id"]) + "," + str(ep) + "," + str(mean) + "," + str(stdev) ,file=fid)

        fid.close()

        fid = open('results/figures/profiles/profile_residuals.csv', 'a')
        residuals = np.append([stat_sonde[:,0]], [v], axis=0).T
        for r in residuals:
            print(str(RS['id']) + "," + str(ep) + "," + str(r[0]) + "," + str(r[1]) , file=fid)


        fid.close()


    initial_ep = initial_ep_temp













#np.save(filename+'.npy',Nw_3D)
#np.save(source_dir+'initial.npy', x0_3D )
#np.save(source_dir+'initial_'+c+'.npy', x0_3D )



#plotRefractivity(filename+'.png', Nw_3D)

#x0_3D = res[0]
