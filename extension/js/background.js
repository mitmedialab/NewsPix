
var requestRandom = false;

chrome.runtime.onMessage.addListener(
function(request, sender, sendResponse) {
	if (sender.tab) {
		var forms;
		var xhr = new XMLHttpRequest();
		if (requestRandom) {
			xhr.open("GET", SERVER_URL + "/random_story", true);
		} else if(request.msg == "requestNextStory") {
			if (request.id == undefined) 
				return false;
			xhr.open("GET", SERVER_URL + "/get_next_story/" + request.id, true);
		} else {
			if (request.id == undefined) 
				return false;
			xhr.open("GET", SERVER_URL + "/get_previous_story/" + request.id, true);
		}

		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				forms = JSON.parse(xhr.responseText);
				sendResponse({story: forms});
			}
		}
		xhr.send();
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