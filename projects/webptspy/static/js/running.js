
function update_summary(){
    var execute_id = $('#stop-execute').attr('data-id');
    post_url = '/api/1.0/execute/running/summary/';
    //渲染数据到html中
    $.ajax({
        type: 'POST',
        url: post_url,
        data: {execute_id: execute_id},
        dataType: 'json',
        timeout: 3000,
        success: function(data){
          if(data.status == 'success'){
               // 渲染数据到html中
                $('.users .box-stats .count').text(data.user_count);
                $('.rps .box-stats .count').text(data.total_rps);
                $('.errors .box-stats .count').text(data.num_failures);
                $('.response .box-stats .count').text(data.time_avg);
            }else if(data.status == 'stop'){
                // 重新刷新网页
                alert("性能测试脚本已经执行完毕了，页面将刷新！");
                location.reload();
            }else if(data.status == 'null'){
                console.log(new Date(), "还没summary数据，稍后刷新");
            };
        },
    })
}

$(document).ready(function(){
    var time_id = setInterval("update_summary()", 5000);
    $('#stop-execute').on('click', function(){
        var result = confirm("是否停止？");
        if(result){
            clearInterval(time_id);
            var execute_id = $(this).attr('data-id');
            //post停止
            var post_url = '/api/1.0/execute/locust/stop/';
            $.ajax({
                type: 'POST',
                url: post_url,
                data: {
                    execute_id: execute_id
                },
                dataType: 'json',
                success: function(data){
                    console.log(data);
                    window.location.reload();
                },
                error: function(xhr, type){
                    console.log(xhr, type);
                }
            })
        }else{
            alert('不停止');
        }
    });
})