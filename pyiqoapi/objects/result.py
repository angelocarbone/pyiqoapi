
class Result:
    """ Docstring about 'Result' class. """
    UNKNOWN_CODE = 901

    def __init__(self):
        self.is_demo = None
        self.currency = None
        self.active = None
        self.active_id = None
        self.user_id = None
        self.refund = None
        self.type_name = None
        self.currency_char = None
        self.user_balance_id = None
        self.id = None
        self.direction = None
        self.profit = None
        self.profit_amount = None
        self.profit_income = None
        self.profit_return = None
        self.sum = None
        self.win = None
        self.win_amount = None
        self.loose_amount = None
        self.value = None
        self.exp_value = None
        self.now = None
        self.created = None
        self.expired = None
        self.game_state = None
        self.rate_finished = None
        self.data = None
        self.error_code = None
        self.error_message = None
        self.message_name = None
        self.type = None
        self.request_id = None

        self.is_list_info_data = False
        self.is_buy_complete = False
        self.is_successful = False

    def set_message(self, data):
        self.data = data
        self.message_name = data['name']

        if self.message_name == 'listInfoData':
            data = data["msg"][0]
            self.is_successful = True
            self.is_list_info_data = True
            self.is_buy_complete = False
            self.id = data['id']
            self.direction = data['dir']
            self.profit = data['profit']
            self.profit_amount = data['profit_amount']
            self.profit_income = data['profit_income']
            self.profit_return = data['profit_return']
            self.sum = data['sum']
            self.win = data['win']
            self.win_amount = data['win_amount']
            self.loose_amount = data['loose_amount']
            self.value = data['value']
            self.exp_value = data['exp_value']
            self.now = data['now']
            self.created = data['created']
            self.expired = data['expired']
            self.game_state = data['game_state']
            self.is_demo = data["is_demo"]
            self.currency = data["currency"]
            self.active = data["active"]
            self.active_id = data["active_id"]
            self.user_id = data["user_id"]
            self.refund = data["refund"]
            self.type_name = data["type_name"]
            self.currency_char = data["currency_char"]
            self.user_balance_id = data["user_balance_id"]

            if "rate_finished" in data:
                self.rate_finished = data['rate_finished']
            else:
                self.rate_finished = False

        elif self.message_name == 'buyComplete':
            is_successful = data['msg']['isSuccessful']

            if not is_successful:
                self.is_successful = False
                self.is_buy_complete = True
                self.is_list_info_data = False
                if 'code' not in data['msg']:
                    data['msg']['code'] = self.UNKNOWN_CODE
                self.error_code = data['msg']['code']
                self.error_message = data['msg']['message']
            else:
                data = data['msg']['result']
                self.is_successful = True
                self.is_buy_complete = True
                self.is_list_info_data = False
                self.id = data['id']
                # self.direction = data['direction']
                # self.profit_income = data['profit_income']
                # self.value = data['value']
                # self.profit_return = data['profit_return']
                # self.created = data['created']
                # self.type = data['type']
                # self.request_id = data['type']
                # self.client_platform_id = data['client_platform_id']
                # self.time_rate = data['time_rate']
                # self.exp_time = data['exp']
                # self.act = data['act']
                # self.price = data['price']
                # self.refund = data['refound_value']

        else:
            self.is_successful = False
            self.is_buy_complete = False
            self.is_list_info_data = False
