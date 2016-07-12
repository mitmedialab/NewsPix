from story import Story

class Analytics:

	def __init__(self, mongo_handler, organization, installations, clicks):
		self.stories = mongo_handler.get_all_stories(organization)
		self.loads = self.get_aggregate_load_count()
		self.clicks = self.get_aggregate_click_count()
		self.clickthrough = self.get_average_clickthrough_rate()
		self.installation_events = self.get_aggregate_events(installations)
		self.click_events = self.get_aggregate_events(clicks)
		self.number_of_installations = len(installations)

	def get_aggregate_load_count(self):
		load_count = 0
		for story in self.stories:
			if story.loadCount is not None:
				load_count += story.loadCount
		return load_count

	def get_aggregate_click_count(self):
		click_count = 0
		for story in self.stories:
			if story.clickCount is not None:
				click_count += story.clickCount
		return click_count;

	def get_average_clickthrough_rate(self):
		if self.loads == 0 or self.clicks == 0:
			return 0
		else:
			return round((float(self.clicks) / float(self.loads)) * 100, 2)

	def get_aggregate_events(self, events):
		if len(events) == 0:
			return []
		current = events[0]

		eventObject = {}
		eventObject['date'] = current.date
		eventObject['close'] = 1

		result = [eventObject]
		result_index = 0
		for i in range(1, len(events)):
			if current.date == events[i].date:
				result[result_index]['close'] += 1
			else:
				current = events[i]
				result_index += 1
				eventObject = {}
				eventObject['date'] = current.date
				eventObject['close'] = 1
				result.append(eventObject)
		return result