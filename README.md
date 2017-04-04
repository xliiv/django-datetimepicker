# django-datetimepicker

Uses xdsoft's datetimepicker to make a datetimepicker widget for django.
This is inspired by the `django-bootstrap3-datetimepicker` application.


## Install

- Run `pip install django-datetimepicker`
- Add `'datetimepicker'` to your `INSTALLED_APPS`

## Usage

Here is an example of how to use the widget.
Further examples can be found in the example project.

1. Assign the `DateTimePicker` to a `DateTimeField`, `DateField` or `TimeField`.

```python
from django import forms
from datetimepicker.widgets import DateTimePicker


class SampleForm(forms.Form):

    datetime = forms.DateTimeField(
        widget=DateTimePicker()
    )
```

This will render the following `html` code:
```html
<div  class=" date input-group" id="datetimepicker_id_datepicker">
	<input  class=" form-control" id="id_datepicker" name="datepicker" type="text" required/>
</div>
<script>(function () {
	$(document).ready(function() {
		$("#id_datepicker").datetimepicker();
	});
})(jQuery);
</script>
```
