window.onload = function () {
    render_table();
}


function render_table() {
    /*渲染全部设备列表*/
    $.ajax({
        type: "GET",
        url: config.web_api + "/get_devices_config",
        dataType: "json",
        success: function (data) {
            if (data.code == '0') {
                devices_info = data.body;
                var row_template = $('.trow');
                for (i = 0; i < devices_info.length; i++) {
                    var row = row_template.clone();
                    row.css('display', '');
                    row.find('.device-name').text(devices_info[i][1]);
                    row.find('.config-link').attr('href', './alert_modify.html?dev_id='+devices_info[i][0]);
                    var alert_params = devices_info[i][4].slice(1, -2).split(',');

                    if (alert_params.length == 1) {
                        // 无配置
                        row.find('.high-line').text("未配置");
                        row.find('.low-line').text("未配置");
                        row.find('.change-time').text("未配置");
                        row.find('.change-level').text("未配置");
                    } else {
                        row.find('.high-line').text(alert_params[0] + "毫米");
                        row.find('.low-line').text(alert_params[1] + "毫米");
                        row.find('.change-time').text(alert_params[2] + "分钟");
                        row.find('.change-level').text(alert_params[3] + "毫米");
                    }
                    row_template.after(row);
                }


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