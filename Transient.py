from Observation import Observation


class Transient:
    # variables
    __location = 0
    __observations = []
    __category = None

    def __init__(self, loc, cat):
        self.__location = loc
        self.__category = cat

    def get_loc(self):
        return self.__location

    def get_cat(self):
        return self.__category

    def add_observation(self, time, loc, mag):
        obs = Observation(time, loc, mag)
        self.__observations.append(obs)

