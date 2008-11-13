from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from opverao.cadestagiarios.relatorios import *

urlpatterns = patterns('opverao.cadestagiarios.relatorios',
    (r'^$', 'index'),
    (r'^valores/$', login_required(valores)),
    (r'^nomes/$', 'nomes'),
    (r'^telefones/$', 'telefones'),
    (r'^falta_pagamento/$', 'falta_pagamento'),
    (r'^falta_pagamento_texto/$', 'falta_pagamento_texto'),
    (r'^falta_pagamento_texto_so_valor/$', 'falta_pagamento_texto_so_valor'),
    (r'^avaliacao/$','avaliacao'),
)
