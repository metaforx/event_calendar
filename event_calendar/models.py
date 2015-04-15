import datetime

from django.db import models
from django.utils.translation import ugettext as _
from filer.fields.image import FilerImageField

from model_utils.models import TimeStampedModel
from django_autoslug.fields import AutoSlugField
from base.models import TimestampedModel
from geoposition.fields import GeopositionField


from cms.models import PlaceholderField, CMSPlugin
from parler.models import TranslatableModel, TranslatedFields
from parler.managers import TranslationManager




class Category(models.Model):
    name = models.CharField(_('Name'), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'event_calendar'


class EventManager(TranslationManager):

    def published(self):
        return self.get_query_set().filter(published=True)

    def completed(self):
        return self.get_query_set().filter(
            published=True,
            event_end__lte=datetime.datetime.utcnow()
        )

    def in_progress(self):
        return self.get_query_set().filter(
            published=True,
            event_end__gte=datetime.datetime.utcnow()
        )



class Event(TimeStampedModel, TranslatableModel):
    title = models.CharField(_('Title'), max_length=50)
    slug = AutoSlugField(populate_from='title', editable=False, blank=True, overwrite=True)
    published = models.BooleanField(default=True)
    #description = MarkdownTextField(blank=True, null=True)
    description = models.TextField(_('Description'))
    content = PlaceholderField('event_content', related_name='event_content')

    translations = TranslatedFields(
        name = models.CharField(_("name"), max_length=200)
    )



    event_start = models.DateTimeField(_('Start time'), blank=False)
    event_end = models.DateTimeField(_('End time'), blank=True, null=True)
    location = models.CharField(_('Location'), max_length=50, blank=True)
    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_("Image"))
    category = models.ForeignKey(Category)
    facebook_url = models.URLField(_('Facebook link'), blank=True)


    # location
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    # country: TBD
    coordinates = GeopositionField(blank=True, null=True)

    objects = EventManager()
    #events = CurrentEventManager()

    class Meta:
        app_label = 'event_calendar'
        ordering = ['event_start']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")



    @models.permalink
    def get_absolute_url(self):
        return 'event_details', (), {'slug': self.slug}

    def google_lat(self):
        self.coordinates.latitude = str(self.coordinates.latitude)
        return self.coordinates.latitude.replace(',','.')

    def google_long(self):
        self.coordinates.longitude = str(self.coordinates.longitude)
        return self.coordinates.longitude.replace(',','.')

    def google_location(self):
        return self.location.replace(' ','+')

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):

        # geocodeing
        if not self.coordinates:
            try:
                from pygeocoder import Geocoder
                address = '%s, %s %s' % (self.address, self.zip_code, self.city)
                results = Geocoder.geocode(address.encode('ascii', 'ignore'))
                lat, lng = results[0].coordinates
                if lat and lng:
                    self.coordinates = '%s,%s' % (lat, lng)

            except Exception, e:
                pass


        super(Event, self).save(*args, **kwargs)

try:
    from cms.models import CMSPlugin
except ImportError:
    pass
else:
    class EventListPlugin(CMSPlugin):
        title = models.CharField(_('Title'), max_length=50)
        category = models.ForeignKey(Category, null=True, blank=True)

        def __unicode__(self):
            return self.category.name if self.category else _('All events')
