window.onload = function () {
    check_login();
    ready_realtime_cards();

    get_devices_info();
    setInterval(function () {
        get_devices_info();
    }, 10000);

    // get_history_chart();
    render_image();
}


function check_login() {
    // 检查登陆状态
    // 伪装登陆
    if (localStorage.getItem('username')) {
        cocoMessage.success("登陆成功", 1500);
    } else {
        location.href = './login.html';
    }
}

function ready_realtime_cards() {
    // 初始化实时状态卡片

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_devices_info",
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
        url: config.web_api + "/get_devices_info",
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

                    if (time_delta > 50 * interval_time) {

                        // cocoMessage.error("有离线设备", 3000);
                        //50次以上上报失败
                        card.find('#status_icon').removeClass();
                        card.find('#status_icon').addClass('fas fa-close fa-2x text-danger');
                    } else {
                        card.find('#status_icon').removeClass();
                        card.find('#status_icon').addClass('fas fa-check fa-2x text-success');
                    }
                    //温度显示
                    var temperature = ((data[i]['data'][0]['temperature']) / 10).toFixed(1);
                    card.find('.rt-temp').text(temperature);
                    // 视频播放按钮
                    card.find('.img-play').attr('href','#img-'+data[i]['name']);
                    // 传感器
                    var sensors = data[i]['data'];
                    card.find('.distance-1').text((sensors[0]['high_level'] / 1000).toFixed(2) + " M");
                    card.find('.sensor-1').text(sensors[0]['sensor_name']);
                    card.find('.rt-water-depth').text((sensors[0]['water_depth'] / 1000).toFixed(2) + " M");
                    if (sensors.length == 2) {
                        // 双传感器情况
                        card.find('.distance-2').text((sensors[1]['high_level'] / 1000).toFixed(2) + " M");
                        card.find('.sensor-2').text(sensors[1]['sensor_name']);
                        card.find('.rt-water-depth').text((sensors[0]['water_depth'] / 1000).toFixed(2) + " M / " + (sensors[1]['water_depth'] / 1000).toFixed(2) + " M");
                    }
                    // 警戒水位超限状态
                    if (data[i]['if_alarm'] == true) {
                        card.find('.card-dev-alarm').text('[超警戒水位]')
                    }

                }

            }
        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

}

function get_homepage_chars_sensors() {
    /*获取首页显示的传感器*/
    let ret = undefined;

    $.ajax({
        type: "GET",
        url: config.web_api + "/homepage_show_sensors",
        async: false,
        dataType: "json",
        success: function (data) {
            // console.log(data)
            ret = data.body;

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
            // cocoMessage.error("请求后台接口失败！", 3000);
            // 一般是指定时间段没有历史记录或条数不够
            ret = undefined;
        },
    });

    return ret;
}


function get_history_chart() {
    /*获取历史记录*/
    var show_sensors = get_homepage_chars_sensors();
    var ret_list = []

    for (i = 0; i < show_sensors.length; i++) {
        var history_list = {'name': '', 'history': undefined};
        var resp = send_history_chart(show_sensors[i]['sensor_id'], getCurrentTime(), get_befor_time(30000), 20);
        if (resp != undefined) {
            var dev_name = (show_sensors[i]['bind_dev_name']);
            var sensor_name = show_sensors[i]['sensor_name'];

            history_list['history'] = (resp['body']);
            history_list['name'] = dev_name + '-' + sensor_name;
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
            stack: '水位' + i,
            data: [],
        }

        for (j = 0; j < ret_list[i]['history'].length; j++) {
            var time = (ret_list[i]['history'][j]['waterlevel'] / 1000).toFixed(2);
            serie['data'].push(time);

            // 临时按照取第一个传感器的时间
            if (title_time_flag == 0) {
                var title_time = ret_list[0]['history'][j]['datetime'];
                ret_time.push(title_time);
            }
        }

        title_time_flag = 1;
        ret_series.push(serie);
    }


    // console.log(ret_series);
    // console.log(ret_time);
    render_history_chart(ret_title, ret_time, ret_series);

}


// 渲染首页历史记录图表
function render_history_chart(ret_title, ret_times, ret_series) {
    // console.log(ret_series);
    var myChart = echarts.init(document.getElementById('history-chart'));
    // 指定图表的配置项和数据
    option = {
        title: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
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


function generate_rt_table() {
    // 获取即时报表
    $.ajax({
        type: "GET",
        url: config.web_api + "/generate_rt_report",
        dataType: "json",
        success: function (data) {
            // console.log(data);
            if (data.code == '0') {

                window.location.href = './static/rt-table/' + data.body;
            } else {

                cocoMessage.error("生成报表失败", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function render_image() {
    // 处理图片预览

    // 防止文件缓存
    var nonce = parseInt(Math.random()*1000000000)
    $('#viewer').children().each(function (i,n){
        var obj = $(n);
        url = obj.find('.img-responsive').attr('data-original')
        var nonce = parseInt(Math.random()*1000000000);
        obj.find('.img-responsive').attr('data-original', url+'?nonce='+nonce);
        obj.find('.img-responsive').attr('src', url+'?nonce='+nonce);
    })


    var viewer = new Viewer(document.getElementById('viewer'), {
        url: 'data-original'
    });
}