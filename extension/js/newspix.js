
var story;

document.addEventListener('DOMContentLoaded', function() {
	
	getStory("requestNextStory");

	document.getElementById('uninstall').addEventListener('click', function() {
        chrome.tabs.update({ url: 'chrome://chrome/extensions' });
    });
}, false);

function buildPage(headline, url, image, imageIsLandscape) {

	document.title = headline;
	
	$('#backstretch').css('background-image', 'url(' + image + ')');
	if (!imageIsLandscape) {
		$('#backstretch').css('background-size', 'contain');
		$('#backstretch').css('-webkit-background-size', 'contain');
	}

	$('#bs-url').attr ("href", url);
	var headlineLink = '<a href="' + url + '">';
	var headlineContent = headlineLink + headline + '</a>';

	$('.headline').text("");
	$(headlineContent).appendTo('.headline');

	$('.facebook-share').attr('href', $('.facebook-share').attr('href') + url);
	$('.twitter-share-button').attr('href', $('.twitter-share-button').attr('href') + headline + " " + url + " via %23NewsPix for the @sentinelsource");
}
function getStory(msg){
	chrome.storage.sync.get('previousStoryId', function(obj) {
		
		var prevId = (obj.previousStoryId == null) ? "0" : obj.previousStoryId.$oid;
		chrome.runtime.sendMessage({msg: msg, id: prevId}, function(response) {
			story = response.story;
			chrome.storage.sync.set({'previousStoryId': story["_id"]});
			buildPage (story["headline"], story["url"], story["image"], story["isLandscape"]);
		});
	});
}

$(document).ready(function() {
	$('.headline').click(function () {
		chrome.runtime.sendMessage({msg: "registerClick", story: story});
	});
	$('#bs-url').click(function () {
		chrome.runtime.sendMessage({msg: "registerClick", story: story});
	});
	$('.help').click(function () {
		$('.help-box').toggle(200);
	});
	$('.forward').click(function () {
		getStory("requestNextStory");
	});
	$('.backward').click(function () {
		getStory("requestPreviousStory");
	});
});
