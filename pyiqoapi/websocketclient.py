"""Module for PyiqoAPI websocket."""

import logging
import websocket


class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, wss_url, on_message_callback=None):
        """
        :param wss_url: Url of websocket
        :param on_message_callback: callback used when on_message method occur
        """
        self._on_message_callback = on_message_callback
        self.wss = websocket.WebSocketApp(wss_url,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close,
                                          on_open=self.on_open)

    def on_message(self, wss, message):
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)
        logger.debug(message)

        if self._on_message_callback:
            self._on_message_callback(message)

    @staticmethod
    def on_error(wss, error):
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)

    @staticmethod
    def on_open(wss):
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")

    @staticmethod
    def on_close(wss):
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")

    def close(self, **kwargs):
        self.wss.close(**kwargs)
