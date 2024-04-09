

class DataObject:
    def __init__(self):
        self.data = []

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