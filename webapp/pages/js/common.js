
function timeFormat(time) {
    var nowTime = new Date();
    var day = nowTime.getDate();
    var hours = parseInt(nowTime.getHours());
    var minutes = nowTime.getMinutes();
    // 开始分解付入的时间
    var timeday = time.substring(8, 10);
    var timehours = parseInt(time.substring(11, 13));
    var timeminutes = time.substring(14, 16);
    var d_day = Math.abs(day - timeday);
    var d_hours = hours - timehours;
    var d_minutes = Math.abs(minutes - timeminutes);
    if (d_day <= 1) {
        switch (d_day) {
            case 0:
                if (d_hours == 0 && d_minutes > 0) {
                    return d_minutes + '分钟前';
                } else if (d_hours == 0 && d_minutes == 0) {
                    return '1分钟前';
                } else {
                    return d_hours + '小时前';
                }
                break;
            case 1:
                if (d_hours < 0) {
                    return (24 + d_hours) + '小时前';
                } else {
                    return d_day + '天前';
                }
                break;
        }
    } else if (d_day > 1 && d_day < 10) {
        return d_day + '天前';
    } else {
        return time;
    }
}


function get_time_delta(datetime1, datetime2){
    // 获取时间差
    var date1 = new Date(datetime1.replace(/-/g, "/"));
    var date2 = new Date(datetime2.replace(/-/g, "/"));

    // 返回秒数绝对值
    return Math.abs((date1.getTime()-date2.getTime())/1000);
}



function getCurrentTime() {
    var date = new Date();//当前时间
    var month = zeroFill(date.getMonth() + 1);//月
    var day = zeroFill(date.getDate());//日
    var hour = zeroFill(date.getHours());//时
    var minute = zeroFill(date.getMinutes());//分
    var second = zeroFill(date.getSeconds());//秒

    //当前时间
    var curTime = date.getFullYear() + "-" + month + "-" + day
            + " " + hour + ":" + minute + ":" + second;

    return curTime;
}

function zeroFill(i){
    if (i >= 0 && i <= 9) {
        return "0" + i;
    } else {
        return i;
    }
}