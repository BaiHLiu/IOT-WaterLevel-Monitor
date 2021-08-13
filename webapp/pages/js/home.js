window.onload = function () {
    console.log("hello!");


    get_devices_info();
    // setInterval(function(){
    //     get_devices_info();
    // }, 3000);

}

function get_devices_info() {

    $.ajax({
        type: "GET",
        url: "http://192.168.123.189:5002/get_devices_info",
        dataType: "json",
        success: function (data) {
            console.log(data)
            var dev_nums = data.length;
            if (dev_nums == 0) {
                cocoMessage.warning("暂无设备数据")
            } else {
                var card_template = $('.rt_card');
                for (i = 0; i < dev_nums; i++) {

                    var card = card_template.clone();

                    card.attr('id', i);
                    card.css('display', '');
                    // 站点名称
                    card.find('.card-dev-name').text(data[i]['name']);
                    // 上报时间
                    card.find('.rt-update-time').text(timeFormat(data[i]['update_time']));
                    //上报状态
                    var interval_time = data[i]['interval_time'];
                    var update_time = data[i]['update_time'];
                    var current_time = getCurrentTime();
                    var time_delta = get_time_delta(current_time, update_time);
                    console.log(time_delta);
                    console.log(interval_time);
                    if (time_delta > 2 * interval_time) {

                        cocoMessage.error("有离线设备", 3000);
                        //2次以上上报失败
                        card.find('#status_icon').removeClass();
                        card.find('#status_icon').addClass('fas fa-close fa-2x text-danger');
                    }

                    // 传感器
                    var sensors = data[i]['data'];
                    card.find('.distance-1').text((sensors[0]['high_level'] / 1000).toFixed(2) + " M")
                    card.find('.sensor-1').text(sensors[0]['sensor_name'])
                    if (sensors.length == 2) {
                        // 双传感器情况
                        card.find('.distance-2').text((sensors[1]['high_level'] / 1000).toFixed(2) + " M")
                        card.find('.sensor-2').text(sensors[1]['sensor_name'])
                    }

                    $('#real-time-cards').append(card);

                }

            }
        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

}


