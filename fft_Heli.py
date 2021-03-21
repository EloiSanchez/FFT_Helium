def fft_he(prefix, times, t_grid, delta_t, pdenpar, pener, is_den):
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
    from get_den import get_den

    logging.info("\n=== Starting Helium FFTs ===\n")

    fig = plt.figure()
    ax = fig.add_subplot()
    freqs_z, freqs_x, freqs_grids = [], [], []
    all_max_x, all_max_z, t_dens = get_den(prefix, t_grid, delta_t, pdenpar, pener, is_den)
    for interval in times:
        t_0, t_f = interval

        indices = [np.argmin(abs(t_dens - t_0)), np.argmin(abs(t_dens - t_f) + 1)]

        t = t_dens[indices[0]:indices[1]]
        max_x = all_max_x[indices[0]:indices[1]]
        max_z = all_max_z[indices[0]:indices[1]]

        ax.plot(t, max_z, label="z {}".format(interval))
        ax.plot(t, max_x, label="x & y {}".format(interval))

        # Remove the means in order to clean up the FFT result
        max_x = max_x - np.mean(max_x)
        max_z = max_z - np.mean(max_z)

        freqs_z.append(rfft(max_z))
        freqs_x.append(rfft(max_x))
        freqs_grids.append(rfftfreq(len(t), t[1] - t[0]))

        logging.info("For ({}, {}) ps, N = {}.\n".format(t_0, t_f, len(t)))

    ax.legend(fontsize=8)
    ax.set_title("First solvation layer maximum evolution")
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel("Helium density (Bohr$^{-3}$)")
    plt.show()
    return freqs_z, freqs_x, freqs_grids, fig, [t_dens, all_max_x, all_max_z]

