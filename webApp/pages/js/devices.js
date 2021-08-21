window.onload = function () {
    // console.log(get_devices_info());
    render_devs();

}

function render_devs() {
    // 生成设备列表
    var dev_conf = get_devices_info();
    console.log(dev_conf);
    var row_template = $('.trow');

    for (i = 0; i < dev_conf.length; i++) {
        var row = row_template.clone();
        row.css('display', '');
        row.find('.device-name').text(dev_conf[i][1]);
        row.find('.device-port').text(dev_conf[i][2]);
        row.find('.time-interval').text(dev_conf[i][6]);
        row.find('.sensor-number').text(get_sensors_info(dev_conf[i][0]).length);
        row.find('.upload-number').text(dev_conf[i][5]);
        row.find('.config-link').attr('href', './device_modify.html?dev_id=' + dev_conf[i][0])

        row_template.after(row);
    }


}

function get_sensors_info(dev_id) {
    // 获取指定设备绑定的传感器信息
    result = undefined;

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_sensors_config",
        data: {'dev_id': dev_id},
        async: false,
        dataType: "json",
        success: function (data) {
            // console.log(data);
            result = data.body;
        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

    return result;

}


function get_devices_info() {
    // 获取所有设备信息
    result = undefined;

    $.ajax({
        type: "GET",
        url: config.web_api + "/get_devices_config",
        async: false,
        dataType: "json",
        success: function (data) {
            // console.log(data);
            result = data.body;
        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });

    return result;

}


function add_device() {
    /*添加串口服务器*/
    swal({
            title: "新增站点上报模块",
            text: "站点名称",
            type: "input",
            showCancelButton: true,
            closeOnConfirm: false,
            animation: "slide-from-top",
            inputPlaceholder: "输入站点名称"
        },
        function (inputValue) {
            if (inputValue === false) return false;

            if (inputValue === "") {
                swal.showInputError("请输入站点名称！");
                return false
            }

            send_add_device(inputValue);

            // swal("成功", "success");

        });
}


function send_add_device(dev_name) {
    /*向后台发送新增设备请求*/
    $.ajax({
        type: "GET",
        url: config.web_api + "/add_device",
        data: {
            'dev_name': dev_name,
            'username': localStorage.getItem('username'),
            'password': localStorage.getItem('password')
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



