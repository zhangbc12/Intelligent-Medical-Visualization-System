var map = new AMap.Map("container", {
    center: [114.142744, 22.2801], //香港大学
    zoom: 14
});


var drivingOption = {
    policy: AMap.DrivingPolicy.LEAST_TIME, // 其它policy参数请参考 https://lbs.amap.com/api/javascript-api/reference/route-search#m_DrivingPolicy
    ferry: 1, // 是否可以使用轮渡
    province: '京' // 车牌省份的汉字缩写
}

var drivingOption2 = {
    policy: AMap.DrivingPolicy.LEAST_TIME, // 其它policy参数请参考 https://lbs.amap.com/api/javascript-api/reference/route-search#m_DrivingPolicy
    ferry: 1, // 是否可以使用轮渡
    province: '京', // 车牌省份的汉字缩写
    map: map,
    panel: 'panel'
}

var origin_point_x = 0;
var origin_point_y = 0;
var number = 0;

var index = 0;
var input_value = -1;

var driving = new AMap.Driving(drivingOption)

var minTime = 0;
var index = 0;
var arr = [];

var final_wt = [];
var waiting_time;

var x_di = [114.179761, 114.157632, 114.177093, 114.129278,
    113.943491, 114.13936,  114.046715, 114.206924,
    114.241388, 114.179645, 114.136584, 114.18024,
    114.036563, 114.274649, 113.980978, 114.000665,
    114.231792, 114.12463];

var y_di = [22.455621,  22.338377,  22.312297,  22.493949,
    22.279291,  22.338407,  22.442575,  22.376603,
    22.267015,  22.306322,  22.267337,  22.273262,
    22.205325,  22.315452,  22.404644,  22.455541,
    22.31996,   22.367308];

// var name = ["Alice Ho Miu Ling Nethersole Hospital",
//     "Caritas Medical Centre",
//     "Kwong Wah Hospital",
//     "North District Hospital",
//     "North Lantau Hospital",
//     "Princess Margaret Hospital",
//     "Pok Oi Hospital",
//     "Prince of Wales Hospital",
//     "Pamela Youde Nethersole Eastern Hospital",
//     "Queen Elizabeth Hospital",
//     "Queen Mary Hospital",
//     "Ruttonjee Hospital",
//     "St John Hospital",
//     "Tseung Kwan O Hospital",
//     "Tuen Mun Hospital",
//     "Tin Shui Wai Hospital",
//     "United Christian Hospital",
//     "Yan Chai Hospital"];
// var name = ["111","222"];
// name[0] = 'Alice Ho Miu Ling Nethersole Hospital';
// name[1] = 'Caritas Medical Centre';

// var hos_name = ["11","22"];
// var hos_name = {0:"Alice Ho Miu Ling Nethersole Hospital", 1:"Caritas Medical Centre"};
var hos_name = new Map();
hos_name.set(0, "Alice Ho Miu Ling Nethersole Hospital");
hos_name.set(1, "Caritas Medical Centre");
hos_name.set(2, "Kwong Wah Hospital");
hos_name.set(3, "North District Hospital");
hos_name.set(4, "North Lantau Hospital");
hos_name.set(5, "Princess Margaret Hospital");
hos_name.set(6, "Pok Oi Hospital");
hos_name.set(7, "Prince of Wales Hospital");
hos_name.set(8, "Pamela Youde Nethersole Eastern Hospital");
hos_name.set(9, "Queen Elizabeth Hospital");
hos_name.set(10, "Queen Mary Hospital");
hos_name.set(11, "Ruttonjee Hospital");
hos_name.set(12, "St John Hospital");
hos_name.set(13, "Tseung Kwan O Hospital");
hos_name.set(14, "Tuen Mun Hospital");
hos_name.set(15, "Tin Shui Wai Hospital");
hos_name.set(16, "United Christian Hospital");
hos_name.set(17, "Yan Chai Hospital");


function clickMap (resolve, reject) {
    map.on('click', function(e) {
        //document.getElementById("lnglat").value = e.lnglat.getLng() + ',' + e.lnglat.getLat();
        document.getElementById("lnglat").value = "Searching Now...";
        origin_point_x = e.lnglat.getLng();
        origin_point_y = e.lnglat.getLat();
        number++;
        input_value = $('input:radio[name="pre"]:checked').val();
        console.log("input_value:");
        console.log(input_value);
        console.log(number);
        resolve('200 OK');
    });
}

// 构造路线导航类

// 根据起终点经纬度规划驾车导航路线
function test (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.179761, 22.455621),
        function(status, result) {
            console.log("p1");
            if (status === 'complete') {
                arr[0] = [result.routes[0].time, 0];
                resolve('200 OK');
            } else {
                arr[0] = [172800, 0];
                resolve('200 OK');
            }
        });
}

function test2 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.157632, 22.338377),
        function(status, result) {
            console.log("p2");
            if (status === 'complete') {
                arr[1] = [result.routes[0].time, 1];
                resolve('200 OK');
            } else {
                arr[1] = [172800, 1];
                resolve('200 OK');
            }
        });
}

function test3 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.177093, 22.312297),
        function(status, result) {
            console.log("p3");
            if (status === 'complete') {
                arr[2] = [result.routes[0].time, 2];
                resolve('200 OK');
            } else {
                arr[2] = [172800, 2];
                resolve('200 OK');
            }
        });
}

function test4 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.129278, 22.493949),
        function(status, result) {
            console.log("p4");
            if (status === 'complete') {
                arr[3] = [result.routes[0].time, 3];
                resolve('200 OK');
            } else {
                arr[3] = [172800, 3];
                resolve('200 OK');
            }
        });
}

function test5 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(113.943491, 22.279291),
        function(status, result) {
            console.log("p5");
            if (status === 'complete') {
                arr[4] = [result.routes[0].time, 4];
                resolve('200 OK');
            } else {
                arr[4] = [172800, 4];
                resolve('200 OK');
            }
        });
}

function test6 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.13936, 22.338407),
        function(status, result) {
            console.log("p6");
            if (status === 'complete') {
                arr[5] = [result.routes[0].time, 5];
                resolve('200 OK');
            } else {
                arr[5] = [172800, 5];
                resolve('200 OK');
            }
        });
}

function test7 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.046715, 22.442575),
        function(status, result) {
            if (status === 'complete') {
                arr[6] = [result.routes[0].time, 6];
                resolve('200 OK');
            } else {
                arr[6] = [172800, 6];
                resolve('200 OK');
            }
        });
}

function test8 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.206924, 22.376603),
        function(status, result) {
            if (status === 'complete') {
                arr[7] = [result.routes[0].time, 7];
                resolve('200 OK');
            } else {
                arr[7] = [172800, 7];
                resolve('200 OK');
            }
        });
}

function test9 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.241388, 22.267015),
        function(status, result) {
            if (status === 'complete') {
                arr[8] = [result.routes[0].time, 8];
                resolve('200 OK');
            } else {
                arr[8] = [172800, 8];
                resolve('200 OK');
            }
        });
}

function test10 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.179645, 22.306322),
        function(status, result) {
            if (status === 'complete') {
                arr[9] = [result.routes[0].time, 9];
                resolve('200 OK');
            } else {
                arr[9] = [172800, 9];
                resolve('200 OK');
            }
        });
}

function test11 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.136584, 22.267337),
        function(status, result) {
            if (status === 'complete') {
                arr[10] = [result.routes[0].time, 10];
                resolve('200 OK');
            } else {
                arr[10] = [172800, 10];
                resolve('200 OK');
            }
        });
}

function test12 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.18024, 22.273262),
        function(status, result) {
            if (status === 'complete') {
                arr[11] = [result.routes[0].time, 11];
                resolve('200 OK');
            } else {
                arr[11] = [172800, 11];
                resolve('200 OK');
            }
        });
}

function test13 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.036563, 22.205325), //testing
        function(status, result) {
            if (status === 'complete') {
                arr[12] = [result.routes[0].time, 12];
                resolve('200 OK');
            } else {
                arr[12] = [172800, 12];
                resolve('200 OK');
            }
        });
}

function test14 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.274649, 22.315452),
        function(status, result) {
            if (status === 'complete') {
                arr[13] = [result.routes[0].time, 13];
                resolve('200 OK');
            } else {
                arr[13] = [172800, 13];
                resolve('200 OK');
            }
        });
}

function test15 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(113.980978, 22.404644),
        function(status, result) {
            if (status === 'complete') {
                arr[14] = [result.routes[0].time, 14];
                resolve('200 OK');
            } else {
                arr[14] = [172800, 14];
                resolve('200 OK');
            }
        });
}

function test16 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.000665, 22.455541),
        function(status, result) {
            if (status === 'complete') {
                arr[15] = [result.routes[0].time, 15];
                resolve('200 OK');
            } else {
                arr[15] = [172800, 15];
                resolve('200 OK');
            }
        });
}

function test17 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.231792, 22.31996),
        function(status, result) {
            if (status === 'complete') {
                arr[16] = [result.routes[0].time, 16];
                resolve('200 OK');
            } else {
                arr[16] = [172800, 16];
                resolve('200 OK');
            }
        });
}

function test18 (resolve, reject) {
    driving.search(new AMap.LngLat(origin_point_x, origin_point_y),
        new AMap.LngLat(114.123793, 22.365811),
        function(status, result) {
            if (status === 'complete') {
                arr[17] = [result.routes[0].time, 17];
                resolve('200 OK');
            } else {
                arr[17] = [172800, 17];
                resolve('200 OK');
            }
        });
}

function help() {
    var obj=document.getElementById('panel');
    obj.innerHTML='';
    var drivingOption3 = {
        policy: AMap.DrivingPolicy.LEAST_TIME, // 其它policy参数请参考 https://lbs.amap.com/api/javascript-api/reference/route-search#m_DrivingPolicy
        ferry: 1, // 是否可以使用轮渡
        map: new AMap.Map("container", {
            center: [114.142744, 22.2801], //香港大学
            zoom: 14
        }),
        panel: 'panel'
    }

    index++;
    document.getElementById("lnglat").value = "Searching Now..."

    var driving3 = new AMap.Driving(drivingOption3);
    driving3.search(new AMap.LngLat(origin_point_x, origin_point_y), //港大 (114.142744, 22.2801) origin_point_x, origin_point_y
        new AMap.LngLat(x_di[arr[index][1]], y_di[arr[index][1]]), //红磡 (114.186686, 22.299936) x_di[arr[index][1]] y_di[arr[index][1]]
        function(status, result) {
            if (status === 'complete') {
                console.log("index222:");
                var num = (arr[index][0] / 60).toFixed(0);
                document.getElementById("res").value = hos_name.get(arr[index][1]) + " , " + num + "min";
                document.getElementById("lnglat").value = "Found!"
                console.log(index);
                console.log(arr[index][1]);
                console.log("OK");
            } else {
                console.log("Fk");
            }
        });
}

function help2() {
    var obj=document.getElementById('panel');
    obj.innerHTML='';
    var drivingOption3 = {
        policy: AMap.DrivingPolicy.LEAST_TIME, // 其它policy参数请参考 https://lbs.amap.com/api/javascript-api/reference/route-search#m_DrivingPolicy
        ferry: 1, // 是否可以使用轮渡
        map: new AMap.Map("container", {
            center: [114.142744, 22.2801], //香港大学
            zoom: 14
        }),
        panel: 'panel'
    }
    document.getElementById("lnglat").value = "Searching Now..."

    index--;

    var driving3 = new AMap.Driving(drivingOption3);
    driving3.search(new AMap.LngLat(origin_point_x, origin_point_y), //港大 (114.142744, 22.2801) origin_point_x, origin_point_y
        new AMap.LngLat(x_di[arr[index][1]], y_di[arr[index][1]]), //红磡 (114.186686, 22.299936) x_di[arr[index][1]] y_di[arr[index][1]]
        function(status, result) {
            if (status === 'complete') {
                var num = (arr[index][0] / 60).toFixed(0);
                document.getElementById("res").value = hos_name.get(arr[index][1]) + " , " + num + "min";
                document.getElementById("lnglat").value = "Found!"
                console.log("index222:");
                console.log(index);
                console.log(arr[index][1]);
                console.log("OK");
            } else {
                console.log("Fk");
            }
        });
}

function final_fun() {

    if(input_value == 0) {
        for(var i = 0; i < 18; i++) {
            arr[i][0] += final_wt[i];
        }
    }
    arr.sort((a,b) => a[0] - b[0]);

    var table = document.getElementById("tab1");//取得表格
    for(var j = 0; j < 3; j++) {
            var oTr=document.createElement('tr');//给该表格创建tr节点
            table.appendChild(oTr);//创建table的⼦节点tr

            var oTd=document.createElement('td');//创建td节点
            oTd.innerHTML=hos_name.get(arr[j][1]);//给创建的td节点赋值
            oTr.appendChild(oTd);//将创建的td交给oTr节点tr

            var oTd=document.createElement('td');//创建td节点
            oTd.innerHTML=(final_wt[arr[j][1]] / 60).toFixed(0);//给创建的td节点赋值
            oTr.appendChild(oTd);//将创建的td交给oTr节点tr

            var oTd=document.createElement('td');//创建td节点
            if(input_value == 0) {
                oTd.innerHTML=(arr[j][0] / 60).toFixed(0);//给创建的td节点赋值
            } else {
                oTd.innerHTML=((arr[j][0] + final_wt[arr[j][1]]) / 60).toFixed(0);//给创建的td节点赋值
            }
            oTr.appendChild(oTd);//将创建的td交给oTr节点tr
    }

    var driving2 = new AMap.Driving(drivingOption2);
    driving2.search(new AMap.LngLat(origin_point_x, origin_point_y), //港大 (114.142744, 22.2801)
        new AMap.LngLat(x_di[arr[0][1]], y_di[arr[0][1]]), //红磡 (114.186686, 22.299936)
        function(status, result) {
            if (status === 'complete') {
                var num = (arr[index][0] / 60).toFixed(0);
                document.getElementById("res").value = hos_name.get(arr[index][1]) + " , " + num + "min";
                document.getElementById("lnglat").value = "Found!"
            } else {
                console.log("Fk");
            }
        });
}

function deal_time (str) {
    var temp = str.split(" ");
    var s1 = temp[0];
    var s2 = temp[1];
    var num2 = parseInt(s2);

    if(s1 == "Over") {
        return (num2 + 0.5) * 3600;
    } else {
        return num2 * 3600;
    }
}

function parse_Json () {
    for(var i = 0; i < 18; i++) {
        final_wt[i] = deal_time(waiting_time[i].topWait);
    }
}

function read_Json (resolve, reject){
    fetch('static/cur.json').then(response => {
        return response.json();
    }).then(data => {
        // Work with JSON data here
        waiting_time = data.waitTime;
        parse_Json();
        resolve("OKOK");

    }).catch(err => {
        // Do something for an error here
        console.log("error");
    });
}

var p_click = new Promise(clickMap);


p_click.then(function () {
        var p1 = new Promise(test);
        var p2 = new Promise(test2);
        var p3 = new Promise(test3);
        var p4 = new Promise(test4);
        var p5 = new Promise(test5);
        var p6 = new Promise(test6);
        var p7 = new Promise(test7);
        var p8 = new Promise(test8);
        var p9 = new Promise(test9);
        var p10 = new Promise(test10);
        var p11 = new Promise(test11);
        var p12 = new Promise(test12);
        var p13 = new Promise(test13);
        var p14 = new Promise(test14);
        var p15 = new Promise(test15);
        var p16 = new Promise(test16);
        var p17 = new Promise(test17);
        var p18 = new Promise(test18);

        var p_read = new Promise(read_Json);
        Promise.all([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,
        p12,p13,p14,p15,p16,p17,p18, p_read]).then( function(){
                final_fun();
        }
        );
    }
    );
