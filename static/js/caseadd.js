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

var wayChange = function() {
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
    // $('.code-way').eq(0).show();

    $('#id_way').on('change', wayChange);
    wayChange();

    $('.mask-shiwu .mask-wrap form input[type="submit"]').on('click', function(event){

        // 获取shiwu的表单 html5新特性，老浏览器不支持
        var formData = new FormData($('.mask-shiwu .mask-wrap form')[0])
        // 防止重复点击
        $(this).attr('disabled', true);
        // 阻止冒泡
        event.stopPropagation();
        // 取消默认提交事件
        event.preventDefault();
        // 提交表单
        var that = this;

        $.ajax({
            type: "POST",
            url: '/api/1.0/shiwu/add/',
            data: formData,
            contentType: false,
            async: true,
            processData: false,
            success: function(data){
                if(data.status === 'success'){
                    // 重置表单：
                    $('.mask-shiwu .mask-wrap form input[type="reset"]').click();
                }else{
                    alert(data.msg);
                }
                // 取消disabled属性
                $(that).removeAttr('disabled')
                // 关闭弹窗
                $('#mask-close').click();
            },
            error: function(err){
                console.log(err);
                // 取消disabled属性
                $(this).removeAttr('disabled')
            }
        });

    })
});