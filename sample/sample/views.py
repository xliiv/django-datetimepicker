from django.views.generic.edit import FormView

from .forms import SampleForm


class SampleView(FormView):

    form_class = SampleForm
    template_name = 'sample.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'data': self.request.GET})
        return kwargs
