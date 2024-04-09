import csv
from data_object import DataObject

def import_csv(filename, data):
    with open(filename, newline='') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in linereader:
            data.append_value(float(row[0]),float(row[1]))

def import_constraints(filename):
    #TODO
    pass
