# FFT_pob
Small program to perform FFTs to populations and helium densities in the results directory of our calculations.

## Usage (see provisional)
Execute with (python v3 with scipy and matplolib):

```bash
python fft_all.py /path/results_directory /path/levels_file is_den
```

It will show a plot of the populations determined in the first column of the _levels_ file and their respective labels from the second column of _levels_ (coma separated).

The _results_directory_ is the directory where the _population.dat_ and the _den.XY.NNNN.dat_ or _tall.x.NNNN.dat_ files are stored. The variable ```is_den``` controls whether to use _den_ (True) or _tall_ (False) formats to read the Helium density.

After showing the plot with all the populations taken from _levels_file_ it will ask for the time intervals to use.

Then, it the user must decide if a fitting to a sigmoid is to be done for the population and the time interval to do so.

After that, all plots (fitting, population used and helium density used) will be shown so the user can see if everything is rigth. After that, the final plot with the FFT of the population and the Helium density are shown.

Finally, the user can save all the plots into a specified directory that will be created in _Results/_. 

## File structure
### Population files

| time  |  lvl0 |  lvl1 |  ...  |
|:-----:|:-----:|:-----:|:-----:|
|  t_0  | p_1_0 | p_2_0 |  ...  |
|  t_1  | p_1_1 | p_2_1 |  ...  |
|  ...  |  ...  |  ...  |  ...  |

Without headers, only the numeric values, see _poblacions.dat_.

### Levels files

```
3	,	j=1
13	,	j=3
31	,	j=5
...
```

See _levels.csv_.

## Provisional
### Fit of the population in the relaxation zone
A fit is performed in order to clean de results of the FFT. 

Problems:
- The declaration of the interval for the fit is done in the main and must be changed.
- Currently fitting to a sigmoid wich is not adequate to fit the evolution of the DCl population.

### Population FFT
Currently performs the FFT of the first level indicated in _levels_fft.csv_.

### General problems
- The calling method must be changed to facilitate the new functionalities, including:
    - Perform the fft of more than one level.
    - Manage I/O and for numerical and logging results.
___

## Author and Contact
Author: Eloi Sanchez Ambros

Contact: eloisanchez16@gmail.com or esancham21@alumnes.ub.edu

## Other Programs for the Group
- [Grid Construction](https://github.com/EloiSanchez/Grid_Construction): To generate helium nanodroplet grids of any size and density.
- [He Movies](https://github.com/EloiSanchez/He_Movies): To generate movies of the helium density from the dynamic simulations results.
