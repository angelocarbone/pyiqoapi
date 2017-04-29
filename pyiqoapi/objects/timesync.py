"""Module for IQ Option TimeSync websocket object."""

import time
import datetime

from .base import Base


class TimeSync(Base):
    """Class for IQ Option TimeSync websocket object."""

    def __init__(self):
        super(TimeSync, self).__init__()
        self.__name = "timeSync"
        self.__server_timestamp = None
        self.__expiration_time = 1

    @property
    def server_timestamp(self):
        """Property to get server timestamp."""
        return self.__server_timestamp / 1000

    @server_timestamp.setter
    def server_timestamp(self, timestamp):
        """Method to set server timestamp."""
        self.__server_timestamp = timestamp

    @property
    def server_datetime(self):
        """Property to get server datetime."""
        return datetime.datetime.fromtimestamp(self.server_timestamp)

    @property
    def expiration_time(self):
        """Property to get expiration time."""
        return self.__expiration_time

    @expiration_time.setter
    def expiration_time(self, minutes):
        """Method to set expiration time"""
        self.__expiration_time = minutes

    @property
    def expiration_datetime(self):
        """Property to get expiration datetime."""
        return self.server_datetime + datetime.timedelta(minutes=self.expiration_time)

    @property
    def expiration_timestamp(self):
        """Property to get expiration timestamp."""
        return time.mktime(self.expiration_datetime.replace(second=0, microsecond=0).timetuple())
