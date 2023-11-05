from common.io.writeToa import readToa
import numpy as np

from config.globalConfig import globalConfig
myglobal = globalConfig()
bands = myglobal.bands

reference = r'C:\EODP_TER_2021\EODP-TS-ISM\output' #Lucia output
outdir = r'C:\EODP_TER_2021\EODP-TS-ISM\myoutput' #My Output
tol = 0.01e-2
three_sigma = 1-0.997

print('Test Optical Module')
print('---------------------')

namee_isrf = []
namee = []
for i in range(len(bands)):
    namee.append('ism_toa_'+'optical_'+str(bands[i])+'.nc')
    namee_isrf.append('ism_toa_'+'isrf_'+str(bands[i])+'.nc')


for inn in range(len(bands)):
    toa_ism = readToa(outdir,namee[inn])
    toa_ism_input = readToa(reference,namee[inn])
    toa_isrf_ism = readToa(outdir,namee_isrf[inn])
    toa_isrf_ism_input = readToa(reference,namee_isrf[inn])

    result =np.zeros((toa_ism.shape[0],toa_ism.shape[1]))
    result_isrf =np.zeros((toa_isrf_ism.shape[0],toa_isrf_ism.shape[1]))

    counter_isrf = 0
    counter =0
    for i in range(toa_ism.shape[0]):
        for j in range(toa_ism.shape[1]):
            result[i,j]=toa_ism[i,j]-toa_ism_input[i,j]
            result_isrf[i,j] = toa_isrf_ism[i,j]-toa_isrf_ism_input[i,j]

            if np.abs(result[i,j]>tol):
                counter += 1
            if np.abs(result_isrf[i,j]>tol):
                counter_isrf+= 1

    points_treshold = toa_ism.shape[0]*toa_ism.shape[1]*three_sigma

    print('---------------------')
    if counter < points_treshold:
        print('Test ' + namee[inn] + ' OK')
    else:
        print('Test ' + namee[inn] + ' NOK')

    if counter_isrf < points_treshold:
        print('Test ' + namee_isrf[inn] + ' OK')
    else:
        print('Test ' + namee_isrf[inn] + ' NOK')
    print('---------------------')

print('Test Detection Module')
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


for inn in range(len(name_e)):

    toa_ism_ds = readToa(outdir,name_ds[inn])
    toa_ism_detection= readToa(outdir,name_detection[inn])
    toa_ism_e = readToa(outdir,name_e[inn])
    toa_ism_prnu = readToa(outdir,name_prnu[inn])

    toa_ism_e_input = readToa(reference,name_e[inn])
    toa_ism_ds_input = readToa(reference,name_ds[inn])
    toa_ism_detection_input= readToa(reference,name_detection[inn])
    toa_ism_prnu_input = readToa(reference,name_prnu[inn])

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
    if counter_e < points_treshold:
        print('Test ' + name_e[inn] + ' OK')
    else:
        print('Test ' + name_e[inn] + ' NOK')

    if counter_ds < points_treshold:
        print('Test ' + name_ds[inn] + ' OK')
    else:
        print('Test ' + name_ds[inn] + ' NOK')

    if counter_detection < points_treshold:
        print('Test ' + name_detection[inn] + ' OK')
    else:
        print('Test ' + name_detection[inn] + ' NOK')

    if counter_prnu < points_treshold:
        print('Test ' + name_prnu[inn] + ' OK')
    else:
        print('Test ' + name_prnu[inn] + ' NOK')
    print('---------------------')
