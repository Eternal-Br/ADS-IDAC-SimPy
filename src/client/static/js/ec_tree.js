var ec_tree = echarts.init(document.getElementById('tree'),);


// 鼠标点击事件放在utiLs.js中
var mydata = [{
	'name': 'root',
	'value': 10086,
}]

var ec_tree_option = {
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

// setInterval(get_tree, 4000)
get_tree()

