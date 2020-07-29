let rudderAngleGuage,speedGuage,guage3Guage;

$(function(){
    rudderAngleGuage = echarts.init(document.getElementById('rudderAngle'));
    rudderAngleGuage.setOption(rudderAngleOption);
    speedGuage = echarts.init(document.getElementById('speed'));
    speedGuage.setOption(speedOption);
    guage3Guage = echarts.init(document.getElementById('guage3'));
    guage3Guage.setOption(guage3Option);
})
let rudderAngleOption = {
   // title: {
   //      textStyle: {
   //          fontWeight: "normal",
   //          color: "#fff",
   //          fontSize: 14
   //      },
   //      text: '舵角', //标题文本内容
   //  },
    backgroundColor: '#1b1b1b',
    tooltip: {
        formatter: '{a} <br/>{c} {b}'
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            // restore: {show: true},
            // saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '速度',
            type: 'gauge',
            min: -35,
            max: 35,
            splitNumber: 14,
            radius: '90%',
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[0.2, 'lime'], [0.8, '#1e90ff'], [1, '#ff4500']],
                    width: 1,
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {            // 坐标轴小标记
                fontWeight: 'bolder',
                color: '#fff',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            },
            splitLine : { //分割线样式（及10、20等长线样式）
                length : 7,
                lineStyle : { // 属性lineStyle控制线条样式
                    width : 2
                }
            },
            axisTick : { //刻度线样式（及短线样式）
                length : 4
            },
            axisLabel : { //文字样式
                color : "white",
                distance : 5 //文字离表盘的距离
            },
            pointer: {           // 分隔线
                shadowColor: '#fff', //默认透明
                shadowBlur: 5
            },
            title: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontSize: 8,
                    fontStyle: 'italic',
                    color: '#fff',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 8
                }
            },
            data: [{value: 0, name: '舵角/度'}]
        }
    ]
};
let speedOption = {
    // title: {
    //     textStyle: {
    //         fontWeight: "normal",
    //         color: "#fff",
    //         fontSize: 14
    //     },
    //     text: '速度', //标题文本内容
    // },
    backgroundColor: '#1b1b1b',
    tooltip: {
        formatter: '{a} <br/>{c} {b}'
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            // restore: {show: true},
            // saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '速度',
            type: 'gauge',
            min: 0,
            max: 25,
            splitNumber: 5,
            radius: '90%',
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[0.2, 'lime'], [0.8, '#1e90ff'], [1, '#ff4500']],
                    width: 1,
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {            // 坐标轴小标记
                fontWeight: 'bolder',
                color: '#fff',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            },
            splitLine : { //分割线样式（及10、20等长线样式）
                length : 7,
                lineStyle : { // 属性lineStyle控制线条样式
                    width : 2
                }
            },
            axisTick : { //刻度线样式（及短线样式）
                length : 4
            },
            axisLabel : { //文字样式
                color : "white",
                distance : 5 //文字离表盘的距离
            },
            pointer: {           // 分隔线
                shadowColor: '#fff', //默认透明
                shadowBlur: 5
            },
            title: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontSize: 8,
                    fontStyle: 'italic',
                    color: '#fff',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 8
                }
            },
            data: [{value: 0, name: '海里/h'}]
        }
    ]
};
let guage3Option = {
    // title: {
    //     textStyle: {
    //         fontWeight: "normal",
    //         color: "#fff",
    //         fontSize: 14
    //     },
    //     text: 'DCPA/RISK/TCPA', //标题文本内容
    // },
    backgroundColor: '',
    tooltip: {
        formatter: '{a} <br/>{c} {b}'
    },
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            // restore: {show: true},
            // saveAsImage: {show: true}
        }
    },
    series: [
        {
            name: '风险',
            type: 'gauge',
            min: 0,
            max: 1,
            splitNumber: 10,
            radius: '80%',
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[0.2, 'lime'], [0.8, '#1e90ff'], [1, '#ff4500']],
                    width: 1,
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {            // 坐标轴小标记
                fontWeight: 'bolder',
                color: '#FFA500',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            },
            splitLine : { //分割线样式（及10、20等长线样式）
                color: '#FFA500',
                length : 7,
                lineStyle : { // 属性lineStyle控制线条样式
                    color: '#FFA500',
                    width : 2
                }
            },
            axisTick : { //刻度线样式（及短线样式）
                color: '#FFA500',
                length : 4
            },
            axisLabel : { //文字样式
                color : "#FFA500",
                distance : 5 //文字离表盘的距离
            },
            pointer: {           // 分隔线
                shadowColor: '#FFA500', //默认透明
                shadowBlur: 5
            },
            title: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontSize: 8,
                    fontStyle: 'italic',
                    color: '#FFA500',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 8
                }
            },
            data: [{value: 0, name: 'RISK'}]
        },
        {
            name: 'DCPA',
            type: 'gauge',
            center: ['18%', '50%'],    // 默认全局居中
            radius: '60%',
            min: 0,
            max: 10,
            endAngle: 45,
            splitNumber: 10,
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[0.29, '#ff4500'], [0.86, '#1e90ff'], [1, 'lime']],
                    width: 2,
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {            // 坐标轴小标记
                fontWeight: 'bolder',
                color: '#FFA500',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            },
            splitLine : { //分割线样式（长线样式）
                color: '#FFA500',
                length : 7,
                lineStyle : { // 属性lineStyle控制线条样式
                    color: '#FFA500',
                    width : 2
                }
            },
            axisTick : { //刻度线样式（及短线样式）
                color: '#FFA500',
                length : 4
            },
            axisLabel : { //文字样式
                color : "#FFA500",
                distance : 5 //文字离表盘的距离
            },
            pointer: {
                width: 5,
                shadowColor: '#fff', //默认透明
                shadowBlur: 5
            },
            title: {
                offsetCenter: [0, '-30%'],       // x, y，单位px
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontStyle: 'italic',
                    fontSize: 8,
                    color: '#FFA500',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            data: [{value: 0, name: 'DCPA/nm'}]
        },
        {
            name: 'TCPA',
            type: 'gauge',
            center: ['83%', '50%'],    // 默认全局居中
            radius: '60%',
            min: 0,
            max: 10,
            startAngle:145,
            splitNumber: 10,
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[0.2,'#ff4500'], [0.8, '#1e90ff'],[1,'lime']],
                    width: 2,
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {            // 坐标轴小标记
                fontWeight: 'bolder',
                color: '#FFA500',
                shadowColor: '#fff', //默认透明
                shadowBlur: 10
            },
            splitLine : { //分割线样式（及长线样式）
                color: '#FFA500',
                length : 7,
                lineStyle : { // 属性lineStyle控制线条样式
                    color: '#FFA500',
                    width : 2
                }
            },
            axisTick : { //刻度线样式（及短线样式）
                color: '#FFA500',
                length : 4
            },
            axisLabel : { //文字样式
                color : "#FFA500",
                distance : 5 //文字离表盘的距离
            },
            pointer: {
                width: 5,
                shadowColor: '#fff', //默认透明
                shadowBlur: 5
            },
            title: {
                offsetCenter: [0, '-30%'],       // x, y，单位px
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontStyle: 'italic',
                    fontSize: 8,
                    color: '#FFA500',
                    shadowColor: '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            data: [{value: 0, name: 'TCPA/min'}]
        },
    ]
};