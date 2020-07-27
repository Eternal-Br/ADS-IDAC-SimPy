let ec_tree,dcpa_chart,tcpa_chart,allnode = [];

$(function(){
	let _iframe = window.parent;
	let _div =_iframe.document.getElementById('main');
	let doc = _div.contentWindow.document;
	let tr = doc.getElementById('tree');
	ec_tree = echarts.init(tr);
	get_tree();
	// Echarts树 结点点击事件
	ec_tree.on('click', function (params) {
		// 控制台打印数据的名称
		$('#dataId').attr('value', params.value);
		var vmid = params.value;
		// var vmid = "2004022208011387";
		getVMData(vmid);
	});
	// let dcpa = doc.getElementById('dcpa');
	// let tcpa = doc.getElementById('tcpa');
	// dcpa_chart = echarts.init(dcpa);
	// dcpa_chart.setOption(dcpaOption);
	// tcpa_chart = echarts.init(tcpa);
	// tcpa_chart.setOption(tcpaOption);
})

// 鼠标点击事件放在utiLs.js中
let mydata = [{
	'name': 'root',
	'value': 10086,
}]

let ec_tree_option = {
	tooltip: {
		trigger: 'item',
		triggerOn: 'mousemove',
		formatter: '{c}', // 字符串模板
	},
	series: [{
		type: 'tree',
		data: mydata,
		top: '5%',
		left: '25%',
		bottom: '5%',
		right: '30%',
		symbol: 'emptyCircle' ,
		symbolSize: 14,
        edgeShape: 'polyline',

		label: {
			show: true,
			position: 'top',
			verticalAlign: 'middle',
			align: 'right',
			fontSize: 16,
			formatter: '{c}', // 字符串模板
		},
		lineStyle: {
			color: "'#838300'",
			width: 1.5,
            curveness: 0.8,

		},

		leaves: {
			label: {
				position: 'right',
				verticalAlign: 'middle',
				align: 'left'
			}
		},

		expandAndCollapse: true,
		initialTreeDepth: 5,
		animationDuration: 550,
		animationDurationUpdate: 750
	}]
}

let dcpaOption = {
    title: {
        text: '折线图'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['DCPA']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'DCPA',
            type: 'line',
			smooth: true,
			data: []
        }
    ]
};

let tcpaOption = {
    title: {
        text: '折线图'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['TCPA']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: 'TCPA',
            type: 'line',
			smooth: true,
			data: []
        }
    ]
};

function get_tree(){
	$.ajax('', {
		url: "/tree",
		success:function(data){
			ec_tree_option.series[0].data = data.data
			ec_tree.setOption(ec_tree_option)
		},
		error:function(xhr,type,errorThrown){

		}
	});
}





