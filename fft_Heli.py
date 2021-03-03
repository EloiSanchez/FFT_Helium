def get_string(jk, j):
    """
    Generate filenames to read
    """
    str1 = "den.{}.0.".format(jk)
    num = "0"*(7-len(str(j))) + str(j)
    return str1 + num + ".dat"

def fft_he(prefix, times, delta_t, pdenpar):
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.fft import rfft, rfftfreq

    freqs_z, freqs_x, freqs_grids = [], [], []
    for interval in times:
        t_0, t_f = interval
        i_t0 = int(t_0 / (delta_t * pdenpar))
        if i_t0 == 0:
            i_t0 = 1
        i_tf = int(t_f / (delta_t * pdenpar)) + 1
        files_X = [get_string("XY",s) for s in range(i_t0, i_tf)]
        files_Z = [get_string("XZ",s) for s in range(i_t0, i_tf)]

        grid_x = []  # Construim nomes una grid perque grid_x = grid_y = grid_z
        with open(prefix + get_string("XY", 1), "r") as fil:
            lines = fil.readlines()
        
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

        # Ens quedem amb el pic de densitat maxima de la seccio negativa dels eixos
        max_x = []
        max_z = []
        N_grid = len(grid_x)
        max_index = np.argmax(all_z[0,:N_grid // 2 + 1])
        print(max_index)
        for i in range(len(all_x[:,0])):
            max_x.append(all_x[i,max_index])
            max_z.append(all_z[i,max_index])

        max_x = np.array(max_x)
        max_z = np.array(max_z)

        max_x = max_x - np.mean(max_x)
        max_z = max_z - np.mean(max_z)

        N_t_grid = len(max_x)
        t_grid = np.array(range(i_t0, i_tf)) * delta_t * pdenpar
        dt_grid = t_grid[1] - t_grid[0]
        
        freqs_z.append(rfft(max_z))
        freqs_x.append(rfft(max_x))
        freqs_grids.append(rfftfreq(N_t_grid, dt_grid))

        print("N_t_grid = {}, N_freqs_grid = {}".format(N_t_grid, len(rfftfreq(N_t_grid, dt_grid))))
        
        plt.plot(t_grid, max_z, label="z {}".format(interval))
        plt.plot(t_grid, max_x, label="x & y {}".format(interval))

    plt.legend(fontsize=8)
    plt.show()
    return freqs_z, freqs_x, freqs_grids
