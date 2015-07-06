// TODO: why isn't this working from extension.config.js?
var SERVER_URL = "http://127.0.0.1:5000"; 
var story;

document.addEventListener('DOMContentLoaded', function() {
	
	chrome.storage.sync.get('previousStoryId', function(obj) {
		
		var prevId = (obj.previousStoryId == null) ? "0" : obj.previousStoryId.$oid;
		chrome.runtime.sendMessage({msg: "requestStory", id: prevId}, function(response) {
			story = response.story;
			chrome.storage.sync.set({'previousStoryId': story["_id"]});
			buildPage (story["headline"], story["url"], story["image"]);
		});
	});

	document.getElementById('uninstall').addEventListener('click', function() {
        chrome.tabs.update({ url: 'chrome://chrome/extensions' });
    });
}, false);

function buildPage(headline, url, image) {

	document.title = headline;
	
	$('#backstretch').css('background-image', 'url(' + image + ')');
	if (!imageIsLandscape (image)) {
		$('#backstretch').css('background-size', 'contain');
		$('#backstretch').css('-webkit-background-size', 'contain');
	}

	$('#bs-url').attr ("href", url);
	var headlineLink = '<a href="' + url + '">';
	var headlineContent = headlineLink + headline + '</a>';

	$(headlineContent).appendTo('.headline');
}

$(document).ready(function() {
	$('.headline').click(function () {
		sendClick ();
	});
	$('#bs-url').click(function () {
		sendClick ();
	});
	$('.help').click(function () {
		$('.help-box').toggle(200);
	});
});

function sendClick () {
	var id = story["_id"]["$oid"];
	var xhr = new XMLHttpRequest();
	xhr.open("POST", SERVER_URL + "/register_click/" + id, true);
	xhr.send();
}

function imageIsLandscape(imageUrl) {
	var img = new Image();
	img.src = imageUrl;
	return img.width > img.height;
}