var SERVER_URL = "http://127.0.0.1:5000"; // TODO: why isn't this working from extension.config.js?
var story;

document.addEventListener('DOMContentLoaded', function() {
	chrome.runtime.sendMessage({msg: "requestStory"}, function(response) {
		story = response.story;
		buildPage (story["headline"], story["url"], story["image"]);
	});
}, false);

function buildPage(headline, url, image) {

	$('#backstretch').css('background-image', 'url(' + image + ')');
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
});

function sendClick () {
	var id = story["_id"]["$oid"];
	var xhr = new XMLHttpRequest();
	xhr.open("POST", SERVER_URL + "/register_click/" + id, true);
	xhr.send();
}