$.getJSON('json/stories.json', function (data) {

})
.done(function (data) {
	var stories = [];
	$.each(data, function(key, val) {
		stories.push(val);
	});

	var randInt = Math.floor(Math.random() * stories[0].length);
	var randStory = stories[0][randInt.toString()];

	var bg = randStory['image'];
	$('#backstretch').css('background-image', bg);
	var path = 'images/news/';
	$('#backstretch').css('background-image', 'url("' + path+bg + '")');

	var headlineLink = '<a href="' + randStory['url'] + '">';
	var headlineContent = headlineLink + randStory['headline'] + '</a>';

	$(headlineContent).appendTo('.headline');
});