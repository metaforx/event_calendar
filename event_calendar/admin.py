from django.contrib import admin
from .models import Event, Category
from admin_enhancer.admin import EnhancedModelAdminMixin
from cms.admin.placeholderadmin import PlaceholderAdminMixin, FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin



class EventAdmin(EnhancedModelAdminMixin, FrontendEditableAdminMixin,
                 PlaceholderAdminMixin, TranslatableAdmin, admin.ModelAdmin):
    list_filter = ('category',)
    list_display = ('title', 'event_start', 'event_end', 'location', 'category')
    frontend_editable_fields = ('event_content', 'title')

    fieldsets = [
        ('Event', {
            'fields': ['title', 'name', 'published', 'description','image', 'category', 'facebook_url']
        }),
        ('Dates', {
            'fields': ['event_start', 'event_end', ],
            'classes': ('collapse',),
        }),
        ('Location', {
            'fields': ['location', 'address', 'zip_code', 'city', ],
            'classes': ('collapse',),
        }),
        ('Map', {
            'fields': ['coordinates'],
        }),

    ]


admin.site.register(Category)
admin.site.register(Event, EventAdmin)