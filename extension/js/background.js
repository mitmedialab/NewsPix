
var requestRandom = false;
var organization = "boston_globe";

chrome.runtime.onMessage.addListener(
function(request, sender, sendResponse) {
	if (sender.tab) {
		var forms;
		var xhr = new XMLHttpRequest();
		if (requestRandom) {
			//console.log("RANDOM: " + organization);
			xhr.open("GET", SERVER_URL + "/random_story/new_york_times", true);
		} else if(request.msg == "requestNextStory") {
			if (request.id == undefined) 
				return false;
			//console.log("NEXT: " + organization);
			xhr.open("GET", SERVER_URL + "/get_next_story/new_york_times/" + request.id, true);
		} else {
			if (request.id == undefined) 
				return false;
			//console.log("PREV: " + organization);
			xhr.open("GET", SERVER_URL + "/get_previous_story/new_york_times/" + request.id, true);
		}

		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				forms = JSON.parse(xhr.responseText);
				sendResponse({story: forms});
			}
		}
		xhr.send();
		//console.log("THERE");
		return true;
	}
});

chrome.runtime.onInstalled.addListener(function(details){
    if (details.reason == "install") {
    	chrome.tabs.create({url: SERVER_URL + "/oninstall"}, function(tab) {
    		
    	});
    }
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.msg == "registerClick") {
		sendClick (request.story);
	}
});

function sendClick (story) {
	var id = story["_id"]["$oid"];
	var xhr = new XMLHttpRequest();
	xhr.open("POST", SERVER_URL + "/register_click/" + id, true);
	xhr.send();
}