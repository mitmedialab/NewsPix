from date import Date 

class Story:

	def __init__(self, news_organization, headline, storyURL, imageURL, fromDate, toDate, _id, loadCount, clickCount, position):
		self.news_organization = news_organization
		self.headline = headline
		self.storyURL = storyURL
		self.imageURL = imageURL
		self.fromDate = fromDate
		self.toDate = toDate
		self._id = _id
		self.date_handler = Date()
		if fromDate is not None:
			self.formatedFromDate = self.date_handler.format_date(fromDate)
		if toDate is not None:
			self.formatedToDate = self.date_handler.format_date(toDate)
		self.loadCount = loadCount
		self.clickCount = clickCount
		if loadCount == 0 or loadCount == None or clickCount == 0 or clickCount == None:
			self.clickthrough = 0
		else:
			self.clickthrough = round((float(clickCount) / float(loadCount)) * 100, 2)
		self.position = position

	def get_story_object(self):
		story = {}
		story['news_organization'] = self.news_organization
		story['headline'] = self.headline
		story['url'] = self.storyURL
		story['image'] = self.imageURL
		story['date'] = self.fromDate
		story['to_date'] = self.toDate
		story['load_count'] = self.loadCount
		story['click_count'] = self.clickCount
		story['clickthrough'] = self.clickthrough
		story['position'] = self.position
		if not self._id:
			return story
		else:
			story['_id'] = self._id
			return story
