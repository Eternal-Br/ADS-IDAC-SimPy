// 百度地图API功能
let map,ship1,ship2;

$(function(){
	map = new BMap.Map("map"); // 创建Map实例
	map.centerAndZoom(new BMap.Point(123.06, 31), 14); // 初始化地图,设置中心点坐标和地图级别
	map.enableScrollWheelZoom(true); //开启鼠标滚轮缩放
    let shipIcon1 = new BMap.Icon("/static/res/ship/freighter_min.png", new BMap.Size(150, 25));
    ship1 = new BMap.Marker(new BMap.Point(0, 0),{icon:shipIcon1});
    map.addOverlay(ship1);

    let shipIcon2 = new BMap.Icon("/static/res/ship/freighter2_min.png", new BMap.Size(105, 25));
    ship2 = new BMap.Marker(new BMap.Point(0, 0),{icon:shipIcon2});
    map.addOverlay(ship2);
})

function my_add_polyline(pois){
	let polyline = new BMap.Polyline(pois, {
		strokeColor:"blue",
		strokeWeight: '1', //折线的宽度，以像素为单位
		strokeOpacity: 0.8, //折线的透明度，取值范围0 - 1
	});
	map.addOverlay(polyline); //增加折线
}

function moveShip(shipNum,point,rotation){
    if(null === ship1.Bc &&  null === ship2.Bc){
        init();
    }
	if(0=== shipNum){
		ship1.setPosition(point);
		ship1.setRotation(rotation-90);
	}else if(1=== shipNum){
		ship2.setPosition(point);
		ship2.setRotation(rotation-90);
	}

}
