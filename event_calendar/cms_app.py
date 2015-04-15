from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from menu import EventCalendarMenu

class EventsApphook(CMSApp): 
    name = _("Events Apphook")
    urls = ["event_calendar.urls"]
    menus = [EventCalendarMenu]
    
apphook_pool.register(EventsApphook)