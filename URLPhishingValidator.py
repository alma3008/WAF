import validator
import csv


class URLPhishingValidator(validator.Validator):
    def __init__(self):
        # http://data.phishtank.com/data/online-valid.csv
        with open("C:\\Users\\USER\\Downloads\\verified_online.csv") as fp:
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            data_read = [row[1].replace("http://", "").replace("https://", "") for row in reader]
            data_read_fixed = []
            for row in data_read:
                if row[len(row) - 1] == '/':
                    row = row[0:-1]
                data_read_fixed.append(row)

            self.forbidden_urls = data_read_fixed

    def validate(self, client_ip, req, url, req_header):
        for bad_url in self.forbidden_urls:
            if bad_url in req:
                return False

            for _, value in req_header.items():
                if bad_url in value:
                    return False

            if bad_url in url:
                return False

        return True
