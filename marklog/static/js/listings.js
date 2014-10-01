$( document ).ready(function() {
	var $container = $('#listings');

	$container.masonry({
		itemSelector: '.listing',
	});

	$container.infinitescroll({
		nextSelector: "div#pagination a:last",
  		navSelector: "div#pagination",
  		itemSelector: "div.listing",
	}, function(newElements) {
    	var $newElems = $(newElements);
    	$container.masonry('appended', $newElems);
  	});
});