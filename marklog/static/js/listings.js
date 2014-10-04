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

	var $header = $("div#header");
	var $title = $("span#title");
	var $desc = $("div#blogdesc");
	var $listings = $("div#listings");
	var atTop = true;
	var slideTime = 100;

	$listings.css({"padding-top": $header.outerHeight(true)});
	$header.css({"max-width": $listings.width()});

	var minimalHeader = function() {
		$desc.slideUp(slideTime);
		$title.animate({"font-size": "1em"}, slideTime);
		$header.animate({"padding-top": "0.2em", "padding-bottom": "0.2em"}, slideTime);
	}
	var maximalHeader = function() {
		$desc.slideDown(slideTime);	
		$title.animate({"font-size": "2em"}, slideTime);
		$header.animate({"padding-top": "4em", "padding-bottom": "6em"}, slideTime);
	}

	$(window).scroll(function(e){
		if ($(window).scrollTop() > 0) {
			if (atTop) {
				minimalHeader();
			}
			atTop = false;
		} else {
			if (!atTop) {
				maximalHeader();
			}
			atTop = true;
		}
	});
});