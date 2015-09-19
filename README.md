NewsPix
=======

A news engagement project with the Future of News Initiative (Matt Carroll) and the Emerson Engagement Lab (@kanarinka, @jayvachon). 


## Setup

**1.** Clone the repository:

```
git clone https://github.com/c4fcm/NewsPix.git
```

**2.** Install dependencies

* [MongoDB](http://www.mongodb.org/downloads) (It is easiest to install this using [Homebrew](http://brew.sh/))
* Use pip to install the following packages:
```
pip install Flask
pip install pymongo
pip install virtualenv
pip install requests
pip install flask-cors
pip install Pillow
```

**3.** Create app.config file

Navigate to Newspix/www, copy the contents of app.config.template, create a new file (in the same directory) called app.config and paste the contents of app.config.template into it. The app.config file should look like this:

```
[app]
admin_username: [your admin username e.g. newspix]
admin_password: [your password e.g. mypassword]

[db]
db: [database name eg mydatabase]
host: localhost
user: [leave blank]
pass: [leave blank]
name: newspix_boston_herald
port: 27017
auth_db:
collection:stories
```

## Run locally

**1.** In Terminal, navigate to the NewsPix server directory:

```
cd NewsPix/www
```

**2.** Start a local server:

```
source venv/bin/activate
python server.py
```

**3.** Open Chrome

1. Use the URL bar to go to chrome://extensions
1. Click **Load unpacked extension...**
2. Select NewsPix/extension

**4.** Open the admin panel at http://127.0.0.1:5000/admin and add some stories

**5.** Open a new tab - you should see a random story!
