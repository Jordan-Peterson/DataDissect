
class Constraint:
    def __init__(self):
        self.rules = []

    def add_rule(self,rule):
        self.rules.append(rule)
    
    def check_high_bound(value):
        pass

class Rule:
    def __init__(self, high, low):
        self.high = high
        self.low = low

    def evaluate(self, value):
        if self.high >= value and value >= self.low:
            return True
        return False

    