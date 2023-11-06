from common.io.writeToa import readToa
import numpy as np

from config.globalConfig import globalConfig
myglobal = globalConfig()
bands = myglobal.bands

reference = r'C:\EODP_TER_2021\EODP-TS-L1C\output' #Lucia Output
outdir = r'C:\EODP_TER_2021\EODP-TS-L1C\myoutput' #My Results
tol = 0.01e-2
three_sigma = 1-0.997

name = []
for i in range(len(bands)):
    name.append('l1c_toa_'+str(bands[i])+'.nc')

for val in range(len(bands)):
    toa_l1c = readToa(outdir, name[val])
    toa_l1c_input = readToa(reference, name[val])
    toa_l1c_sort = np.sort(toa_l1c)
    toa_l1c_input_sort = np.sort(toa_l1c_input)
    result =np.zeros(toa_l1c.shape[0])
    counter = 0
    for i in range(toa_l1c.shape[0]):
            result[i] = toa_l1c_sort[i]-toa_l1c_input_sort[i]

            if np.abs(result[i]>tol):
                counter += 1

    points_threshold = toa_l1c.shape[0] * three_sigma

    print('---------------------')
    if counter < points_threshold:
        print('Test ' + name[val] + ' OK')
    else:
        print('Test ' + name[val] + ' NOK')

#     self.plotL1cToa(self,)
#
def plotL1cToa(self,lat_l1c,lon_l1c, toa_l1c, band):
    '''
    NOTE: doesn't work, bug in the color property
    Plot the L1B and L1C grids superimposed
    :param lat: L1B latitudes [deg]
    :param lon: L1B longitudes [deg]
    :param lat_l1c: L1C latitudes [deg] - MGRS grid
    :param lon_l1c: L1C longitudes [deg]
    :return: NA
    '''

    jet = cm.get_cmap('jet', len(lat_l1c))
    toa_l1c[np.argwhere(toa_l1c<0)] = 0
    max_toa = np.max(toa_l1c)

    # Plot stuff
    fig = plt.figure(figsize=(20,10))
    for ii in range(100): # range(len(lat_l1c)):
        clr = jet(toa_l1c[ii]/max_toa)
        plt.plot(lon_l1c, lat_l1c, '.',color=clr, markersize=10)
    plt.title('Projection on ground', fontsize=20)
    plt.xlabel('Longitude [deg]', fontsize=16)
    plt.ylabel('Latitude [deg]', fontsize=16)
    plt.grid()
    plt.axis('equal')
    plt.savefig(self.outdir + 'toa_' + band + '.png')
    plt.close(fig)
