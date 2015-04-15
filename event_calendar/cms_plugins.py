import random
from sekizai.context import SekizaiContext
from django.utils.translation import ugettext as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from models import EventListPlugin, Event

class EventList(CMSPluginBase):
    model = EventListPlugin
    name = _('Event list')
    render_template = 'event_calendar/event_list_plugin.html'

    def render(self, context, instance, placeholder):
        object_list = Event.objects.in_progress()
        if instance.category:
            object_list = object_list.filter(category=instance.category)
        context.update({'instance': instance, 'object_list': object_list})
        return context

        #return SekizaiContext({
        #    'object_list': object_list,
        #    'instance': instance
        #})
plugin_pool.register_plugin(EventList)
