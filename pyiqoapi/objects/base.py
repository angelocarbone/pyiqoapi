"""Module for IQ Option Base websocket object."""


class Base(object):
    """Class for IQ Option Base websocket object."""

    def __init__(self):
        self.__name = None

    @property
    def name(self):
        """Property to get websocket object name."""
        return self.__name
