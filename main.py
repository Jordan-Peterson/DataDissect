from data_import import *
from data_object import *
from constraint import *
from plotting import *
import configparser
import tkinter as tk
from tkinter.filedialog import askopenfilename



def main():
    tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

    filename = askopenfilename()
    print("user chose", filename)

    data = DataObject()
    constraints = Constraint()
    xlabel = ""
    ylabel = ""
    highT = ""
    lowT = ""
    config = configparser.ConfigParser()
    config.read('dd_config.ini')
    xlabel = config['xaxis']['xlabel']
    ylabel = config['yaxis']['ylabel']
    highT = config['high-tolerance']['highT']
    lowT = config['low-tolerance']['lowT']

    import_csv(filename, data, float(highT), float(lowT))
    import_constraints("example_rules.json", constraints)
    data.table()
    export_csv(filename + "-output.csv", data.short_data)
    plot_data(data, xlabel, ylabel)


if __name__ == "__main__":
    main()