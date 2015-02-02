chrome.runtime.onMessage.addListener(
function(request, sender, sendResponse) {
	if (sender.tab) {
		var forms;
		var xhr = new XMLHttpRequest();
		xhr.open("GET", SERVER_URL + "/random_story", true);
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