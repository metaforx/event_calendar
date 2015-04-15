from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from menus.base import Modifier, Menu, NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from models import Event

class EventCalendarMenu(CMSAttachMenu):
    
    name = _("Event Calendar Menu")
    
    def get_nodes(self, request):
        nodes = []

        for event in Event.objects.all().filter(published=True).order_by("event_start"):
            node = NavigationNode(
                event.title,
                event.get_absolute_url(),
                event.pk,
                #category.parent_id
            )
            nodes.append(node)
        
        return nodes
    
menu_pool.register_menu(EventCalendarMenu)


