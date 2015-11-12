
var requestRandom = false;
var url_map = {"http://www.sentinelsource.com/": "new_york_times"};

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
	chrome.storage.sync.get('newspix_organization', function(obj){
		var newspix_organization = (obj.newspix_organization == null) ? "NONE" : obj.newspix_organization;
		if (sender.tab){
			var forms;
			var xhr = new XMLHttpRequest();
			if (requestRandom) {
				xhr.open("GET", SERVER_URL + "/random_story/" + newspix_organization, true);
			} else if(request.msg == "requestNextStory") {
				if (request.id == undefined) 
					return false;
				xhr.open("GET", SERVER_URL + "/get_next_story/" + newspix_organization + "/" + request.id, true);
			} else {
				if (request.id == undefined) 
					return false;
				xhr.open("GET", SERVER_URL + "/get_previous_story/" + newspix_organization + "/" + request.id, true);
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
	})
	return true;		
});

chrome.runtime.onInstalled.addListener(function(details){
    if (details.reason == "install") {
    	chrome.tabs.create({url: SERVER_URL + "/oninstall"}, function(tab) {
    		chrome.tabs.query({}, function(tabs){
    			tabs.forEach(function(tab){
    				if (tab.url in url_map){
    					var organization = url_map[tab.url];
    					chrome.storage.sync.set({'newspix_organization': organization});
    					sendInstall(organization);
    					return;
    				}
    			})
    		});	
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

function sendInstall(newspix_organization){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", SERVER_URL + "/register_install/" + newspix_organization, true);
	xhr.send();
}