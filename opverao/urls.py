from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
#from django.contrib import databrowse
from cadestagiarios.models import Estagiario, AvaliacaoDeEstagiario

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^estagiarios/', include('cadestagiarios.urls')),
#    url(r'^db/(.*)', databrowse.site.root),
    url(r'^', include('cadestagiarios.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#databrowse.site.register(Estagiario)
#databrowse.site.register(AvaliacaoDeEstagiario)
#
