
def fft_pob(prefix, times, pobl_t, t_grid, index):
    import numpy as np
    from scipy.fft import rfft, rfftfreq

    print("\n=== Starting population FFTs ===\n")

    freqs, freqs_grids = [], []
    for interval in times:
        t_0, t_f = interval

        # Save the arrays in the interval of interest
        t_lim_0 = t_grid.index(t_0)
        t_lim_f = t_grid.index(t_f) + 1
        t_util = t_grid[t_lim_0:t_lim_f]
        N_samples = len(t_util)
        dt = t_util[1] - t_util[0]
        pobl_util = pobl_t[t_lim_0:t_lim_f,:]

        # Substract means from populations
        pobl_util = pobl_util - np.mean(pobl_util, axis=0)

        print("For ({}, {}) ps, N = {}.\n".format(t_0, t_f, N_samples))

        # Perform FFT and save in freqs
        freqs_grids.append(rfftfreq(N_samples, dt)[:N_samples//2 + 1])
        freqs.append(rfft(pobl_util[:,index]))
        
    return freqs, freqs_grids
