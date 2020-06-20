let ec_tree,dtpa_chart;
let nodeList1 = [],nodeList2 = [];
let allnode = [nodeList1,nodeList2];

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
	let dtpa = doc.getElementById('dtpa');
	dtpa_chart = echarts.init(dtpa);
	dtpa_chart.setOption(option);
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
		left: '10%',
		bottom: '5%',
		right: '10%',
		symbol: 'emptyCircle' ,
		symbolSize: 14,

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

		},

		leaves: {
			label: {
				position: 'right',
				verticalAlign: 'middle',
				align: 'left'
			}
		},

		expandAndCollapse: false,
		initialTreeDepth: 5,
		animationDuration: 550,
		animationDurationUpdate: 750
	}]
}

let option = {
    title: {
        text: '折线图'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['DCPA1', 'TCPA1','DCPA2', 'TCPA2']
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
            name: 'DCPA1',
            type: 'line',
			smooth: true,
			data: []
        },
        {
            name: 'TCPA1',
            type: 'line',
			smooth: true,
			data: []
        },
		 {
            name: 'DCPA2',
            type: 'line',
			smooth: true,
			data: []
        },
        {
            name: 'TCPA2',
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





