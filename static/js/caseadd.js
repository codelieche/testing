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
    $('.mask-shiwu').css('width', window.outerWidth + 'px');
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

// 点击移出 事务列表
var removeShiwu = function(ele){
    $(ele).parent('div').parent('li').remove();
}
// 点击添加事务，到事务列表
var addShiwu = function(ele){
    var html = '<li class="clearfix">' +
    '<input class="shiwu" name="shiwu" value="VALUE" type="checkbox" checked>' +
    '<span>NAME</span>' +
    '<div class="buttons fr">' +
        '<div class="btn btn-default" onclick="removeShiwu(this);">移出</div>' +
        '<div class="btn btn-primary" onclick="editShiwu(this);">编辑</div>' +
    '</div>' +
'</li>'
    var value = $(ele).parent().data('id');
    var name = $(ele).parent().parent().find('span').text();
    html = html.replace('VALUE', value);
    html = html.replace('NAME', name);
    var x = $('.code-way .shiwu-list').find('input[value="' + value +'"]').length
    if(value && html && x === 0){
         $('.code-way .shiwu-list').append(html)
    }
}

// 点击clone事务，并添加到事务列表
var cloneShiwu = function(shiwu_id, user_id){
    console.log("Clone shiwu " + shiwu_id +" to user " + user_id +" TODO!");
    // 通过ajax把shiwu clone成 user_id的，返回status, id, name
    var html = '<li class="clearfix">' +
    '<input class="shiwu" name="shiwu" value="VALUE" type="checkbox" checked>' +
    '<span>NAME</span>' +
    '<div class="buttons fr">' +
        '<div class="btn btn-default" onclick="removeShiwu(this);">移出</div>' +
        '<div class="btn btn-primary" onclick="editShiwu(this);">编辑</div>' +
    '</div>' +
'</li>'

    $.ajax({
        url: '/api/1.0/shiwu/clone/',
        type: 'POST',
        data: {shiwu_id: shiwu_id, user_id: user_id},
        success: function (data) {
            console.log(data);
            if(data.status == 'success'){
                html = html.replace('VALUE', data.id);
                html = html.replace('NAME', data.name);
                var x = $('.code-way .shiwu-list').find('input[value="' + data.id +'"]').length
                if(data.id && html && x === 0){
                     $('.code-way .shiwu-list').append(html)
                }
            }
        }
    })
}


// 点击编辑事务
var editShiwu = function(ele){
    var id = $(ele).parent().parent().find('input').val();
    if(id){
        var url = '/api/1.0/shiwu/' + id + '/edit/';
        window.scrollTo(0, 0);
        $.ajax({
            url: url,
            type: 'GET',
            success: function(data) {
                $('.mask-alert').html(data).show();
            },
        });
    }
};

// 点击关闭mask-弹窗
var maskAlertClose = function(){
    $('.mask-alert').hide().html('');
};

// post edit shiwu
var postEditShiwu = function(ele, event){
    // 获取表单信息
    var form = $('.mask-alert .case form')[0];
    var formData = new FormData(form);
    // 防止冒泡和默认行为
    event.stopPropagation();
    event.preventDefault();
    // post 传递数据
    var that = this;
    $(this).attr('disabled', true);
    var url = $(form).attr('action');
    $.ajax({
            type: "POST",
            url: url,
            data: formData,
            contentType: false,
            async: true,
            processData: false,
            success: function(data){
                console.log(data);
                // 关闭弹窗
                maskAlertClose();
                // 把编辑的shiwu的前端name修改下。
                var shiwu_id = url.match(/shiwu\/(\d+)\/edit/)[1];
                $('.shiwu[value="' + shiwu_id + '"]').parent().find('span').text(formData.get('name'));
            },
            error: function(err){
                console.log(err);
                // 关闭弹窗
                maskAlertClose();
            }
        });
};


// post Check shiwu
var postCheckShiwu = function(ele, event){
    // 获取表单信息
    // 防止冒泡和默认行为
    event.stopPropagation();
    event.preventDefault();
    // post 传递数据
    var that = this;
    $(this).attr('disabled', true);
    var post_data = {
        shiwu_id: $(ele).data('id'),
        cookies: $('#id_cookies').val()
    }
    $.ajax({
            type: "POST",
            url: '/api/1.0/shiwu/check/',
            data: post_data,
            // contentType: false,
            // async: true,
            // processData: false,
            success: function(data){
                console.log(data);
                alert(data);
            },
            error: function(err){
                console.log(err);
                alert('error');
            }
        });
};


//  请求body
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
                $('.code-way .shiwu-list').append(data);
                $('.mask-shiwu .mask-wrap form input[type="reset"]').click();
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