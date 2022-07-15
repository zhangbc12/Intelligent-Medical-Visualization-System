var origin_lng;
var origin_lat;
var lnglat_str = document.getElementById("lnglat").value;

if (lnglat_str !== "") {
    var splited = lnglat_str.split(",");
    origin_lng = parseFloat(splited[0]);
    origin_lat = parseFloat(splited[1]);
}
else {
    origin_lng = 114.142744;
    origin_lat = 22.2801;
}

var map = new AMap.Map('container', {
    resizeEnable: true, //是否监控地图容器尺寸变化
    zoom:14, //初始化地图层级
    center: [origin_lng, origin_lat] //初始化地图中心点
});

map.on('click', function(e) {
    if (e !== "") {
        origin_lng = e.lnglat.getLng();
        origin_lat = e.lnglat.getLat();
    }

    map.remove(origin);

    origin = new AMap.Marker({
        position: [parseFloat(origin_lng), parseFloat(origin_lat)],   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
        title: "Origin"
    });

    // origin.position = [parseFloat(origin_lng), parseFloat(origin_lat)]
    map.add(origin)
    document.getElementById("lnglat").value = e.lnglat.getLng() + ',' + e.lnglat.getLat()
});


origin = new AMap.Marker({
    position: [origin_lng, origin_lat],
    title: "Origin",
});
map.add(origin)

var walking = new AMap.Walking(
    {
        map: map,
        panal: "panal"
    }
);

// var idx = 0;
// var marker_list = [];
//
// function add_marker(lng, lat) {
//     marker_list[idx].position = [lng, lat]
//     idx++;
// }

function visualize_markers(markers) {
    console.log(markers)
    markers.forEach(function(marker) {
        new AMap.Marker({
            map: map,
            position: [marker[0], marker[1]],
        });
    });
    map.setFitView();
}

function walk_helper(lng, lat) {
    walking.search([origin_lng, origin_lat], [parseFloat(lng), parseFloat(lat)]);
}
