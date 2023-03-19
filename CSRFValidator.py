import validator
import config


class CSRFValidator(validator.Validator):
    def validate(self, client_ip, req, url, req_header):
        for phrase in ['referer', 'Referer']:
            try:
                if config.hostname not in req_header[phrase] and req_header[phrase] != '':
                    return False
            except KeyError as e:
                pass

        return True
