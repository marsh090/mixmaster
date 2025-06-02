import json
import requests
from typing import List, Dict, Set

BASE_URL = "http://localhost:8000/api/drinks"

# Mapeamento de tipos de utensílios
UTENSIL_TYPES = {
    "Copos baixo (rocks)": {"nome": "Copos", "nome_en": "Glasses"},
    "Coqueteleira": {"nome": "Preparo", "nome_en": "Preparation"},
    "Taça de martini": {"nome": "Copos", "nome_en": "Glasses"},
    "Colher de mistura": {"nome": "Preparo", "nome_en": "Preparation"},
    "Copos margarita": {"nome": "Copos", "nome_en": "Glasses"},
    "Copos rocks": {"nome": "Copos", "nome_en": "Glasses"},
    "Copo de vinho": {"nome": "Copos", "nome_en": "Glasses"},
    "Copos alto (collins)": {"nome": "Copos", "nome_en": "Glasses"}
}

# Mapeamento de tipos de ingredientes
INGREDIENT_TYPES = {
    "Bourbon": {"nome": "Destilado", "nome_en": "Spirit"},
    "Açúcar": {"nome": "Adoçante", "nome_en": "Sweetener"},
    "Bitters Angostura": {"nome": "Bitters", "nome_en": "Bitters"},
    "Casca de laranja": {"nome": "Decoração", "nome_en": "Garnish"},
    "Gin": {"nome": "Destilado", "nome_en": "Spirit"},
    "Vermute tinto": {"nome": "Fortificado", "nome_en": "Fortified"},
    "Campari": {"nome": "Licor", "nome_en": "Liqueur"},
    "Rum branco": {"nome": "Destilado", "nome_en": "Spirit"},
    "Limão": {"nome": "Fruta", "nome_en": "Fruit"},
    "Xarope simples": {"nome": "Adoçante", "nome_en": "Sweetener"},
    "Vermute seco": {"nome": "Fortificado", "nome_en": "Fortified"},
    "Bitters de limão": {"nome": "Bitters", "nome_en": "Bitters"},
    "Tequila prata": {"nome": "Destilado", "nome_en": "Spirit"},
    "Cointreau": {"nome": "Licor", "nome_en": "Liqueur"},
    "Suco de lima": {"nome": "Suco", "nome_en": "Juice"},
    "Suco de limão": {"nome": "Suco", "nome_en": "Juice"},
    "Sal": {"nome": "Tempero", "nome_en": "Seasoning"},
    "Vodka": {"nome": "Destilado", "nome_en": "Spirit"},
    "Licor de café": {"nome": "Licor", "nome_en": "Liqueur"},
    "Café espresso": {"nome": "Café", "nome_en": "Coffee"},
    "Clara de ovo": {"nome": "Ovo", "nome_en": "Egg"},
    "Rye whiskey": {"nome": "Destilado", "nome_en": "Spirit"},
    "Vermute doce": {"nome": "Fortificado", "nome_en": "Fortified"},
    "Aperol": {"nome": "Licor", "nome_en": "Liqueur"},
    "Prosecco": {"nome": "Vinho", "nome_en": "Wine"},
    "Água com gás": {"nome": "Água", "nome_en": "Water"},
    "Hortelã": {"nome": "Erva", "nome_en": "Herb"}
}

def extract_unique_items(drinks_data: List[Dict]) -> tuple[Set[str], Set[str]]:
    """Extrai utensílios e ingredientes únicos da lista de drinks."""
    utensils = set()
    ingredients = set()
    
    for drink in drinks_data:
        utensils.update(drink["utensilios"])
        ingredients.update(drink["ingredientes"])
    
    return utensils, ingredients

def create_utensil_types():
    """Cria os tipos de utensílios únicos."""
    unique_types = {type_data["nome"]: type_data for type_data in UTENSIL_TYPES.values()}
    
    for ordem, (type_name, type_data) in enumerate(unique_types.items(), start=1):
        response = requests.post(
            f"{BASE_URL}/tipos-utensilio/",
            json={
                "nome": type_data["nome"],
                "nome_en": type_data["nome_en"],
                "ordem": ordem
            }
        )
        print(f"Criado tipo de utensílio: {type_name}")
        response.raise_for_status()

def create_ingredient_types():
    """Cria os tipos de ingredientes únicos."""
    unique_types = {type_data["nome"]: type_data for type_data in INGREDIENT_TYPES.values()}
    
    for ordem, (type_name, type_data) in enumerate(unique_types.items(), start=1):
        response = requests.post(
            f"{BASE_URL}/tipos-ingrediente/",
            json={
                "nome": type_data["nome"],
                "nome_en": type_data["nome_en"],
                "ordem": ordem
            }
        )
        print(f"Criado tipo de ingrediente: {type_name}")
        response.raise_for_status()

def create_utensils(utensils: Set[str]):
    """Cria os utensílios."""
    for utensil in utensils:
        type_data = UTENSIL_TYPES[utensil]
        response = requests.post(
            f"{BASE_URL}/utensilios/",
            json={
                "nome": utensil,
                "nome_en": utensil,  # Poderia ter uma tradução específica
                "descricao": f"Utensílio do tipo {type_data['nome']}",
                "tipo": type_data["nome"]
            }
        )
        print(f"Criado utensílio: {utensil}")
        response.raise_for_status()

def create_ingredients(ingredients: Set[str]):
    """Cria os ingredientes."""
    for ingredient in ingredients:
        type_data = INGREDIENT_TYPES[ingredient]
        response = requests.post(
            f"{BASE_URL}/ingredientes/",
            json={
                "nome": ingredient,
                "nome_en": ingredient,  # Poderia ter uma tradução específica
                "descricao": f"Ingrediente do tipo {type_data['nome']}",
                "tipo": type_data["nome"],
                "unidades_permitidas": ["ml", "oz", "dash", "unit"]  # Unidades padrão
            }
        )
        print(f"Criado ingrediente: {ingredient}")
        response.raise_for_status()

def create_drinks(drinks_data: List[Dict]):
    """Cria os drinks."""
    for drink in drinks_data:
        # Mapeia dificuldade para enum
        dificuldade_map = {
            "fácil": "facil",
            "médio": "medio",
            "difícil": "dificil"
        }
        
        # Mapeia teor alcoólico para enum
        teor_map = {
            "baixo": "baixo",
            "médio": "medio",
            "alto": "alto"
        }
        
        response = requests.post(
            f"{BASE_URL}/drinks/",
            json={
                "nome": drink["nome"],
                "nome_en": drink["nome_en"],
                "nivel_dificuldade": dificuldade_map[drink["nivel_dificuldade"]],
                "teor_alcoolico": teor_map[drink["teor_alcoolico"]],
                "descricao": drink["descricao"],
                "modo_preparo": drink["modo_preparo"],
                "utensilios": drink["utensilios"],
                "ingredientes": drink["ingredientes"]
            }
        )
        print(f"Criado drink: {drink['nome']}")
        response.raise_for_status()

def main():
    """Função principal que coordena a população do banco de dados."""
    try:
        # Carrega os dados do arquivo JSON
        with open("classic_cocktails.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            drinks_data = data["classic_cocktails"]
        
        # Extrai itens únicos
        utensils, ingredients = extract_unique_items(drinks_data)
        
        # Cria tipos
        print("\nCriando tipos de utensílios...")
        create_utensil_types()
        
        print("\nCriando tipos de ingredientes...")
        create_ingredient_types()
        
        # Cria utensílios
        print("\nCriando utensílios...")
        create_utensils(utensils)
        
        # Cria ingredientes
        print("\nCriando ingredientes...")
        create_ingredients(ingredients)
        
        # Cria drinks
        print("\nCriando drinks...")
        create_drinks(drinks_data)
        
        print("\nPopulação concluída com sucesso!")
        
    except Exception as e:
        print(f"\nErro durante a população: {str(e)}")

if __name__ == "__main__":
    main() 