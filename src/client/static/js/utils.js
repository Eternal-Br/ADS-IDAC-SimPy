// Echarts树 结点点击事件
ec_tree.on('click', function (params) {
    // 控制台打印数据的名称
    // alert("value:"+params.value + " dataIndex:"+params.dataIndex+"\nseriesIndex:"+params.seriesIndex+" seriesName:"+ params.seriesName );
	// , params.seriesIndex, params.seriesName
	$('#dataId').attr('value', params.value);
	var vmid = params.value;
	// var vmid = "2004022208011387";
	getVMData(vmid);
	
	// getVMData(vmid, function(err, data){
	// 	console.log("VMData callback 测试: ", data);
		
	// });
	
	// console.log("测试调用之后VMData: ", mysimdata);
	// draw_dynamic_polyLine(VMData);
});


// // 切换为英文 按钮点击事件
// $("#S2E").click(function(event) {
// 	window.location.href="/en_version"
// });
// // 切换为中文 按钮点击事件
// $("#S2Z").click(function(event) {

// });

// 清除绘图 按钮点击事件
$("#clearPolyline").click(function(event) {
	// alert("clear polyline")
	map.clearOverlays();
});

// 测试动态更新VO图 点击事件
$("#testDynamicImg").click(function(event) {
	updateVoImg("1000010086312797");
	// 方式2 Ajax方式
	// $.ajax('', {
	// 	url: "/testS2F/1000010086312797",
	// 	success:function(data){
	// 		console.log("data: ", data)
	// 		$('#voImg').attr('src', "data:image/png;base64,"+data);
	// 	},
	// 	error:function(xhr,type,errorThrown){
	// 		alert(error);
	// 	}
	// });
});

// 获取最新仿真树
$("#getSimTree").click(function(event) {
	// 先清理掉当前的绘图PolyLine
	map.clearOverlays();
	// var treeid = "Tree2004022208017821";
	// var treeid = "Tree2004022316511498";
	// treeUrl = "/tree/" + treeid;
	lastestTreeUrl = "/tree/lastest";
	$.ajax('', {
		url: lastestTreeUrl,
		dataType:"json",
		success:function(data){
			ec_tree_option.series[0].data = data.TREEData.data;
			ec_tree.setOption(ec_tree_option);
			// 将TREEID填写到treeId输入框中
			$('#treeId').attr('value', data.TREEID);
		},
		error:function(xhr,type,errorThrown){
			alert(error);
		}
	});
});

// 绘制动态绘制polyLine 按钮点击事件
// $("#drawPolyline").click(function(event) {
	// var pois = [
	// 	new BMap.Point(122.326654, 31.110672),
	// 	new BMap.Point(122.216654, 31.110672),
	// 	new BMap.Point(122.146654, 31.210672),
	// 	new BMap.Point(122.426654, 31.260672),
	// ];
	// var pois = get_pois();

	// my_add_polyline(pois);
	// setTimeout(function(){
	// 	my_add_polyline(pois2);
	// 	setTimeout(function(){
	// 		my_add_polyline(pois3);
	// 	}, 1000);
	// }, 1000);

// 	draw_dynamic_polyLine(pois);
// });

// 获取用于绘制polyLine的数据集合（数组）
// function get_pois(){
// 	return ([[
// 		new BMap.Point(122.326654, 31.110672),
// 		new BMap.Point(122.216654, 31.110672),
// 		new BMap.Point(122.146654, 31.210672),
// 		new BMap.Point(122.426654, 31.260672),
// 	],[
// 		new BMap.Point(122.226654, 31.210672),
// 		new BMap.Point(122.316654, 31.210672),
// 		new BMap.Point(122.346654, 31.310672),
// 		new BMap.Point(122.226654, 31.260672),
// 	]]);
// }

// 动态绘制polyLine功能函数
// 目前的是绘制两条船
//感谢杨总 倾情相助
function draw_dynamic_polyLine(pois, Voarr) {
	// 首先将初始位置的点添加进去
	// console.log('Voarr传入参数测试：', Voarr);
	my_add_polyline([pois[0][0], pois[0][1]]);
	my_add_polyline([pois[1][0], pois[1][1]]);
	updateVoImg(Voarr[0])
	// console.log(0, pois[0][0], pois[0][1]);
	var lineDataIndex = 1;
	if (pois[0].length > 0) {
		var intervalId = setInterval(() => {
			if (lineDataIndex == pois[0].length - 1) {
				clearInterval(intervalId);
				// console.log("this is clearInterval.");
			}
			if (lineDataIndex < pois[0].length - 1) {
				my_add_polyline([pois[0][lineDataIndex], pois[0][lineDataIndex + 1]]);
				my_add_polyline([pois[1][lineDataIndex], pois[1][lineDataIndex + 1]]);
				updateVoImg(Voarr[lineDataIndex])
				// console.log(lineDataIndex, pois[0][lineDataIndex], pois[0][lineDataIndex + 1]);
			}
			lineDataIndex++;
		}, 500);
	}
	updateVoImg(Voarr[pois[0].length-1])
}

// 更新VO图功能函数
function updateVoImg(imgName){
	console.log("imgName: ", imgName)
	// imgName: String
	// imgUrl = "/img/"+ imgName.toString();
	
	// TODO: 有毒！！！
	// imgUrl = "/vm/2004071252277034";
	imgUrl = "/img/"+ imgName;
	// 方式1：DOM操作img 属性
	// $('#voImg').attr('src', imgUrl);
	
	// 方式2 Ajax方式
	$.ajax('', {
		url: imgUrl,
		success:function(data){
			// console.log("前端调用测试data:", data)
			$('#voImg').attr('src', "data:image/png;base64,"+data);
		},
		error:function(xhr,type,errorThrown){
			alert(error);
		}
	});
}

// 输入VMID，绘制PolyLine
function getVMData(VMID){
	vmUrl = "/vm/" + VMID.toString();
	$.ajax('', {
		url: vmUrl,
		dataType:"json",
		success:function(data){
			var SimData = data.SimData;
			var shipPos = new Array();
			// console.log("VMData 测试: ", SimData)
			var shipNum = data.SimData[0].length; // 当前虚拟机中船的数量，由于每组中数据的量和格式是一致的，只需要解读第0组即可
			var shipVOImg = new Array(); // 用于保存主船的VOImdID
			// 下面初始化用于绘制PolyLine的array
			for (var i=0; i<shipNum; i++){ 
				shipPos.push(new Array());
				// shipPos[i] 用于记录第i条船的坐标序列
			}
			// console.log('shipPos: ', shipPos)
			for(var moment=0; moment<SimData.length; moment++){ 
				if (SimData[moment][0].VOImgID){
					shipVOImg.push(SimData[moment][0].VOImgID);
				}
				else{
					shipVOImg.push('figure');
				}
				for(var ship=0; ship<SimData[moment].length; ship++){
					shipPos[ship].push(new BMap.Point(SimData[moment][ship].lon, SimData[moment][ship].lat));
					// console.log("lon, lat", SimData[moment][ship].lon, SimData[moment][ship].lat)
				}
			}
			// 从这里开始已经处理好数据，shipPos里面就是可以直接绘制PolyLine的数据了
			// console.log('测试return shipPos: ', shipPos);
			var f = function(){
				return draw_dynamic_polyLine(shipPos, shipVOImg);
			}
			f();
			// return shipPos;
		},
		error:function(xhr,type,errorThrown){
			console.log(error)
			// return [];
			// alert(error);
		}
	});
}