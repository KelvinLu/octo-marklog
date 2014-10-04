$( document ).ready(function() {
	var $smallheader = $("div#smallheader");
	var $bigheader = $("div#bigheader");
	var $postcontent = $("div#post")
	var atTop = true;
	var slideTime = 100;

	$smallheader.hide();
	$postcontent.css({"padding-top": $bigheader.outerHeight(true) + 100});
	$("div.header").css({"max-width": $postcontent.outerWidth(true)});

	var showSmallHeader = function() {
		$bigheader.slideUp(slideTime, function() {
			$smallheader.slideDown(slideTime);
		});
	}

	var showBigHeader = function() {
		$smallheader.slideUp(slideTime, function() {
			$bigheader.slideDown(slideTime);
		});	
	}

	$(window).scroll(function(e){
		if ($(window).scrollTop() > 0) {
			if (atTop) {
				showSmallHeader();
			}
			atTop = false;
		} else {
			if (!atTop) {
				showBigHeader();
			}
			atTop = true;
		}
	});
});



