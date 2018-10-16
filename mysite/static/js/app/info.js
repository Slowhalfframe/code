/*
* @Author: 慢 半 帧
* @Date:   2018-09-21 11:49:43
* @Last Modified by:   慢 半 帧
* @Last Modified time: 2018-09-21 11:55:20
*/
$(function(){
	$("#grzl").click(function(){
		$(".two,.three").hide();
		$(".one").show();
	});
	$("#xgzl").click(function(){
		console.log("x")
		$(".one,.three").hide();
		$(".two").show();
	});
	$("#xgmm").click(function(){
		console.log("x")
		$(".one,.two").hide();
		$(".three").show();
	});
})