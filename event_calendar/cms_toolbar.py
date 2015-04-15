from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class EventCalendarToolbar(CMSToolbar):

    def populate(self):

        menu = self.toolbar.get_or_create_menu('event_calendar-app', _('Event Calendar'))
        url = reverse('admin:event_calendar_event_changelist')
        # menu.add_sideframe_item(_('Project List'), url=url)
        menu.add_link_item(_('Event List'), url=url)

        url = reverse('admin:event_calendar_event_add')
        menu.add_link_item(_('Add New Event'), url=url)


