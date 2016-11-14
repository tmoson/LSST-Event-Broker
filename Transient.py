from Observation import Observation
from Classifier import Classifier
from Functiongenerator import get_function_1
from Functiongenerator import get_function_2


class Transient:
    # variables

    def __init__(self, loc, cls):
        self.__location = loc
        self.__classification = cls
        self.__observations = []
        self.t1 = []
        self.t2 = []
        self.cls = Classifier()
        for i in range(0, 100):
            self.t1.append(get_function_1())
            self.t2.append(get_function_2(i))
        self.__s1 = [self.cls.mean(self.t1), self.cls.stdev(self.t2)]
        self.__s2 = [self.cls.mean(self.t2), self.cls.stdev(self.t2)]
        self.__classes = {'Supernova':self.__s1, 'Nova':self.__s2}

    def get_loc(self):
        return self.__location

    # def get_cat(self):
    #    return self.__category

    def load_observation(self, observation):
        self.__observations.insert(observation.get_loc(), observation)

    def add_observation(self, observation):
        self.__observations.insert(observation.get_loc(), observation)
        # add observation to txt
        file_o_name = "trans_db/" + str(observation.get_loc()) + ".txt"
        file_o = open(file_o_name, 'a+')
        file_o.write(
            "{0}-{1}-{2}\n".format(str(observation.get_time()),
                                   str(observation.get_loc()),
                                   str(observation.get_mag())))
        file_o.close()
        #  self.update_probability()

    def get_observation(self):
        return self.__observations

    def update_probability(self):
        self.__classification = self.cls.predict(self.cls.summarize(self.__observations), self.__classes)

    def get_classification(self):
        return self.__classification

