#-*- coding: utf-8 -*-
from cadestagiarios.models import Banco, Projeto, Cidade, Estado, ConjAtividade, Atividade, ConjAtividadeEspecifica, AtividadeEspecifica, Coordenador, SubProjeto, InstituicaoDeEnsino, Curso, Estagiario, Local, EstadoDoDocumento, TipoDeDocumento, Documento, TipoDePendencia, Pendencia, TipoDeContatamento, Contatamento, Instituicao, Contato, ItemFotografado, Foto, AvaliacaoDeEstagiario, AvaliacaoDeTodosOsEstagiarios
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class Atividade_Inline(admin.StackedInline):
    model = Atividade
    extra = 1

class AtividadeEspecifica_Inline(admin.TabularInline):
    model = AtividadeEspecifica
    extra = 1

class Pendencia_Inline(admin.TabularInline):
    model = Pendencia
    extra = 1

class Contatamento_Inline(admin.TabularInline):
    model = Contatamento
    extra = 1

class Foto_Inline(admin.TabularInline):
    model = Foto

class DocumentoOptions(admin.ModelAdmin):
    list_display = ('estagiario','tipo_de_documento','local_atual','preenchido','assinado')
    list_filter = ('tipo_de_documento','local_atual','data_de_envio_ou_chegada','preenchido','assinado','estagiario')
    search_fieldsets = ['estagiario']       # nao funcionou com foreign

class ContatamentoOptions(admin.ModelAdmin):
    list_display = ('estagiario','data_e_hora','tipo_de_contatamento','ocorrido','pag_ok')
    date_hierarchy = 'data_e_hora'

class EstagiarioOptions(admin.ModelAdmin):
    inlines = [Pendencia_Inline, Contatamento_Inline]
    fieldsets = (
        (None, {'fields':(
                'nome_do_estagiario','falta_pagamento','reclamou_pagamento',
                'verificar_pagamento', 'email', 'subprojeto','numero_no_ciee',
                'rg','cpf','num_matricula_ufpr','obs','pagamento_pendente')}),
        ('Telefones', {'fields':
                ('telefones',)}),
        ('Filiação', {'fields':('nome_da_mae','data_nasc_mae')}),
        ('Outros', {'fields':('projeto','nome_do_solicitante')}),
        ('Banco',{'fields':('banco','agencia', 'conta_corrente')}),
        ('Endereço', {'fields':('end_rua', 'end_num', 'end_compl', 'end_bairro',
                                'end_cidade','end_estado')}),
        #('Atividades', {'fields':('conj_atividades',)}),
        ('Períodos / Blocos', {'fields':('bloco1', 'bloco2')}),
        ('Instituição de Ensino', 
            {'fields':('instituicao_de_ensino','estudante_da_ufpr','curso')}),
        ('Valor da Bolsa', {'fields':('bloco1_valor','bloco2_valor'),'classes': ('collapse',)}),
        ('Período do Estágio', 
            {'fields':('data_prevista_para_inicio','data_prevista_para_termino','data_de_inicio_do_estagio','data_de_termino_do_estagio')}),
	('Textos',
	    {'fields':('texto1',)}),
        #('Testes', {'fields':('teste2',)}),
        )
    list_display = (
        #'nome_do_estagiario', 'telefones', 'cpf','rg','pag_ok','recpag_ok','verificado',
        'nome_do_estagiario', 'telefones','pag_ok', #,'nao_reclamou','verificado',
        #'nome_do_estagiario', 'telefones', 'cpf','rg','falta_pagamento','reclamou_pagamento','verificar_pagamento',
        'data_de_inicio_do_estagio','data_de_termino_do_estagio')
    #list_display = ('nome_do_estagiario','telefones')
    #list_filter = ('estudante_da_ufpr',)
    list_per_page = 25
    search_fieldsets = ['nome_do_estagiario']
    list_filter = ('falta_pagamento','reclamou_pagamento', 'verificar_pagamento', 'subprojeto','instituicao_de_ensino','end_cidade')#,'data_da_ultima_atualizacao','data_do_cadastro')
    ordering = ('nome_do_estagiario',)
    save_on_top = True
    #date_hierarchy = 'data_da_ultima_atualizacao'

class ProjetoOptions(admin.ModelAdmin):
    list_display = ('numero_do_projeto', 'nome_do_projeto')

class ConjAtividadeOptions(admin.ModelAdmin):
    inlines = [Atividade_Inline]

class CoordenadorOptions(admin.ModelAdmin):
    list_display = ('nome','telefone')

class ContatoOptions(admin.ModelAdmin):
    list_display = ('nome', 'instituicao','telefone')
    search_fieldsets = ('nome','instituicao')

class ConjAtividadeEspecificaOptions(admin.ModelAdmin):
    inlines = [AtividadeEspecifica_Inline]

class ItemFotografadoOptions(admin.ModelAdmin):
    inlines = [Foto_Inline]

class EstadoDoDocumentoOptions(admin.ModelAdmin):
    list_filter = ('estado',)

class BancoOptions(admin.ModelAdmin):
    list_display = ('numero_do_banco', 'nome_do_banco')

class PendenciaOptions(admin.ModelAdmin):
    list_filter = ('tipo_de_pendencia','data_da_atualizacao','estagiario')
    #search_fieldsets = ('estagiario',)
    date_hierarchy = 'data_da_atualizacao'

class AvaliacaoDeEstagiarioOptions(admin.ModelAdmin):
    fieldsets = (
        ('1. Identificação do Estagiário', {'fields':(
            'operacao','estagiario')}),
        ('2. Critérios para Avaliação', {'fields':
            ('avaliacao_unica',
             'assiduidade','criatividade','iniciativa','responsabilidade',
             'conduta','dominio_do_conhecimento_tecnico',
             'dominio_de_habilidades_necessarias_ao_desempenho','outros',
             'total_de_horas_efetivamente_realizadas',)}),
        ('3. Desempenho do Estagiario', {'fields':('parecer_sobre_o_desempenho_do_estagiario',)}),
        ('4. Supervisão',{'fields':
            ('modalidade_de_supervisao','horas_orientador','horas_supervisor')}),
        (None, {'fields':
            ('avaliado',)}),
    )

    list_filter = ('avaliado',)
     
    radio_fields = {"avaliacao_unica":admin.HORIZONTAL,
                    "assiduidade":admin.HORIZONTAL,
                    "criatividade":admin.HORIZONTAL,
                    "iniciativa":admin.HORIZONTAL,
                    "responsabilidade":admin.HORIZONTAL,
                    "conduta":admin.HORIZONTAL,
                    "dominio_do_conhecimento_tecnico":admin.HORIZONTAL,
                    "dominio_de_habilidades_necessarias_ao_desempenho":admin.HORIZONTAL,
                    "outros":admin.HORIZONTAL
    }

    """Este não funciona 
    radio_fields = {("assiduidade","criatividade",
                    "iniciativa","responsabilidade",
                    "conduta") : admin.HORIZONTAL
    }
    """

admin.site.register(TipoDeDocumento)
admin.site.register(InstituicaoDeEnsino)
admin.site.register(Curso)
admin.site.register(Local)
admin.site.register(Documento, DocumentoOptions)
admin.site.register(Contatamento, ContatamentoOptions)
admin.site.register(Estagiario, EstagiarioOptions)
admin.site.register(Estado)
admin.site.register(Projeto, ProjetoOptions)
admin.site.register(ConjAtividade, ConjAtividadeOptions)
admin.site.register(Cidade)
admin.site.register(Coordenador, CoordenadorOptions)
admin.site.register(Contato, ContatoOptions)
admin.site.register(Instituicao)
admin.site.register(TipoDeContatamento)
admin.site.register(ConjAtividadeEspecifica, ConjAtividadeEspecificaOptions)
admin.site.register(SubProjeto)
admin.site.register(ItemFotografado, ItemFotografadoOptions)
admin.site.register(EstadoDoDocumento, EstadoDoDocumentoOptions)
admin.site.register(Banco, BancoOptions)
admin.site.register(TipoDePendencia)
admin.site.register(Pendencia, PendenciaOptions)
admin.site.register(AvaliacaoDeEstagiario, AvaliacaoDeEstagiarioOptions)
admin.site.register(AvaliacaoDeTodosOsEstagiarios)
