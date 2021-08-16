var page_count = 0;

window.onload = function () {
    get_button_action();
}


function get_button_action() {

    /*响应按钮事件*/
    var start_time = $('#start-time').val();
    var end_time = $('#end-time').val();
    if (!start_time || !end_time) {
        end_time = getCurrentTime();
        start_time = get_befor_time(86400);

    }

    /*获取全部传感器信息*/
    var all_sensors = get_all_sensors();
    console.log(all_sensors);


    /*准备历史记录卡片*/
    if (page_count == 0) {
        var card_template = $('.chart-card');
        for (let i = 0; i < all_sensors.length; i++) {
            var card = card_template.clone();
            card.css('display', '');
            card.attr('id', all_sensors[i][0]);
            card.find('.card-title').text(all_sensors[i][1]);
            card.find('#history-chart').attr('id', 'history-chart' + all_sensors[i][0]);
            $('#history-cards').append(card);

        }

        page_count = 1;
    }


    get_history_chart(all_sensors, start_time + ' 00:00:00', end_time + ' 24:00:00');


}


function get_all_sensors() {
    /*获取所有传感器信息*/
    let ret = new Array();
    $.ajax({
        type: "GET",
        url: config.web_api + "/get_devices_info",
        async: false,
        dataType: "json",
        success: function (data) {
            // console.log(data);
            for (let i = 0; i < data.length; i++) {
                // 遍历设备
                for (let j = 0; j < data[i]['data'].length; j++) {
                    //遍历传感器
                    let sen_info = data[i]['data'][j];
                    let sen_id = sen_info['sensor_id'];
                    let show_name = data[i]['name'] + '-' + sen_info['sensor_name'];

                    ret.push([sen_id, show_name]);
                }
            }


        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

    return ret;


}


function send_history_chart(sensor_id, time_end, time_start, limit) {
    /*向后台请求历史记录*/
    let ret = undefined;

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_period_history",
        async: false,
        data: {'sensor_id': sensor_id, 'time_end': time_end, 'time_start': time_start, 'limit': limit},
        dataType: "json",
        success: function (data) {
            ret = data;

        },
        error: function (jqXHR) {
            cocoMessage.error("有设备指定时段内无记录", 3000);
            // 一般是指定时间段没有历史记录或条数不够
            ret = undefined;
        },
    });

    return ret;
}


function get_history_chart(show_sensors, start_time, end_time) {
    /*获取历史记录*/
    var ret_list = []

    for (i = 0; i < show_sensors.length; i++) {
        var history_list = {'name': '', 'history': undefined};
        var resp = send_history_chart(show_sensors[i][0], end_time, start_time, 15);
        if (resp != undefined) {
            var sensor_name = show_sensors[i][1];

            history_list['history'] = (resp['body']);
            history_list['name'] = sensor_name;
            ret_list.push(history_list);
        }

    }
    // console.log(ret_list);

    // 遍历结果，整理成charts的数据格式
    var ret_title = new Array();
    var ret_time = new Array();
    var ret_series = new Array();
    var title_time_flag = 0;
    for (i = 0; i < ret_list.length; i++) {
        var name = (ret_list[i]['name']);
        ret_title.push(name);


        serie = {
            name: name,
            type: 'line',
            stack: '水位',
            data: []
        }

        for (j = 0; j < ret_list[i]['history'].length; j++) {
            var time = (ret_list[i]['history'][j]['waterlevel'] / 1000).toFixed(2);
            serie['data'].push(time);

            // 临时按照取第一个传感器的时间
            // TODO:图表传感器时间显示处理
            if (title_time_flag == 0) {
                var title_time = ret_list[0]['history'][j]['datetime'];
                ret_time.push(title_time);
            }
        }

        title_time_flag = 1;
        ret_series.push(serie);

        /*        console.log([name]);
                console.log(ret_time);
                console.log(serie);
                console.log(show_sensors[i][0]);*/

        render_history_chart([name], ret_time, serie, show_sensors[i][0]);
    }


    // console.log(ret_series);

    // console.log(ret_time);


}


// 渲染首页历史记录图表
function render_history_chart(ret_title, ret_times, ret_series, card_id) {

    var myChart = echarts.init(document.getElementById('history-chart' + card_id));
    // 指定图表的配置项和数据
    option = {
        title: {},
        tooltip: {
            trigger: 'axis'

        },
        legend: {
            data: ret_title
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
            data: ret_times
        },
        yAxis: {
            type: 'value'
        },
        series: ret_series,
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
