""" Exceptions """

class PyiqoError(Exception):
    """ Generic error class, catches pyiqo response errors """

    def __init__(self, error_response):
        self.error_response = error_response
        msg = "Pyiqo API returned error code %s (%s) " % \
              (error_response['code'], error_response['message'])
        super(PyiqoError, self).__init__(msg)


class BadEnvironment(Exception):
    """ Environment should be: demo or live. """

    def __init__(self, environment):
        msg = "Environment '%s' does not exist" % environment
        super(BadEnvironment, self).__init__(msg)


class BadArguments(Exception):
    """ Environment should be: demo or live. """

    def __init__(self, argument):
        msg = "Argument {0} isn\'t valid".format(argument)
        super(BadArguments, self).__init__(msg)


class LoginError(Exception):
    """ LoginError Exception. """

    def __init__(self):
        msg = 'Invalid login or password'
        super(LoginError, self).__init__(msg)