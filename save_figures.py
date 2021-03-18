
def actual_save(fig, name):
    import matplotlib.pyplot as plt
    fig.savefig(name, format="png", transparent=True, dpi=600)
    print("Saved {}.".format(name))

def save_figures(inici, pobl, fit, he, final):
    import matplotlib.pyplot as plt
    import os

    directory=input("Enter the name of the directory with the figures >> ")
    if not directory.endswith("/"):
        directory += "/"
    directory = "Results/" + directory
    
    os.system('mkdir -p Results')
    os.system('mkdir -p {}'.format(directory))

    actual_save(inici, directory + "all_population.png")
    actual_save(pobl, directory + "population_for_fft.png")
    actual_save(fit, directory + "fit.png")
    actual_save(he, directory + "helium_dens_for_fft.png")
    actual_save(final, directory + "final_result.png")

