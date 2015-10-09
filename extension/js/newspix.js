
var story;
var twitter_share_url = "https://twitter.com/intent/tweet?text=";
var facebook_share_url = "https://www.facebook.com/sharer/sharer.php?u=";

document.addEventListener('DOMContentLoaded', function() {
	
	getStory("requestNextStory");

	document.getElementById('uninstall').addEventListener('click', function() {
        chrome.tabs.update({ url: 'chrome://chrome/extensions' });
    });
}, false);

function buildPage(headline, url, image, imageIsLandscape) {

	url = url + "?src=newspix";

	document.title = headline;
	$('#backstretch').hide()
	$( ".headline" ).hide()

	$('#backstretch').css('background-image', 'url(' + image + ')');
	if (!imageIsLandscape) {
		$('#backstretch').css('background-size', 'contain');
		$('#backstretch').css('-webkit-background-size', 'contain');
	} else {
		$('#backstretch').css('background-size', 'cover');
		$('#backstretch').css('-webkit-background-size', 'cover');
	}
	$( "#backstretch" ).fadeIn( "slow");

	$('#bs-url').attr ("href", url);
	var headlineLink = '<a href="' + url + '">';
	var headlineContent = headlineLink + headline + '</a>';

	
	$('.headline').text("");
	$(headlineContent).appendTo('.headline');
	$( ".headline" ).fadeIn( "slow");

	$('.facebook-share').attr('href', facebook_share_url + url);
	$('.twitter-share-button').attr('href', twitter_share_url + headline + " " + url + " via %23NewsPix for the @sentinelsource");
}
function getStory(msg){
	chrome.storage.sync.get('previousStoryId', function(obj) {
		
		var prevId = (obj.previousStoryId == null) ? "0" : obj.previousStoryId.$oid;
		chrome.runtime.sendMessage({msg: msg, id: prevId}, function(response) {
			story = response.story;
			if (story == null){
				buildPage("No New Stories", "", "../images/logos/newspixlogo.png", true);
				$('.facebook-share').hide();
				$('.twitter-share-button').hide();
			} else {
				chrome.storage.sync.set({'previousStoryId': story["_id"]});
				$('.facebook-share').show();
				$('.twitter-share-button').show();
				buildPage(story["headline"], story["url"], story["image"], story["isLandscape"]);
			}
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
		$( ".headline" ).fadeOut("slow");
		$( "#backstretch" ).fadeOut( "slow", function() {
		    getStory("requestNextStory");
		});
		
	});
	$('.backward').click(function () {
		$( ".headline" ).fadeOut("slow");
		$( "#backstretch" ).fadeOut( "slow", function() {
		    getStory("requestPreviousStory");
		});
		
	});
	$(document).keydown(function(e){
		// left arrow key
		if (e.which == 37){
			$( ".headline" ).fadeOut("slow");
			$( "#backstretch" ).fadeOut( "slow", function() {
		    	getStory("requestPreviousStory");
			});
		}
		// right arrow key
		if (e.which == 39){
			$( ".headline" ).fadeOut("slow");
			$( "#backstretch" ).fadeOut( "slow", function() {
		    	getStory("requestNextStory");
			});
		}
	})
});
