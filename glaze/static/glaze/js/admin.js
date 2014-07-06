
var glaze = glaze || {};

glaze.submitAction = function(action) {
	var $ = django.jQuery;
	var input = $('<input type="hidden" name="glaze_action" />').val(action);
	$("form").first().append(input);
	$("input[name='_continue']").first().click();
};


