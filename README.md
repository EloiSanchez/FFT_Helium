# FFT_pob
Small program to perform FFTs to population.dat files

## File structure
### Population files

| time  |  lvl0 |  lvl1 |  ...  |
|:-----:|:-----:|:-----:|:-----:|
|  t_0  | p_1_0 | p_2_0 |  ...  |
|  t_1  | p_1_1 | p_2_1 |  ...  |
|  ...  |  ...  |  ...  |  ...  |

Without headers, only the numeric values, see _population.dat_.

### Levels files

```
3	,	j=1
13	,	j=3
31	,	j=5
...
```

Of the form (see _levels.csv_):

## Usage
Execute with (python v3 with scipy and matplolib):

```bash
python fft_poblacio.py /path/poupulation_input_file /path/levels_file
```

It will show a plot of the populations determined in the first column of the _levels_ file and their respective labels from the second column of _levels_ (coma separated) (Example in results _Ex_pre_pob.png_. Then it will ask for `t_0` and `t_f`, and the `output_name`, which will be saved in the folder `Results/`. Example is _HCl_1_3_5.png_.
