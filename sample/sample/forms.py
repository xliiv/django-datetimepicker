from django import forms

from bootstrap3_datetime.widgets import DateTimePicker


class SampleForm(forms.Form):

    datepicker = forms.DateField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d", "pickTime": False},
    ))

    timepicker = forms.TimeField(widget=DateTimePicker(
        options={"format": "%H:%M", "pickDate": False},
    ))

    datetimepicker = forms.DateTimeField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d %H:%M", "pickSeconds": False},
    ))
