from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import sys
from fft_poblacio import fft_pob
from fft_Heli import fft_he
from fit_sigmoid import fit_sigmoid

# Input check
if len(sys.argv) != 3:
    print('ERROR: You must call the program with "python fft_poblacio input_path levels_path"')
    quit()

fft_index = 0

# Get some variables from DFT4He3dt.namelist.read
prefix = sys.argv[1]
with open(prefix + "/DFT4He3dt.namelist.read", "r") as fil:
    lines = fil.readlines()

for line in lines:
    if line.strip().startswith("DELTAT"):
        delta_t = float(line.split("=")[1][:-2])
        print(delta_t)
    elif line.strip().startswith("PENER"):
        pener = int(line.split("=")[1][:-2])
    elif line.strip().startswith("PDENPAR"):
        pdenpar = int(line.split("=")[1][:-2])
# We obtained delta_t, pener and pdenpar to get the correct times fromt he density outputs

# Indices to analyse and respective labels
with open(sys.argv[2], "r") as fil:
    lines = fil.readlines()

# Parse indices and labels
indices = []
labels = []
for line in lines:
    i, lab = line.split(",")
    indices.append(int(i))
    labels.append(lab.strip())

# Read from file
with open(sys.argv[1] + "/poblacions.dat", "r") as fil:
    lines = fil.readlines()

# Parse information. Populations of interest saved in pobl_t
t_grid = []
pobl_t = []
for line in lines:
    aux = [float(s) for s in line.split()[0:-1]]
    t_grid.append(aux[0])
    pobl_t.append([aux[i] for i in indices])
pobl_t = np.array(pobl_t)

# Define some standards for all plots
plt.style.use("seaborn-colorblind")
rcParams['font.family'] = "Arial"
rcParams['font.size'] = 12

# Plot of populations chosen
fig1 = plt.figure()
ax = fig1.add_subplot()
for i in range(len(indices)):
    ax.plot(t_grid, pobl_t[:,i], label=labels[i])
ax.legend(fontsize=10)
ax.grid(True)
plt.show()

# Now we get the time intervals we want to plot
times = []
times_s = input("Introduce intervals t0:tf >> ").strip().split(" ")
for interval in times_s:
    t0, tf = interval.split(":")
    times.append((float(t0),float(tf)))
print(times)

# We fit the data to a sigmoid to improve the results of the FFT
inp = input("Do you want to fit the data to a sigmoid? (y/n) ")
if inp.capitalize().startswith("Y"):
    fit_interval = [float(s) for s in input("Introduce the interval for the fit as t0:tf >> ").split(":")]
    fit_interval = (int(fit_interval[0]//(pener*delta_t)) + 1, int(fit_interval[1]//(pener*delta_t)) + 2)
    fit = fit_sigmoid(t_grid[fit_interval[0]:fit_interval[1]], pobl_t[fit_interval[0]:fit_interval[1],0])
    pobl_t[fit_interval[0]:fit_interval[1],0] = pobl_t[fit_interval[0]:fit_interval[1],0] - fit
else:
    print("Skipping the fit")

# Now we get the results of the fft for populations and He density
intensities_pop, grids_pop = fft_pob(prefix, times, pobl_t, t_grid, fft_index)
intensities_he_z, intensitites_he_x, grids_he = fft_he(prefix, times, delta_t, pdenpar)

# From here we make the plots of the ffts
fig2 = plt.figure(figsize=(6.4*1.2,4.8*1.5))
ax1 = fig2.add_subplot(211)

ax1.set_title("FFT for population of j=1")

for i in range(len(times)):
    ax1.plot(grids_pop[i], abs(intensities_pop[i]), label=r"t$_0$={} ps, t$_f$={} ps".format(times[i][0], times[i][1]))

ax2 = fig2.add_subplot(212)
axs = [ax1, ax2]

ax2.set_title("FFT for first solvation layer of He")


for i in range(len(times)):
    ax2.plot(grids_he[i], abs(intensities_he_z[i]), label=r"t$_0$={} ps, t$_f$={} ps".format(times[i][0], times[i][1]))

for ax in axs:
    ax.legend(fontsize=8)
    ax.set_xlim((0, np.max(grids_he[0])))
    ax.set_ylabel("Intensity (A.U)")
    ax.set_xlabel(r"Frequency (ps$^{-1}$)")

plt.tight_layout()
plt.show()