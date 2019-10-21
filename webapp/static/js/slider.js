$(document).ready(function() {

    //Показать управление страницами и активировать первую ссылку
    $(".indexActivate").show();
    $(".indexActivate li:first").addClass("active");

    function resizePostImg() {
        var imageWidth = $('.slideWrp').find('.slide-block-img').width();

        $('.slideWrp').find('.slide-block-img').css('height', 0.5625 * imageWidth + 'px');
    }

    resizePostImg();

    $(window).resize(function() {
        resizePostImg();
    });

     /* resizing of slider
    alert(field);
    $('.Wrap').css('width', field + 'px');
    $('.Wrap').find('.slideWrp').css('width', field + 'px');
    $('.Wrap').find('.slide-block').css('width', field + 'px');
    */

    //Функции слайдера и страничной навигации
    rotate = function(){
        var field = document.querySelector('.slide-block');
        var width = field.offsetWidth;
        var triggerID = $active.attr("num") - 1; //Получаем количество
        var reelPosition = triggerID * width; //Определяем расстояние между изображениями

        $(".indexActivate li").removeClass('active'); //Удаляются все активные классы
        $(".indexActivate li").css({"background-color":"#ccc"});
        $active.addClass('active'); //Добавляем класс - active (the $active is declared in the rotateSwitch function)
        $(".active").css({"background-color":"#A24444"});

        //Слайдер Анимация
        $(".slideWrp").animate({
            left: -reelPosition
        }, 500 );
    };

    //Вращение и синхронизация событий
    rotateSwitch = function(){
        play = setInterval(function(){ //Устанавливаем таймер - это будет повторяться каждые 7 секунд
            $active = $('.indexActivate li.active').next();
            if ( $active.length === 0) { //Если навигация достигает конца...
                $active = $('.indexActivate li:first'); //возвращаемся к первому
            }
            rotate(); //Запускаем слайдер и страничную навигацию
        }, 5000); //Таймер скорости в миллисекундах (7 секунд)
    };

    rotateSwitch(); //Выполняем функцию запуск

    //При наведении
    $(".slideWrp").hover(function() {
        clearInterval(play); //Останавливаем вращение
    }, function() {
        rotateSwitch(); //Продолжаем вращение
    });

    //При нажатии
    $(".indexActivate li").click(function() {
        $active = $(this); //Останавливаем вращение
        //Сброс таймера
        clearInterval(play); //Останавливаем вращение
        rotate(); //Запускаем вращения
        rotateSwitch(); //Продолжаем вращение
        return false; //Не допускаем перехода по ссылке
    });

    activateFirst = function(){
        play = setInterval(function(){ 
            $active = $('.indexActivate li:first');
            rotate(); //Запускаем слайдер и страничную навигацию
        }, 5000); //Таймер скорости в миллисекундах (7 секунд)
    };

});