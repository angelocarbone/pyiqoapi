"""Module for IQ Option Candles websocket object."""

from .base import Base


class Candle(object):
    """Class for IQ Option candle."""

    def __init__(self, candle_data):
        self.__candle_data = candle_data

    @property
    def candle_time(self):
        """Property to get candle time."""
        return self.__candle_data[0]

    @property
    def candle_open(self):
        """Property to get candle open value."""
        return self.__candle_data[1]

    @property
    def candle_close(self):
        """Property to get candle close value."""
        return self.__candle_data[2]

    @property
    def candle_high(self):
        """Property to get candle high value."""
        return self.__candle_data[3]

    @property
    def candle_low(self):
        """Property to get candle low value."""
        return self.__candle_data[4]

    @property
    def candle_type(self):
        """Property to get candle type value."""
        if self.candle_open < self.candle_close:
            return "green"
        elif self.candle_open > self.candle_close:
            return "red"


class Candles(Base):
    """Class for IQ Option Candles websocket object."""

    def __init__(self):
        super(Candles, self).__init__()
        self.__name = "candles"
        self.__candles_data = None

    @property
    def candles_data(self):
        """Property to get candles data."""
        return self.__candles_data

    @candles_data.setter
    def candles_data(self, candles_data):
        """Method to set candles data."""
        self.__candles_data = candles_data

    @property
    def first_candle(self):
        """Method to get first candle."""
        return Candle(self.candles_data[0])

    @property
    def second_candle(self):
        """Method to get second candle."""
        return Candle(self.candles_data[1])

    @property
    def current_candle(self):
        """Method to get current candle."""
        return Candle(self.candles_data[-1])
