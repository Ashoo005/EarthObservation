from common.io.writeToa import readToa
import matplotlib.pyplot as plt
import numpy as np
import os

# 0. Read outputs
dir_isrf = r'C:\EODP_TER_2021\EODP-TS-L1B\input'
dir_l = r'C:\EODP_TER_2021\EODP-TS-L1B\output'
dir_a_true = r'C:\EODP_TER_2021\EODP-TS-L1B\output1'
dir_a_false = r'C:\EODP_TER_2021\EODP-TS-L1B\output_eq_false'

bands = ['VNIR-0', 'VNIR-1', 'VNIR-2', 'VNIR-3']

# # 1. Check for all bands that the differences with respect to the output TOA (l1b_toa_) are <0.01% for at
# # least 3-sigma of the points.
# toa_l_eq = []
# toa_a_eq = []
# for band in bands:
#     toa_l = readToa(dir_l, f'l1b_toa_eq_{band}.nc')
#     toa_a = readToa(dir_a_true, f'l1b_toa_eq_{band}.nc')
#     toa_l_eq.append(toa_l)
#     toa_a_eq.append(toa_a)

# if len(toa_l_eq) == len(toa_a_eq):
#     substraction_max_toa = []
#     substraction_min_toa = []
#     for i in range(len(toa_l_eq)):
#         substraction_eq = toa_l_eq[i] - toa_a_eq[i]
#
#         max = np.max(substraction_eq)
#         min = np.max(substraction_eq)
#
#         print(substraction_max_toa.append(max))
#         print(substraction_min_toa.append(max))

#2. For the central ALT position, plot the restored signal (l1b_toa), and the TOA after the ISRF
#(ism_toa_isrf). Explain the differences.
for band in bands:
    toa_rest = readToa(dir_a_true, f'l1b_toa_{band}.nc')
    toa_isrf = readToa(dir_isrf, f'ism_toa_isrf_{band}.nc')

    plt.figure()
    plt.plot(toa_rest[50, :], 'r-', label="Restored Signal", linewidth=1.0)
    plt.plot(toa_isrf[50, :], 'b-', label="TOA after ISRF", linewidth=1.0)
    plt.xlabel("ACT [-]")
    plt.ylabel("TOA [mW/m2/sr]")
    plt.legend()
#
    output_dir = r'C:\EODP_TER_2021\EODP-TS-L1B\plots_true'
    output_filename = os.path.join(output_dir, f'plot_{band}.png')
    plt.savefig(output_filename)
    plt.close()

#3. Do another run of the L1B with the equalization enabled to false. Plot the restored signal for this case
#and for the case with the equalization set to True. Compare.
for band in bands:
    toa_eq_false = readToa(dir_a_false, f'l1b_toa_{band}.nc')
    toa_eq_true = readToa(dir_a_true, f'l1b_toa_{band}.nc')

    plt.figure()
    plt.plot(toa_eq_false[50, :], 'r-', label="Restored Signal without equalization", linewidth=1.0)
    plt.plot(toa_eq_true[50, :], 'b-', label="Restored Signal with equalization", linewidth=1.0)
    plt.xlabel("ACT [-]")
    plt.ylabel("TOA [mW/m2/sr]")
    plt.legend()

    output_dir = r'C:\EODP_TER_2021\EODP-TS-L1B\plots_true_false_compared'
    output_filename = os.path.join(output_dir, f'plot_{band}.png')
    plt.savefig(output_filename)
    plt.close()


# from common.io.writeToa import readToa
# import numpy as np
# import matplotlib.pyplot as plt
#
# from config.globalConfig import globalConfig
# myglobal = globalConfig()
# bands = myglobal.bands
#
# from l1b.src.l1b import l1b
#
# # Directory - this is the common directory for the execution of the E2E, all modules
# #auxdir = r'C:\EarthObs\work\auxiliary'
# #indir = r'C:\EODP_TER_2021\EODP-TS-L1B\input'
#
# ref = r'C:\EODP_TER_2021\EODP-TS-L1B\output' # Lucia Results
# outdir = r'C:\EODP_TER_2021\EODP-TS-L1B\output1' # My Results
# dirisrf = r'C:\EODP_TER_2021\EODP-TS-L1B\input' # Equalized
# outdir_no_eq = r'C:\EODP_TER_2021\EODP-TS-L1B\output_no_eq' # My Results No Equalization
#
# tol = 0.01e-2
# three_sigma = 1-0.997
#
# name1 = []
# name2 = []
# name3 = []
# name4 = []
#
# for i in range(len(bands)):
#     name1.append('l1b_toa_'+'eq_'+str(bands[i])+'.nc')
#     name2.append('ism_toa_'+'isrf_'+str(bands[i])+'.nc')
#     name3.append('ism_toa_'+'isrf_'+str(bands[i]))
#     name4.append(('l1b_toa_'+str(bands[i])+'.nc'))
#
# for value in range(len(name1)):
#     toa_l1b = readToa(outdir,name1[value])
#     toa_input = readToa(ref,name1[value])
#     toa_l1b_eq = readToa(outdir_no_eq,name4[value])
#     # toa_lib_eq_input = readToa(outdir_no_eq,name4[value])
#
#     counter = 0
#     counter_eq = 0
#     points_threshold = toa_input.shape[0] * toa_input.shape[1] * three_sigma
#
#     result = np.zeros((toa_l1b.shape[0], toa_l1b.shape[1]))
#     # result_eq = np.zeros((toa_l1b_eq.shape[0], toa_l1b_eq.shape[1]))
#     for i in range(toa_l1b.shape[0]):
#         for j in range(toa_l1b.shape[1]):
#             result[i, j] = toa_l1b[i, j] - toa_input[i, j]
#             # result_eq[i, j] = toa_l1b_eq[i, j] - toa_lib_eq_input[i, j]
#     #
#             if np.abs(result[i, j] > tol):
#                 counter += 1
#     #
#             # if np.abs(result_eq[i, j] > tol):
#             #     counter_eq += 1
#     print('Band ' + bands[value])
#     if counter < points_threshold:
#         print('Test with eq ' + name1[value] + ' Pass')
#     else:
#         print('Test with eq ' + name1[value] + ' Not Pass')
#
#     if counter_eq < points_threshold:
#         print('Test with no eq ' + name4[value] + ' Pass')
#     else:
#         print('Test with no eq ' + name4[value] + ' No Pass')