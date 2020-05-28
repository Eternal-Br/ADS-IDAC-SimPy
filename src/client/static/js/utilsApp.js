// Echarts树 结点点击事件
ec_tree.on('click', function (params) {
	$('#dataId').attr('value', params.value);
	var vmid = params.value;
	getVMData(vmid);
});
// 清除绘图 按钮点击事件
$("#clearPolyline").click(function(event) {
	// alert("clear polyline")
	map.clearOverlays();
});
// 测试动态更新VO图 点击事件
$("#testDynamicImg").click(function(event) {
	updateVoImg("1000010086312797");
});

// 获取最新仿真树
$("#getSimTree").click(function(event) {
	// 先清理掉当前的绘图PolyLine
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

// 输入VMID，绘制PolyLine
function getVMData(VMID){
	vmUrl = "/vm/" + VMID.toString();
	$.ajax('', {
		url: vmUrl,
		dataType:"json",
		success:function(data){
//			let SimData = data.SimData;
			let SimData = [[{
					heading: 45,
					interval: 100,
					lat: 200,
					lon: 0,
					shipid: "10086",
					speed: 7,
					time: 0
			},{
					heading: 0,
					interval: 100,
					lat: 100,
					lon: 0,
					shipid: "10086",
					speed: 7,
					time: 0
			}],[{
					heading: 45,
					interval: 100,
					lat: 140,
					lon: 60,
					shipid: "10086",
					speed: 7,
					time: 0
			},{
					heading: 0,
					interval: 100,
					lat: 100,
					lon: 60,
					shipid: "10086",
					speed: 7,
					time: 0
			}],[{
					heading: 45,
					interval: 100,
					lat: 80,
					lon: 120,
					shipid: "10086",
					speed: 7,
					time: 0
			},{
					heading: 0,
					interval: 100,
					lat: 100,
					lon: 120,
					shipid: "10086",
					speed: 7,
					time: 0
			}]]
			if(null != SimData && SimData.length > 1){
			    let shipPositionList = [];
			    for(let i = 0;i < SimData[0].length;i++){
			        // let x = -transLon(SimData[0][i].lon,SimData[0][i].lat);
					// let y = -transLat(SimData[0][i].lat);
					let x = SimData[0][i].lon;
					let y = SimData[0][i].lat;
			        let rot = -Math.cos(SimData[0][i].heading);
			        let shipPosition = new ShipPosition(x,y,rot);
                    shipPositionList.push(shipPosition)
                }
			    initShip(shipPositionList);

			    for(let j= 0; j< SimData.length; j++){
			    	let moveInfoList = [];
			    	for(let k = 0 ; k< SimData[j].length;k++){
			    		// let x = -transLon(SimData[j][k].lon,SimData[j][k].lat);
			        	// let y = -transLat(SimData[j][k].lat);
						let x = SimData[j][k].lon;
						let y = SimData[j][k].lat;
			        	let rot = -Math.cos(SimData[j][k].heading);
			        	if(j+1 < SimData.length){
			        		// let tx = -transLon(SimData[j+1][k].lon,SimData[j+1][k].lat)
							// let ty = -transLat(SimData[j+1][k].lat);
							let tx = SimData[j+1][k].lon;
							let ty = SimData[j+1][k].lat;
			        		let moveInfo = new MoveInfo(x,y,rot,tx,ty,1,-1);
							moveInfoList.push(moveInfo);
						}
					}
			    	updateMoveInfo(moveInfoList);
				}

            }
		},
		error:function(xhr,type,errorThrown){
			console.log(error)
		}
	});
}

function MoveInfo(locationX,locationY,picRotation,targetX,targetY,speedX,speedY){
    this.locationX = locationX;
    this.locationY = locationY;
    this.picRotation = picRotation;
    this.targetX = targetX;
    this.targetY = targetY;
    this.speedX = speedX;
    this.speedY = speedY;
}

//船舶数据类型,用于船舶位置加载
function ShipPosition(xPosition,yPosition,shipRotation){
    this.shipRotation = shipRotation;
    this.xPosition = xPosition;
    this.yPosition = yPosition;
}

function transLon(gc_lon,gc_lat){
	let min_x = 11705648;
	let zoom_rate = 5.5;
	let DeltaMeter =gc_lon * 111 * Math.cos(gc_lat * Math.PI / 180) * 1000;
	let resultX = (DeltaMeter - min_x) / zoom_rate;
	return resultX;
}

function transLat(gc_lat){
	let min_y = 3444255 ;
	let zoom_rate = 5.5;
    let DeltaMeter = gc_lat * 111120 ;
	let resultY = (DeltaMeter - min_y) / zoom_rate;
	return resultY;
}