from django.conf.urls.defaults import *
from django.views.generic import list_detail
from antidote.red.models import Tag, Entry

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

def get_tags():
    return Tag.objects.order_by('name')

entry_info = {
    'queryset': Entry.objects.all(),
    'template_name': 'entry_list.html',
    'template_object_name': 'entry',
    'extra_context': {'tag_list': get_tags},
}

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^search/$', 'antidote.red.views.search'),
    (r'^archive/$', list_detail.object_list, entry_info),
    (r'^export/(?P<entry_id>\d+)/$', 'antidote.red.views.export'),
    (r'^$', 'antidote.red.views.upload_file'),
)
