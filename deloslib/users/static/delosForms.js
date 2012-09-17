$(document).ready(function() {
	/* show and hide help text from form fields */
	$("textarea, input, select").on('focus', function() {
		$(this).nextAll(".help-block").css('display', 'inline');
	});

	$("textarea, input, select").on('blur', function() {
		$(this).nextAll(".help-block").css('display', 'none');
	});
	/* Django pagination plugin endless */
	$("a.endless_page_link").live("click", function() {
		var page_template = $(this).closest(".endless_page_template");
		if(!page_template.hasClass("endless_page_skip")) {
			var data = "querystring_key=" + $(this).attr("rel").split(" ")[0];
			page_template.load($(this).attr("href"), data);
			return false;
		};
	});
	/* end Django pagination endless plugin */

	var msgFloat = {
		showError : function(msg, body) {
			return msgFloat.show(msg, 'error', body);
		},
		showSuccess : function(msg, body) {
			return msgFloat.show(msg, 'success', body);
		},
		show : function(msg, type, body) {
			var template = '<div class="alert-' + type + ' fade in">' + msg + '<button class="close" data-dismiss="alert">×</button></div>';
			if(body == undefined) {
				body = '#system-msg';
			}
			$(body).html(template);
			$(body).fadeIn();
			window.setTimeout(function() {
				$(body).fadeOut()
			}, 3500);
		},
		show2 : function(msg, type, body) {
			var template = '<div class="alert alert-' + type + ' fade in"><p>' + msg + '</p><button class="close" data-dismiss="alert">×</button></div>';
			if(body == undefined) {
				body = 'body';
			}
			$(body).prepend(template).html();
		}
	}
});
