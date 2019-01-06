(function () {
	$(document).ready(function() {
        $.datetimepicker.setLocale({{ lang }});
		$("#{{ input_id }}").datetimepicker({{ options|safe }});
	});
})(jQuery);
