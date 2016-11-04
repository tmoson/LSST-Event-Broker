from Observation import Observation
from Classifier import Classifier
from Functiongenerator import get_function_1
from Functiongenerator import get_function_2

class Transient:
    # variables

    def __init__(self, loc, cat):
        self.__location = loc
        self.__category = cat
        self.__observations = []
        self.__t1 = {}
        self.__t2 = {}
        self.cls = Classifier
        for i in range (0, 100):
            self.__t1[i] = get_function_1()
            self.__t2[i] = get_function_2(i)
        self.__classes = { 'Supernova':self.cls.summarize(self.__t1), 'Nova':self.cls.summarize(self.__t2)}

    def get_loc(self):
        return self.__location

    def get_cat(self):
        return self.__category

    def add_observation(self, observation):
        self.__observations.append(observation)
        self.update_probability()


    def get_observation(self):
        return self.__observations

    def update_probability(self):
        self.classification =  self.cls.predict(self.cls.summarize(self.__observations), self.__classes)