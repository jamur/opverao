#from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from opverao.cadestagiarios.models import Estagiario, AvaliacaoDeEstagiario, Curso
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta

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

def avaliacao(request):
    resposta = HttpResponse(mimetype='text/csv')
    resposta['Content-Disposition'] = 'attachment; filename=avaliacoes.csv'

    writer = csv.writer(resposta)
    #writer = csv.writer(resposta, dialect="excel", delimiter=";")
    writer.writerow(['nome','curso','inicio','fim',
                    'ass_mb','ass_b','ass_r','ass_i',
                    'cri_mb','cri_b','cri_r','cri_i',
                    'ini_mb','ini_b','ini_r','ini_i',
                    'resp_mb','resp_b','resp_r','resp_i',
                    'cond_mb','cond_b','cond_r','cond_i',
                    'dom_conh_mb','dom_conh_b','dom_conh_r','dom_conh_i',
                    'dom_hab_mb','dom_hab_b','dom_hab_r','dom_hab_i',
                    'outros_mb','outros_b','outros_r','outros_i',
                    'total_de_horas',
                    'parecer',
                    'sup_direta','sup_semi_direta','sup_indireta',
                    'horas_orientador',
                    'horas_supervisor',
                    'data_dia',
                    'data_mes',
                    'data_ano']
    )

    # Percorre as avaliacoes
    for av in AvaliacaoDeEstagiario.objects.all():
        nome = av.estagiario.nome_do_estagiario
        curso = av.estagiario.curso.nome_do_curso if av.estagiario.curso else ' '
        inicio = av.estagiario.data_de_inicio_do_estagio
        fim = av.estagiario.data_de_termino_do_estagio
        ass_mb = 'X' if av.assiduidade == 'MB' else ' '
        ass_b = 'X' if av.assiduidade == 'B' else ' '
        ass_r = 'X' if av.assiduidade == 'R' else ' '
        ass_i = 'X' if av.assiduidade == 'I' else ' '

        cri_mb = 'X' if av.criatividade == 'MB' else ' '
        cri_b = 'X' if av.criatividade == 'B' else ' '
        cri_r = 'X' if av.criatividade == 'R' else ' '
        cri_i = 'X' if av.criatividade == 'I' else ' '

        ini_mb = 'X' if av.iniciativa == 'MB' else ' '
        ini_b = 'X' if av.iniciativa == 'B' else ' '
        ini_r = 'X' if av.iniciativa == 'R' else ' '
        ini_i = 'X' if av.iniciativa == 'I' else ' '

        resp_mb = 'X' if av.responsabilidade == 'MB' else ' '
        resp_b = 'X' if av.responsabilidade == 'B' else ' '
        resp_r = 'X' if av.responsabilidade == 'R' else ' '
        resp_i = 'X' if av.responsabilidade == 'I' else ' '

        cond_mb = 'X' if av.conduta == 'MB' else ' '
        cond_b = 'X' if av.conduta == 'B' else ' '
        cond_r = 'X' if av.conduta == 'R' else ' '
        cond_i = 'X' if av.conduta == 'I' else ' '

        dom_conh_mb = 'X' if av.dominio_do_conhecimento_tecnico == 'MB' else ' '
        dom_conh_b = 'X' if av.dominio_do_conhecimento_tecnico == 'B' else ' '
        dom_conh_r = 'X' if av.dominio_do_conhecimento_tecnico == 'R' else ' '
        dom_conh_i = 'X' if av.dominio_do_conhecimento_tecnico == 'I' else ' '

        dom_hab_mb = 'X' if av.dominio_de_habilidades_necessarias_ao_desempenho == 'MB' else ' '

        dom_hab_b = 'X' if av.dominio_de_habilidades_necessarias_ao_desempenho == 'B' else ' '
        dom_hab_r = 'X' if av.dominio_de_habilidades_necessarias_ao_desempenho == 'R' else ' '
        dom_hab_i = 'X' if av.dominio_de_habilidades_necessarias_ao_desempenho == 'I' else ' '

        outros_mb = 'X' if av.outros == 'MB' else ' '
        outros_b = 'X' if av.outros == 'B' else ' '
        outros_r = 'X' if av.outros == 'R' else ' '
        outros_i = 'X' if av.outros == 'I' else ' '

        if av.estagiario.data_de_termino_do_estagio and av.estagiario.data_de_inicio_do_estagio:
            total_de_horas = ((av.estagiario.data_de_termino_do_estagio - 
                         av.estagiario.data_de_inicio_do_estagio).days / 7 * 30)
        else:
            total_de_horas = 0
        parecer = av.parecer_sobre_o_desempenho_do_estagiario
        sup_direta = 'X' if av.modalidade_de_supervisao == 'D' else ' '
        sup_semi_direta = 'X' if av.modalidade_de_supervisao == 'SD' else ' '
        sup_indireta = 'X' if av.modalidade_de_supervisao == 'I' else ' '
        horas_orientador = total_de_horas / 3 
        horas_supervisor = total_de_horas / 3 * 2
        data_dia = datetime.now().day
        data_mes = datetime.now().month
        data_ano = datetime.now().year
      
        #problema com unicode
        nome = nome.encode("utf-8")
        curso = curso.encode("utf-8") 
        
        writer.writerow([nome,curso,inicio,fim,
                    ass_mb,ass_b,ass_r,ass_i,
                    cri_mb,cri_b,cri_r,cri_i,
                    ini_mb,ini_b,ini_r,ini_i,
                    resp_mb,resp_b,resp_r,resp_i,
                    cond_mb,cond_b,cond_r,cond_i,
                    dom_conh_mb,dom_conh_b,dom_conh_r,dom_conh_i,
                    dom_hab_mb,dom_hab_b,dom_hab_r,dom_hab_i,
                    outros_mb,outros_b,outros_r,outros_i,
                    total_de_horas,
                    parecer,
                    sup_direta,sup_semi_direta,sup_indireta,
                    horas_orientador,
                    horas_supervisor,
                    data_dia,
                    data_mes,
                    data_ano]
        )
 
    return resposta
