from date import Date 

class Installation:

	def __init__(self, organization, date):
		self.organization = organization
		self.date = date

	def get_installation_object(self):
		installation = {}
		installation['organization'] = self.organization
		installation['date'] = self.date
		return installation