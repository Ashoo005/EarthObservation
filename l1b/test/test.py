from common.io.writeToa import readToa
import numpy as np
import matplotlib.pyplot as plt
import os

from config.globalConfig import globalConfig
myglobal = globalConfig()
bands = myglobal.bands

bands1 = ['VNIR-0', 'VNIR-1', 'VNIR-2', 'VNIR-3']


reference = r'C:\EODP_TER_2021\EODP-TS-L1B\output'
outdir = r'C:\EODP_TER_2021\EODP-TS-L1B\output1' #My results
outdir2 = r'C:\EODP_TER_2021\EODP-TS-L1B\input'
outdir_no_eq = r'C:\EODP_TER_2021\EODP-TS-L1B\output_eq_false' #MY results no_eq


# 1. Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at
# least 3-sigma of the points.

tol = 0.01e-2
three_sigma = 1-0.997

name1 = []
name2 = []
name3 = []
name4 = []
for i in range(len(bands)):
    name1.append('l1b_toa_' + 'eq_' + str(bands[i]) + '.nc')
    name2.append('ism_toa_'+'isrf_'+str(bands[i])+'.nc')
    name3.append('ism_toa_'+'isrf_'+str(bands[i]))
    name4.append(('l1b_toa_'+str(bands[i])+'.nc'))

for val in range(len(name1)):
    toa_l1b = readToa(outdir, name1[val])
    toa_input = readToa(reference, name1[val])
    toa_l1b_eq = readToa(outdir_no_eq, name4[val])
    toa_lib_eq_input = readToa(outdir_no_eq, name4[val])

    counter = 0
    counter_eq = 0
    points_threshold = toa_input.shape[0] * toa_input.shape[1] * three_sigma

    result =np.zeros((toa_l1b.shape[0],toa_l1b.shape[1]))
    result_eq =np.zeros((toa_l1b_eq.shape[0],toa_l1b_eq.shape[1]))
    for i in range(toa_l1b.shape[0]):
        for j in range(toa_l1b.shape[1]):
            result[i, ] = toa_l1b[i,j]-toa_input[i,j]
            result_eq[i,j] - toa_l1b_eq[i,j]-toa_lib_eq_input[i,j]

            if np.abs(result[i,j]>tol):
                counter += 1

            if np.abs(result_eq[i,j]>tol):
                counter_eq += 1
    print('Band ' + bands[val])
    if counter < points_threshold:
        print('Test with eq ' + name1[val] + ' OK')
    else:
        print('Test with eq ' + name1[val] + ' NOK')

    if counter_eq < points_threshold:
        print('Test with no eq ' + name4[val] + ' OK')
    else:
        print('Test with no eq ' + name4[val] + ' NOK')

# 2. For the central ALT position, plot the restored signal (l1b_toa), and the TOA after the ISRF
# (ism_toa_isrf). Explain the differences.

    for bend in bands1:
        toa_rest = readToa(outdir, f'l1b_toa_{bend}.nc')
        toa_ref = readToa(outdir2, f'ism_toa_isrf_{bend}.nc')

        plt.figure()
        plt.plot(toa_rest[50, :], 'r-', label="Restored Signal", linewidth=1.0)
        plt.plot(toa_ref[50, :], 'b-', label="TOA after ISRF", linewidth=1.0)
        plt.xlabel("ACT [-]")
        plt.ylabel("TOA [mW/m2/sr]")
        plt.legend()

        output_dir = r'C:\EODP_TER_2021\EODP-TS-L1B\plots_true_eq_central_alt'
        output_filename = os.path.join(output_dir, f'plot_{bend}.png')
        plt.savefig(output_filename)
        plt.close()

# EQUALIZATION PLOTS

    toa_1 = readToa(outdir, name1[val])
    mid_value = int(toa_1.shape[0]/2)
    fig4,ax4 = plt.subplots()
    plt.grid(False)
    plt.suptitle('Alt = '+str(mid_value))
    plt.xlabel('Across Track [-]')
    plt.ylabel('Radiances [mW/m2/sr]')
    ax4.plot(toa_1[mid_value,:],'k')
    fig4.savefig(outdir +'/' + name1[val] + 'equalized' + '_graph.png')
    plt.show()

# NO EQUALIZATION PLOTS

    toa_eq = readToa(outdir_no_eq,name4[val])
    mid_value = int(toa_eq.shape[0]/2)
    fig3,ax3 = plt.subplots()
    plt.grid(False)
    plt.suptitle('Alt = '+str(mid_value))
    plt.xlabel('Across Track [-]')
    plt.ylabel('Radiances [mW/m2/sr]')
    ax3.plot(toa_eq[mid_value,:],'k')
    fig3.savefig(outdir_no_eq+'/'+name4[val]+'_non_equalized'+'_graph.png')
    plt.show()


