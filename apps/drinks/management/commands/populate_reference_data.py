from django.core.management.base import BaseCommand
from apps.drinks.models import (
    TipoIngrediente, TipoUtensilio, UnidadeMedida, 
    PerfilSabor, Ingrediente, Utensilio
)

class Command(BaseCommand):
    help = 'Popula as coleções de referência com dados iniciais'

    def handle(self, *args, **kwargs):
        # Tipos de Ingrediente
        tipos_ingrediente = [
            {"nome": "Destilado", "nome_en": "Spirit", "ordem": 1},
            {"nome": "Fruta", "nome_en": "Fruit", "ordem": 2},
            {"nome": "Xarope", "nome_en": "Syrup", "ordem": 3},
            {"nome": "Suco", "nome_en": "Juice", "ordem": 4},
            {"nome": "Especiaria", "nome_en": "Spice", "ordem": 5},
            {"nome": "Erva", "nome_en": "Herb", "ordem": 6},
            {"nome": "Licor", "nome_en": "Liqueur", "ordem": 7},
            {"nome": "Bitter", "nome_en": "Bitter", "ordem": 8},
        ]
        
        for tipo in tipos_ingrediente:
            if not TipoIngrediente.find_one({"nome": tipo["nome"]}):
                TipoIngrediente.create(tipo)
                self.stdout.write(f'Tipo de ingrediente criado: {tipo["nome"]}')

        # Tipos de Utensílio
        tipos_utensilio = [
            {"nome": "Preparo", "nome_en": "Preparation", "ordem": 1},
            {"nome": "Medição", "nome_en": "Measurement", "ordem": 2},
            {"nome": "Decoração", "nome_en": "Garnish", "ordem": 3},
            {"nome": "Copo", "nome_en": "Glass", "ordem": 4},
        ]
        
        for tipo in tipos_utensilio:
            if not TipoUtensilio.find_one({"nome": tipo["nome"]}):
                TipoUtensilio.create(tipo)
                self.stdout.write(f'Tipo de utensílio criado: {tipo["nome"]}')

        # Unidades de Medida
        unidades_medida = [
            {"nome": "ml", "nome_en": "ml", "tipo": "volume", "conversao_ml": 1.0},
            {"nome": "oz", "nome_en": "oz", "tipo": "volume", "conversao_ml": 29.5735},
            {"nome": "dash", "nome_en": "dash", "tipo": "volume", "conversao_ml": 0.92},
            {"nome": "unidade", "nome_en": "unit", "tipo": "unidade", "conversao_ml": None},
            {"nome": "fatia", "nome_en": "slice", "tipo": "unidade", "conversao_ml": None},
            {"nome": "folha", "nome_en": "leaf", "tipo": "unidade", "conversao_ml": None},
        ]
        
        for unidade in unidades_medida:
            if not UnidadeMedida.find_one({"nome": unidade["nome"]}):
                UnidadeMedida.create(unidade)
                self.stdout.write(f'Unidade de medida criada: {unidade["nome"]}')

        # Perfis de Sabor
        perfis_sabor = [
            {"nome": "Doce", "nome_en": "Sweet", "ordem": 1},
            {"nome": "Azedo", "nome_en": "Sour", "ordem": 2},
            {"nome": "Amargo", "nome_en": "Bitter", "ordem": 3},
            {"nome": "Salgado", "nome_en": "Salty", "ordem": 4},
        ]
        
        for perfil in perfis_sabor:
            if not PerfilSabor.find_one({"nome": perfil["nome"]}):
                PerfilSabor.create(perfil)
                self.stdout.write(f'Perfil de sabor criado: {perfil["nome"]}')

        # Ingredientes Básicos
        ingredientes_basicos = [
            {
                "nome": "Rum Branco",
                "nome_en": "White Rum",
                "tipo": "Destilado",
                "unidades_permitidas": ["ml", "oz"],
                "descricao": "Rum claro, ideal para drinks como Mojito e Daiquiri"
            },
            {
                "nome": "Gin",
                "nome_en": "Gin",
                "tipo": "Destilado",
                "unidades_permitidas": ["ml", "oz"],
                "descricao": "Destilado aromático com zimbro"
            },
            {
                "nome": "Limão",
                "nome_en": "Lime",
                "tipo": "Fruta",
                "unidades_permitidas": ["ml", "unidade", "fatia"],
                "descricao": "Limão tahiti fresco"
            },
            {
                "nome": "Hortelã",
                "nome_en": "Mint",
                "tipo": "Erva",
                "unidades_permitidas": ["folha", "unidade"],
                "descricao": "Folhas frescas de hortelã"
            },
        ]
        
        for ingrediente in ingredientes_basicos:
            if not Ingrediente.find_one({"nome": ingrediente["nome"]}):
                Ingrediente.create(ingrediente)
                self.stdout.write(f'Ingrediente criado: {ingrediente["nome"]}')

        # Utensílios Básicos
        utensilios_basicos = [
            {
                "nome": "Coqueteleira",
                "nome_en": "Shaker",
                "tipo": "Preparo",
                "descricao": "Utensílio para misturar e resfriar drinks"
            },
            {
                "nome": "Copo Long Drink",
                "nome_en": "Long Drink Glass",
                "tipo": "Copo",
                "descricao": "Copo alto para drinks refrescantes"
            },
            {
                "nome": "Pilão",
                "nome_en": "Muddler",
                "tipo": "Preparo",
                "descricao": "Utensílio para macerar ingredientes"
            },
        ]
        
        for utensilio in utensilios_basicos:
            if not Utensilio.find_one({"nome": utensilio["nome"]}):
                Utensilio.create(utensilio)
                self.stdout.write(f'Utensílio criado: {utensilio["nome"]}') 