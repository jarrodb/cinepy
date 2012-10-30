import re

class Validators(object):
    ip_re = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    def __init__(self):
        pass

    @classmethod
    def ip_address(self, value):
        return bool(re.match(self.ip_re, value))

