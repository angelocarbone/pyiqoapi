"""Module for IQ Option API."""

import time
import json
import requests
import threading

# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from pyiqoapi.websocketclient import WebsocketClient
from pyiqoapi.objects.candles import Candles
from .exceptions import LoginError
from .objects.profile import Profile
from .objects.result import Result
from .objects.timesync import TimeSync

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class PyiqoAPI(object):
    """Class for communication with IQ Option API."""

    _timesync = TimeSync()
    _profile = Profile()
    _candles = Candles()

    def __init__(self, hostname, username, password, proxies=None):
        """
        :param str hostname: The hostname or ip address of a IQ Option server.
        :param str username: The username of a IQ Option server.
        :param str password: The password of a IQ Option server.
        :param dict proxies: (optional) The http request proxies.
        """
        self.https_url = "https://{host}/api".format(host=hostname)
        self.wss_url = "wss://{host}/echo/websocket".format(host=hostname)
        self._websocket_client = None
        self._session = requests.Session()
        self._session.verify = True
        self._session.trust_env = False
        self._username = username
        self._password = password
        self._proxies = proxies

        self._ticket_counter = 0
        self._request_in_pending = []
        self._request_in_progress = {}
        self._request_complete = {}
        self._request_dictionary = {}

    # *******************************
    #   PROPERTIES
    # *******************************

    @property
    def websocket(self):
        """Property to get websocket.

        :returns: The instance of :class:`WebSocket <websocket.WebSocket>`.
        """
        return self._websocket_client.wss

    # *******************************
    #   HTTP CHANEL METHODS
    # *******************************

    def get_actives(self):
        resource = 'actives'

        return self._get(resource)

    def get_appinit(self):
        resource = 'appinit'

        return self._get(resource)

    def change_balance(self, data=None, headers=None):
        resource = "/".join(('profile', 'changebalance'))

        return self._post(resource, data, headers)

    def get_profile(self):
        resource = 'getprofile'

        return self._get(resource)

    def get_register_data(self):
        resource = '/'.join(('register', 'getregdata'))

        return self._get(resource)

    def get_token(self):
        resource = "/".join(('auth', 'token'))

        return self._get(resource)

    def _login(self, username, password):
        """Login in IQOption server"""
        resource = 'login'
        data = {'email': username, 'password': password}

        response = self._post(resource, data)

        if response.status_code != 200:
            raise LoginError()

        return response

    # *******************************
    #   WEBSOCKET CHANEL METHODS
    # *******************************

    def buy(self, price, active, option, direction, exp_timeout=60):
        """Method to send message to buy option using websocket chanel."""
        name = 'buyV2'
        server_timestamp = self._timesync.server_timestamp
        expiration_timestamp = self._timesync.expiration_timestamp + exp_timeout
        data = {'price': price,
                'act': active,
                'type': option,
                'direction': direction,
                'time': server_timestamp,
                'exp': expiration_timestamp}
        self._send_websocket_request(name, data)

    def buyback(self):
        """Method to send message to buyback using websocket chanel."""
        name = 'buyback'
        data = {}

        self._send_websocket_request(name, data)

    def get_candles(self, active_id, duration, chunk_size=25):
        """Method to send message to get candles using websocket chanel."""
        name = 'candles'
        data = {'active_id': active_id,
                '_duration': duration,
                'chunk_size': chunk_size,
                'from': self._timesync.server_timestamp - (duration * 2),
                'till': self._timesync.server_timestamp}

        self._send_websocket_request(name, data)

    def set_actives(self, actives):
        """Method to send message to set actives using websocket chanel."""
        name = 'setActives'
        data = {'actives': actives}

        self._send_websocket_request(name, data)

    def set_ssid(self, ssid):
        """Method to send message to set ssid using websocket chanel."""
        name = 'ssid'

        self._send_websocket_request(name, ssid)

    def subscribe(self, chanel_name):
        """Method used to subscribe to chanel using websocket."""
        name = 'subscribe'

        self._send_websocket_request(name, chanel_name)

    def unsubscribe(self, chanel_name):
        """Method used to unsubscribe from chanel using websocket."""
        name = 'unsubscribe'

        self._send_websocket_request(name, chanel_name)

    def disconnect(self):
        self._websocket_client.close()

    def open_position(self, active_id, price, option, direction, exp_timeout=60):
        ticket_num = self._append_to_request_in_pending()

        self.buy(price, active_id, option, direction, exp_timeout)

        return ticket_num

    def close_position(self, position_id):
        pass

    def connect(self):
        """Method for connection to IQ Option API."""
        response = self._login(self._username, self._password)
        ssid = response.cookies["ssid"]
        self._set_session_cookies()
        self._websocket_client = WebsocketClient(self.wss_url, self._on_message_callback)

        websocket_thread = threading.Thread(target=self.websocket.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

        time.sleep(5)

        self.set_ssid(ssid)

    def get_result(self, ticket_number):
        try:
            return self._request_complete.pop(ticket_number)
        except KeyError:
            return None

    # *******************************
    #   PRIVATE METHODS
    # *******************************
    def _get(self, resource):
        return self._send_http_request(resource, 'GET')

    def _post(self, resource, data=None, headers=None):
        return self._send_http_request(resource, 'POST', data=data, headers=headers)

    def _send_http_request(self, resource, method, data=None, params=None, headers=None):
        """
        Send http request to IQ Option server.

        :param resource: ...
        :param str method: The http request method.
        :param dict data: (optional) The http request data.
        :param dict params: (optional) The http request params.
        :param dict headers: (optional) The http request headers.

        :returns: The instance of :class:`Response <requests.Response>`.
        """

        url = '/'.join((self.https_url, resource))

        response = self._session.request(
            url=url,
            method=method,
            data=data,
            params=params,
            headers=headers,
            proxies=self._proxies)
        response.raise_for_status()

        return response

    def _send_websocket_request(self, name, msg):
        """
        Send websocket request to IQ Option server.

        :param str name: The websocket request name.
        :param dict msg: The websocket request msg.
        """
        data = json.dumps(dict(name=name, msg=msg))
        self.websocket.send(data)

    def _set_session_cookies(self):
        """Method to set session cookies."""
        cookies = dict(platform="9")
        requests.utils.add_dict_to_cookiejar(self._session.cookies, cookies)
        self.get_profile()

    # *******************************
    #   CALLBACK METHODS
    # *******************************

    def _on_message_callback(self, msg):
        message = json.loads(str(msg))

        if message["name"] == "timeSync":
            self._timesync.server_timestamp = message["msg"]

        if message["name"] == "profile":
            self._profile.balance = message["msg"]["balance"]

        if message["name"] == "candles":
            self._candles.candles_data = message["msg"]["data"]

        if message["name"] == "buyComplete":
            self._append_to_request_in_progress(message)

        if message["name"] == "listInfoData":
            self._append_to_request_done(message)

    # **************************************
    #   REQUEST MESSAGE MANAGEMENT METHODS
    # **************************************

    def _append_to_request_in_pending(self):
        self._ticket_counter += 1
        ticket_num = self._ticket_counter
        self._request_in_pending.append(ticket_num)

        print('Position with ticket_num {} in pending'.format(ticket_num))

        return ticket_num

    def _append_to_request_in_progress(self, message):

        ticket_num = self._request_in_pending.pop(0)
        result_obj = Result()
        result_obj.set_message(message)
        result_id = result_obj.id

        self._request_dictionary[result_id] = ticket_num
        self._request_in_progress[result_id] = result_obj

        print('Position with ticket_num {} and result_id {} in progress'.format(ticket_num, result_id))

    def _append_to_request_done(self, message):
        result_obj = Result()
        result_obj.set_message(message)
        result_id = result_obj.id
        ticket_num = self._request_dictionary.get(result_id)
        self._request_in_progress.get(result_id)
        self._request_complete[ticket_num] = result_obj

        print('Position with ticket_num {} and result_id {} in done'.format(ticket_num, result_id))
