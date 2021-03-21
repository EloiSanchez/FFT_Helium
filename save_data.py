
def save_data(
    directory, int_pob_all, grid_pob_all, int_he_all, grid_he_all,
    pob_fitted, pob_time, prefix, max_he
    ):
    import os
    import numpy as np
    import logging

    os.system('mkdir -p {}/Data'.format(directory))
    os.system('mv FFT_out.tmp {}'.format(directory + "Data/FFT_out.log"))
    data_dir = directory + "/Data/"

    logging.info('Saved logfile')

    for i in range(len(int_pob_all)):
        int_pob = int_pob_all[i]
        grid_pob = grid_pob_all[i]
        with open(data_dir + "FFT_pob_{}.dat".format(i+1), "w") as f:
            f.write('# FFT for the population time interval {}\n'.format(i+1))
            for j in range(len(int_pob)):
                f.write("{} {}\n".format(grid_pob[j], np.abs(int_pob[j])))
    logging.info('Saved FFT_pob.dat')
    
    for i in range(len(int_he_all)):
        int_he = int_he_all[i]
        grid_he = grid_he_all[i]
        with open(data_dir + "FFT_he_{}.dat".format(i+1), "w") as f:
            f.write('# FFT for the first solvation layer of the helium density time interval {}\n'.format(i+1))
            for j in range(len(int_he)):
                f.write("{} {}\n".format(grid_he[j], np.abs(int_he[j])))
    logging.info('Saved FFT_he.dat')
    
    os.system('cp {}/poblacions.dat {}'.format(prefix, data_dir))
    logging.info('Saved poblacions.dat')

    with open(data_dir + "fit_population.dat", "w") as f:
        f.write("# Only the column of the population with the fitted substracted\n")
        for i in range(len(pob_time)):
            f.write('{} {}\n'.format(pob_time[i], pob_fitted[i,0]))
    logging.info('Saved fit_population.dat')

    os.system('mv He_solv_layer.tmp {}/he_solv_layer.dat'.format(data_dir))
    logging.info('Saved he_solv_layer.dat')

