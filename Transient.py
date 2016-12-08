class Transient:
    # create a transient using the ra and dec
    def __init__(self, r, d):
        self.__ra = r
        self.__dec = d
        # create observations dictionary, period, frequency, and max/min magnitude variables
        self.__observations = []
        self.lastClassifier = None
        self.period = None
        self.freq = None
        # create classification variable
        self.classification = None

    def set_period(self, p):
        self.period = p

    def set_frequency(self, f):
        self.freq = f

    def get_numobs(self):
        return len(self.__observations)

    def get_ra(self):
        return self.__ra

    def get_dec(self):
        return self.__dec

    def get_classification(self):
        return self.classification

    def add_observation(self, observation):
        self.__observations.append(observation)

    def get_observation(self):
        return self.__observations
