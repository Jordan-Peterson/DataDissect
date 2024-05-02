import copy
import csv
import json
from data_object import *
from constraint import Constraint, Rule

def import_csv(filename, data, sens_high, sens_low):
    temp_dwell = Dwell()
    temp_ramp = Ramp()
    event_border = ()
    dwell_started = False
    ramp_started = False
    ramp_start_data = ()
    ramp_end_data = ()
    data_window = []
    slope_window = []
    i = 0
    prev_data = ()
    with open(filename, newline='') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in linereader:
            data_point = (float(row[0]),float(row[1]))
            data.append_value(data_point[0],data_point[1])
            if i == 0:
                initial_value = (data_point)
            elif i == 1:
                cur_slope = calc_slope(initial_value, data_point)
                slope_window = list_put(cur_slope, slope_window)
                data_window = list_put([initial_value,data_point], data_window)
            elif i >= 2:

                cur_slope = calc_slope(prev_data, data_point)
                
                slope_window = list_put(cur_slope, slope_window)
                data_window = list_put([prev_data, data_point], data_window)

                if i > 5:
                    ## check Dwell Start/Ramp Stop
                    if check_window(sens_high, sens_low, slope_window, data_window, "dwell"):
                        ## Start Dwell
                        if not dwell_started:
                            event_border, data_window = list_get(data_window)
                            _, slope_window = list_get(slope_window)
                            temp_dwell.set_start(event_border[0][0])
                            temp_dwell.id = i
                            dwell_started = True
                        
                        temp_dwell.point_count = temp_dwell.point_count + 1
                        temp_dwell.set_average_temp((temp_dwell.average_temp + data_point[1])/2)
                        if abs(data_point[1]) > abs(temp_dwell.peak_temp):
                            temp_dwell.peak_temp = data_point[1]

                        ## End Ramp
                        if ramp_started:
                            event_border, data_window = list_get(data_window)
                            _, slope_window = list_get(slope_window)
                            temp_ramp.set_end(event_border[0][0])
                            ramp_end_data = event_border[0]
                            temp_ramp.average_ramp = calc_slope(ramp_start_data, ramp_end_data)
                            data.ramp_cycle.append(copy.deepcopy(temp_ramp))
                            ramp_started = False
                            temp_ramp.start = 0
                            temp_ramp.end = 0
                            temp_ramp.average_ramp = 0
                            temp_ramp.peak_ramp = 0
                            temp_ramp.point_count = 0


                    ## check Dwell Stop/Ramp Start
                    if check_window(sens_high, sens_low, slope_window, data_window, "ramp"):
                        ## End Dwell
                        if dwell_started:
                            event_border, data_window = list_get(data_window)
                            _, slope_window = list_get(slope_window)
                            temp_dwell.set_end(event_border[0][0])
                            data.dwell_cycle.append(copy.deepcopy(temp_dwell))
                            dwell_started = False
                            temp_dwell.start = 0
                            temp_dwell.end = 0
                            temp_dwell.average_temp = 0
                            temp_dwell.peak_temp = 0
                            temp_dwell.point_count = 0

                        ## Start Ramp
                        if not ramp_started:
                            event_border, data_window = list_get(data_window)
                            _, slope_window = list_get(slope_window)
                            temp_ramp.set_start(event_border[0][0])
                            temp_ramp.id = i
                            ramp_start_data = event_border[0]
                            ramp_started = True
                        
                        temp_ramp.point_count = temp_ramp.point_count + 1
                        if abs(cur_slope) > abs(temp_ramp.peak_ramp):
                            temp_ramp.peak_ramp = cur_slope
            prev_data = data_point
            i = i + 1
        if ramp_started:
            if ramp_started:
                event_border, data_window = list_get(data_window)
                _, slope_window = list_get(slope_window)
                temp_ramp.set_end(event_border[0][0])
                data.ramp_cycle.append(copy.deepcopy(temp_ramp))
                ramp_started = False
                temp_ramp.start = 0
                temp_ramp.end = 0
                temp_ramp.average_ramp = 0
                temp_ramp.peak_ramp = 0
                temp_ramp.point_count = 0

def export_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Step #", "Step Type", "Start Time", "End Time", "Duration", "Average:Dwell Temp/Ramp Rate","Peak:Dwell Temp/Ramp Rate"])
        i = 0
        for item in data:
            i = i + 1
            spamwriter.writerow([str(i), item.type, str(item.start), str(item.end), str(item.duration), str(item.average), str(item.peak)])
            

def import_constraints(filename, constraints):
    with open(filename) as jsonfile:
        data = json.load(jsonfile)
        for rule in data["constraints"]:
            constraints.add_rule(Rule(rule["high"], rule["low"]))


def check_window(sens_high, sens_low, slope_window, data_window, type):
    for slope in slope_window:
        if type == "dwell":
            if (slope >= sens_high or slope <= sens_low):
                return False
        if type == "ramp":
            if slope <= sens_high and slope >= sens_low:
                return False
    for temp in data_window:
        if type == "dwell":
            if (temp[0][0] <= 50 and temp[0][0] >= -50):
                return False
    return True

def calc_slope(tuple1, tuple2):
    return (tuple1[1]-tuple2[1])/(tuple1[0]-tuple2[0])


def list_put(value, list):
    if list_full(list):
        tmp_list = []
        for i in range(4):
            tmp_list.append(list[i+1])
        list = tmp_list
    list.append(value)
    return list

def list_get(list):
    temp_value = list[0]
    tmp_list = []
    for i in range(len(list)-1):
            tmp_list.append(list[i+1])
    return temp_value, tmp_list

def list_full(check):
    if len(check) == 5:
        return True
    return False