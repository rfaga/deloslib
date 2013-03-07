$(function() {
	//$('.control-group textarea').parents('.control-group').addClass('span6');
	//$('.control-group input').parents('.control-group').addClass('span6');
	//$('.control-group').addClass('span12');
	
	$("textarea, input, select").on('focus', function(){
		$(this).parents('.control').find(".help-block").css('display', 'inline'); });
	$("textarea, input, select").on('blur', function(){ 
		$(this).parents('.control').find(".help-block").css('display', 'none'); });
	
});