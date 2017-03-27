from django import forms

from datetimepicker.widgets import DateTimePicker


class SampleForm(forms.Form):

    datepicker = forms.DateField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d", "timepicker": False},
    ))

    timepicker = forms.TimeField(widget=DateTimePicker(
        options={"format": "%H:%M", "datepicker": False},
    ))

    datetimepicker = forms.DateTimeField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d %H:%M"},
    ))
