# import


class Observation:
    # variables

    def __init__(self, time, loc, mag):
        self.__time_obs = time
        self.__location = loc
        self.__magnitude = mag

    def set_time(self, time):
        self.__time_obs = time

    def get_time(self):
        return self.__time_obs

    def set_loc(self, loc):
        self.__location = loc

    def get_loc(self):
        return self.__location

    def set_mag(self, mag):
        self.__magnitude = mag

    def get_mag(self):
        return self.__magnitude

