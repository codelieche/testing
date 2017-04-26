var fieldAddClick = function(ele){
    var e = $('.box').first().clone();
    e.find('.field').val('');
    $(ele).parent('.box').after(e);
};

var fieldDelClick = function(ele){
    var bodydata = $(ele).parent('.box').parent('.body-data');
    if(bodydata.find('.box').length > 1){
        $(ele).parent('.box').remove();
    }else{
        alert('至少需要保留一个!');
    }
};

var showShiwuMask = function(){
    // 显示遮罩
    var mask = $('.mask-shiwu');
    $('.mask-shiwu').css('height', window.outerHeight + 'px');
    mask.show();
    window.scrollTo(0, 0);
}

var wayChangen = function() {
        if($('#id_way').val() === 'shiwu'){
            $('.code-way').eq(0).show();
            $('.code-way').eq(1).hide();
        }else{
            $('.code-way').eq(1).show();
            $('.code-way').eq(0).hide();
        }
    }

$(function(){
   // 关闭mask
    $('#mask-close').on('click', function(){
        $('.mask').hide();
    });
    $('.code-way').eq(0).show();

    $('#id_way').on('change', wayChangen);
    wayChangen();
});