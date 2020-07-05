
// 清除绘图 按钮点击事件
$(document).on('click',"#clearPolyline",function(){
	map.clearOverlays();
	$('#voImg').attr('src', "../static/res/Figure1.png");
})

// 测试动态更新VO图 点击事件
$(document).on('click',"#testDynamicImg",function(){
	updateVoImg("1000010086312797");
})

// 获取最新仿真树
$(document).on("click","#getSimTree",function(){
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
})

// 动画功能
function animation(SimData) {
	let timeOut = 400;
	let pointSize = 100;
	let shipVOImg = new Array(); // 用于保存主船的VOImdID

	for(let moment=0; moment<SimData.length-1; moment++){
		if (SimData[moment][0].VOImgID){
			shipVOImg.push(SimData[moment][0].VOImgID);
		}else{
			shipVOImg.push('figure');
		}
	}

	for(let moment=0; moment<SimData.length-1; moment++){
		let fromInfo = SimData[moment];
		let toInfo = SimData[moment+1];
		let shipNum = fromInfo.length;
		if (shipNum > 0) {
			let shipPointList = [];
			let rotationList = [];
			for(let ship = 0;ship< shipNum;ship++) {
				let lonStep = (toInfo[ship].lon - fromInfo[ship].lon) / pointSize;
				let latStep = (toInfo[ship].lat - fromInfo[ship].lat) / pointSize;
				let pointList = [];
				let rotation = toInfo[ship].heading;
				rotationList.push(rotation);
				for (let i = 0; i < pointSize; i++) {
					let p = new BMap.Point(fromInfo[ship].lon + i * lonStep, fromInfo[ship].lat + i * latStep);
					pointList.push(p);
				}
				shipPointList.push(pointList);
			}
			for(let i=0;i<pointSize-1;i++){
				for(let ship = 0;ship< shipNum;ship++) {
					(function(ship,pointList,timeOut,i,rotation){
					setTimeout(()=>{
						moveShip(ship,pointList[i + 1],rotation);
						my_add_polyline([pointList[i], pointList[i + 1]]);
					},timeOut);
				})(ship,shipPointList[ship],timeOut,i,rotationList[ship])
				}
			}
			updateVoImg(shipVOImg[moment]);
	}
	}
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
			alert("error");
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
			let SimData = data.SimData;
			let deciResult = data.DeciResult;
			let vmid = data.VMID;
			/*----------弹窗数据-------------------*/
			$("body").translucent({
				titleGroundColor:"#5396BA",
				backgroundColor:"#ffffff",
				titleFontColor:"#ffffff",
				titleFontSize:14,
				titleText:vmid,
				opacity:1,
				zIndex:100,
				textHtml:'<div><span style="color:sandybrown">是否汇遇：</span><span id="met" style="color:green"></span></div>'+
					     '<div><span style="color:sandybrown">是否决策：</span><span id="deci" style="color:green"></span></div>'+
					     '<div><span style="color:sandybrown">GoHead：</span><span id="GoHead" style="color:green"></span></div>'+
						 '<div><span style="color:sandybrown">TurnLeft：</span><span id="TurnLeft" style="color:green"></span></div>'+
						 '<div><span style="color:sandybrown">TurnRight：</span><span id="TurnRight" style="color:green"></span></div>'+
					     '<div><span style="color:sandybrown">PrAlert：</span><span id="prAlert" style="color:green"></span></div>'+
				   		 '<div><span style="color:sandybrown">RiskCurrent：</span><span id="RiskCurrent" style="color:green"></span></div>'+
						 '<div><span style="color:sandybrown">RiskThreshold：</span><span id="RiskThreshold" style="color:green"></span></div>',
				close:function ($dom) {
//	            	alert("确定要关闭吗？")
				}
			});
			if(0 === deciResult.MET){
				$("#met").text("未相遇");
			}else if(1 === deciResult.MET){
				$("#met").text("相遇");
			}

			if(1 === deciResult.FLAG){
				$("#deci").text("已决策");
				$("#GoHead").text(deciResult.GoHead);
				$("#TurnLeft").text(deciResult.TurnLeft);
				$("#TurnRight").text(deciResult.TurnRight);
			}else{
				$("#deci").text("未决策");
				$("#GoHead").text(0);
				$("#TurnLeft").text(0);
				$("#TurnRight").text(0);
			}

			$("#prAlert").text(deciResult.message.PrAlert);
			$("#RiskCurrent").text(deciResult.message.RiskCurrent);
			$("#RiskThreshold").text(deciResult.message.RiskThreshold);
			/*--------------折线图数据------------------*/
			for(let i = 0;i<SimData.length;i++){
				let node = {}
				node.time = SimData[i][0].time
				node.DCPA = SimData[i][0].DCPA
				node.TCPA = SimData[i][0].TCPA
				allnode.push(node)
			}
			let timeList = [],dcpaList = [],tcpaList = [];

			for(let l=0;l<allnode.length;l++){
				dcpaList.push(allnode[l].DCPA)
				tcpaList.push(allnode[l].TCPA)
				timeList.push(allnode[l].time)
			}

			dcpaOption.xAxis.data = timeList
			dcpaOption.series[0].data = dcpaList
			tcpaOption.xAxis.data = timeList
			tcpaOption.series[0].data = tcpaList
			dcpa_chart.setOption(dcpaOption)
			tcpa_chart.setOption(tcpaOption)
			animation(SimData);
		},
		error:function(xhr,type,errorThrown){
			console.log(error)
		}
	});
}