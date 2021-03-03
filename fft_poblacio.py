
def fft_pob(prefix, times, pobl_t, t_grid, index):
    import numpy as np
    from scipy.fft import rfft, rfftfreq

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

        # Perform FFT and save in freqs
        freqs_grids.append(rfftfreq(N_samples, dt)[:N_samples//2 + 1])
        freqs.append(rfft(pobl_util[:,index]))
        # freqs = []
        # for i in range(len(indices)):
        #     freqs.append(rfft(pobl_util[:,i]))
        
    return freqs, freqs_grids

        # # Plot results
        # fig = plt.figure(figsize=(6.4*1.3, 4.8*1.5))
        # ax1 = fig.add_subplot(211)
        # ax2 = fig.add_subplot(212)
        # axs = [ax1, ax2]

        # [ax.grid(True) for ax in axs]

        # for i in range(len(indices)):
        #     ax1.plot(t_util, pobl_util[:, i], label=labels[i])
        #     ax2.plot(freqs_grid, abs(freqs[i]), label=labels[i])

        # [ax.legend(fontsize=10) for ax in axs]
        # ax1.set_title("Population evolution mean subtracted")
        # ax2.set_title("FFT of population evolution")

        # out_file = input("Introduce the output filename (without .png) >> ")
        # ax1.set_ylabel(r"$|⟨j,m_j|φ(t)⟩|^{2}$")
        # ax1.set_xlabel("Time (ps)")
        # ax2.set_ylabel("?????")
        # ax2.set_xlabel(r"Frequencies (ps$^{-1}$)")

        # ax1.set_xlim(t_util[0], t_util[-1])
        # ax2.set_xlim(0, freqs_grid[-1])
        # ax2.set_ylim(0)

        # plt.tight_layout()
        # plt.savefig("Results/" + out_file + ".png", format="png", dpi=600, transparent=True)
        # # plt.show()

