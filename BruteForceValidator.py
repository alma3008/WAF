import validator
import time
import re


class TimeAndNumberOfRequests:
    def __init__(self):
        self.request_number = 0
        self.request_time = time.time()


class BruteForceValidator(validator.Validator):

    DISALLOWED_URLS = [".*(L|l)(O|o)(G|g)(I|i)(N|n).*"]
    ALLOWED_ACTIONS = 10

    def __init__(self):
        self.ip_to_first_request = {}

    def validate(self, client_ip, req, url, req_header):
        found = False
        for disallowed_url in self.DISALLOWED_URLS:
            if re.match(disallowed_url, url) is not None:
                found = True
                break

        if not found:
            return True

        if client_ip not in self.ip_to_first_request.keys():
            self.ip_to_first_request[client_ip] = TimeAndNumberOfRequests()

        self.ip_to_first_request[client_ip].request_number += 1

        if time.time() - self.ip_to_first_request[client_ip].request_time < 6000:  # 12 hours
            if self.ip_to_first_request[client_ip].request_number > self.ALLOWED_ACTIONS:
                return False
        else:
            self.ip_to_first_request.pop(client_ip)

        return True
