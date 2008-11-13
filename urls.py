from django.conf.urls.defaults import *
from django.contrib import databrowse
from opverao.cadestagiarios.models import Estagiario, AvaliacaoDeEstagiario

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    #(r'^admin/', include('django.contrib.admin.urls')),
    (r'^estagiarios/', include('opverao.cadestagiarios.urls')),
    (r'^db/(.*)', databrowse.site.root),
    (r'^', include('opverao.cadestagiarios.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

databrowse.site.register(Estagiario)
databrowse.site.register(AvaliacaoDeEstagiario)
#
