$(document).ready(function() {
	function resizePostTitle() {
		var postWidth = $('.main-post-inner-desc').width();
		var popularPostWidth = $('.right-popular').width();

		var adviceSetWidth = $('.f-read-set').width(); // width of blocks set of random advice
		var adviceAmountBlocks = 4 //Amount of random advice blocks

		var blockWidth = (adviceSetWidth-100)/4; // width of one block in random advice


		$('.main').find('.main-post-inner-desc').css('height', 0.5625 * postWidth + 'px');
		$('.main').find('.main-post-inner').css('height', 0.5625 * postWidth + 'px');

		$('.right-popular').find('.right-popular-inner').css('height', 0.5625 * popularPostWidth + 'px');

		$('.f-read-set').find('.f-read-block').css('width', (adviceSetWidth-100)/4 + 'px');
		$('.f-read-set').find('.f-read-block-img').css('height', 0.5625 * blockWidth + 'px');

	}

	resizePostTitle();

	$(window).resize(function() {
        resizePostTitle();
    });
});