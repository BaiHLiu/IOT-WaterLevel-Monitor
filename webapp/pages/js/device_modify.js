window.onload = function (){
    render_modify_device(getQueryVariable('dev_id'));
}


/*修改信息页面*/

function render_modify_device(dev_id){
    // 渲染修改配置-串口服务器信息
    var devices = get_devices_info();
    var device_card = $('#device-info');

    // 从所有设备信息中查到指定设备信息
    for(i=0;i<devices.length;i++){
        if(devices[i][0] == dev_id){
            device_card.find('.device-name').attr('value',devices[i][1]);
            device_card.find('.device-port').attr('value',devices[i][2]);
            device_card.find('.device-time').attr('value',devices[i][6]);
            device_card.find('.device-distance').attr('value',devices[i][7]);
            device_card.find('.device-temperature').attr('value',devices[i][8]);

        }
    }

}
