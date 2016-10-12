from Observation import Observation


class Transient:
    # variables
    __location = 0
    __observations = []
    __classification = None

    def __init__(self, loc):
        self.__location = loc

    def get_loc(self):
        return self.__location

    def add_observation(self, time, loc, mag):
        obs = Observation(time, loc, mag)
        self.__observations.append(obs)

