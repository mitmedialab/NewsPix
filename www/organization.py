class Organization:
	def __init__(self, name, login_username, login_password, url, logo_url, _id):
		self._id = _id
		self.name = name
		self.login_username = login_username
		self.login_password = login_password
		self.url = url
		self.logo_url = logo_url
		self.number_of_installations = 0

	def get_organization_object(self):
		organization = {}
		organization['name'] = self.name
		organization['login_username'] = self.login_username
		organization['login_password'] = self.login_password
		organization['url'] = self.url
		organization['logo_url'] = self.logo_url
		organization['number_of_installations'] = self.number_of_installations
		if not self._id:
			return organization
		else:
			organization['_id'] = self._id
			return organization