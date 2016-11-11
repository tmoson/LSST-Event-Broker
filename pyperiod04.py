import os
import numpy as np


def period04(lc, copy_lc='temp.lc', output_ft='temp.ft', output_project='project.p04', batchfile='batch_temp.bat'):
    """
    [1] lc: array, col1 = time, col2 = mag, col3 = error_mag
    """

    # Constant values ...
    fmin, fmax = str(0), str(50)  # range of frequencies: mim to max
    np.savetxt(copy_lc, lc)  # Write out the light curve file

    # The new version of Period04 was supported by Patrick Lenz.
    f = open(batchfile, 'w')
    f.write('import to ' + copy_lc + '\n')
    f.write('fourier ' + fmin + ' ' + fmax + ' o y\n')
    # f.write('addharmonics 3 \n')
    #f.write('fit o 2 \n')
    #f.write('saveproject ' + output_project + '\n')
    f.write('savefourier ' + fmin + ' ' + fmax + ' o y ' + output_ft + '\n')
    f.write('exit\n')
    f.close()

    os.system('period04 -batch=' + batchfile)  # Run the batch file
    ft = np.loadtxt(output_ft)  # Read in the FT
    if copy_lc == 'temp.lc': os.remove(copy_lc)  # clean up light curve copy
    if batchfile == 'batch_temp.bat': os.remove(batchfile)  # clean up batch file
    print("123")
    return ft  # Return the Period04


file = open("test.dat", 'r')
flines = sum(1 for line in file)

obs = np.empty([flines, 2])
file.seek(0)
count = 0
while count < flines:
    ln = file.readline()
    ln_list = ln.split()
    #print(ln_list)
    obs[count, 0] = ln_list[0]
    obs[count, 1] = ln_list[1]
    count += 1

file.close()
ft = period04(obs)

print(str(ft))
