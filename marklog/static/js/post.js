$( document ).ready(function() {
	var $smallheader = $("div#smallheader");
	var $bigheader = $("div#bigheader");
	var atTop = true;
	var slideTime = 100;

	$smallheader.hide();

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



