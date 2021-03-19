def get_string(jk, j):
    """
    Generate filenames to read
    """
    str1 = "{}.0.".format(jk)
    num = "0"*(7-len(str(j))) + str(j)
    return str1 + num + ".dat"

def fft_he(prefix, times, delta_t, pdenpar, pener, is_den):
    """
    Input
    prefix (str): Path to the files.
    times (list of tuples): Time intervals to FFT in picosecs.
    delta_t (float): Time increment in picosecs.
    pdenpar (int): Print den.XZ.---.dat every pdenpar.
    pener (int): Print population and tall.x.---.dat every pener.
    is_den (bool): Controls whether which format to use

    Return: freqs_z, freqs_x, freqs_grids
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.fft import rfft, rfftfreq
    import logging

    logging.info("\n=== Starting Helium FFTs ===\n")

    fig = plt.figure()
    ax = fig.add_subplot()
    freqs_z, freqs_x, freqs_grids = [], [], []
    for interval in times:
        t_0, t_f = interval

        # Generate the indexes with the files generated
        if is_den:
            i_t0 = int(t_0 / (delta_t * pdenpar))
            i_tf = int(t_f / (delta_t * pdenpar)) + 1
        else:
            i_t0 = int(t_0 / (delta_t * pener))
            i_tf = int(t_f / (delta_t * pener)) + 1

        # The file with __.0.00000 is not printed
        if i_t0 == 0:
            i_t0 = 1

        # Generate the filenames to be read
        if is_den:
            files_X = [get_string("den.XY", s) for s in range(i_t0, i_tf)]
            files_Z = [get_string("den.XZ", s) for s in range(i_t0, i_tf)]
        else:
            files_Z = ["/" + get_string("tall.z", s) for s in range(i_t0, i_tf)]
            files_X = ["/" + get_string("tall.x", s) for s in range(i_t0, i_tf)]

        grid_x = []  # Construim nomes una grid perque grid_x = grid_y = grid_z

        with open(prefix + files_X[0], "r") as fil:
            lines = fil.readlines()
        
        # Bloc de lectura en cas que fem servir format den.__.dat
        if is_den:
            for line in lines:
                x, y, den = [float(s) for s in line.split()]
                if abs(y) < 0.001 and x not in grid_x:
                    grid_x.append(x)
                
            all_x = []
            for name in files_X:
                with open(prefix + name, "r") as fil:
                    lines = fil.readlines()

                den_x = []  # Ignorem y per que x i y son simetrics
                for line in lines:
                    x, y, den = [float(s) for s in line.split()]

                    # if abs(x) < 0.001:
                    #     # den_y.append(den)

                    if abs(y) < 0.001:
                        den_x.append(den)
                all_x.append(den_x)

            all_z = []
            for name in files_Z:
                with open(prefix + name, "r") as fil:
                    lines = fil.readlines()
                den_z = []
                for line in lines:
                    x, z, den = [float(s) for s in line.split()]

                    if abs(x) < 0.001:
                        den_z.append(den)
                all_z.append(den_z)
            all_x, all_z = np.array(all_x), np.array(all_z)

        # Bloc de lectura en cas que fem servir format tall.__.dat
        else:
            for line in lines:
                x, den = [float(s) for s in line.split()]
                grid_x.append(x)
            all_x = []
            for name in files_X:
                with open(prefix + name, "r") as fil:
                    lines = fil.readlines()

                den_x = []  # Ignorem y per que x i y son simetrics
                for line in lines:
                    x, den = [float(s) for s in line.split()]
                    # den_y.append(den)
                    den_x.append(den)
                all_x.append(den_x)

            all_z = []
            for name in files_Z:
                with open(prefix + name, "r") as fil:
                    lines = fil.readlines()
                den_z = []
                for line in lines:
                    z, den = [float(s) for s in line.split()]
                    den_z.append(den)
                all_z.append(den_z)
            all_x, all_z = np.array(all_x), np.array(all_z)

            
        # Ens quedem amb el pic de densitat maxima de la seccio negativa dels eixos
        max_x = []
        max_z = []
        N_grid = len(grid_x)
        max_index = np.argmax(all_z[0,:N_grid // 2 + 1])
        for i in range(len(all_x[:,0])):
            max_x.append(all_x[i,max_index])
            max_z.append(all_z[i,max_index])

        max_x = np.array(max_x)
        max_z = np.array(max_z)

        N_t_grid = len(max_x)
        if is_den:
            t_grid = np.array(range(i_t0, i_tf)) * delta_t * pdenpar
        else:
            t_grid = np.array(range(i_t0, i_tf)) * delta_t * pener
        dt_grid = t_grid[1] - t_grid[0]
        
        ax.plot(t_grid, max_z, label="z {}".format(interval))
        ax.plot(t_grid, max_x, label="x & y {}".format(interval))

        # Remove the means in order to clean up the FFT result
        max_x = max_x - np.mean(max_x)
        max_z = max_z - np.mean(max_z)

        freqs_z.append(rfft(max_z))
        freqs_x.append(rfft(max_x))
        freqs_grids.append(rfftfreq(N_t_grid, dt_grid))

        logging.info("For ({}, {}) ps, N = {}.\n".format(t_0, t_f, N_t_grid))

    ax.legend(fontsize=8)
    ax.set_title("First solvation layer maximum evolution")
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel("Helium density (Bohr$^{-3}$)")
    plt.show()
    return freqs_z, freqs_x, freqs_grids, fig
