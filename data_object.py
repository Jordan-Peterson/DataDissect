
from tabulate import tabulate

class DataObject:
    def __init__(self):
        self.data = []
        self.short_data = []
        ## collection of dwells
        self.dwell_cycle = []
        self.ramp_cycle = []

    def append_value(self,x,y):
        self.data.append((x,y))

    def export_x_data(self):
        x_data = []
        for coord in self.data:
            x_data.append(coord[0])
        return x_data
    
    def export_y_data(self):
        y_data = []
        for coord in self.data:
            y_data.append(coord[1])
        return y_data
    
    def append_dwell(self,dwell):
        self.cycle.append(dwell)

    def table(self):
        head = ["Step #", "Step Type", "Start Time", "End Time", "Duration", "Average:\nDwell Temp\nRamp Rate","Peak:\nDwell Temp\nRamp Rate"]
        body = []
        table_item_list = []

        for i in self.dwell_cycle:
            tmp_table_item = TableItem()
            tmp_table_item.injest_dwell(i)
            table_item_list.append(tmp_table_item)
        for i in self.ramp_cycle:
            tmp_table_item = TableItem()
            tmp_table_item.injest_ramp(i)
            table_item_list.append(tmp_table_item)

        table_item_list.sort(key=sortId)
        self.short_data = table_item_list
        i = 0
        for item in table_item_list:
            i = i + 1
            body.append([str(i), item.type, str(item.start), str(item.end), str(item.duration), str(item.average), str(item.peak)])
        print(tabulate(body, head, tablefmt="grid"))

class Dwell:
    def __init__(self):
        self.start = 0.0
        self.end = 0.0
        self.average_temp = 0.0
        self.peak_temp = 0.0
        self.point_count = 0
        self.id = 0

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set_average_temp(self, temp):
        self.average_temp = temp

    def set_peak_temp(self, temp):
        self.peak_temp = temp

class Ramp:
    def __init__(self):
        self.start = 0.0
        self.stop = 0.0
        self.average_ramp = 0.0
        self.peak_ramp = 0.0
        self.point_count = 0
        self.id = 0

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set_average_ramp(self, ramp):
        self.average_ramp = ramp

    def set_peak_ramp(self, ramp):
        self.peak_ramp = ramp
    

class TableItem:
    def __init__(self):
        self.id = 0
        self.type = ""
        self.start = 0
        self.end = 0
        self.duration = 0
        self.average = 0
        self.peak = 0
    
    def injest_dwell(self, dwell):
        self.id = dwell.id
        self.type = "Dwell"
        self.start = dwell.start
        self.end = dwell.end
        self.duration = dwell.end - dwell.start
        self.average = dwell.average_temp
        self.peak = dwell.peak_temp

    def injest_ramp(self, ramp):
        self.id = ramp.id
        self.type = "Ramp"
        self.start = ramp.start
        self.end = ramp.end
        self.duration = ramp.end - ramp.start
        self.average = ramp.average_ramp
        self.peak = ramp.peak_ramp

def sortId(item):
    return item.id