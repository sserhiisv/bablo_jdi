$(document).ready(function() {
	function resizePostImg() {
		var postWidth = $('.post').width();
		var divImage = $("#post-content").find("div");
		var similarPostWidth = $('.post-similar-block').width();
		var iframe = $("#post-content").find("iframe");

		var styleImg = {
			'max-width': postWidth + 'px',
			'max-height': '100vh'
		};

		var stylePostImg = {
			'max-width': postWidth + 'px',
			'max-height': '100vh'
		};

		var divStyle = {
			'width': postWidth + 'px',
			//'background': '#F7DBDB',
			//'background': 'E7E8EB',
			'background': '#E7E8EB',
			'margin-left': '-30px',
		};

		var iframeStyle = {
			'width': postWidth + 'px',
			'height': (postWidth * 0.5625) + 'px'
		};

		$('.post-img').find('img').css(stylePostImg);

		$(iframe, window.parent.document).css(iframeStyle);

		$(divImage).each(function(index, element) {
			$(element).css(divStyle);
			$(element).find('img').css(styleImg);
		});

		$('.post-similar-set').find('.post-similar-img').css('height', 0.5625 * similarPostWidth + 'px');
	}

	resizePostImg();

	$(window).resize(function() {
        resizePostImg();
    });


	var images = $("#post-content").find("div");
	$(images).css({'cursor': 'pointer'});

	$(images).click(function() {
		var img = $(this).find("img");
	    var src = img.attr('src');

	    var modal = document.getElementById('myModal');
		var modalImg = document.getElementById("img01");

	    modal.style.display = "block";
	    modalImg.src = src;

	    var imageHeight = $('#img01').height();
		var windowHeight = $(window).height();
		var padding = windowHeight/2 - imageHeight/2;
		$('.modal').css({'padding-top': padding + 'px'});

		modal.onclick = function() {
		    modal.style.display = "none";
		}
	});

});