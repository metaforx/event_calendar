from django.conf.urls import patterns, url
from .views import EventListView, EventDetailView

urlpatterns = patterns('event_calendar.views',
    url(r'$', EventListView.as_view(), name='events_list'),
    url(r'^(?P<slug>[-\w]+)/$', EventDetailView.as_view(), name='event_details'),
)
