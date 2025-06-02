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
    nome = forms.CharField(max_length=100, label='Nome', help_text='Nome em português')
    nome_en = forms.CharField(max_length=100, label='Nome em inglês', help_text='Nome em inglês')

class UnidadeMedidaForm(MongoModelForm):
    """Form para unidades de medida"""
    nome = forms.CharField(max_length=100, label='Nome', help_text='Nome em português')
    nome_en = forms.CharField(max_length=100, label='Nome em inglês', help_text='Nome em inglês')
    tipo = forms.ChoiceField(
        choices=[
            ('volume', 'Volume'),
            ('peso', 'Peso'),
            ('unidade', 'Unidade')
        ],
        label='Tipo',
        help_text='Tipo de unidade de medida'
    )
    conversao_ml = forms.FloatField(
        required=False,
        label='Conversão para ml',
        help_text='Conversão para mililitros (apenas para unidades de volume)'
    )

class IngredienteForm(MongoModelForm):
    """Form para ingredientes"""
    nome = forms.CharField(max_length=100, label='Nome', help_text='Nome em português')
    nome_en = forms.CharField(max_length=100, label='Nome em inglês', help_text='Nome em inglês')
    tipo = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Tipos',
        help_text='Tipos do ingrediente',
        widget=forms.SelectMultiple(attrs={'size': '5'})
    )
    unidades_permitidas = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Unidades permitidas',
        help_text='Unidades de medida permitidas para este ingrediente',
        widget=forms.SelectMultiple(attrs={'size': '5'})
    )
    descricao = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Descrição',
        help_text='Descrição do ingrediente'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buscar tipos de ingrediente e unidades de medida do MongoDB
        tipos = TipoIngrediente.find()
        unidades = UnidadeMedida.find()
        self.fields['tipo'].choices = [
            (t['nome'], t['nome']) for t in tipos
        ]
        self.fields['unidades_permitidas'].choices = [
            (u['nome'], u['nome']) for u in unidades
        ]

class UtensilioForm(MongoModelForm):
    """Form para utensílios"""
    nome = forms.CharField(max_length=100, label='Nome', help_text='Nome em português')
    nome_en = forms.CharField(max_length=100, label='Nome em inglês', help_text='Nome em inglês')
    tipo = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Tipos',
        help_text='Tipos do utensílio',
        widget=forms.SelectMultiple(attrs={'size': '5'})
    )
    descricao = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Descrição',
        help_text='Descrição do utensílio'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buscar tipos de utensílio do MongoDB
        tipos = TipoUtensilio.find()
        self.fields['tipo'].choices = [
            (t['nome'], t['nome']) for t in tipos
        ]

class DrinkForm(MongoModelForm):
    """Form para drinks"""
    nome = forms.CharField(max_length=100, label='Nome', help_text='Nome em português')
    nome_en = forms.CharField(max_length=100, label='Nome em inglês', help_text='Nome em inglês')
    nivel_dificuldade = forms.ChoiceField(
        choices=[
            ('facil', 'Fácil'),
            ('medio', 'Médio'),
            ('dificil', 'Difícil')
        ],
        label='Nível de dificuldade'
    )
    teor_alcoolico = forms.ChoiceField(
        choices=[
            ('zero', 'Zero'),
            ('baixo', 'Baixo'),
            ('medio', 'Médio'),
            ('alto', 'Alto')
        ],
        label='Teor alcoólico'
    )
    descricao = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Descrição',
        help_text='Descrição do drink'
    )
    modo_preparo = forms.CharField(
        widget=forms.Textarea,
        label='Modo de preparo',
        help_text='Instruções passo a passo para preparar o drink'
    )
    spirits = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Spirits',
        help_text='Destilados e licores',
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        required=False
    )
    outros_ingredientes = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Outros Ingredientes',
        help_text='Frutas, xaropes, sucos, etc',
        widget=forms.SelectMultiple(attrs={'size': '5'}),
        required=False
    )
    utensilios = forms.MultipleChoiceField(
        choices=[],  # Será preenchido no __init__
        label='Utensílios',
        help_text='Utensílios necessários',
        widget=forms.SelectMultiple(attrs={'size': '5'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buscar ingredientes e utensílios do MongoDB
        ingredientes = list(Ingrediente.find())
        utensilios = list(Utensilio.find())

        # Separar ingredientes por tipo
        spirits = [i for i in ingredientes if 'Destilado' in i.get('tipo', []) or 'Licor' in i.get('tipo', [])]
        outros = [i for i in ingredientes if 'Destilado' not in i.get('tipo', []) and 'Licor' not in i.get('tipo', [])]

        self.fields['spirits'].choices = [
            (i['nome'], i['nome']) for i in spirits
        ]
        self.fields['outros_ingredientes'].choices = [
            (i['nome'], i['nome']) for i in outros
        ]
        self.fields['utensilios'].choices = [
            (u['nome'], u['nome']) for u in utensilios
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Combinar spirits e outros_ingredientes em uma única lista
        spirits = cleaned_data.get('spirits', [])
        outros = cleaned_data.get('outros_ingredientes', [])
        cleaned_data['ingredientes'] = spirits + outros
        return cleaned_data

class MongoModelAdmin:
    """Admin base para modelos MongoDB"""
    form_class = MongoModelForm
    list_display = ['nome']
    template_dir = 'admin/drinks'
    has_order = False  # Flag para indicar se o modelo usa ordem automática

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
        info = self.opts.app_label, self.model_name
        return [
            path('', self.list_view, name='%s_%s_list' % info),
            path('add/', self.add_view, name='%s_%s_add' % info),
            path('<str:object_id>/change/', self.change_view, name='%s_%s_change' % info),
            path('<str:object_id>/delete/', self.delete_view, name='%s_%s_delete' % info),
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
                'change_url': reverse('admin:%s_%s_change' % (self.opts.app_label, self.model_name), args=[obj_id]),
                'delete_url': reverse('admin:%s_%s_delete' % (self.opts.app_label, self.model_name), args=[obj_id])
            })

        context = self.get_context(request, {
            'results': results,
            'list_headers': headers,
            'add_url': reverse('admin:%s_%s_add' % (self.opts.app_label, self.model_name)),
        })
        
        return render(request, f'{self.template_dir}/list.html', context)

    def add_view(self, request):
        """View para adicionar objetos"""
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if self.has_order:
                    # Encontrar a maior ordem atual
                    last_item = next(self.model.find().sort([('ordem', -1)]).limit(1), None)
                    data['ordem'] = (last_item['ordem'] + 1) if last_item else 1
                # Se for um drink, remover os campos temporários
                if isinstance(form, DrinkForm):
                    data.pop('spirits', None)
                    data.pop('outros_ingredientes', None)
                self.model.insert_one(data)
                return HttpResponseRedirect(reverse('admin:%s_%s_list' % (self.opts.app_label, self.model_name)))
        else:
            form = self.form_class()

        adminform = type('AdminForm', (), {
            'form': form,
            'fieldsets': [(None, {'fields': list(form.fields.keys())})],
        })

        context = self.get_context(request, {
            'adminform': adminform,
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
                data = form.cleaned_data
                # Se for um drink, remover os campos temporários
                if isinstance(form, DrinkForm):
                    data.pop('spirits', None)
                    data.pop('outros_ingredientes', None)
                self.model.update_one(
                    {'_id': ObjectId(object_id)},
                    {'$set': data}
                )
                return HttpResponseRedirect(reverse('admin:%s_%s_list' % (self.opts.app_label, self.model_name)))
        else:
            # Se for um drink, separar os ingredientes em spirits e outros
            if isinstance(self.form_class, type(DrinkForm)):
                ingredientes = obj.get('ingredientes', [])
                # Buscar todos os ingredientes para verificar seus tipos
                todos_ingredientes = {i['nome']: i for i in Ingrediente.find()}
                spirits = []
                outros = []
                for ing in ingredientes:
                    if ing in todos_ingredientes:
                        tipos = todos_ingredientes[ing].get('tipo', [])
                        if 'Destilado' in tipos or 'Licor' in tipos:
                            spirits.append(ing)
                        else:
                            outros.append(ing)
                obj['spirits'] = spirits
                obj['outros_ingredientes'] = outros
            form = self.form_class(instance=obj)

        adminform = type('AdminForm', (), {
            'form': form,
            'fieldsets': [(None, {'fields': list(form.fields.keys())})],
        })

        context = self.get_context(request, {
            'adminform': adminform,
            'form': form,
            'object_id': object_id,
            'show_save': True,
            'show_save_and_continue': True,
            'show_delete': True,
            'delete_url': reverse('admin:%s_%s_delete' % (self.opts.app_label, self.model_name), args=[object_id]),
        })
        
        return render(request, f'{self.template_dir}/form.html', context)

    def delete_view(self, request, object_id):
        """View para excluir objetos"""
        obj = self.model.find_one({'_id': ObjectId(object_id)})
        if request.method == 'POST':
            self.model.delete_one({'_id': ObjectId(object_id)})
            return HttpResponseRedirect(reverse('admin:%s_%s_list' % (self.opts.app_label, self.model_name)))

        context = self.get_context(request, {
            'object': obj,
            'cancel_url': reverse('admin:%s_%s_list' % (self.opts.app_label, self.model_name)),
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
        tipo_ingrediente_admin.has_order = True

        tipo_utensilio_admin = MongoModelAdmin(TipoUtensilio)
        tipo_utensilio_admin.form_class = TipoReferenciaForm
        tipo_utensilio_admin.list_display = ['nome', 'nome_en', 'ordem']
        tipo_utensilio_admin.has_order = True

        unidade_medida_admin = MongoModelAdmin(UnidadeMedida)
        unidade_medida_admin.form_class = UnidadeMedidaForm
        unidade_medida_admin.list_display = ['nome', 'nome_en', 'tipo', 'conversao_ml']

        perfil_sabor_admin = MongoModelAdmin(PerfilSabor)
        perfil_sabor_admin.form_class = TipoReferenciaForm
        perfil_sabor_admin.list_display = ['nome', 'nome_en', 'ordem']
        perfil_sabor_admin.has_order = True

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
        
        return drinks_urls + urls

# Registrar o site de administração personalizado
admin_site = DrinksAdminSite(name='drinks_admin')
admin.site = admin_site
