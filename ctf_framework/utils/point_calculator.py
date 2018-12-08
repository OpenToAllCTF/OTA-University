import math

class DynamicPointCalculator():

    def __init__(self, min_val=50, max_val=500, decay=30):

        self.min_val = min_val
        self.max_val = max_val
        self.decay = decay

    def calculate(self, number_of_solves):

        value = (self.min_val - self.max_val) / (self.decay ** 2) \
                * (number_of_solves ** 2) \
                + self.max_val

        value = math.ceil(value)
        return max(int(value), int(self.min_val))
