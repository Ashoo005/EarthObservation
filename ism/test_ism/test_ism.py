from common.io.writeToa import readToa
import numpy as np

from config.globalConfig import globalConfig
myglobal = globalConfig()
bands = myglobal.bands

reference = r'C:\EODP_TER_2021\EODP-TS-ISM\output' #Lucia output
outdir = r'C:\EODP_TER_2021\EODP-TS-ISM\myoutput' #My Output
tol = 0.01e-2
three_sigma = 1-0.997

print('Test 1: Optical Module')
print('---------------------')

name1_isrf = []
name1 = []
for i in range(len(bands)):
    name1.append('ism_toa_' + 'optical_' + str(bands[i]) + '.nc')
    name1_isrf.append('ism_toa_' + 'isrf_' + str(bands[i]) + '.nc')


for val in range(len(bands)):
    toa_ism = readToa(outdir, name1[val])
    toa_ism_input = readToa(reference, name1[val])
    toa_isrf_ism = readToa(outdir, name1_isrf[val])
    toa_isrf_ism_input = readToa(reference, name1_isrf[val])

    result =np.zeros((toa_ism.shape[0],toa_ism.shape[1]))
    result_isrf =np.zeros((toa_isrf_ism.shape[0],toa_isrf_ism.shape[1]))

    counter_isrf = 0
    counter =0
    for i in range(toa_ism.shape[0]):
        for j in range(toa_ism.shape[1]):
            result[i,j] = toa_ism[i,j]-toa_ism_input[i, j]
            result_isrf[i,j] = toa_isrf_ism[i, j]-toa_isrf_ism_input[i, j]

            if np.abs(result[i,j]>tol):
                counter += 1
            if np.abs(result_isrf[i,j]>tol):
                counter_isrf+= 1

    points_threshold = toa_ism.shape[0] * toa_ism.shape[1] * three_sigma

    print('---------------------')
    if counter < points_threshold:
        print('Test ' + name1[val] + ' OK')
    else:
        print('Test ' + name1[val] + ' NOK')

    if counter_isrf < points_threshold:
        print('Test ' + name1_isrf[val] + ' OK')
    else:
        print('Test ' + name1_isrf[val] + ' NOK')
    print('---------------------')

print('Test 2: Detection Module')
print('---------------------')

name_e = []
name_detection = []
name_ds = []
name_prnu = []
for i in range(len(bands)):
    name_e.append('ism_toa_'+'e_'+str(bands[i])+'.nc')
    name_detection.append('ism_toa_'+'detection_'+str(bands[i])+'.nc')
    name_ds.append('ism_toa_'+'ds_'+str(bands[i])+'.nc')
    name_prnu.append(('ism_toa_'+'prnu_'+str(bands[i])+'.nc'))

if len(name_e) != len(name_detection) != len(name_ds) != len(name_prnu):
    print('Error with the size of the toa in the Detection Module')


for val in range(len(name_e)):

    toa_ism_ds = readToa(outdir, name_ds[val])
    toa_ism_detection= readToa(outdir, name_detection[val])
    toa_ism_e = readToa(outdir, name_e[val])
    toa_ism_prnu = readToa(outdir, name_prnu[val])

    toa_ism_e_input = readToa(reference, name_e[val])
    toa_ism_ds_input = readToa(reference, name_ds[val])
    toa_ism_detection_input= readToa(reference, name_detection[val])
    toa_ism_prnu_input = readToa(reference, name_prnu[val])

    result_e =np.zeros((toa_ism_e.shape[0],toa_ism_e.shape[1]))
    result_ds =np.zeros((toa_ism_ds.shape[0],toa_ism_ds.shape[1]))
    results_detection = np.zeros((toa_ism_detection.shape[0],toa_ism_detection.shape[1]))
    results_prnu= np.zeros((toa_ism_prnu.shape[0],toa_ism_prnu.shape[1]))

    counter_e = 0
    counter_ds = 0
    counter_detection = 0
    counter_prnu = 0


    for i in range(toa_ism_e.shape[0]):
        for j in range(toa_ism_e.shape[1]):

            result_e[i,j]=toa_ism_e[i,j]-toa_ism_e_input[i,j]
            result_ds[i,j]=toa_ism_ds[i,j]-toa_ism_ds_input[i,j]
            results_detection[i,j]=toa_ism_detection[i,j]-toa_ism_detection_input[i,j]
            results_prnu[i,j]=toa_ism_prnu[i,j]-toa_ism_prnu_input[i,j]

            if np.abs(result_e[i,j]>tol):
                counter_e += 1
            if np.abs(result_ds[i,j]>tol):
                counter_ds+= 1
            if np.abs(results_detection[i,j]>tol):
                counter_detection += 1
            if np.abs(results_prnu[i,j]>tol):
                counter_prnu += 1

    print('---------------------')
    if counter_e < points_threshold:
        print('Test ' + name_e[val] + ' OK')
    else:
        print('Test ' + name_e[val] + ' NOK')

    if counter_ds < points_threshold:
        print('Test ' + name_ds[val] + ' OK')
    else:
        print('Test ' + name_ds[val] + ' NOK')

    if counter_detection < points_threshold:
        print('Test ' + name_detection[val] + ' OK')
    else:
        print('Test ' + name_detection[val] + ' NOK')

    if counter_prnu < points_threshold:
        print('Test ' + name_prnu[val] + ' OK')
    else:
        print('Test ' + name_prnu[val] + ' NOK')
    print('---------------------')
