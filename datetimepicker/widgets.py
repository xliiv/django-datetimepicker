import json
import warnings

from functools import reduce

from django.conf import settings
from django.forms.utils import flatatt
from django.forms.widgets import DateTimeInput
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.encoding import force_text


FORMAT_MAP = {'d': r'%d',
              'm': r'%m',
              'Y': r'%Y',
              'H': r'%H',
              'i': r'%M'}


def _py_datetime_format_to_js(format_string):
    return (
        format_string is not None and
        reduce(
            lambda format_string, args: format_string.replace(*reversed(args)),
            FORMAT_MAP.items(),
            format_string
        ) or
        None
    )


def _js_datetime_format_to_py(format_string):
    return (
        format_string is not None and
        reduce(
            lambda format_string, args: format_string.replace(*args),
            FORMAT_MAP.items(),
            format_string
        ) or
        None
    )


class DateTimePicker(DateTimeInput):

    def __init__(self,
                 attrs={},
                 format_string=None,  # falsy is not enough, None required (*)
                 options={},
                 div_attrs={},
                 script_tag=True):

        # copy the dicts to avoid overriding the attribute dict
        attrs = attrs.copy()
        options = options.copy()
        div_attrs = div_attrs.copy()

        # the attribute's datetime is set in js format
        # if it is set, we need to convert it to a valid python format
        datetime = attrs.get('datetime')

        # get the set of given formats
        formats = {
            datetime and _js_datetime_format_to_py(datetime) or None,
            format_string,
            options.get('format')
        } - {None}  # and this is why (*)

        if len(formats) is 0:
            format_string = getattr(settings, self.format_key)[0]
        elif len(formats) is 1:
            format_string = formats.pop()
        else:
            warnings.warn('format is set more than once', UserWarning)

        attrs.update({'class': ' '.join(
            set(attrs.get('class', '').split(' ') + ['form-control'])
        )})

        div_attrs.update({'class': ' '.join(set(
            div_attrs.get('class', '').split(' ') + ['input-group', 'date']
        ))})

        # make sure 'format' is set in the options, the if clause is used just
        # in case the format is set in the options and the attributes, but not
        # as the 'format' keyword argument
        if format_string:
            options.update({'format': format_string})

        self.options = options
        self.div_attrs = div_attrs
        self.use_script_tag = script_tag

        super(DateTimePicker, self).__init__(attrs, format_string)

    def format_value(self, value):
        return super().format_value(value) or ''

    def render(
        self, name, value, attrs=None, renderer=None, prefix='datetimepicker'
    ):
        context = self.get_context(name, value, attrs)
        input_attrs = context['widget']['attrs']
        input_attrs.update({
            'name': name,
            'value': context['widget']['value'],
            'type': context['widget']['type'],
        })
        self.div_attrs.update({
            'id': '{prefix}_{field_id}'.format(
                prefix=prefix,
                field_id=input_attrs.get('id'),
            )
        })

        rendered = render_to_string(
            'datetimepicker/div.html',
            context={'div_attrs': flatatt(self.div_attrs),
                     'input_attrs': flatatt(input_attrs)}
        )

        if self.use_script_tag:
            js_options = json.dumps(dict(
                format=_py_datetime_format_to_js(self.options.get('format')),
                **{key: val
                   for key, val in self.options.items()
                   if key != 'format'}
            ))
            js = render_to_string(
                'datetimepicker/script.html',
                context={
                    'input_attrs': input_attrs,
                    'options': js_options,
                    # datetimepicker Plugin now handles lang globally
                    # (instead of previous via widget-initialization)
                    'lang': self.options.pop(
                        'lang', translation.get_language()
                    ),
                }
            )
            rendered += js

        return rendered

    class Media:
        js = ('datetimepicker/vendor/js/jquery.min.js',
              'datetimepicker/js/jquery.datetimepicker.full.js')
        css = {'all': ('datetimepicker/css/jquery.datetimepicker.min.css',)}
