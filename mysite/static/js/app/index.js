/*
* @Author: m
* @Date:   2018-09-18 16:58:40
* @Last Modified by:   m
* @Last Modified time: 2018-09-19 21:52:28
*/


$(document).ready(function () {
    $.goup({

        trigger: 200,

        bottomOffset: 111,

        locationOffset: 100,

        title: '回到顶部',

        titleAsText: true
    });
});


$(document).ready(function() {
	var nice = $("html").niceScroll();  // The document page (body)
	$("#div1").html($("#div1").html()+' '+nice.version);
    $("#boxscroll").niceScroll({cursorborder:"",cursorcolor:"#00F",boxzoom:true}); // First scrollable DIV
    $("#boxscroll2").niceScroll("#contentscroll2",{cursorcolor:"#F00",cursoropacitymax:0.7,boxzoom:true,touchbehavior:true});  // Second scrollable DIV
    $("#boxframe").niceScroll("#boxscroll3",{cursorcolor:"#0F0",cursoropacitymax:0.7,boxzoom:true,touchbehavior:true});  // This is an IFrame (iPad compatible)
    $("#boxscroll4").niceScroll("#boxscroll4 .wrapper",{boxzoom:true});  // hw acceleration enabled when using wrapper
  });

var Sys = {};
var ua = navigator.userAgent.toLowerCase();
if( window.ActiveXObject ){
    document.body.oncopy = function(){
        event.returnValue = false;
        var t=document.selection.createRange().text;
        var s="源自于慢半帧网站，请尊重版权。<br />原文链接："+location.href;
        clipboardData.setData('Text',t+'\r\n'+s);
    };
    
}else{
    function addLink(){
        var body_element = document.getElementsByTagName('body')[0];
        var selection;
        selection = window.getSelection();
        var pagelink =" <<<<< ----- ----- ----- 源自于慢半帧网站，请尊重版权。"+"<br /> 原文链接："+location.href;
        var copytext = selection + pagelink;
        var newdiv = document.createElement('div');
        newdiv.style.position='absolute';
        newdiv.style.left='-99999px';
        body_element.appendChild(newdiv);
        newdiv.innerHTML = copytext;
        selection.selectAllChildren(newdiv);
        window.setTimeout(function(){body_element.removeChild(newdiv);},0);
    }
    document.oncopy = addLink;
}   

var fnTextPopup = function (arr, options) {
    // arr参数是必须的
    if (!arr || !arr.length) {
        return;    
    }
    // 主逻辑
    var index = 0;
    document.documentElement.addEventListener('click', function (event) {
        var x = event.pageX, y = event.pageY;
        var eleText = document.createElement('span');
        eleText.className = 'text-popup';
        this.appendChild(eleText);
        if (arr[index]) {
            eleText.innerHTML = arr[index];
        } else {
            index = 0;
            eleText.innerHTML = arr[0];
        }
        // 动画结束后删除自己
        eleText.addEventListener('animationend', function () {
            eleText.parentNode.removeChild(eleText);
        });
        // 位置
        eleText.style.left = (x - eleText.clientWidth / 2) + 'px';
        eleText.style.top = (y - eleText.clientHeight) + 'px';
        // index递增
        index++;
    });    
};

fnTextPopup(['国家','富强', '民主', '文明', '和谐', '社会','自由', '平等', '公正', '法治', '人民','爱国', '敬业', '诚信', '友善','不忘初心','牢记使命','高举中国特色社会主义伟大旗帜','决胜全面建成小康社会','夺取新时代中国特色社会主义伟大胜利','为实现中华民族伟大复兴的中国梦不懈奋斗','坚持党对一切工作的领导。','坚持以人民为中心','坚持全面深化改革','坚持新发展理念','坚持人民当家作主','坚持全面依法治国','坚持社会主义核心价值体系','坚持人与自然和谐共生','坚持总体国家安全观','坚持以习近平新时代中国特色社会主义思想为行动指南','中国共产党人的初心和使命','就是为中国人民谋幸福','为中华民族谋复兴','中国特色社会主义进入了新时代','中华民族迎来了从站起来、富起来到强起来的伟大飞跃','把人民对美好生活的向往作为奋斗目标','依靠人民创造历史伟业','让全体人民住有所居','党始终同人民想在一起、干在一起','人民有信仰','国家有力量','民族有希望']);

