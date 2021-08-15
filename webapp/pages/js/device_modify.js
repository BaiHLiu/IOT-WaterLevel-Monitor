window.onload = function () {
    render_modify_device(getQueryVariable('dev_id'));
    render_modify_sensor(getQueryVariable('dev_id'));

}



/*修改信息页面*/

function render_modify_device(dev_id) {
    // 渲染串口服务器信息
    var devices = get_devices_info();
    var device_card = $('#device-info');

    // 从所有设备信息中查到指定设备信息
    for (i = 0; i < devices.length; i++) {
        if (devices[i][0] == dev_id) {
            //渲染标题
            $('#dev-name-render').text(devices[i][1]);
            //渲染卡片
            device_card.find('.device-name').attr('value', devices[i][1]);
            device_card.find('.device-port').attr('value', devices[i][2]);
            device_card.find('.device-time').attr('value', devices[i][6]);
            device_card.find('.device-distance').attr('value', devices[i][7]);
            device_card.find('.device-temperature').attr('value', devices[i][8]);
            device_card.find('.dev_id').text(devices[i][0]);

            // 新增传感器按钮函数传参
            $('#add-sensor-button').attr('onclick', 'add_sensor(' + devices[i][0] + ')');
        }
    }


}


function change_device_config() {
    // 修改串口服务器配置
    var device_card = $('#device-info');

    var device_id = device_card.find('.dev_id').text();
    var device_name = device_card.find('.device-name').val();
    var device_port = device_card.find('.device-port').val();
    var device_time = device_card.find('.device-time').val();
    var distance = device_card.find('.device-distance').val();
    var temperature = device_card.find('.device-temperature').val();

    var req_data = {
        'dev_id': device_id,
        'dev_name': device_name,
        'dev_port': device_port,
        'interval_time': device_time,
        'distance_query_arg': distance,
        'temperature_query_arg': temperature,
        'alarm_params': '',
        // TODO:添加报警参数
    }

    // console.log(req_data);
    $.ajax({
        type: "GET",
        url: config.web_api + "/modify_device_config",
        data: req_data,
        dataType: "json",
        success: function (data) {
            if (data.code == '0') {
                cocoMessage.success("配置保存成功！");
            } else {
                console.log(data);
                cocoMessage.error("配置保存失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

}


function render_modify_sensor(dev_id) {
    // 渲染传感器信息卡片
    var sensor_card_template = $('.sensor_info');

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_sensors_config",
        data: {'dev_id': dev_id},
        dataType: "json",
        success: function (data) {
            console.log(data);
            var sensors = data['body']
            for (i = 0; i < sensors.length; i++) {
                var sensor_card = sensor_card_template.clone();
                sensor_card.css('display', '');
                sensor_card.find('.sensor_name').attr('value', sensors[i][1]);
                sensor_card.find('.sensor-offset').attr('value', sensors[i][3]);
                sensor_card.find('.sensor_address').attr('value', sensors[i][4]);
                sensor_card.find('.sensor-id').text(sensors[i][0]);

                sensor_card.attr('id', sensors[i][0]);

                // 修改传感器配置函数传参
                sensor_card.find('.set-offset-button').attr('onclick', 'set_offset('+sensors[i][0]+')');
                sensor_card.find('.change-sensor-conf').attr('onclick', 'change_sensor_config(' + sensors[i][0] + ')');
                sensor_card.find('.rm-sensor').attr('onclick', 'rm_sensor(' + sensors[i][0] + ')');
                if (sensors[i][5] == 1) {
                    sensor_card.find('.home-graph-check').attr('checked', '');
                }

                $('#sensors-card').append(sensor_card);
            }


        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function change_sensor_config(sensor_id) {
    /*修改传感器参数*/


    var sensor_card = $('#sensors-card').find('#' + sensor_id);
    var sensor_name = sensor_card.find('.sensor_name').val();
    var sensor_address = sensor_card.find('.sensor_address').val();
    var offset = sensor_card.find('.sensor-offset').val();
    if (sensor_card.find('.home-graph-check').is(':checked')) {
        var is_home_graph = 1;
    } else {
        var is_home_graph = 0;
    }

    req_data = {
        'sensor_id': sensor_id,
        'sensor_name': sensor_name,
        'distance_offset': offset,
        'hex_address': sensor_address,
        'home_graph': is_home_graph

    }

    console.log(req_data);
    $.ajax({
        type: "GET",
        url: config.web_api + "/modify_sensor_config",
        data: req_data,
        dataType: "json",
        success: function (data) {
            if (data.code == '0') {
                cocoMessage.success("配置保存成功！");
                location.reload();
            } else {
                console.log(data);
                cocoMessage.error("配置保存失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function add_sensor(bind_dev_id) {
    /*新增传感器用户调用函数*/
    swal({
            title: "新增传感器",
            text: "传感器名称",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "输入传感器名称"
        },
        function (inputValue) {
            if (inputValue === false) return false;

            if (inputValue === "") {
                swal.showInputError("请输入传感器名称！");
                return false
            }

            send_add_sensor(bind_dev_id, inputValue);
            swal("成功", "success");
        });
}


function send_add_sensor(bind_dev_id, sensor_name) {
    /*向后台发送新增传感器请求*/

    $.ajax({
        type: "GET",
        url: config.web_api + "/add_sensor",
        data: {
            'sensor_name': sensor_name,
            'bind_dev_id': bind_dev_id
        },
        dataType: "json",
        success: function (data) {
            if (data.code == '0') {
                cocoMessage.success("配置保存成功！");
                location.reload();
            } else {
                console.log(data);
                cocoMessage.error("配置保存失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function rm_sensor(sensor_id) {
    /*删除传感器*/
    swal({
            title: "确定删除吗？",
            text: "非维护人员请勿删除传感器！",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定删除！",
            closeOnConfirm: false
        },
        function () {

            $.ajax({
                type: "GET",
                url: config.web_api + "/rm_sensor",
                data: {
                    'sensor_id': sensor_id
                },
                dataType: "json",
                success: function (data) {
                    if (data.code == '0') {
                        swal("删除！", "成功删除传感器", "success");
                        location.reload();
                    } else {
                        console.log(data);
                        cocoMessage.error("配置保存失败！", 3000);
                    }

                },
                error: function (jqXHR) {
                    cocoMessage.error("请求后台接口失败！", 3000);
                },
            });


        });

}


function rm_device() {
    /*删除设备*/
    console.log('删除设备');
    var dev_id = $('.dev_id').text();

    $.ajax({
        type: "GET",
        url: config.web_api + "/rm_device",
        data: {
            'dev_id': dev_id
        },
        dataType: "json",
        success: function (data) {
            if (data.code == '0') {
                cocoMessage.success("配置保存成功！");
                location.reload();
            } else {
                console.log(data);
                cocoMessage.error("配置保存失败！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}


function set_offset(sensor_id) {
    /*校准设备*/
    // 计算公式：真实值(level) = 距离值(distance) - 偏差值(offset)

    console.log(get_distance(sensor_id));


    swal({
            title: "校准水位",
            text: "当前真实水位(毫米值)",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "输入当前真实水位(毫米值)"
        },
        function (inputValue) {
            if (inputValue === false) return false;

            if (inputValue === "") {
                swal.showInputError("请输入当前真实水位！");
                return false
            }


            $.ajax({
                type: "GET",
                url: config.web_api + "/set_offset",
                data: {
                    'sensor_id': sensor_id,
                    'offset' : get_distance(sensor_id) - inputValue
                },
                dataType: "json",
                success: function (data) {
                    if (data.code == '0') {
                        swal("成功", "success");
                        location.reload();
                    } else {
                        console.log(data);
                        cocoMessage.error("配置保存失败！", 3000);
                    }

                },
                error: function (jqXHR) {
                    cocoMessage.error("请求后台接口失败！", 3000);
                },
            });


        });

}


function get_distance(sensor_id){
    /*获取传感器测量值*/

    let distance = undefined;

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_distance",
        data: {
            'sensor_id': sensor_id
        },
        async : false,
        dataType: "json",
        success: function (data) {
            // console.log(data);
            distance = data.body
        }
    });


    return distance;

}