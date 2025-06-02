from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, include
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from bson import ObjectId

from .models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida,
    PerfilSabor, Ingrediente, Utensilio, Drink
)

class MongoModelForm(forms.Form):
    """Form base para modelos MongoDB"""
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            for field_name, field in self.fields.items():
                if field_name in instance:
                    field.initial = instance[field_name]

class TipoReferenciaForm(MongoModelForm):
    """Form para tipos de referência (ingredientes, utensílios, etc)"""
    nome = forms.CharField(max_length=100)
    nome_en = forms.CharField(max_length=100)
    ordem = forms.IntegerField(required=False)

class UnidadeMedidaForm(MongoModelForm):
    """Form para unidades de medida"""
    nome = forms.CharField(max_length=100)
    nome_en = forms.CharField(max_length=100)
    tipo = forms.ChoiceField(choices=[('volume', 'Volume'), ('peso', 'Peso'), ('unidade', 'Unidade')])
    conversao_ml = forms.FloatField(required=False, help_text='Conversão para mililitros (apenas para unidades de volume)')

class IngredienteForm(MongoModelForm):
    """Form para ingredientes"""
    nome = forms.CharField(max_length=100)
    nome_en = forms.CharField(max_length=100)
    tipo = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea, required=False)
    descricao_en = forms.CharField(widget=forms.Textarea, required=False)
    perfis_sabor = forms.MultipleChoiceField(choices=[], required=False)
    teor_alcoolico = forms.FloatField(required=False)
    densidade = forms.FloatField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar opções dinâmicas
        self.fields['tipo'].widget = forms.Select(choices=[(t['nome'], t['nome']) for t in TipoIngrediente.find()])
        self.fields['perfis_sabor'].choices = [(p['nome'], p['nome']) for p in PerfilSabor.find()]

class UtensilioForm(MongoModelForm):
    """Form para utensílios"""
    nome = forms.CharField(max_length=100)
    nome_en = forms.CharField(max_length=100)
    tipo = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea, required=False)
    descricao_en = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar opções dinâmicas
        self.fields['tipo'].widget = forms.Select(choices=[(t['nome'], t['nome']) for t in TipoUtensilio.find()])

class DrinkForm(MongoModelForm):
    """Form para drinks"""
    nome = forms.CharField(max_length=100)
    nome_en = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea, required=False)
    descricao_en = forms.CharField(widget=forms.Textarea, required=False)
    nivel_dificuldade = forms.ChoiceField(choices=[
        ('facil', 'Fácil'),
        ('medio', 'Médio'),
        ('dificil', 'Difícil')
    ])
    tempo_preparo = forms.IntegerField(help_text='Tempo em minutos')
    rendimento = forms.IntegerField(help_text='Quantidade de drinks')
    teor_alcoolico = forms.FloatField(required=False)
    calorias = forms.FloatField(required=False)
    ingredientes = forms.CharField(widget=forms.Textarea, help_text='Um ingrediente por linha, no formato: quantidade unidade nome')
    utensilios = forms.MultipleChoiceField(choices=[], required=False)
    modo_preparo = forms.CharField(widget=forms.Textarea)
    modo_preparo_en = forms.CharField(widget=forms.Textarea)
    dicas = forms.CharField(widget=forms.Textarea, required=False)
    dicas_en = forms.CharField(widget=forms.Textarea, required=False)
    tags = forms.CharField(widget=forms.Textarea, required=False, help_text='Uma tag por linha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar opções dinâmicas
        self.fields['utensilios'].choices = [(u['nome'], u['nome']) for u in Utensilio.find()]

    def clean_ingredientes(self):
        """Converte a string de ingredientes em uma lista de dicionários"""
        ingredientes = []
        for linha in self.cleaned_data['ingredientes'].split('\n'):
            if not linha.strip():
                continue
            partes = linha.strip().split()
            if len(partes) >= 3:
                quantidade = float(partes[0])
                unidade = partes[1]
                nome = ' '.join(partes[2:])
                ingredientes.append({
                    'quantidade': quantidade,
                    'unidade': unidade,
                    'nome': nome
                })
        return ingredientes

    def clean_tags(self):
        """Converte a string de tags em uma lista"""
        return [tag.strip() for tag in self.cleaned_data['tags'].split('\n') if tag.strip()]

class MongoModelAdmin:
    """Admin base para modelos MongoDB"""
    form_class = MongoModelForm
    list_display = ['nome']
    template_dir = 'admin/drinks'

    def __init__(self, model_class):
        self.model = model_class
        self.model_name = model_class.__name__.lower()
        self.opts = type('Options', (), {
            'app_label': 'drinks',
            'model_name': self.model_name,
            'verbose_name': self.model_name.title(),
            'verbose_name_plural': f"{self.model_name}s".title()
        })

    def get_urls(self):
        """Retorna as URLs do admin"""
        return [
            path('', self.list_view, name=f'drinks_{self.model_name}_list'),
            path('add/', self.add_view, name=f'drinks_{self.model_name}_add'),
            path('<str:object_id>/change/', self.change_view, name=f'drinks_{self.model_name}_change'),
            path('<str:object_id>/delete/', self.delete_view, name=f'drinks_{self.model_name}_delete'),
        ]

    @property
    def urls(self):
        return self.get_urls()

    def get_context(self, request, extra_context=None):
        """Retorna o contexto base para os templates"""
        context = {
            'opts': self.opts,
            'app_label': self.opts.app_label,
            'has_add_permission': True,
            'has_change_permission': True,
            'has_delete_permission': True,
        }
        if extra_context:
            context.update(extra_context)
        return context

    def list_view(self, request):
        """View para listar objetos"""
        objects = list(self.model.find())
        headers = [field.replace('_', ' ').title() for field in self.list_display]
        
        results = []
        for obj in objects:
            items = [obj.get(field) for field in self.list_display]
            obj_id = str(obj['_id'])
            results.append({
                'items': items,
                'change_url': reverse(f'admin:drinks_{self.model_name}_change', args=[obj_id]),
                'delete_url': reverse(f'admin:drinks_{self.model_name}_delete', args=[obj_id])
            })

        context = self.get_context(request, {
            'results': results,
            'list_headers': headers,
            'add_url': reverse(f'admin:drinks_{self.model_name}_add'),
        })
        
        return render(request, f'{self.template_dir}/list.html', context)

    def add_view(self, request):
        """View para adicionar objetos"""
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                self.model.insert_one(form.cleaned_data)
                return HttpResponseRedirect(reverse(f'admin:drinks_{self.model_name}_list'))
        else:
            form = self.form_class()

        context = self.get_context(request, {
            'form': form,
            'add': True,
            'show_save': True,
            'show_save_and_continue': True,
            'show_save_and_add_another': True,
        })
        
        return render(request, f'{self.template_dir}/form.html', context)

    def change_view(self, request, object_id):
        """View para editar objetos"""
        obj = self.model.find_one({'_id': ObjectId(object_id)})
        if request.method == 'POST':
            form = self.form_class(request.POST, instance=obj)
            if form.is_valid():
                self.model.update_one(
                    {'_id': ObjectId(object_id)},
                    {'$set': form.cleaned_data}
                )
                return HttpResponseRedirect(reverse(f'admin:drinks_{self.model_name}_list'))
        else:
            form = self.form_class(instance=obj)

        context = self.get_context(request, {
            'form': form,
            'object_id': object_id,
            'show_save': True,
            'show_save_and_continue': True,
            'show_delete': True,
            'delete_url': reverse(f'admin:drinks_{self.model_name}_delete', args=[object_id]),
        })
        
        return render(request, f'{self.template_dir}/form.html', context)

    def delete_view(self, request, object_id):
        """View para excluir objetos"""
        obj = self.model.find_one({'_id': ObjectId(object_id)})
        if request.method == 'POST':
            self.model.delete_one({'_id': ObjectId(object_id)})
            return HttpResponseRedirect(reverse(f'admin:drinks_{self.model_name}_list'))

        context = self.get_context(request, {
            'object': obj,
            'cancel_url': reverse(f'admin:drinks_{self.model_name}_list'),
        })
        
        return render(request, f'{self.template_dir}/delete.html', context)

class DrinksAdminSite(admin.AdminSite):
    """Site de administração personalizado para o app drinks"""
    site_header = 'Administração de Drinks'
    site_title = 'Administração de Drinks'
    index_title = 'Administração de Drinks'
    index_template = 'admin/drinks/index.html'
    
    def get_urls(self):
        urls = super().get_urls()
        
        # Criar instâncias dos admins
        tipo_ingrediente_admin = MongoModelAdmin(TipoIngrediente)
        tipo_ingrediente_admin.form_class = TipoReferenciaForm
        tipo_ingrediente_admin.list_display = ['nome', 'nome_en', 'ordem']
        
        tipo_utensilio_admin = MongoModelAdmin(TipoUtensilio)
        tipo_utensilio_admin.form_class = TipoReferenciaForm
        tipo_utensilio_admin.list_display = ['nome', 'nome_en', 'ordem']
        
        unidade_medida_admin = MongoModelAdmin(UnidadeMedida)
        unidade_medida_admin.form_class = UnidadeMedidaForm
        unidade_medida_admin.list_display = ['nome', 'nome_en', 'tipo', 'conversao_ml']
        
        perfil_sabor_admin = MongoModelAdmin(PerfilSabor)
        perfil_sabor_admin.form_class = TipoReferenciaForm
        perfil_sabor_admin.list_display = ['nome', 'nome_en', 'ordem']
        
        ingrediente_admin = MongoModelAdmin(Ingrediente)
        ingrediente_admin.form_class = IngredienteForm
        ingrediente_admin.list_display = ['nome', 'nome_en', 'tipo']
        
        utensilio_admin = MongoModelAdmin(Utensilio)
        utensilio_admin.form_class = UtensilioForm
        utensilio_admin.list_display = ['nome', 'nome_en', 'tipo']
        
        drink_admin = MongoModelAdmin(Drink)
        drink_admin.form_class = DrinkForm
        drink_admin.list_display = ['nome', 'nome_en', 'nivel_dificuldade', 'teor_alcoolico']
        
        # Adicionar URLs dos admins
        drinks_urls = [
            path('drinks/tipo-ingrediente/', include(tipo_ingrediente_admin.urls)),
            path('drinks/tipo-utensilio/', include(tipo_utensilio_admin.urls)),
            path('drinks/unidade-medida/', include(unidade_medida_admin.urls)),
            path('drinks/perfil-sabor/', include(perfil_sabor_admin.urls)),
            path('drinks/ingrediente/', include(ingrediente_admin.urls)),
            path('drinks/utensilio/', include(utensilio_admin.urls)),
            path('drinks/drink/', include(drink_admin.urls)),
        ]
        
        return urls + drinks_urls

# Registrar o site de administração personalizado
admin_site = DrinksAdminSite(name='drinks_admin')
admin.site = admin_site
