$(document).ready(function() {
	styles = {"border-bottom": 'solid 1px #cc0000',
			  "height": '30px'};

	$('.new-facts-events').find('.new-section').css(styles);

	function resizeNew() {
		var imagePostWidth = $('.new-posts-img').width();
		var imageEventWidth = $('.new-events-img').width();
		var imageFactWidth = $('.new-facts-img').width();

		$('.new-posts-inner').find('.new-posts-img').css('height', 0.5625 * imagePostWidth + 'px');
		$('.new-posts-inner').css('height', 0.5625 * imagePostWidth + 'px');

		$('.new-facts-inner').find('.new-facts-img').css('height', 0.5625 * imageFactWidth + 'px');
		$('.new-facts-inner').css('height', 0.5625 * imageFactWidth + 10 + 'px');
		$('.new-facts-title').css('height', 0.5625 * imageFactWidth + 'px');

		$('.new-events-inner').find('.new-events-img').css('height', 0.5625 * imageEventWidth + 'px');
		$('.new-events-inner').css('height', 0.5625 * imageEventWidth + 10 + 'px');
		$('.new-events-title').css('height', 0.5625 * imageFactWidth + 'px');

	}

	resizeNew();

	$(window).resize(function() {
        resizeNew();
    });

});