function initSideControls() {
  var control_min_width = $('.active-area').width();
  var content_width = $('#page').width(); //Здесь должна быть ширина вашего сайта (если верстка не резиновая).
  var window_width = $(window).width();
  var $bar_wrap = $('.leftbar-wrap');
  var $bar = $bar_wrap.find('.left-controlbar');
  var $scroll_back = $('#scroll-back');
  var prev_top = parseInt($scroll_back.attr('href').substr(1));
   
  if (window_width - content_width - (2 * control_min_width) > 0) {
    $bar.show();
     
    var bar_width = (window_width - content_width) / 2;
     
    $bar_wrap.css({width: bar_width});
     
    if (!prev_top) $scroll_back.hide();
     
    $bar.off('click').on('click', function(e) {
      e.preventDefault();
      prev_top = $(window).scrollTop();
      $('html, body').animate({scrollTop: 0}, 'fast', function() {
        $scroll_back.attr('href', '#' + prev_top).css({display: 'block', opacity: 0}).animate({opacity: 1}, 'fast');
      });
    });
  }
  else {
    $bar.hide();
  }
}
$(document).ready(function() {
  var $scroll_back = $('#scroll-back');
  var $bar = $('.left-controlbar');
   
  var threshold = 500; //порог полной видимости кнопки при скроллинге
   
  $(window)
    /* функция, которая управляет видимостью кнопки "Вверх" в зависимости от положения полос прокрутки */
    .scroll(function() {
      var new_opacity = ($(window).scrollTop() < threshold) ? $(window).scrollTop() / threshold : 1;
      new_opacity ? $bar.show(300) : $bar.hide();
      $bar.css({opacity: new_opacity});
      var offset = parseInt($scroll_back.attr('href').substr(1));
      if (new_opacity) {
        $scroll_back.hide();
      }
      else {
        if (offset) $scroll_back.css({display: 'block', opacity: 0}).animate({opacity: 1}, 'fast');
      }
    })
    .scroll()
    /* связываем событие изменения размеров окна браузера и функцию инициализации кнопок */
    .resize(initSideControls)
    .resize();
   
  /* функция для возврата пользователя на место, с которого он поднялся вверх */
  $scroll_back.click(function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop: $(this).attr('href').substr(1)}, 'normal');
    $(this).attr('href', '#0').hide();
  });
});			