// React when a browser action's icon is clicked.
chrome.browserAction.onClicked.addListener(function(activeTab){
  var newURL = "http://localhost:5000";
  chrome.tabs.create({ url: newURL });
});
