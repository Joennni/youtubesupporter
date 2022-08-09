$(document).ready(function () {

    // var $moreBtn = $('.more-btn');
    
    $('.more-btn').click(function(){
        $(this).toggleClass('active');
        $('.main-navigation').toggleClass('active');
    })

});