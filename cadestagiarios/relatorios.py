#from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from opverao.cadestagiarios.models import Estagiario

def index(request):
    return render_to_response('estagiarios/index.html')

def valores(request):
    estagiarios = Estagiario.objects.all()
    return render_to_response('estagiarios/valores.html', {'es': estagiarios})

def nomes(request):
    estagiarios = Estagiario.objects.all().order_by('nome_do_estagiario')
    return render_to_response('estagiarios/nomes.html', {'estagiarios': estagiarios})

def telefones(request):
    estagiarios = Estagiario.objects.all().order_by('nome_do_estagiario')
    return render_to_response('estagiarios/nomes.html', {'estagiarios': estagiarios,'com_telefones':True})
    
def falta_pagamento(request):
    estagiarios = Estagiario.objects.filter(falta_pagamento__exact=True).order_by('nome_do_estagiario')
    return render_to_response('estagiarios/falta_pagamento.html', {'estagiarios': estagiarios})

def falta_pagamento_texto(request):
    estagiarios = Estagiario.objects.filter(falta_pagamento__exact=True).order_by('nome_do_estagiario')
    return render_to_response('estagiarios/falta_pagamento_texto.html', {'estagiarios': estagiarios})

def falta_pagamento_texto_so_valor(request):
    estagiarios = Estagiario.objects.filter(falta_pagamento__exact=True).order_by('nome_do_estagiario')
    return render_to_response('estagiarios/falta_pagamento_texto_so_valor.html', {'estagiarios': estagiarios})


#def contratos_na_ufpr(request)
    #estagiarios = Estagiario.objects.all().order_by('nome_do_estagiario') # FIXME
    #return render_to_response('estagiarios/contratosaqui.html', {'estagiarios': estagiarios, 'com_telefones':True})
