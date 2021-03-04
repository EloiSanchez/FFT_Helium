def sigmoid(x, a, b):
    import numpy as np
    return 1 - 1 / (1 + np.exp(-a * (x - b)))

def fit_sigmoid(x, y):
    import numpy as np
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt

    popt, pcov = curve_fit(sigmoid, x, y, p0=(0.1, 0.5 * (x[-1] + x[0])), bounds=(0.0001, [100, 1000]))

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(x, y, label="data")
    ax.plot(x, sigmoid(x, *popt), label="fit")

    print("\nFitted to f(t) = 1 - (1 / (1 + exp(-a * (x - b))")
    print("a = {}, b = {}\n".format(popt[0], popt[1]))

    ax.legend()
    plt.show()
    return sigmoid(x, *popt)
