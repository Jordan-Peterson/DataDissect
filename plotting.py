import matplotlib.pyplot as plt



def plot_data(data,xlabel,ylabel):
    plt.plot(data.export_x_data(), data.export_y_data())
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    

