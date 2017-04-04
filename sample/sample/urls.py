from django.conf.urls import include, url

from .views import SampleView


urlpatterns = [url(r'^datetimepicker/', include('datetimepicker.urls')),
               url(r'^', SampleView.as_view())]
