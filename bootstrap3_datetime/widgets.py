import warnings

from django.conf import settings
from django.forms.utils import flatatt
from django.forms.widgets import DateTimeInput
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

try:
    import json
except ImportError:
    from django.utils import simplejson as json
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:  # python3
    from django.utils.encoding import force_text


class DateTimePicker(DateTimeInput):
    class Media:
        class JsFiles(object):
            def __iter__(self):
                yield 'https://code.jquery.com/jquery-2.2.4.min.js'
                yield 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
                yield 'bootstrap3_datetime/js/moment.min.js'
                yield 'bootstrap3_datetime/js/bootstrap-datetimepicker.min.js'
                lang = translation.get_language()
                if lang:
                    lang = lang.lower()
                    #There is language name that length>2 *or* contains uppercase.
                    lang_map = {
                        'ar-ma': 'ar-ma',
                        'en-au': 'en-au',
                        'en-ca': 'en-ca',
                        'en-gb': 'en-gb',
                        'en-us': 'en-us',
                        'fa-ir': 'fa-ir',
                        'fr-ca': 'fr-ca',
                        'ms-my': 'ms-my',
                        'pt-br': 'bt-BR',
                        'rs-latin': 'rs-latin',
                        'tzm-la': 'tzm-la',
                        'tzm': 'tzm',
                        'zh-cn': 'zh-CN',
                        'zh-tw': 'zh-TW',
                        'zh-hk': 'zh-TW',
                    }
                    if len(lang) > 2:
                        lang = lang_map.get(lang, 'en-us')
                    if lang not in ('en', 'en-us'):
                        yield 'bootstrap3_datetime/js/locales/bootstrap-datetimepicker.%s.js' % (lang)

        js = JsFiles()
        css = {'all': ('bootstrap3_datetime/css/bootstrap-datetimepicker.min.css',
                       'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                       'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css')}

    # http://momentjs.com/docs/#/parsing/string-format/
    # http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    FORMAT_MAP = (('DDD', r'%j'),
                  ('DD', r'%d'),
                  ('MMMM', r'%B'),
                  ('MMM', r'%b'),
                  ('MM', r'%m'),
                  ('YYYY', r'%Y'),
                  ('YY', r'%y'),
                  ('HH', r'%H'),
                  ('hh', r'%I'),
                  ('mm', r'%M'),
                  ('ss', r'%S'),
                  ('a', r'%p'),
                  ('ZZ', r'%z'),
    )

    @classmethod
    def conv_datetime_format_py2js(cls, format):
        for js, py in cls.FORMAT_MAP:
            format = format.replace(py, js)
        return format

    @classmethod
    def conv_datetime_format_js2py(cls, format):
        for js, py in cls.FORMAT_MAP:
            format = format.replace(js, py)
        return format

    js_template = '''
        <script>
            (function(window) {
                var callback = function() {
                    $(function(){$("#%(picker_id)s:has(input:not([readonly],[disabled]))").datetimepicker(%(options)s);});
                };
                if(window.addEventListener)
                    window.addEventListener("load", callback, false);
                else if (window.attachEvent)
                    window.attachEvent("onload", callback);
                else window.onload = callback;
            })(window);
        </script>'''

    def __init__(self,
                 attrs={},
                 format=None,
                 options={},
                 div_attrs={},
                 icon_attrs={}):

        # copy the dicts to avoid overriding the attribute dict
        attrs = attrs.copy()
        options = options.copy()
        div_attrs = div_attrs.copy()
        icon_attrs = icon_attrs.copy()

        # if datetime is given, convert the format to a python valid format
        datetime = attrs.get('datetime')
        if datetime is not None:
            datetime = self.conv_datetime_format_js2py(attrs.get('datetime'))

        # 3 possible ways to set the format
        formats = set([datetime,
                       format,
                       options.get('format')]) - {None}

        # extract the format
        if len(formats) is 0:
            format = getattr(settings, self.format_key)[0]
        elif len(formats) is 1:
            format = formats.pop()
        else:
            warnings.wart('format is set more than once', UserWarning)
        
        attrs.update({'class': ' '.join(
            set(attrs.get('class', '').split(' ') + ['form-control'])
        )})

        div_attrs.update({'class': ' '.join(
            set(div_attrs.get('class', '').split(' ') + ['input-group', 'date'])
        )})

        classes = 'glyphicon glyphicon-calendar'
        if not options.get('pickDate', True):
            classes = 'glyphicon glyphicon-time'


        icon_attrs.update({
            'class': icon_attrs.get('class', classes)
        })

        # make sure 'format' is set in the options, the if clause is used just
        # in case the format is set in the options and the attributes, but not
        # as the 'format' keyword argument
        if format:
            options.update({'format': format})
        options.update({'language': translation.get_language()})

        self.options = options
        self.div_attrs = div_attrs
        self.icon_attrs = icon_attrs

        super(DateTimePicker, self).__init__(attrs, format)


    def render(self, name, value, attrs=None, prefix='bootstrap3'):

        if value is None:
            value = ''

        input_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            input_attrs.update({'value': force_text(self._format_value(value))})

        self.div_attrs.update({
            'id': '{prefix}_{field_id}'.format(
                prefix=prefix,
                field_id=input_attrs.get('id'),
            )
        })

        html = render_to_string(
            'bootstrap3_datetime/div.html',
            context={'div_attrs': flatatt(self.div_attrs),
                     'input_attrs': flatatt(input_attrs),
                     'icon_attrs': flatatt(self.icon_attrs)}
        )
        if self.options:
            self.options['language'] = translation.get_language()
            js = self.js_template % dict(picker_id=picker_id,
                                         options=json.dumps(self.options or {}))
        else:
            js = ''
        return mark_safe(force_text(html + js))
