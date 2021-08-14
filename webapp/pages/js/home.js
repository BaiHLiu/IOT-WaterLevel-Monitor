

window.onload = function () {
    console.log("hello!");
    ready_realtime_cards();

    get_devices_info();
    setInterval(function () {
        get_devices_info();
    }, 1000);

    get_history_chart();

}

function ready_realtime_cards() {
    // 初始化实时状态卡片

    $.ajax({
        type: "GET",
        url: config.web_api+"/get_devices_info",
        dataType: "json",
        success: function (data) {
            // console.log(data)
            var dev_nums = data.length;
            var card_template = $('.rt_card');

            for (i = 0; i < dev_nums; i++) {
                var card = card_template.clone();
                card.attr('id', i);
                card.css('display', '');

                $('#real-time-cards').append(card);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

}


function get_devices_info() {
    // 更新设备实时数据
    $.ajax({
        type: "GET",
        url: config.web_api+"/get_devices_info",
        dataType: "json",
        success: function (data) {
            // console.log(data)
            var dev_nums = data.length;
            if (dev_nums == 0) {
                cocoMessage.warning("暂无设备数据")
            } else {
                for (i = 0; i < dev_nums; i++) {
                    var card = $('#real-time-cards').find('#' + i);

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

                    if (time_delta > 2 * interval_time) {

                        // cocoMessage.error("有离线设备", 3000);
                        //2次以上上报失败
                        card.find('#status_icon').removeClass();
                        card.find('#status_icon').addClass('fas fa-close fa-2x text-danger');
                    } else {
                        card.find('#status_icon').removeClass();
                        card.find('#status_icon').addClass('fas fa-check fa-2x text-success');
                    }
                    //温度显示
                    var temperature = ((data[i]['data'][0]['temperature']) / 10).toFixed(1);
                    card.find('.rt-temp').text(temperature);
                    // 传感器
                    var sensors = data[i]['data'];
                    card.find('.distance-1').text((sensors[0]['high_level'] / 1000).toFixed(3) + " M")
                    card.find('.sensor-1').text(sensors[0]['sensor_name'])
                    if (sensors.length == 2) {
                        // 双传感器情况
                        card.find('.distance-2').text((sensors[1]['high_level'] / 1000).toFixed(3) + " M")
                        card.find('.sensor-2').text(sensors[1]['sensor_name'])
                    }

                }

            }
        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

}


// 首页历史记录图表
function get_history_chart() {
    var myChart = echarts.init(document.getElementById('history-chart'));
    // 指定图表的配置项和数据
    option = {
    title: {
    },
    tooltip: {
        trigger: 'axis'

    },
    legend: {
        data: ['龙池-柳疃', '柳疃-城北', '城北-城东', '城东-金口']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            // saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['60分', '50分', '40分', '30分', '20分', '10分']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '龙池-柳疃',
            type: 'line',
            stack: '总量',
            data: [13.2, 10.1, 13.4, 9.0, 23.0, 21.0]
        },
        {
            name: '柳疃-城北',
            type: 'line',
            stack: '总量',
            data: [18.2, 19.1, 23.4, 29.0, 33.2, 31.1]
        },
        {
            name: '城北-城东',
            type: 'line',
            stack: '总量',
            data: [23.2, 20.1, 15.4, 19.0, 33.2, 41.0]
        },
        {
            name: '城东-金口',
            type: 'line',
            stack: '总量',
            data: [ 33.2, 30.1, 33.4, 39.0, 33.5, 32.4]
        },
    ]
};
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
