$( document ).ready(function() {
	var $container = $('#listings');

	$container.imagesLoaded(function(){
		$container.masonry({
			itemSelector: '.listing',
		});
	});

	$container.infinitescroll({
		nextSelector: "div#pagination a:last",
  		navSelector: "div#pagination",
  		itemSelector: "div.listing",
  		loading: {
  			finishedMsg: "",
  		}
	}, function(newElements) {
    	var $newElems = $(newElements);
    	$newElems.css({opacity: 0,});
		$newElems.imagesLoaded(function(){
			$newElems.animate({opacity: 1,}, 100);
    		$container.masonry('appended', $newElems);
		});    	
  	});
});