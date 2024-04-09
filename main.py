from data_import import *
from data_object import *
from constraint import *
from plotting import *
import sys


def main():
    args = sys.argv
    if(len(args) != 4):
        print("Usage: python3 main.py <csv file> <x-label> <y-label>")
        return

    data = DataObject()
    constraints = []
    import_csv(sys.argv[1], data)
    plot_data(data, sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()