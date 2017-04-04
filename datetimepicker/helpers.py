from urllib.parse import urlencode

from django.urls import reverse


def js_loader_url(field, input_id):
    attrs = field.widget.options.copy()
    attrs.update({'datetimepicker': input_id})

    return '{base}?{querystring}'.format(
        base=reverse('datetimepicker-loader'),
        querystring=urlencode(attrs),
    )
