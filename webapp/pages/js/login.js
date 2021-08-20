function login() {
    // 登陆函数
    var username = $('#username').val();
    var password = $('#password').val();

    $.ajax({
        type: "GET",
        url: config.web_api + "/login",
        data: {
            'username': username,
            'password': password
        },
        xhrFields   : {withCredentials: true},
        crossDomain: true,
        dataType: "json",
        success: function (data) {
            // console.log(data);
            if (data.code == '0') {
                localStorage.setItem('username',username);
                localStorage.setItem('password',password);
                window.location.href = './index.html';
            } else {

                cocoMessage.error("用户名或密码错误！", 3000);
            }

        },
        error: function (jqXHR) {
            cocoMessage.error("请求后台接口失败！", 3000);
        },
    });
}