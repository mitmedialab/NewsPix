
var story;

function buildPage(headline, url, image, imageIsLandscape) {

	url += "?src=newspix";

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
	$('.twitter-share-button').attr('href', twitter_share_url + headline + " " + url + " via %23NewsPix");
}

function getStory(msg){
	chrome.storage.sync.get('previousStoryId', function(obj) {
		var prevId = (obj.previousStoryId == null) ? "0" : obj.previousStoryId.$oid;
		chrome.runtime.sendMessage({msg: msg, id: prevId}, function(response){
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

function populate_popup(){
	var xhr = new XMLHttpRequest();
	xhr.open("GET", SERVER_URL + "/news_organizations", true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
		  response = JSON.parse(xhr.responseText);
		  for (var i = 0; i < response.length; i++){
		  	var organization = response[i];
		  	var organization_name = organization.name;
		  	var organization_id = organization.login_username;

		  	var column_div = $("<div class='col-md-6 organization_box' id='" + organization_id + "'>");
		  	column_div.append($("<h3>" + organization_name + "</h3>"));
		  	column_div.append($("<img class='organization_logo' src='images/logos/" + organization_id + ".png' height='200px' width='200px'>"));

		  	$("#modal_body_div").append(column_div);

		  }
		}
	}
	xhr.send();
}

function sendInstall(newspix_organization){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", SERVER_URL + "/register_install/" + newspix_organization, true);
	xhr.send();
}

$(document).ready(function() {

	// Setup organization logo
	$("#organization_logo").css({'visibility': 'visible'});
	$("#organization_logo").attr('src', "images/logos/" + newspix_organization + ".png");
	$("#organization_home").attr('href', organization_url);
	
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

	$(document).on("click", "#uninstall", function(){
		chrome.tabs.update({ url: 'chrome://chrome/extensions' });
	})

    getStory("requestNextStory");

});
