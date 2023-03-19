import validator
import re


class SqliValidator(validator.Validator):
    REGEX_PHRASE_FOR_COMMANDS = [".*(D|d)(R|r)(O|o)(P|p).*(T|t)(A|a)(B|b)(L|l)(E|e).*",
                                 ".*(I|i)(N|n)(S|s)(E|e)(R|r)(T|t).*(I|i)(N|n)(T|t)(O|o).*",
                                 ".*(D|d)(R|r)(O|o)(P|p).*",
                                 ".*(I|i)(N|n)(S|s)(E|e)(R|r)(T|t).*",
                                 ".*(S|s)(E|e)(L|l)(E|e)(C|c)(T|t).*",
                                 ".*(o|O)(r|R).*"
                                 ]

    FORBIDDEN_SPECIAL_CHARS = ['\'', '"']

    def validate(self, client_ip, req, url, req_header):
        # {'id': ['1']}  --> id1
        req_str = ''
        for key in req.keys():
            req_str += key
            for item in req[key]:
                req_str += item
        for pattern in self.REGEX_PHRASE_FOR_COMMANDS:
            if re.match(pattern, req_str) is not None:
                for char in self.FORBIDDEN_SPECIAL_CHARS:
                    if char in req_str:
                        return False

        return True
