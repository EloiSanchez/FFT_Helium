# FFT_pob
Small program to perform FFTs to _poblacions.dat_ files

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

## Usage (see provisional)
Execute with (python v3 with scipy and matplolib):

```bash
python fft_poblacio.py /path/poupulation_input_file /path/levels_file
```

It will show a plot of the populations determined in the first column of the _levels_ file and their respective labels from the second column of _levels_ (coma separated) (Example in results _Ex_pre_pob.png_. Then it will ask for `t_0` and `t_f`, and the `output_name`, which will be saved in the folder `Results/`. Example is _DCl_1_3_5.png_.

## Provisional
### Usage provisional
Just type ```make``` in the terminal. It will show the plot of the populations. Then, introduce the time intervals for the FFT as ```t_01:t_2 t_11:t12 ...```. Not really functional at this stage due to not managing the fit interval.

### He FFT
The FFT of the peak of the first solvation layer of the He density (z axis) is now shown alongside the FFT of the populations.

Before performing the FFT there is a plot showing the variation of the first solvation layer peaks (x, y and z axis).

Biguest problem
- Since we print every 1000 iterations the He density, the resolution of the FFT and the frequency domain is not good enough.

### Fit of the population in the relaxation zone
A fit is performed in order to clean de results of the FFT. 

Problems:
- The declaration of the interval for the fit is done in the main and must be changed.
- Currently fitting to a sigmoid wich is not adequate to fit the evolution of the DCl population.

### Population FFT
Currently performs the FFT of the first level indicated in _levels_fft.csv_.

### General problems
- This program was initially intended to be a small script. However, adding more and more features makes both hard and time consuming to mantain properly. Is it worth? 
- The calling method must be changed to facilitate the new functionalities, including:
    - Provide the interval of the fit, if required (in the HCl case this is going to be easy, since the fit to a sigmoid will be very adequate).
    - Perform the fft of more than one level.
    - Somehow indicate which levels to considerate.
    - Somehow control which plots to show.
    - Manage I/O and for both numerical results and figures/animations.
___

## Author: Eloi Sanchez