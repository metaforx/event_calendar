from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from .models import Event, Category
from django.utils.translation import ugettext_lazy as _
from .settings import get_setting
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext

class EventListView(ListView):
    model = Event
    template_name = 'event_calendar/event_list.html'

    def get_context_data(self, **kwargs):

        context = super(EventListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self, **kwargs):
        qs = Event.objects.in_progress()
        return qs


class EventDetailView(DetailView):
    model = Event
    slug_field = 'slug'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['use_placeholder'] = get_setting('USE_PLACEHOLDER')
        menu = request.toolbar.get_or_create_menu('event_calendar-app', _('Event Calendar'))
        menu.add_link_item(_('Edit This Event'), url=reverse('admin:event_calendar_event_change', args=[self.object.pk]))

        print context['use_placeholder']

        return self.render_to_response(context)



class CategoryListView(ListView):
    model = Category
