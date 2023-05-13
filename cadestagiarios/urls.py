from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^valores/$', views.valores),
    url(r'^nomes/$', views.nomes),
    url(r'^telefones/$', views.telefones),
    url(r'^falta_pagamento/$', views.falta_pagamento),
    url(r'^falta_pagamento_texto/$', views.falta_pagamento_texto),
    url(r'^falta_pagamento_texto_so_valor/$', views.falta_pagamento_texto_so_valor),
    url(r'^avaliacao/$',views.avaliacao),
]
