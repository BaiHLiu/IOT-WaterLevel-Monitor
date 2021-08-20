window.onload = function () {
    render_card();
}

function render_card() {
    $.ajax({
        type: "GET",
        url: config.web_api + "/get_devices_config",
        dataType: "json",
        data: {'dev_id': getQueryVariable('dev_id')},
        success: function (data) {
            if (data.code == '0') {
                var devices_info = data.body;

                var alert_params = devices_info[4].slice(1, -1).split(', ');
                console.log(alert_params);
                var card = $('#alarm-control');

                if (alert_params.length == 1) {
                    // 无配置
                    card.find('#max-line').attr('value', 0);
                    card.find('#min-line').attr('value', 0);
                    card.find('#change-time').attr('value', 0);
                    card.find('#change-level').attr('value', 0);
                } else {
                    card.find('#max-line').attr('value', alert_params[0]);
                    card.find('#min-line').attr('value', alert_params[1]);
                    card.find('#change-time').attr('value', alert_params[2]);
                    card.find('#change-level').attr('value', alert_params[3]);

                }
                card.find('#save-button').attr('onclick', 'save_alarm();');

            } else {
                console.log(data);
                cocoMessage.error("获取配置失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function save_alarm() {
    var card = $('#alarm-control');
    var max_line = card.find('#max-line').val();
    var min_line = card.find('#min-line').val();
    var change_time = card.find('#change-time').val();
    var change_level = card.find('#change-level').val();

    $.ajax({
        type: "GET",
        url: config.web_api + "/set_alarm",
        dataType: "json",
        data: {
            'dev_id': getQueryVariable('dev_id'),
            'high_line': max_line,
            'low_line': min_line,
            'change_time': change_time,
            'change_level': change_level,
            'username': localStorage.getItem('username'),
            'password': localStorage.getItem('password')
        },
        success: function (data) {
            if (data.code == '0') {
                cocoMessage.success("设置成功！,2000");
                location.reload();
            } else {
                console.log(data);
                cocoMessage.error("获取配置失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}