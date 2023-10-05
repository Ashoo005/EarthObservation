
# MAIN FUNCTION TO CALL THE L1B MODULE

from l1b.src.l1b import l1b

# Directory - this is the common directory for the execution of the E2E, all modules
auxdir = r'C:\EarthObs\work\auxiliary'
indir = r'C:\EODP_TER_2021\EODP-TS-L1B\input'
# outdir = r'C:\EODP_TER_2021\EODP-TS-L1B\output'
# outdir = r'C:\EODP_TER_2021\EODP-TS-L1B\output1'
outdir = r'C:\EODP_TER_2021\EODP-TS-L1B\output_eq_false'


# Initialise the ISM
myL1b = l1b(auxdir, indir, outdir)
myL1b.processModule()
