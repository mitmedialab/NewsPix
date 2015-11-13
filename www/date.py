import datetime

class Date:

	def __init__(self):
		now = datetime.datetime.now()
		self.today = datetime.datetime(now.year, now.month, now.day)
		self.tomorrow = self.today + datetime.timedelta(days=1)

	def format_date(self, date):
		month = date.month
		if month < 10:
			month = "0" + str(month)
		day = date.day
		if day < 10:
			day = "0" + str(day)
		year = date.year
		return str(month) + "/" + str(day) + "/" + str(year)

	def format_date_for_chart(self, date):
		month = date.month
		if month < 10:
			month = "0" + str(month)
		day = date.day
		if day < 10:
			day = "0" + str(day)
		year = date.year
		return str(year) + "-" + str(month) + "-" + str(day)

	def date_to_datetime(self, date):
		month = int(date[:2])
		day = int(date[3:5])
		year = int(date[6:])
		return datetime.datetime(year, month, day)