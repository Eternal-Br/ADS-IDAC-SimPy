// 百度地图API功能
var map = new BMap.Map("map"); // 创建Map实例
map.centerAndZoom(new BMap.Point(123.06, 31), 14); // 初始化地图,设置中心点坐标和地图级别
map.enableScrollWheelZoom(true); //开启鼠标滚轮缩放
// var sy = new BMap.Symbol(BMap_Symbol_SHAPE_BACKWARD_OPEN_ARROW, {
// 	scale: 0.6, //图标缩放大小
// 	strokeColor: '#fff', //设置矢量图标的线填充颜色
// 	strokeWeight: '2', //设置线宽
// });
// var icons = new BMap.IconSequence(sy, '10', '30');
// 创建polyline对象
// var pois = [
// 	new BMap.Point(122.226654, 31.210672),
// 	new BMap.Point(122.116654, 31.310672),
// 	new BMap.Point(122.546654, 31.510672),
// 	new BMap.Point(122.226654, 31.410672),
// ];
// var polyline = new BMap.Polyline(pois, {
// 	enableEditing: false, //是否启用线编辑，默认为false
// 	enableClicking: true, //是否响应点击事件，默认为true
// 	icons: [icons],
// 	// icons: new BMap.IconSequence(sy, '10', '30'),
// 	strokeWeight: '8', //折线的宽度，以像素为单位
// 	strokeOpacity: 0.8, //折线的透明度，取值范围0 - 1
// 	strokeColor: "#18a45b" //折线颜色
// });


// map.addOverlay(polyline); //增加折线

function my_add_polyline(pois){
	// 测试随机颜色
	// var getRandomColor = function(){
	//     return ('#'+('00000'+(Math.random()*0x1000000<<0).toString(16)).slice(-6));
	// 	// console.log(getRandomColor);
	//  }
	 // 测试失败
	 
	var sy = new BMap.Symbol(BMap_Symbol_SHAPE_BACKWARD_OPEN_ARROW, {
		scale: 0.6, //图标缩放大小
		strokeColor: '#fff', //设置矢量图标的线填充颜色
		strokeWeight: '2', //设置线宽
	});
	var icons = new BMap.IconSequence(sy, '10', '30');
	var polyline = new BMap.Polyline(pois, {
		enableEditing: false, //是否启用线编辑，默认为false
		enableClicking: true, //是否响应点击事件，默认为true
		icons: [icons],
		// icons: new BMap.IconSequence(sy, '10', '30'),
		strokeWeight: '8', //折线的宽度，以像素为单位
		strokeOpacity: 0.8, //折线的透明度，取值范围0 - 1
		strokeColor: "#18a45b" //折线颜色
	});
	map.addOverlay(polyline); //增加折线
}

// function my_add_polyline(function(pois){
	
// })


// my_add_polyline(pois)
// 假设数据格式为 ：
// data = {"data": [(d1, d2), (d3, d4)]}
// var data = {
// 	"data": [{
// 		"lon": 122.226654,
// 		"lat": 31.210672
// 	}, {
// 		"lon": 122.226654,
// 		"lat": 31.210672
// 	}]
// }

// function get_my_map_data() {
// 	map.removeOverlay(polyline); // 移除旧的ployline
// 	// map.clearOverlays()
// 	$.ajax('', {
// 		url: "/map",
// 		success: function(data) {
// 			// console.log(data)
// 			var pois = [];
// 			for (var i = 0; i < data.data.length; i++) {
// 				//TODO
// 				var point = new BMap.Point(data.data[i].lon, data.data[i].lat);
// 				// var point = new BMap.Point(data[i][lon], data[i][lat]);
// 				pois.push(point);
// 			}
			
// 			var polyline = new BMap.Polyline(pois, {
// 				enableEditing: false, //是否启用线编辑，默认为false
// 				enableClicking: true, //是否响应点击事件，默认为true
// 				icons: [icons],
// 				strokeWeight: '8', //折线的宽度，以像素为单位
// 				strokeOpacity: 0.8, //折线的透明度，取值范围0 - 1
// 				strokeColor: "#18a45b" //折线颜色
// 			});
			
// 			// 此处得到新的polyline
// 			// 这里有问题
// 			map.addOverlay(polyline)

// 		},
// 		error: function(xhr, type, errorThrown) {
			
// 		}
// 	});
// }

// setInterval(get_my_map_data, 4000)