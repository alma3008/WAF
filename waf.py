import time

import SqliValidator
import DDOSValidator
import XssValidator
import BruteForceValidator
import CSRFValidator
import URLPhishingValidator


class BlockedRequest(Exception):
	pass


class WAF:
	MAX_RELEASE_TIME = 60 * 60 * 24  # 1 DAY

	def __init__(self):
		self.validators = [
			SqliValidator.SqliValidator(),
			DDOSValidator.DDOSValidator(),
			XssValidator.XssValidator(),
			BruteForceValidator.BruteForceValidator(),
			CSRFValidator.CSRFValidator(),
			URLPhishingValidator.URLPhishingValidator()
		]

		self.blocked_ips = []
		self.last_release_time = 0

	def validate_req(self, client_ip, req, url, req_header):
		if (time.time() - self.last_release_time) > self.MAX_RELEASE_TIME:  # time.time return time in seconds 1.1.1970
			self.blocked_ips = []
			self.last_release_time = time.time()

		if client_ip in self.blocked_ips:
			raise BlockedRequest()

		for validator in self.validators:
			if not validator.validate(client_ip, req, url, req_header):
				print(type(validator))
				self.blocked_ips += client_ip
				raise BlockedRequest()
