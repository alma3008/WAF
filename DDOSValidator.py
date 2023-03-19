import validator
import time


class TimeAndNumberOfRequests:
    def __init__(self):
        self.request_number = 0
        self.request_time = time.time()


class DDOSValidator(validator.Validator):
    def __init__(self):
        self.ip_to_first_request = {}

    def validate(self, client_ip, req, url, req_header):
        if client_ip not in self.ip_to_first_request.keys():
            self.ip_to_first_request[client_ip] = TimeAndNumberOfRequests()

        self.ip_to_first_request[client_ip].request_number += 1

        # 1.1.1970 -> time.time() == seconds
        AVERAGE_GET_PER_CLIENT = 10
        AVERAGE_NUMBER_OF_PAGES = 10
        if time.time() - self.ip_to_first_request[client_ip].request_time < 60:
            if self.ip_to_first_request[client_ip].request_number > AVERAGE_GET_PER_CLIENT * AVERAGE_NUMBER_OF_PAGES:
                return False
        else:
            self.ip_to_first_request.pop(client_ip)

        return True
