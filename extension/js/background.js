chrome.tabs.onCreated.addListener(function(tab) {
		var xhr = new XMLHttpRequest();
		xhr.open("GET","http://127.0.0.1:5000/random_story", true);
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				forms = JSON.parse(xhr.responseText);
				console.log(forms);
				console.log("done");
			}
		}
		xhr.send();
	}
);