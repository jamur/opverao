from django.conf.urls.defaults import *
from django.contrib import databrowse
from opverao.cadestagiarios.models import Estagiario

databrowse.site.register(Estagiario)

urlpatterns = patterns('',
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^estagiarios/', include('opverao.cadestagiarios.urls')),
    (r'^db/(.*)', databrowse.site.root),
    (r'^', include('opverao.cadestagiarios.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
