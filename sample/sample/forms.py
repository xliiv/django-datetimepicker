from django import forms

from datetimepicker.helpers import js_loader_url
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

    datepicker_no_script_tag = forms.DateField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d", "timepicker": False},
        script_tag=False,
    ))
    timepicker_no_script_tag = forms.TimeField(widget=DateTimePicker(
        options={"format": "%H:%M", "datepicker": False},
        script_tag=False,
    ))
    datetimepicker_no_script_tag = forms.DateTimeField(widget=DateTimePicker(
        options={"format": "%Y-%m-%d %H:%M"},
        script_tag=False,
    ))

    @property
    def media(self):
        js_urls = js_loader_url(
            fields=self.fields,
            input_ids=['datepicker_no_script_tag',
                       'timepicker_no_script_tag',
                       'datetimepicker_no_script_tag']
        )

        form_media = forms.Media(js=js_urls)
        return super(SampleForm, self).media + form_media
