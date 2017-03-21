from django.conf.urls import url

from .views import SampleView


urlpatterns = [url(r'^', SampleView.as_view())]
