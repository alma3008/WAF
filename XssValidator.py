import validator
import re


class XssValidator(validator.Validator):
    XSS_REGEX_PHRASES = [".*<.*>.*<.*>.*"]

    def validate(self, client_ip, req, url, req_header):
        # transforms dict to string {} -> ""
        req_str = ''
        for key in req.keys():
            req_str += key
            for item in req[key]:
                req_str += item

        for pattern in self.XSS_REGEX_PHRASES:
            if re.match(pattern, req_str) is not None:
                return False

        return True
