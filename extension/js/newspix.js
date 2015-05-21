document.addEventListener('DOMContentLoaded', function() {
	chrome.runtime.sendMessage({msg: "requestStory"}, function(response) {
		buildPage (response.story["headline"], response.story["url"], response.story["image"]);
	});
}, false);

function buildPage(headline, url, image) {

	$('#backstretch').css('background-image', 'url(' + image + ')');
	$('#bs-url').attr ("href", url);
	var headlineLink = '<a href="' + url + '">';
	var headlineContent = headlineLink + headline + '</a>';

	$(headlineContent).appendTo('.headline');
}