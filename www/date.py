from datetime import datetime
from datetime import timedelta
from pytz import timezone
from dateutil.tz import *

class Date:

	def __init__(self):
		self.now = datetime.now()
		self.today = datetime(self.now.year, self.now.month, self.now.day)
		self.tomorrow = self.today + timedelta(days=1)

	def set_to_local_timezone(self, time_zone):
		local = tzlocal()
		now = datetime.now()
		now = now.replace(tzinfo = local)

		if time_zone is None:
			tz = local
		else:
			tz = timezone(time_zone)
		now = now.astimezone(tz)

		self.now = now
		self.today = datetime(self.now.year, self.now.month, self.now.day)
		self.tomorrow = self.today + timedelta(days=1)


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
		dateObj = datetime.strptime(date, '%m/%d/%Y')
		return datetime.combine(dateObj, datetime.min.time())