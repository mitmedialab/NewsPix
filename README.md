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
