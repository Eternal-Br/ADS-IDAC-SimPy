(function($, window, document, undefined){
    var Translucent = function (elem,options) {
        this.elem = elem;
        this.$elem = $(elem);
        this.options = options;
        this.$win = $(window);
        this.$doc = $(document);
        this.docHeight = this.$doc.height();
    };
    Translucent.prototype = {
        defaults: {
            target:"translucentDefultId",
            width:230, //默认宽度
            height:220, //默认高度
            drag:true, //启动拖拽
            opacity:0.8, //透明度
            border:"1px solid #ddd",
            borderRadius:8,
            wallGlass:false, //启动毛玻璃效果
            backgroundColor:"rgb(225, 225, 225)",//默认背景色
            titleHeight:"40px",//title高度
            titleGroundColor:"#999",//title默认背景色
            shadow:true,//开启阴影
            positionTop:420,  //弹出位置
            positionLeft:10,  //弹出位置
            titleText:"新建弹窗",
            titleFontSize:12,
            titleFontColor:"#000",
            titleFontFamily:"微软雅黑",
            textHtml:"<p>这是一个新建的弹窗！</p>",
            titleTextCenter:false,
            close:null,
            zIndex:10,
            //私有的属性
            _isScale:true,
            _isMax:true,
            _width:500
        },
        init:function () {
            this.config = $.extend({}, this.defaults, this.options);
            //this._width = this.config.width;
            this.drawInfoWindow();
            if(this.config.drag){
                this.dragWindow();
                $(".translucent-title").addClass("translucent-move");
            }
            this.smallWindow();
            this.closeWindow();
            this.maxWindow();
        },
        drawInfoWindow:function () {
            var context = this;
            context.$elem.addClass("translucent-relative");
            var html = '';
                html += '<div id="'+context.config.target+'" class="translucent-container">';
                    html += '<div class="translucent-title"><span>'+context.config.titleText+'</span><div class="translucent-control"><img id="translucent_small" title="最小化" src="'+context.getPath()+'icon/small.png"/><img id="translucent_big" title="最大化" src="'+context.getPath()+'icon/big.png"/><img id="translucent_close" title="关闭" src="'+context.getPath()+'icon/close.png"/></div></div>';
                    html += '<div class="translucent-content">'+context.config.textHtml+'</div>';
                html += '</div>';
            if($(".translucent-container").length > 0){
                $(".translucent-container").remove();
                // context.config._isMax = false;
            }
            context.$elem.append(html);
            var translucentContainer = $(".translucent-container");
            var translucentTitle = $(".translucent-title");
            translucentContainer.css({
                width:context.config.width,
                height:context.config.height,
                backgroundColor:context.config.backgroundColor,
                top:context.config.positionTop,
                left:context.config.positionLeft,
                opacity:context.config.opacity,
                border:context.config.border,
                borderRadius:context.config.borderRadius,
                zIndex:context.config.zIndex
            }).addClass("translucent-absolute");
            if(context.config.shadow){
                translucentContainer.addClass("translucent-shadow");
            }
            translucentTitle.css({
                height:context.config.titleHeight,
                backgroundColor:context.config.titleGroundColor,
                fontSize:context.config.titleFontSize,
                color:context.config.titleFontColor,
                fontFamily:context.config.titleFontFamily,
                borderTopLeftRadius:context.config.borderRadius,
                borderTopRightRadius:context.config.borderRadius
            });
            if(context.config.titleTextCenter){
                translucentTitle.addClass("translucent-center");
            }
            translucentTitle.find("span").css({
                lineHeight:context.config.titleHeight,
                marginLeft:10
            });
            var _titleHeight = translucentTitle.height();
            var _top = (_titleHeight-20)/2;
            $(".translucent-control").css({
                top:0,
                height:context.config.titleHeight,
                lineHeight:context.config.titleHeight
            });
        },
        smallWindow:function () {
            var context = this;
            var translucentContainer = $(".translucent-container");
            var translucentContent = $(".translucent-content");
            var translucentControl = $(".translucent-control");
            var translucentTitle = $(".translucent-title");
            translucentControl.bind("click",function (e) {
                e.preventDefault();  //阻止默认事件
                e.stopPropagation();    //阻止冒泡事件
            });
            context.defaults._isScale = true;
            $("#translucent_small").bind("click",function (e) {
                var top = $("body").height() - parseInt(context.config.titleHeight)-6;
                if(context.defaults._isScale){
                    translucentContainer.animate({
                        height:context.config.titleHeight,
                        top:top,
                        left:0,
                        width:"230px",
                        opacity:1,
                        borderTopRightRadius:0,
                        borderTopLeftRadius:0
                    });
                    translucentTitle.css({
                        borderTopRightRadius:0,
                        borderTopLeftRadius:0
                    });
                    translucentContent.hide();
                    $(this).attr("src",context.getPath()+"icon/fangda.png");
                    $(this).attr("title","还原");
                    $("#translucent_big").attr("src",context.getPath()+"icon/big.png");
                    $("#translucent_big").attr("title","最大化");
                    context.defaults._isScale = false;
                    context.defaults._isMax = true;
                }else{
                    translucentContainer.animate({
                        height:context.config.height,
                        left:context.config.positionLeft,
                        top:context.config.positionTop,
                        width:context.config.width,
                        opacity:context.config.opacity,
                        borderTopRightRadius:context.config.borderRadius,
                        borderTopLeftRadius:context.config.borderRadius
                    });
                    translucentTitle.css({
                        borderTopRightRadius:context.config.borderRadius,
                        borderTopLeftRadius:context.config.borderRadius
                    });
                    translucentContent.show();
                    $(this).attr("src",context.getPath()+"icon/small.png");
                    $(this).attr("title","最小化");
                    context.defaults._isScale = true;
                }
                e.preventDefault();  //阻止默认事件
                e.stopPropagation();    //阻止冒泡事件
            })
        },
        closeWindow:function () {
            var context = this;
            $("#translucent_close").bind("click",function () {
                if(context.config.close!== null && typeof context.config.close === "function"){
                    context.config.close($(".translucent-container"));
                }
                $(".translucent-container").remove();
            });
        },
        maxWindow:function () {
            var context = this;
            var translucentBig = $("#translucent_big");
            var translucentContainer = $(".translucent-container");
            var translucentContent = $(".translucent-content");
            var translucentControl = $(".translucent-control");
            var translucentSmall = $("#translucent_small");
            var $body = $("body");
            context.defaults._isMax = true;
            translucentBig.bind("click",function (e) {
                if(!context.defaults._isScale){return;}
                if(context.defaults._isMax){
                    translucentContainer.animate({
                        width:"80%",
                        left:"10%"
                    });
                    $(this).attr("src",context.getPath()+"icon/huanyuan.png");
                    $(this).attr("title","还原");
                    //context.config.width = ($body.width())*(0.8);
                    context.defaults._isMax = false;
                }else{
                    translucentContainer.animate({
                        width:context.config.width,
                        left:context.config.positionLeft
                    });
                    $(this).attr("src",context.getPath()+"icon/big.png");
                    $(this).attr("title","最大化");
                    //context.config.width = context._width;
                    context.defaults._isMax = true;
                }
            });
        },
        dragWindow:function(){
            var context = this;
            context.defaults._isScale = true;
            context.config._isMax = true;
            function drag(obj1,obj3) {
                //想要实现鼠标拖拽，必须是在鼠标按下之后，松开之前，所以需要绑定鼠标按下事件
                obj1.mousedown(function(ev){
                    if(context.defaults._isScale && context.config._isMax){
                        //获取点击时刻的X轴坐标和Y坐标(前一个获取不到就获取后一个)
                        var dx = ev.clientX||ev.pageX;
                        var dy = ev.clientY||ev.pageY;
                        //获取div距左和距顶的距离，offset是边距
                        var dialogleft = obj3.offset().left;
                        var dialogtop = obj3.offset().top;
                        context.config.positionLeft = dialogleft;
                        context.config.positionTop = dialogtop;
                        //定义一个开关，默认鼠标点击之后开启
                        var flag = true;
                        //绑定鼠标移动事件，要在全屏移动，所以用绑定document
                        $(document).mousemove(function(e){
                            if(flag){
                                var bodyWidth = $("body").width() - context.config.width;
                                var bodyHeight = $("body").height() - context.config.height;
                                //鼠标移动后的X轴坐标和Y轴坐标
                                var mx = e.clientX||e.pageX;
                                var my = e.clientY||e.pageY;
                                //用移动后的X轴和Y轴坐标减去点击时刻的坐标再加上原先div距左和距顶的距离
                                var _left = mx-dx+dialogleft;
                                var _top = my-dy+dialogtop;
                                if(_left < 0){return;}
                                if(_top < 0){return;}
                                if(_left > bodyWidth){return;}
                                if(_top > bodyHeight){return;}
                                //重新为div的left和top赋值
                                obj3.css({"left":_left+"px","top":_top+"px"});
                            }

                        }).mouseup(function(){
                            flag = false;
                        })
                    }
                })
            }
            drag($(".translucent-title"),$(".translucent-container"));
        },
        getPath:function () {
            var scripts = document.scripts;
            for(var i = 0;i < scripts.length;i ++){
                var item = scripts[i];
                var name = $(item).attr("src").split("/").reverse()[0];
                if(name === "jquery-translucent.js"){
                    var pathArr = $(item).attr("src").split("/");
//                  pathArr.reverse();
                    var pathString = '';
                    for(var k = 0;k < pathArr.length;k ++){
                        var len = pathArr.length;
                        if(k !== len-1){
                            pathString += (pathArr[k] + "/");
                        }
                    }
			
                    return pathString;
                }
            }
        }
    };
    $.fn.translucent = function(options) {
        new Translucent(this, options).init();
        return this;
    };
    
})( jQuery, window , document );
