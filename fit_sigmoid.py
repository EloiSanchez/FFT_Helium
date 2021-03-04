def sigmoid(x, a, b):
    import numpy as np
    return 1 - 1 / (1 + np.exp(-a * (x - b)))

def fit_sigmoid(x, y):
    import numpy as np
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt

    popt, pcov = curve_fit(sigmoid, x, y, p0=(1, 0.5 * (x[-1] + x[0])), bounds=(0.1, [100, 1000]))

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(x, y, label="data")
    ax.plot(x, sigmoid(x, *popt), label="fit")

    ax.legend()
    plt.show()
    return sigmoid(x, *popt)